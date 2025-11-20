"""
Producers for AK4 jet energy scale and resolution corrections, object selections, overlap vetoes, and quantities to be stored.
"""

from ..quantities import output as q
from ..quantities import nanoAOD, nanoAOD_run2
from code_generation.producer import Producer, ProducerGroup

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES, SCOPES


#
# JET ENERGY SCALE AND RESOLUTION CORRECTIONS
#


# create jet energy correction producers for AK4 jets for Run 2
JetEnergyCorrection_data_Run2, JetEnergyCorrectionRun2, RenameJetsDataRun2 = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.Jet_pt,
        "jet_eta": nanoAOD.Jet_eta,
        "jet_phi": nanoAOD.Jet_phi,
        "jet_mass": nanoAOD.Jet_mass,
        "jet_area": nanoAOD.Jet_area,
        "jet_raw_factor": nanoAOD.Jet_rawFactor,
        "jet_id": nanoAOD.Jet_jetId,
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
    lhc_run=2,
)

# create jet energy correction producers for AK4 jets
JetEnergyCorrection_data, JetEnergyCorrection, RenameJetsData = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.Jet_pt,
        "jet_eta": nanoAOD.Jet_eta,
        "jet_phi": nanoAOD.Jet_phi,
        "jet_mass": nanoAOD.Jet_mass,
        "jet_area": nanoAOD.Jet_area,
        "jet_raw_factor": nanoAOD.Jet_rawFactor,
        "jet_id": nanoAOD.Jet_jetId,
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
    lhc_run=3,  # TODO also add producer for Run 2
)


#
# AK4 JET SELECTION
#

# correct the jet ID value for Run3 samples
JetIDRun3NanoV12Corrected = Producer(
    name="JetIDRun3NanoV12Corrected",
    call="physicsobject::jet::quantities::CorrectJetIDRun3NanoV12({df}, {output}, {input})",
    input=[
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_jetId,
        nanoAOD.Jet_neHEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Jet_muEF,
        nanoAOD.Jet_chEmEF,
    ],
    output=[q.Jet_ID_corrected],
    scopes=GLOBAL_SCOPES,
)

# for Run 2, the Jet ID implementation is correct, just rename the column
JetIDRun2 = Producer(
    name="JetIDRun2",
    call="event::quantity::Rename<ROOT::RVec<UChar_t>>({df}, {output}, {input})",
    input=[nanoAOD.Jet_jetId],
    output=[q.Jet_ID_corrected],
    scopes=GLOBAL_SCOPES,
)

# jet selection including the pileup ID (for CHS jets)
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

# jet selection not applying the pileup ID (for PUPPI jets)
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

# base jet selection for b jets including the pileup ID (for CHS jets)
GoodBJetsBaseWithPUID = Producer(
    name="GoodBJetsBaseWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto}, {ak4jet_puid_wp}, {ak4jet_puid_max_pt})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        q.Jet_ID_corrected,
        nanoAOD_run2.Jet_puId,
    ],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# base jet selection for b jets not applying the pileup ID (for PUPPI jets)
GoodBJetsBaseWithoutPUID = Producer(
    name="GoodBJetsBaseWithoutPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_apply_jet_horn_veto})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_jetId,
    ],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# requirement on b tagging score
BTagCut = Producer(
    name="BTagCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {bjet_min_deepjet_score})",
    input=[nanoAOD_run2.Jet_btagDeepFlavB],
    output=[q.Jet_deepjet_b_tagged_medium],
    scopes=GLOBAL_SCOPES,
)

# b jet selection combining the base b jet selection and the b tagging requirement not applying the pileup ID (for PUPPI jets)
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

# b jet selection combining the base b jet selection and the b tagging requirement including the pileup ID (for CHS jets)
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

# combined jet-bjet mask (OR)
GoodJetsCombinedWithoutPUID = Producer(
    name="GoodJetsCombinedWithoutPUID",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "any_of")',
    input=[q.good_jets_mask, q.good_bjets_mask],
    output=[q.good_jets_combined_mask],
    scopes=GLOBAL_SCOPES,
)


#
# OVERLAP VETOES
# TODO could be simplified by designing a generic function
#


# check whether a jet is overlapping with the tight lepton candidates from resolved selection
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

# check whether a jet is overlapping with the tight lepton candidates from boosted selection
VetoOverlappingJets_boosted = Producer(
    name="VetoOverlappingJets_boosted",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {ak4jet_veto_min_delta_r})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.jet_overlap_veto_mask_boosted],
    scopes=SCOPES,
)

# create a mask that includes selected jets that do not overlap with the lepton candidates from the resolved selection
GoodJetsWithVeto = ProducerGroup(
    name="GoodJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_mask],
    output=[],
    scopes=SCOPES,
    subproducers=[VetoOverlappingJets],
)

# create a mask that includes selected jets that do not overlap with the lepton candidates from the boosted selection
GoodJetsWithVeto_boosted = ProducerGroup(
    name="GoodJetsWithVeto_boosted",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_mask],
    output=[],
    scopes=SCOPES,
    subproducers=[VetoOverlappingJets_boosted],
)

# create a mask that includes selected jets + b jets that do not overlap with the lepton candidates from the resolved selection
GoodJetsCombinedWithVeto = Producer(
    name="GoodCombinedJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_combined_mask, q.jet_overlap_veto_mask],
    output=[],
    scopes=SCOPES,
)

# create a mask that includes selected b-jets that do not overlap with the lepton candidates from the resolved selection
GoodBJetsWithVeto = Producer(
    name="GoodBJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_bjets_mask, q.jet_overlap_veto_mask],
    output=[],
    scopes=SCOPES,
)

