"""
Producers for jet energy scale and resolution corrections, object selections, overlap vetoes, and quantities to be stored.
"""

from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES, SCOPES


#
# JET ENERGY SCALE AND RESOLUTION CORRECTIONS
#

# create jet energy correction producers for AK4 jets
JetEnergyCorrection_data, JetEnergyCorrection, RenameJetsData = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.Jet_pt,
        "jet_eta": nanoAOD.Jet_eta,
        "jet_phi": nanoAOD.Jet_phi,
        "jet_mass": nanoAOD.Jet_mass,
        "jet_area": nanoAOD.Jet_area,
        "jet_raw_factor": nanoAOD.Jet_rawFactor,
        "jet_id": nanoAOD.Jet_ID,
        "gen_jet_pt": nanoAOD.GenJet_pt,
        "gen_jet_eta": nanoAOD.GenJet_eta,
        "gen_jet_phi": nanoAOD.GenJet_phi,
        "rho": nanoAOD.rho_v12,
    },
    output={
        "jet_pt_corrected": q.Jet_pt_corrected,
        "jet_mass_corrected": q.Jet_mass_corrected,
    },
    scopes=GLOBAL_SCOPES,
    producer_prefix="Jet",
    config_parameter_prefix="jet",
)


#
# JET SELECTION
#


# jet selection including the pileup ID (for CHS jets)
GoodJetsWithPUID = Producer(
    name="GoodJetsWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {ak4jet_min_pt}, {ak4jet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_puid_wp}, {ak4jet_puid_max_pt})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_ID,
        nanoAOD.Jet_PUID,
    ],
    output=[q.good_jets_mask],
    scopes=GLOBAL_SCOPES,
)

# jet selection not applying the pileup ID (for PUPPI jets)
GoodJetsWithoutPUID = Producer(
    name="GoodJetsWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {ak4jet_min_pt}, {ak4jet_max_abs_eta}, {ak4jet_id_wp})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_ID,
    ],
    output=[q.good_jets_mask],
    scopes=GLOBAL_SCOPES,
)

# use the selection with pileup ID as default 
GoodJets = GoodJetsWithoutPUID

# base jet selection for b jets including the pileup ID (for CHS jets)
GoodBJetsBaseWithPUID = Producer(
    name="GoodBJetsBaseWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp}, {ak4jet_puid_wp}, {ak4jet_puid_max_pt})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_ID,
    ],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# base jet selection for b jets not applying the pileup ID (for PUPPI jets)
GoodBJetsBaseWithoutPUID = Producer(
    name="GoodBJetsBaseWithoutPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {bjet_min_pt}, {bjet_max_abs_eta}, {ak4jet_id_wp})",
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_ID,
    ],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# use the selection with pileup ID as default
GoodBJetsBase = GoodBJetsBaseWithoutPUID

# requirement on b tagging score
BTagCut = Producer(
    name="BTagCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {bjet_min_deepjet_score})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# b jet selection combining the base b jet selection and the b tagging requirement
GoodBJets = ProducerGroup(
    name="GoodBJets",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=GoodJets.output,
    output=[q.good_bjets_mask],
    subproducers=[
        GoodBJetsBase,
        BTagCut,
    ],
    scopes=GLOBAL_SCOPES,
)


#
# B JET ENERGY SCALE CORRECTIONS
#


# pt correction from energy scale corrections
BJetPtCorrection = Producer(
    name="BJetPtCorrection",
    call="physicsobject::jet::BJetPtCorrection({df}, {output}, {input})",
    input=[
        q.Jet_pt_corrected,
        q.good_bjets_mask,
        nanoAOD.BJet_bRegCorr,
    ],
    output=[q.Jet_pt_corrected_bReg],
    scopes=GLOBAL_SCOPES,
)

# mass correction from energy scale corrections
BJetMassCorrection = Producer(
    name="BJetMassCorrection",
    call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
    input=[
        q.Jet_mass_corrected,
        q.Jet_pt_corrected,
        q.Jet_pt_corrected_bReg,
    ],
    output=[q.Jet_mass_corrected_bReg],
    scopes=GLOBAL_SCOPES,
)

# producer group for b jet energy corrections to apply
BJetEnergyCorrection = ProducerGroup(
    name="BJetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    subproducers=[
        BJetPtCorrection,
        BJetMassCorrection,
    ],
    scopes=GLOBAL_SCOPES,
)


#
# OVERLAP VETOES
# TODO could be simplified by designing a generic function
#


# check whether a jet is overlapping with the tight lepton candidates from resolved selection
VetoOverlappingJets = Producer(
    name="VetoOverlappingJets",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
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
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
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
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_jet_collection],
    scopes=SCOPES,
    subproducers=[GoodJetsWithVeto],
)

# final jet collection as list of indices of selected jets, ordered by pt for the boosted selection
JetCollection_boosted = ProducerGroup(
    name="JetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_jet_collection_boosted],
    scopes=SCOPES,
    subproducers=[GoodJetsWithVeto_boosted],
)

# final b jet collection as list of indices of selected jets, ordered by pt for the resolved selection
BJetCollection = ProducerGroup(
    name="BJetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_bjet_collection],
    scopes=SCOPES,
    subproducers=[GoodBJetsWithVeto],
)

# final b jet collection as list of indices of selected jets, ordered by pt for the boosted selection
BJetCollection_boosted = ProducerGroup(
    name="BJetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_bjet_collection_boosted],
    scopes=SCOPES,
    subproducers=[GoodBJetsWithVeto_boosted],
)


#
# JET QUANTITIES
# TODO simplify this by designing a generic function
#


LVJet1 = Producer(
    name="LVJet1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        q.good_jet_collection,
    ],
    output=[q.jet_p4_1],
    scopes=SCOPES,
)
LVJet2 = Producer(
    name="LVJet2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        q.good_jet_collection,
    ],
    output=[q.jet_p4_2],
    scopes=SCOPES,
)
NumberOfJets = Producer(
    name="NumberOfJets",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_jet_collection],
    output=[q.njets],
    scopes=SCOPES,
)
NumberOfJets_boosted = Producer(
    name="NumberOfJets_boosted",
    call="physicsobject::Count({df}, {output}, {input})",
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
    input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
    output=[q.jtag_value_1],
    scopes=SCOPES,
)
jtag_value_2 = Producer(
    name="jtag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
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
        NumberOfJets_boosted,
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
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        q.good_bjet_collection,
    ],
    output=[q.bjet_p4_1],
    scopes=SCOPES,
)
LVBJet2 = Producer(
    name="LVBJet2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected_bReg,
        q.good_bjet_collection,
    ],
    output=[q.bjet_p4_2],
    scopes=SCOPES,
)
NumberOfBJets = Producer(
    name="NumberOfBJets",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_bjet_collection],
    output=[q.nbtag],
    scopes=SCOPES,
)
NumberOfBJets_boosted = Producer(
    name="NumberOfBJets_boosted",
    call="physicsobject::Count({df}, {output}, {input})",
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
    input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
    output=[q.btag_value_1],
    scopes=SCOPES,
)
btag_value_2 = Producer(
    name="btag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
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
        NumberOfBJets_boosted,
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
