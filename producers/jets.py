"""
Producers for AK4 jet energy scale and resolution corrections, object selections, overlap vetoes, and quantities to be stored.
"""

from ..quantities import output as q
from ..quantities import nanoAOD, nanoAOD_run2
from analysis_configurations.quantities import nanoAODv12_run3
from code_generation.producer import Producer, ProducerGroup

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES, SCOPES, AvailableBJetIDs, BJET_ID_ALGORITHM


#
# JET ID
#

# Rename the jet ID stored in the NANOAOD samples for run 2 samples
JetIDRun2 = Producer(
    name="JetIDRun2",
    call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
    input=[nanoAODv12_run3.Jet_jetId],
    output=[q.Jet_ID_corrected],
    scopes=GLOBAL_SCOPES,
)

# Correct the jet ID stored in run 3 NANOAODv12 samples
JetIDRun3NanoV12 = Producer(
    name="JetIDRun3NanoV12Corrected",
    call="physicsobject::jet::quantities::CorrectJetIDRun3NanoV12({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAODv12_run3.Jet_jetId,
        nanoAOD.Jet_neHEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_muEF,
        nanoAOD.Jet_chEmEF,
    ],
    output=[q.Jet_ID_corrected],
    scopes=GLOBAL_SCOPES,
)

# Calculate the jet ID from a correction JSON for run 3 NANOAODv15 samples
JetIDRun3NanoV15 = Producer(
    name="JetIDRun3",
    call="physicsobject::jet::quantity::ID({df}, correctionManager, {output}, {input}, \"{ak4jet_id_file}\", \"{ak4jet_id_name}\")",
    input=[
        nanoAOD.Jet_eta,
        nanoAOD.Jet_chHEF,
        nanoAOD.Jet_neHEF,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_muEF,
        nanoAOD.Jet_chMultiplicity,
        nanoAOD.Jet_neMultiplicity,
    ],
    output=[q.Jet_ID_corrected],
    scopes=GLOBAL_SCOPES,
)


#
# JET ENERGY SCALE AND RESOLUTION CORRECTIONS
#

# Create jet energy correction producers for AK4 jets
JetEnergyCorrection_data, JetEnergyCorrection, RenameJetsData = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.Jet_pt,
        "jet_eta": nanoAOD.Jet_eta,
        "jet_phi": nanoAOD.Jet_phi,
        "jet_mass": nanoAOD.Jet_mass,
        "jet_area": nanoAOD.Jet_area,
        "jet_raw_factor": nanoAOD.Jet_rawFactor,
        "jet_id": q.Jet_ID_corrected,
        "gen_jet_pt": nanoAOD.GenJet_pt,
        "gen_jet_eta": nanoAOD.GenJet_eta,
        "gen_jet_phi": nanoAOD.GenJet_phi,
        "rho": nanoAOD.Rho_fixedGridRhoFastjetAll,
        "luminosity_block": nanoAOD.luminosityBlock,
        "run": nanoAOD.run,
        "event": nanoAOD.event,
    },
    output={
        "jet_pt_corrected": q.Jet_pt_corrected,
        "jet_mass_corrected": q.Jet_mass_corrected,
    },
    scopes=GLOBAL_SCOPES,
    producer_prefix="Jet",
    config_parameter_prefix="ak4jet",
)


#
# AK4 JET SELECTION
#

# Jet selection for run 2 (CHS jets)
GoodJetsWithPUID = Producer(
    name="GoodJetsWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {ak4jet_min_pt}, {ak4jet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto}, {ak4jet_puid_wp}, {ak4jet_puid_max_pt})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.Jet_ID_corrected,
        nanoAOD_run2.Jet_puId,
    ],
    output=[q.good_jets_mask],
    scopes=GLOBAL_SCOPES,
)

# Jet selection for run 3 (PUPPI jets)
GoodJetsWithoutPUID = Producer(
    name="GoodJetsWithoutPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {ak4jet_min_pt}, {ak4jet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.Jet_ID_corrected,
    ],
    output=[q.good_jets_mask],
    scopes=GLOBAL_SCOPES,
)

# Kinematic b jet selection for run 2 (CHS jets)
GoodBJetsBaseWithPUID = Producer(
    name="GoodBJetsBaseWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto}, {ak4jet_puid_wp}, {ak4jet_puid_max_pt})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.Jet_ID_corrected,
        nanoAOD_run2.Jet_puId,
    ],
    output=[q.base_bjets_mask],
    scopes=GLOBAL_SCOPES,
)