# create a mask that includes selected b-jets that do not overlap with the lepton candidates from the boosted selection
GoodBJetsWithVeto_boosted = Producer(
    name="GoodBJetsWithVeto_boosted",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_bjets_mask, q.jet_overlap_veto_mask_boosted],
    output=[],
    scopes=SCOPES,
)

# final jet collection as list of indices of selected jets, ordered by pt for the resolved selection
JetCollection = ProducerGroup(
    name="JetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_jet_collection],
    scopes=SCOPES,
    subproducers=[GoodJetsWithVeto],
)

# final jet collection as list of indices of selected jets, ordered by pt for the boosted selection
JetCollection_boosted = ProducerGroup(
    name="JetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_jet_collection_boosted],
    scopes=SCOPES,
    subproducers=[GoodJetsWithVeto_boosted],
)

# final b jet collection as list of indices of selected jets, ordered by pt for the resolved selection
BJetCollection = ProducerGroup(
    name="BJetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_bjet_collection],
    scopes=SCOPES,
    subproducers=[GoodBJetsWithVeto],
)

# final b jet collection as list of indices of selected jets, ordered by pt for the boosted selection
BJetCollection_boosted = ProducerGroup(
    name="BJetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_bjet_collection_boosted],
    scopes=SCOPES,
    subproducers=[GoodBJetsWithVeto_boosted],
)

# final combined jet collection as list of indices of selected jets, ordered by pt for the resolved selection
JetCombinedCollection = ProducerGroup(
    name="JetCombinedCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected],
    output=[q.good_jet_combined_collection],
    scopes=SCOPES,
    subproducers=[GoodJetsCombinedWithVeto],
)

#
# JET QUANTITIES
# TODO simplify this by designing a generic function
#


jet_column_producers = []
for q_input, q_output, data_type in [
    (q.Jet_pt_corrected, q.jet_pt, "float"),
    (nanoAOD.Jet_eta, q.jet_eta, "float"),
    (nanoAOD.Jet_phi, q.jet_phi, "float"),
    (q.Jet_mass_corrected, q.jet_mass, "float"),
    (q.Jet_ID_corrected, q.jet_id, "UChar_t"),
    (nanoAOD.Jet_btagDeepFlavB, q.jet_deepjet_b_score, "float"),
    (q.Jet_deepjet_b_tagged_medium, q.jet_deepjet_b_tagged_medium, "int"),
]:
    jet_column_producers.append(
        Producer(
            name=f"JetColumn_{q_output.name}",
            call=f"event::quantity::Take<{data_type}>({{df}}, {{output}}, {{input}})",
            input=[q_input, q.good_jet_combined_collection],
            output=[q_output],
            scopes=SCOPES,
        )
    )


# columns for jet pt regression with PNet
jet_column_producers.extend(
    [
        Producer(
            name="JetColumn_jet_pt_pnet",
            call="jet::quantities::JetPtPNetRegression({df}, {output}, {input})",
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
            call="jet::quantities::JetPtPNetRegressionWithNeutrino({df}, {output}, {input})",
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
            call="jet::quantities::JetPtPNetRegressionResolution({df}, {output}, {input})",
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


JetColumns = ProducerGroup(
    name="JetColumns",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=jet_column_producers,
)


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
    output=[q.njets],
    scopes=SCOPES,
)
NumberOfJets_boosted = Producer(
    name="NumberOfJets_boosted",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_jet_collection_boosted],
    output=[q.njets_boosted],
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
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD_run2.Jet_btagDeepFlavB, q.good_jet_collection],
    output=[q.jtag_value_1],
    scopes=SCOPES,
)
jtag_value_2 = Producer(
    name="jtag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD_run2.Jet_btagDeepFlavB, q.good_jet_collection],
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
        # NumberOfJets_boosted,
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
    output=[q.nbtag],
    scopes=SCOPES,
)
NumberOfBJets_boosted = Producer(
    name="NumberOfBJets_boosted",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_bjet_collection_boosted],
    output=[q.nbtag_boosted],
    scopes=SCOPES,
)
bpt_1 = Producer(
    name="bpt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.bpt_1],
    scopes=SCOPES,
)
bpt_2 = Producer(
    name="bpt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.bpt_2],
    scopes=SCOPES,
)
beta_1 = Producer(
    name="beta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.beta_1],
    scopes=SCOPES,
)
beta_2 = Producer(
    name="beta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.beta_2],
    scopes=SCOPES,
)
bphi_1 = Producer(
    name="bphi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.bphi_1],
    scopes=SCOPES,
)
bphi_2 = Producer(
    name="bphi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.bphi_2],
    scopes=SCOPES,
)
btag_value_1 = Producer(
    name="btag_value_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD_run2.Jet_btagDeepFlavB, q.good_bjet_collection],
    output=[q.btag_value_1],
    scopes=SCOPES,
)
btag_value_2 = Producer(
    name="btag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD_run2.Jet_btagDeepFlavB, q.good_bjet_collection],
    output=[q.btag_value_2],
    scopes=SCOPES,
)
BasicBJetQuantities = ProducerGroup(
    name="BasicBJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=[
        # LVBJet1,
        # LVBJet2,
        NumberOfBJets,
        # NumberOfBJets_boosted,
        # bpt_1,
        # beta_1,
        # bphi_1,
        # btag_value_1,
        # bpt_2,
        # beta_2,
        # bphi_2,
        # btag_value_2,
    ],
)
