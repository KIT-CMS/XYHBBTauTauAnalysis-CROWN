"""
Producers for AK8 jet energy scale and resolution corrections, object selections, overlap vetoes, and quantities to be stored.
"""



from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES


#
# JET ENERGY SCALE AND RESOLUTION CORRECTIONS
#


# create jet energy correction producers for AK8 jets (Run 2)
FatJetEnergyCorrection_data_Run2, FatJetEnergyCorrectionRun2, RenameFatJetsDataRun2 = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.FatJet_pt,
        "jet_eta": nanoAOD.FatJet_eta,
        "jet_phi": nanoAOD.FatJet_phi,
        "jet_mass": nanoAOD.FatJet_mass,
        "jet_area": nanoAOD.FatJet_area,
        "jet_raw_factor": nanoAOD.FatJet_rawFactor,
        "jet_id": nanoAOD.FatJet_jetId,
        "gen_jet_pt": nanoAOD.GenJetAK8_pt,
        "gen_jet_eta": nanoAOD.GenJetAK8_eta,
        "gen_jet_phi": nanoAOD.GenJetAK8_phi,
        "rho": nanoAOD.Rho_fixedGridRhoFastjetAll,
        "luminosity_block": nanoAOD.luminosityBlock,
        "run": nanoAOD.run,
        "event": nanoAOD.event,
    },
    output={
        "jet_pt_corrected": q.FatJet_pt_corrected,
        "jet_mass_corrected": q.FatJet_mass_corrected,
    },
    scopes=GLOBAL_SCOPES,
    producer_prefix="FatJet",
    config_parameter_prefix="ak8jet",
    lhc_run=2,
)



# create jet energy correction producers for AK8 jets
FatJetEnergyCorrection_data, FatJetEnergyCorrection, RenameFatJetsData = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.FatJet_pt,
        "jet_eta": nanoAOD.FatJet_eta,
        "jet_phi": nanoAOD.FatJet_phi,
        "jet_mass": nanoAOD.FatJet_mass,
        "jet_area": nanoAOD.FatJet_area,
        "jet_raw_factor": nanoAOD.FatJet_rawFactor,
        "jet_id": nanoAOD.FatJet_jetId,
        "gen_jet_pt": nanoAOD.GenJetAK8_pt,
        "gen_jet_eta": nanoAOD.GenJetAK8_eta,
        "gen_jet_phi": nanoAOD.GenJetAK8_phi,
        "rho": nanoAOD.Rho_fixedGridRhoFastjetAll,
        "luminosity_block": nanoAOD.luminosityBlock,
        "run": nanoAOD.run,
        "event": nanoAOD.event,
    },
    output={
        "jet_pt_corrected": q.FatJet_pt_corrected,
        "jet_mass_corrected": q.FatJet_mass_corrected,
    },
    scopes=GLOBAL_SCOPES,
    producer_prefix="FatJet",
    config_parameter_prefix="ak8jet",
    lhc_run=3,
)


#
# AK8 JET SELECTION
#


# jet selection not applying the pileup ID (for PUPPI jets)
GoodFatJetsWithoutPUID = Producer(
    name="GoodFatJetsWithPUID",
    call="xyh::object_selection::jet({df}, {output}, {input}, {ak8jet_min_pt}, {ak8jet_max_abs_eta}, {ak8jet_id_wp})",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_jetId,
    ],
    output=[q.good_fatjets_mask],
    scopes=GLOBAL_SCOPES,
)

# use the selection with pileup ID as default
GoodFatJets = GoodFatJetsWithoutPUID


#
# OVERLAP VETOES
# TODO could be simplified by designing a generic function
#


# check whether an AK8 jet is overlapping with the tight lepton candidates from resolved selection
VetoOverlappingFatJets = Producer(
    name="VetoOverlappingFatJets",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, q.p4_1, q.p4_2],
    output=[q.fatjet_overlap_veto_mask],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

# check whether an AK8 jet is overlapping with the tight lepton candidates from boosted selection
VetoOverlappingFatJets_boosted = Producer(
    name="VetoOverlappingFatJets_boosted",
    call="physicsobject::jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.fatjet_overlap_veto_mask_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

# create a mask that includes selected AK8 jets that do not overlap with the lepton candidates from the resolved selection
GoodFatJetsWithVeto = ProducerGroup(
    name="GoodJetsWithVeto",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_fatjets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingFatJets],
)