# Kinematic b jet selection for run 3 (PUPPI jets)
GoodBJetsBaseWithoutPUID = Producer(
    name="GoodBJetsBaseWithoutPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.Jet_ID_corrected,
    ],
    output=[q.base_bjets_mask],
    scopes=GLOBAL_SCOPES,
)

# Tag whether a jet is b-tagged.
# The NANOAOD column for the b tagging score is taken from the analysis
# configuration.
BTagCut = Producer(
    name="BTagCut",
    call="physicsobject::CutMin<float>({df}, {output}, \"{bjet_score_column}\", {bjet_min_score})",
    input=[],
    output=[q.Jet_is_btagged],
    scopes=GLOBAL_SCOPES,
)

# Full b jet selection for run 2, including the b tagging requirement (CHS jets)
GoodBJetsWithPUID = ProducerGroup(
    name="GoodBJetsWithPUID",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[q.good_bjets_mask],
    subproducers=[
        GoodBJetsBaseWithPUID,
        BTagCut,
    ],
    scopes=GLOBAL_SCOPES,
)

# Full b jet selection for run 3, including the b tagging requirement (PUPPI jets)
GoodBJetsWithoutPUID = ProducerGroup(
    name="GoodBJetsWithoutPUID",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[q.good_bjets_mask],
    subproducers=[
        GoodBJetsBaseWithoutPUID,
        BTagCut,
    ],
    scopes=GLOBAL_SCOPES,
)

# Producer group for jet and b jet selection in run 2 (CHS jets)
BaseJetSelectionWithPUID = ProducerGroup(
    name="GoodJetSelectionWithPUID",
    call=None,
    input=None,
    output=None,
    scopes=GLOBAL_SCOPES,
    subproducers=[
        GoodJetsWithPUID,
        GoodBJetsWithPUID,
    ],
)

# Producer group for jet and b jet selection in run 3 (PUPPI jets)
BaseJetSelectionWithoutPUID = ProducerGroup(
    name="GoodJetSelectionWithoutPUID",
    call=None,
    input=None,
    output=None,
    scopes=GLOBAL_SCOPES,
    subproducers=[
        GoodJetsWithoutPUID,
        GoodBJetsWithoutPUID,
    ],
)


#
# OVERLAP VETOES
#

# Check whether a jet is overlapping with the tight lepton candidates from resolved selection
VetoOverlappingJets = Producer(
    name="VetoOverlappingJets",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {ak4jet_veto_min_delta_r})",
    input=[
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.p4_1,
        q.p4_2,
    ],
    output=[q.jet_overlap_veto_mask],
    scopes=SCOPES,
)

# Create a mask that includes selected jets that do not overlap with the lepton candidates from the resolved selection
GoodJetsWithVeto = Producer(
    name="GoodJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_mask, q.jet_overlap_veto_mask],
    output=[q.good_jets_with_veto_mask],
    scopes=SCOPES,
)

# Create a mask that includes selected b jets that do not overlap with the lepton candidates from the resolved selection
GoodBJetsWithVeto = Producer(
    name="GoodBJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_bjets_mask, q.jet_overlap_veto_mask],
    output=[q.good_bjets_with_veto_mask],
    scopes=SCOPES,
)

# Create a mask that merged the masks for the selected jets and b jets after overlap cleaning
GoodJetsOrBJetsWithVeto = Producer(
    name="GoodJetsOrBJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "any_of")',
    input=[q.good_jets_with_veto_mask, q.good_bjets_with_veto_mask],
    output=[],
    scopes=SCOPES,
)

# Final jet collection as list of indices of selected jets, ordered by pt for the resolved selection
JetCollection = ProducerGroup(
    name="JetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_jet_collection],
    scopes=SCOPES,
    subproducers=[GoodJetsOrBJetsWithVeto],
)

# Final b jet collection as list of indices of selected jets, ordered by pt for the resolved selection
BJetCollection = Producer(
    name="BJetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected, q.good_bjets_with_veto_mask],
    output=[q.good_bjet_collection],
    scopes=SCOPES,
)

