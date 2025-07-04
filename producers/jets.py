from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES


#
# jet energy corrections
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


####################
# Set of producers used for selection possible good jets
####################
JetPtCut = Producer(
    name="JetPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_jet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=GLOBAL_SCOPES,
)
BJetPtCut = Producer(
    name="BJetPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_bjet_pt})",
    input=[q.Jet_pt_corrected],
    output=[],
    scopes=GLOBAL_SCOPES,
)
JetEtaCut = Producer(
    name="JetEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_jet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=GLOBAL_SCOPES,
)
BJetEtaCut = Producer(
    name="BJetEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {max_bjet_eta})",
    input=[nanoAOD.Jet_eta],
    output=[],
    scopes=GLOBAL_SCOPES,
)
JetIDCut = Producer(
    name="JetIDCut",
    call="physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {jet_id})",
    input=[nanoAOD.Jet_ID],
    output=[q.jet_id_mask],
    scopes=GLOBAL_SCOPES,
)
JetPUIDCut = Producer(
    name="JetPUIDCut",
    call="physicsobject::jet::CutPileupID({df}, {output}, {input}, {jet_puid}, {jet_puid_max_pt})",
    input=[nanoAOD.Jet_PUID, q.Jet_pt_corrected],
    output=[q.jet_puid_mask],
    scopes=GLOBAL_SCOPES,
)
BTagCut = Producer(
    name="BTagCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {btag_cut})",
    input=[nanoAOD.BJet_discriminator],
    output=[],
    scopes=GLOBAL_SCOPES,
)
GoodJets = ProducerGroup(
    name="GoodJets",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[q.good_jets_mask],
    scopes=GLOBAL_SCOPES,
    subproducers=[JetPtCut, JetEtaCut, JetIDCut, JetPUIDCut],
)
GoodBJets = ProducerGroup(
    name="GoodBJets",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.jet_id_mask, q.jet_puid_mask],
    output=[q.good_bjets_mask],
    scopes=GLOBAL_SCOPES,
    subproducers=[BJetPtCut, BJetEtaCut, BTagCut],
)
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
BJetEnergyCorrection = ProducerGroup(
    name="BJetEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=GLOBAL_SCOPES,
    subproducers=[BJetPtCorrection, BJetMassCorrection],
)

####################
# Set of producers to apply a veto of jets overlapping with ditaupair candidates and ordering jets by their pt
# 1. check all jets vs the two lepton candidates, if they are not within deltaR = 0.5, keep them --> mask
# 2. Combine mask with good_jets_mask
# 3. Generate JetCollection, an RVec containing all indices of good Jets in pt order
# 4. generate jet quantity outputs
####################
VetoOverlappingJets = Producer(
    name="VetoOverlappingJets",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, q.p4_1, q.p4_2],
    output=[q.jet_overlap_veto_mask],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

VetoOverlappingJets_boosted = Producer(
    name="VetoOverlappingJets_boosted",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_jet_veto})",
    input=[nanoAOD.Jet_eta, nanoAOD.Jet_phi, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.jet_overlap_veto_mask_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

GoodJetsWithVeto = ProducerGroup(
    name="GoodJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingJets],
)

GoodJetsWithVeto_boosted = ProducerGroup(
    name="GoodJetsWithVeto_boosted",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_jets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingJets_boosted],
)

GoodBJetsWithVeto = Producer(
    name="GoodBJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_bjets_mask, q.jet_overlap_veto_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

GoodBJetsWithVeto_boosted = Producer(
    name="GoodBJetsWithVeto_boosted",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_bjets_mask, q.jet_overlap_veto_mask_boosted],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

JetCollection = ProducerGroup(
    name="JetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_jet_collection],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodJetsWithVeto],
)
JetCollection_boosted = ProducerGroup(
    name="JetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_jet_collection_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodJetsWithVeto_boosted],
)

BJetCollection = ProducerGroup(
    name="BJetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_bjet_collection],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodBJetsWithVeto],
)
BJetCollection_boosted = ProducerGroup(
    name="BJetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.Jet_pt_corrected_bReg],
    output=[q.good_bjet_collection_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodBJetsWithVeto_boosted],
)

##########################
# Basic Jet Quantities
# njets, pt, eta, phi, b-tag value
##########################

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
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
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
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfJets = Producer(
    name="NumberOfJets",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_jet_collection],
    output=[q.njets],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfJets_boosted = Producer(
    name="NumberOfJets_boosted",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_jet_collection_boosted],
    output=[q.njets_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jpt_1 = Producer(
    name="jpt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jpt_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jpt_2 = Producer(
    name="jpt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jpt_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jeta_1 = Producer(
    name="jeta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jeta_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jeta_2 = Producer(
    name="jeta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jeta_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jphi_1 = Producer(
    name="jphi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.jet_p4_1],
    output=[q.jphi_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jphi_2 = Producer(
    name="jphi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.jet_p4_2],
    output=[q.jphi_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jtag_value_1 = Producer(
    name="jtag_value_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
    output=[q.jtag_value_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
jtag_value_2 = Producer(
    name="jtag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.good_jet_collection],
    output=[q.jtag_value_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
mjj = Producer(
    name="m_jj",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.jet_p4_1, q.jet_p4_2],
    output=[q.mjj],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
BasicJetQuantities = ProducerGroup(
    name="BasicJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
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
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
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
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfBJets = Producer(
    name="NumberOfBJets",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_bjet_collection],
    output=[q.nbtag],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfBJets_boosted = Producer(
    name="NumberOfBJets_boosted",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_bjet_collection_boosted],
    output=[q.nbtag_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpt_1 = Producer(
    name="bpt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.bpt_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpt_2 = Producer(
    name="bpt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.bpt_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
beta_1 = Producer(
    name="beta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.beta_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
beta_2 = Producer(
    name="beta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.beta_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bphi_1 = Producer(
    name="bphi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bjet_p4_1],
    output=[q.bphi_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bphi_2 = Producer(
    name="bphi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bjet_p4_2],
    output=[q.bphi_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
btag_value_1 = Producer(
    name="btag_value_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
    output=[q.btag_value_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
btag_value_2 = Producer(
    name="btag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.good_bjet_collection],
    output=[q.btag_value_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
BasicBJetQuantities = ProducerGroup(
    name="BasicBJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
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