# create a mask that includes selected AK8 jets that do not overlap with the lepton candidates from the boosted selection
GoodFatJetsWithVeto_boosted = ProducerGroup(
    name="GoodJetsWithVeto_boosted",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[q.good_fatjets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingFatJets_boosted],
)

# final AK8 jet collection as list of indices of selected jets, ordered by pt for the resolved selection
FatJetCollection = ProducerGroup(
    name="FatJetCollection",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.good_fatjet_collection],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodFatJetsWithVeto],
)

# final AK8 jet collection as list of indices of selected jets, ordered by pt for the boosted selection
FatJetCollection_boosted = ProducerGroup(
    name="FatJetCollection_boosted",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.good_fatjet_collection_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodFatJetsWithVeto_boosted],
)

# final AK8 jet collection as list of indices of selected jets without veto, ordered by pt for the boosted selection
FatJetCollectionWithoutVeto = Producer(
    name="FatJetCollectionWithoutVeto",
    call="physicsobject::OrderByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected, q.good_fatjets_mask],
    output=[q.good_fatjet_collection_without_veto],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)


#
# JET QUANTITIES
# TODO simplify this by designing a generic function
#


LVFatJet1 = Producer(
    name="LVFatJet1",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.good_fatjet_collection,
    ],
    output=[q.fatjet_p4_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LVFatJet2 = Producer(
    name="LVFatJet2",
    call="lorentzvector::Build({df}, {output}, {input}, 1)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.good_fatjet_collection,
    ],
    output=[q.fatjet_p4_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

NumberOfFatJets = Producer(
    name="NumberOfFatJets",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_fatjet_collection],
    output=[q.nfatjets],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfFatJets_boosted = Producer(
    name="NumberOfFatJets_boosted",
    call="physicsobject::Size<Int_t>({df}, {output}, {input})",
    input=[q.good_fatjet_collection_boosted],
    output=[q.nfatjets_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_pt_1 = Producer(
    name="fj_pt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_pt_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_eta_1 = Producer(
    name="fj_eta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_eta_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_phi_1 = Producer(
    name="fj_phi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_phi_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_mass_1 = Producer(
    name="fj_mass_1",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.fatjet_p4_1],
    output=[q.fj_mass_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_msoftdrop_1 = Producer(
    name="msoftdrop_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.good_fatjet_collection],
    output=[q.fj_msoftdrop_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_particleNet_XbbvsQCD_1 = Producer(
    name="particleNet_XbbvsQCD_1",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, nanoAOD.FatJet_particleNet_QCD, q.good_fatjet_collection],
    output=[q.fj_particleNet_XbbvsQCD_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_2over1_1 = Producer(
    name="nsubjettiness_2over1_1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_2over1_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_3over2_1 = Producer(
    name="nsubjettiness_3over2_1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_3over2_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_pt_2 = Producer(
    name="fj_pt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.fatjet_p4_2],
    output=[q.fj_pt_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_eta_2 = Producer(
    name="fj_eta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.fatjet_p4_2],
    output=[q.fj_eta_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_phi_2 = Producer(
    name="fj_phi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.fatjet_p4_2],
    output=[q.fj_phi_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_mass_2 = Producer(
    name="fj_mass_2",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.fatjet_p4_2],
    output=[q.fj_mass_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_msoftdrop_2 = Producer(
    name="msoftdrop_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.FatJet_msoftdrop, q.good_fatjet_collection],
    output=[q.fj_msoftdrop_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_particleNet_XbbvsQCD_2 = Producer(
    name="particleNet_XbbvsQCD_2",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 1)",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, nanoAOD.FatJet_particleNet_QCD, q.good_fatjet_collection],
    output=[q.fj_particleNet_XbbvsQCD_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_2over1_2 = Producer(
    name="nsubjettiness_2over1_2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 1)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_2over1_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_nsubjettiness_3over2_2 = Producer(
    name="nsubjettiness_3over2_2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 1)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.good_fatjet_collection],
    output=[q.fj_nsubjettiness_3over2_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

BasicFatJetQuantities = ProducerGroup(
    name="BasicFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVFatJet1,
        # LVFatJet2,
        NumberOfFatJets,
        NumberOfFatJets_boosted,
        fj_pt_1,
        fj_eta_1,
        fj_phi_1,
        fj_mass_1,
        fj_msoftdrop_1,
        fj_particleNet_XbbvsQCD_1,
        fj_nsubjettiness_2over1_1,
        fj_nsubjettiness_3over2_1,
        # fj_pt_2,
        # fj_eta_2,
        # fj_phi_2,
        # fj_mass_2,
        # fj_msoftdrop_2,
        # fj_particleNet_XbbvsQCD_2,
        # fj_nsubjettiness_2over1_2,
        # fj_nsubjettiness_3over2_2,
    ],
)

#
# AK8 JET-B JET MATCHING
#

FindFatjetMatchingBjet = Producer(
    name="FindFatjetMatchingBjet",
    call="fatjet::FindFatjetMatchingBjet({df}, {output}, {input}, {fatjet_bpair_matching_max_dR})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.bpair_p4_1,
    ],
    output=[q.bpair_fatjet],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVmatchedFatJet = Producer(
    name="LVmatchedFatJet",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.bpair_fatjet,
    ],
    output=[q.matched_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_pt = Producer(
    name="fj_matched_pt",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_eta = Producer(
    name="fj_matched_eta",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_phi = Producer(
    name="fj_matched_phi",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_mass = Producer(
    name="fj_matched_mass",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_msoftdrop = Producer(
    name="fj_matched_msoftdrop",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.bpair_fatjet],
    output=[q.fj_matched_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_particleNet_XbbvsQCD = Producer(
    name="fj_matched_particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, nanoAOD.FatJet_particleNet_QCD, q.bpair_fatjet],
    output=[q.fj_matched_particleNet_XbbvsQCD],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_nsubjettiness_2over1 = Producer(
    name="fj_matched_nsubjettiness_2over1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.bpair_fatjet],
    output=[q.fj_matched_nsubjettiness_2over1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_nsubjettiness_3over2 = Producer(
    name="fj_matched_nsubjettiness_3over2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.bpair_fatjet],
    output=[q.fj_matched_nsubjettiness_3over2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

BasicMatchedFatJetQuantities = ProducerGroup(
    name="BasicMatchedFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVmatchedFatJet,
        fj_matched_pt,
        fj_matched_eta,
        fj_matched_phi,
        fj_matched_mass,
        fj_matched_msoftdrop,
        fj_matched_particleNet_XbbvsQCD,
        fj_matched_nsubjettiness_2over1,
        fj_matched_nsubjettiness_3over2,
    ],
)

FindXbbFatjet = Producer(
    name="FindXbbFatjet",
    call="fatjet::FindXbbFatjet({df}, {output}, {input})",
    input=[
        q.good_fatjet_collection,
        nanoAOD.FatJet_particleNet_XbbVsQCD,
        nanoAOD.FatJet_particleNet_QCD,
    ],
    output=[q.Xbb_fatjet],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVXbbFatJet = Producer(
    name="LVXbbFatJet",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.Xbb_fatjet,
    ],
    output=[q.Xbb_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_pt = Producer(
    name="fj_Xbb_pt",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_eta = Producer(
    name="fj_Xbb_eta",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_phi = Producer(
    name="fj_Xbb_phi",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_mass = Producer(
    name="fj_Xbb_mass",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_msoftdrop = Producer(
    name="fj_Xbb_msoftdrop",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.Xbb_fatjet],
    output=[q.fj_Xbb_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_particleNet_XbbvsQCD = Producer(
    name="fj_Xbb_particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, nanoAOD.FatJet_particleNet_QCD, q.Xbb_fatjet],
    output=[q.fj_Xbb_particleNet_XbbvsQCD],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nsubjettiness_2over1 = Producer(
    name="fj_Xbb_nsubjettiness_2over1",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.Xbb_fatjet],
    output=[q.fj_Xbb_nsubjettiness_2over1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nsubjettiness_3over2 = Producer(
    name="fj_Xbb_nsubjettiness_3over2",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.Xbb_fatjet],
    output=[q.fj_Xbb_nsubjettiness_3over2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_hadflavor = Producer(
    name="fj_Xbb_hadflavor",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_hadronFlavour, q.Xbb_fatjet],
    output=[q.fj_Xbb_hadflavor],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nBhad = Producer(
    name="fj_Xbb_nBhad",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nBHadrons, q.Xbb_fatjet],
    output=[q.fj_Xbb_nBhad],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nChad = Producer(
    name="fj_Xbb_nChad",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nCHadrons, q.Xbb_fatjet],
    output=[q.fj_Xbb_nChad],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
BasicXbbFatJetQuantities = ProducerGroup(
    name="BasicXbbFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVXbbFatJet,
        fj_Xbb_pt,
        fj_Xbb_eta,
        fj_Xbb_phi,
        fj_Xbb_mass,
        fj_Xbb_msoftdrop,
        fj_Xbb_particleNet_XbbvsQCD,
        fj_Xbb_nsubjettiness_2over1,
        fj_Xbb_nsubjettiness_3over2,
        fj_Xbb_hadflavor,
        fj_Xbb_nBhad,
        fj_Xbb_nChad,
    ],
)

FindXbbFatjet_boosted = Producer(
    name="FindXbbFatjet_boosted",
    call="fatjet::FindXbbFatjet({df}, {output}, {input})",
    input=[
        q.good_fatjet_collection_boosted,
        nanoAOD.FatJet_particleNet_XbbVsQCD,
        nanoAOD.FatJet_particleNet_QCD,
    ],
    output=[q.Xbb_fatjet_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVXbbFatJet_boosted = Producer(
    name="LVXbbFatJet_boosted",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.Xbb_fatjet_boosted,
    ],
    output=[q.Xbb_fatjet_p4_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_pt_boosted = Producer(
    name="fj_Xbb_pt_boosted",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_pt_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_eta_boosted = Producer(
    name="fj_Xbb_eta_boosted",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_eta_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_phi_boosted = Producer(
    name="fj_Xbb_phi_boosted",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_phi_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_mass_boosted = Producer(
    name="fj_Xbb_mass_boosted",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_mass_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_msoftdrop_boosted = Producer(
    name="fj_Xbb_msoftdrop_boosted",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_msoftdrop_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_particleNet_XbbvsQCD_boosted = Producer(
    name="fj_Xbb_particleNet_XbbvsQCD_boosted",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, nanoAOD.FatJet_particleNet_QCD, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_particleNet_XbbvsQCD_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nsubjettiness_2over1_boosted = Producer(
    name="fj_Xbb_nsubjettiness_2over1_boosted",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau2, nanoAOD.FatJet_tau1, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_nsubjettiness_2over1_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nsubjettiness_3over2_boosted = Producer(
    name="fj_Xbb_nsubjettiness_3over2_boosted",
    call="quantities::fatjet::nsubjettiness_ratio({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_tau3, nanoAOD.FatJet_tau2, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_nsubjettiness_3over2_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_hadflavor_boosted = Producer(
    name="fj_Xbb_hadflavor_boosted",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_hadronFlavour, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_hadflavor_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nBhad_boosted = Producer(
    name="fj_Xbb_nBhad_boosted",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nBHadrons, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_nBhad_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nChad_boosted = Producer(
    name="fj_Xbb_nChad_boosted",
    call="event::quantity::Get<UChar_t>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nCHadrons, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_nChad_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
BasicXbbFatJetQuantities_boosted = ProducerGroup(
    name="BasicXbbFatJetQuantities_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVXbbFatJet_boosted,
        fj_Xbb_pt_boosted,
        fj_Xbb_eta_boosted,
        fj_Xbb_phi_boosted,
        fj_Xbb_mass_boosted,
        fj_Xbb_msoftdrop_boosted,
        fj_Xbb_particleNet_XbbvsQCD_boosted,
        fj_Xbb_nsubjettiness_2over1_boosted,
        fj_Xbb_nsubjettiness_3over2_boosted,
        fj_Xbb_hadflavor_boosted,
        fj_Xbb_nBhad_boosted,
        fj_Xbb_nChad_boosted,
    ],
)
LVLeadingFatJet = Producer(
    name="LVLeadingFatJet",
    call="lorentzvector::Build({df}, {output}, {input}, 0)",
    input=[
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.good_fatjet_collection_without_veto,
    ],
    output=[q.leading_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_leading_pt = Producer(
    name="fj_leading_pt",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.leading_fatjet_p4],
    output=[q.fj_leading_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_leading_msoftdrop = Producer(
    name="fj_leading_msoftdrop",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.good_fatjet_collection_without_veto],
    output=[q.fj_leading_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LeadingFatJetQuantities = ProducerGroup(
    name="LeadingFatJetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[
        LVLeadingFatJet,
        fj_leading_pt,
        fj_leading_msoftdrop,
    ],
)