# Producer group for the jet selection in the scopes after cleaning against leptons
JetSelection = ProducerGroup(
    name="JetSelection",
    call=None,
    input=[],
    output=[],
    scopes=SCOPES,
    subproducers=[
        VetoOverlappingJets,
        GoodJetsWithVeto,
        GoodBJetsWithVeto,
        JetCollection,
        BJetCollection,
    ],
)


#
# JET QUANTITIES
#

"""
# columns for jet pt regression with PNet
jet_column_producers.extend(
    [
        Producer(
            name="JetColumn_jet_pt_pnet",
            call="physicsobject::jet::quantities::JetPtPNetRegression({df}, {output}, {input})",
            input=[
                nanoAOD.Jet_pt,
                nanoAOD.Jet_rawFactor,
                nanoAOD.Jet_PNetRegPtRawCorr,
                q.good_jet_combined_collection,
            ],
            output=[q.jet_pt_pnet],
            scopes=SCOPES,
        ),
        Producer(
            name="JetColumn_jet_pt_pnet_with_neutrino",
            call="physicsobject::jet::quantities::JetPtPNetRegressionWithNeutrino({df}, {output}, {input})",
            input=[
                nanoAOD.Jet_pt,
                nanoAOD.Jet_rawFactor,
                nanoAOD.Jet_PNetRegPtRawCorr,
                nanoAOD.Jet_PNetRegPtRawCorrNeutrino,
                q.good_jet_combined_collection
            ],
            output=[q.jet_pt_pnet_with_neutrino],
            scopes=SCOPES,
        ),
        Producer(
            name="JetColumn_jet_pt_resolution_pnet_with_neutrino",
            call="physicsobject::jet::quantities::JetPtPNetRegression({df}, {output}, {input})",
            input=[
                nanoAOD.Jet_pt,
                nanoAOD.Jet_rawFactor,
                nanoAOD.Jet_PNetRegPtRawRes,
                q.good_jet_combined_collection,
            ],
            output=[q.jet_pt_pnet_resolution],
            scopes=SCOPES,
        ),
    ]
)
"""


#
# Number of jets (depending on the b jet tagger)
#

NumberOfJets = Producer(
    name="NumberOfJets",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_jet_collection],
    output=[q.n_jets],
    scopes=SCOPES,
)


#
# Quantities for the two leading jets
#

LVJet1 = Producer(
    name="LVJet1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection,
    ],
    output=[q.jet_p4_1],
    scopes=SCOPES,
)

LVJet2 = Producer(
    name="LVJet2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_jet_collection,
    ],
    output=[q.jet_p4_2],
    scopes=SCOPES,
)

NumberOfJets = Producer(
    name="NumberOfJets",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_jet_collection],
    output=[q.n_jets],
    scopes=SCOPES,
)

NumberOfJets_boosted = Producer(
    name="NumberOfJets_boosted",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_jet_collection_boosted],
    output=[q.n_jets_boosted],
    scopes=SCOPES,
)

jpt_1 = Producer(
    name="jpt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jpt_1],
    scopes=SCOPES,
)
jpt_2 = Producer(
    name="jpt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jpt_2],
    scopes=SCOPES,
)
jeta_1 = Producer(
    name="jeta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jeta_1],
    scopes=SCOPES,
)
jeta_2 = Producer(
    name="jeta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jeta_2],
    scopes=SCOPES,
)
jphi_1 = Producer(
    name="jphi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jphi_1],
    scopes=SCOPES,
)
jphi_2 = Producer(
    name="jphi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jphi_2],
    scopes=SCOPES,
)
jtag_value_1 = Producer(
    name="jtag_value_1",
    call="event::quantity::Get<float>({df}, {output}, \"{bjet_score_column}\", {input}, 0)",
    input=[q.good_jet_collection],
    output=[q.jtag_value_1],
    scopes=SCOPES,
)
jtag_value_2 = Producer(
    name="jtag_value_2",
    call="event::quantity::Get<float>({df}, {output}, \"{bjet_score_column}\", {input}, 1)",
    input=[q.good_jet_collection],
    output=[q.jtag_value_2],
    scopes=SCOPES,
)
mjj = Producer(
    name="m_jj",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.jet_p4_1, q.jet_p4_2],
    output=[q.mjj],
    scopes=SCOPES,
)
BasicJetQuantities = ProducerGroup(
    name="BasicJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=[
        LVJet1,
        LVJet2,
        NumberOfJets,
        jpt_1,
        jeta_1,
        jphi_1,
        jtag_value_1,
        jpt_2,
        jeta_2,
        jphi_2,
        jtag_value_2,
        mjj,
    ],
)

##########################
# Basic b-Jet Quantities
# nbtag, pt, eta, phi, b-tag value
##########################

LVBJet1 = Producer(
    name="LVBJet1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_bjet_collection,
    ],
    output=[q.bjet_p4_1],
    scopes=SCOPES,
)
LVBJet2 = Producer(
    name="LVBJet2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        q.good_bjet_collection,
    ],
    output=[q.bjet_p4_2],
    scopes=SCOPES,
)

NumberOfBJets = Producer(
    name="NumberOfBJets",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_bjet_collection],
    output=[q.n_bjets],
    scopes=SCOPES,
)

NumberOfBJets_boosted = Producer(
    name="NumberOfBJets_boosted",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_bjet_collection_boosted],
    output=[q.n_bjets_boosted],
    scopes=SCOPES,
)

# bpt_1 = Producer(
#     name="bpt_1",
#     call="lorentzvector::GetPt({df}, {output}, {input})",
#     input=[q.bjet_p4_1],
#     output=[q.bpt_1],
#     scopes=SCOPES,
# )
# bpt_2 = Producer(
#     name="bpt_2",
#     call="lorentzvector::GetPt({df}, {output}, {input})",
#     input=[q.bjet_p4_2],
#     output=[q.bpt_2],
#     scopes=SCOPES,
# )
# beta_1 = Producer(
#     name="beta_1",
#     call="lorentzvector::GetEta({df}, {output}, {input})",
#     input=[q.bjet_p4_1],
#     output=[q.beta_1],
#     scopes=SCOPES,
# )
# beta_2 = Producer(
#     name="beta_2",
#     call="lorentzvector::GetEta({df}, {output}, {input})",
#     input=[q.bjet_p4_2],
#     output=[q.beta_2],
#     scopes=SCOPES,
# )
# bphi_1 = Producer(
#     name="bphi_1",
#     call="lorentzvector::GetPhi({df}, {output}, {input})",
#     input=[q.bjet_p4_1],
#     output=[q.bphi_1],
#     scopes=SCOPES,
# )
# bphi_2 = Producer(
#     name="bphi_2",
#     call="lorentzvector::GetPhi({df}, {output}, {input})",
#     input=[q.bjet_p4_2],
#     output=[q.bphi_2],
#     scopes=SCOPES,
# )
# btag_value_deepjet_1 = Producer(
#     name="btag_value_deepjet_1",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
#     input=[nanoAOD.Jet_btagDeepFlavB, q.good_bjet_collection],
#     output=[q.btag_value_1],
#     scopes=SCOPES,
# )
# btag_value_deepjet_2 = Producer(
#     name="btag_value_deepjet_1",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
#     input=[nanoAOD.Jet_btagDeepFlavB, q.good_bjet_collection],
#     output=[q.btag_value_2],
#     scopes=SCOPES,
# )
# btag_value_pnet_1 = Producer(
#     name="btag_value_pnet_1",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
#     input=[nanoAOD.Jet_btagPNetB, q.good_bjet_collection],
#     output=[q.btag_value_1],
#     scopes=SCOPES,
# )
# btag_value_pnet_2 = Producer(
#     name="btag_value_pnet_2",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
#     input=[nanoAOD.Jet_btagPNetB, q.good_bjet_collection],
#     output=[q.btag_value_2],
#     scopes=SCOPES,
# )
# btag_value_upart_1 = Producer(
#     name="btag_value_upart_1",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
#     input=[nanoAOD.Jet_btagUParTAK4B, q.good_bjet_collection],
#     output=[q.btag_value_1],
#     scopes=SCOPES,
# )
# btag_value_pnet_2 = Producer(
#     name="btag_value_upart_2",
#     call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
#     input=[nanoAOD.Jet_btagUParTAK4B, q.good_bjet_collection],
#     output=[q.btag_value_2],
#     scopes=SCOPES,
# )
BasicBJetQuantities = ProducerGroup(
    name="BasicBJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=[
        NumberOfBJets,
    ],
)
