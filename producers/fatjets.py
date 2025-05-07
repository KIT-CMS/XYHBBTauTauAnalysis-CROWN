from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.quantity import Quantity
from code_generation.producer import Producer, ProducerGroup
from typing import Dict, List

from ._helpers import jerc_producer_factory
from ..constants import GLOBAL_SCOPES


def fatjet_matched_object_quantities_producer_factory(
    input: Dict[str, Quantity],
    output: Dict[str, Quantity],
    position: int,
    scopes: List[str],
    producer_prefix: str = "FaJetMatchedObject",
):
    # check input quantity keys
    input_keys = {"match_index", "other_pt", "other_eta", "other_phi", "other_mass"}
    if set(input.keys()) != input_keys:
        raise ValueError(
            f"Input quantities must be {input_keys}"
        )

    # check output quantity keys
    output_keys = {"matched_object_pt", "matched_object_eta", "matched_object_phi", "matched_object_mass", "matched_object_charge"}
    if set(output.keys()) != output_keys:
        raise ValueError(
            f"Output quantities must be {output_keys}",
        )

    producers = []
    for quantity, template_type in [("pt", "float"), ("eta", "float"), ("phi", "float"), ("mass", "float"), ("charge", "UChar_t")]:
        producers.append(Producer(
            name=f"{producer_prefix}{position + 1}{quantity.capitalize()}",
            call=f"fatjet::matching::matched_object_quantity<{template_type}>({{df}}, {{output}}, {{input}}, {position}",
            input=[input[f"other_{quantity}"], input["match_index"]],
            output=[output[f"matched_object_{quantity}"]],
            scopes=scopes,
        ))

    # create the producer group for the matched object quantities
    producer_group = ProducerGroup(
        name=f"{producer_prefix}{position + 1}Quantities",
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=producers,
    )

    return producer_group


def single_fatjet_producer_factory(
    input: dict[str, Quantity],
    output: dict[str, Quantity],
    fatjet_position: int,
    producer_prefix="FatJet",
):

    # get input quantities
    good_fatjet_index = input["good_fatjet_index"]
    fatjet_pt_nanoaod = input["fatjet_pt_nanoaod"]
    fatjet_eta_nanoaod = input["fatjet_eta_nanoaod"]
    fatjet_phi_nanoaod= input["fatjet_phi_nanoaod"]
    fatjet_mass_nanoaod = input["fatjet_mass_nanoaod"]
    fatjet_mass_softdrop_nanoaod = input["fatjet_mass_softdrop_nanoaod"]
    fatjet_particlenet_mass_corr_nanoaod = output["fatjet_particlenet_mass_corr_nanoaod"]
    fatjet_particlenet_qcd_nanoaod = output["fatjet_particlenet_qcd_nanoaod"]
    fatjet_particlenet_xbb_vs_qcd_nanoaod = output["fatjet_particlenet_xbb_vs_qcd_nanoaod"]
    fatjet_particlenet_xte_vs_qcd_nanoaod = output["fatjet_particlenet_xte_vs_qcd_nanoaod"]
    fatjet_particlenet_xtm_vs_qcd_nanoaod = output["fatjet_particlenet_xtm_vs_qcd_nanoaod"]
    fatjet_particlenet_xtt_vs_qcd_nanoaod = output["fatjet_particlenet_xtt_vs_qcd_nanoaod"]
    fatjet_tau_1_nanoaod = input["fatjet_tau_1_nanoaod"]
    fatjet_tau_2_nanoaod = input["fatjet_tau_2_nanoaod"]
    fatjet_tau_3_nanoaod = input["fatjet_tau_3_nanoaod"]

    # get the output quantities
    fatjet_p4 = output["fatjet_p4"]
    fatjet_pt = output["fatjet_pt"]
    fatjet_eta = output["fatjet_eta"]
    fatjet_phi = output["fatjet_phi"]
    fatjet_mass = output["fatjet_mass"]
    fatjet_mass_softdrop = output["fatjet_mass_softdrop"]
    fatjet_mass_particlenet = output["fatjet_particlenet_mass_corr"]
    fatjet_particlenet_qcd = output["fatjet_particlenet_qcd"]
    fatjet_particlenet_xbb_vs_qcd = output["fatjet_particlenet_xbb_vs_qcd"]
    fatjet_particlenet_xte_vs_qcd = output["fatjet_particlenet_xte_vs_qcd"]
    fatjet_particlenet_xtm_vs_qcd = output["fatjet_particlenet_xtm_vs_qcd"]
    fatjet_particlenet_xtt_vs_qcd = output["fatjet_particlenet_xtt_vs_qcd"]
    fatjet_nsubjettiness_2over1 = output["fatjet_nsubjettiness_2over1"]
    fatjet_nsubjettiness_3over2 = output["fatjet_nsubjettiness_3over2"]

    # produce the fatjet four vector and its components
    p4_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}LV",
        call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
        input=[
            good_fatjet_index,
            fatjet_pt_nanoaod,
            fatjet_eta_nanoaod,
            fatjet_phi_nanoaod,
            fatjet_mass_nanoaod,
        ],
        output=[fatjet_p4],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    pt_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Pt",
        call="quantities::pt({df}, {output}, {input})",
        input=[fatjet_p4],
        output=[fatjet_pt],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    eta_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Eta",
        call="quantities::eta({df}, {output}, {input})",
        input=[fatjet_p4],
        output=[fatjet_eta],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    phi_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Phi",
        call="quantities::phi({df}, {output}, {input})",
        input=[fatjet_p4],
        output=[fatjet_phi],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    mass_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Mass",
        call="quantities::mass({df}, {output}, {input})",
        input=[fatjet_p4],
        output=[fatjet_mass],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )

    # other fatjet mass algorithms
    mass_softdrop_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}MassSoftdrop",
        call=f"quantities::fatjet::msoftdrop({{df}}, {{output}}, {{input}}, {fatjet_position})",
        input=[fatjet_mass_softdrop_nanoaod, good_fatjet_index],
        output=[fatjet_mass_softdrop],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    mass_particlenet_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}MassSoftdrop",
        call=f"quantities::fatjet::mass_particlenet({{df}}, {{output}}, {{input}}, {fatjet_position})",
        input=[fatjet_mass_nanoaod, fatjet_particlenet_mass_corr_nanoaod, good_fatjet_index],
        output=[fatjet_mass_particlenet],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )

    # ParticleNet scores
    pnet_qcd_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}ParticleNetQCD",
        call=f"basefunctions::getvar<float>({{df}}, {{output}}, {fatjet_position}, {{input}})",
        input=[good_fatjet_index, fatjet_particlenet_qcd_nanoaod],
        output=[fatjet_particlenet_qcd],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    pnet_xbb_vs_qcd_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}ParticleNetXbbVsQCD",
        call=f"basefunctions::getvar<float>({{df}}, {{output}}, {fatjet_position}, {{input}})",
        input=[good_fatjet_index, fatjet_particlenet_xbb_vs_qcd_nanoaod],
        output=[fatjet_particlenet_xbb_vs_qcd],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    pnet_xte_vs_qcd_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}ParticleNetXteVsQCD",
        call=f"basefunctions::getvar<float>({{df}}, {{output}}, {fatjet_position}, {{input}})",
        input=[good_fatjet_index, fatjet_particlenet_xte_vs_qcd_nanoaod],
        output=[fatjet_particlenet_xte_vs_qcd],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    pnet_xtm_vs_qcd_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}ParticleNetXtmVsQCD",
        call=f"basefunctions::getvar<float>({{df}}, {{output}}, {fatjet_position}, {{input}})",
        input=[good_fatjet_index, fatjet_particlenet_xtm_vs_qcd_nanoaod],
        output=[fatjet_particlenet_xtm_vs_qcd],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    pnet_xtt_vs_qcd_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}ParticleNetXttVsQCD",
        call=f"basefunctions::getvar<float>({{df}}, {{output}}, {fatjet_position}, {{input}})",
        input=[good_fatjet_index, fatjet_particlenet_xtt_vs_qcd_nanoaod],
        output=[fatjet_particlenet_xtt_vs_qcd],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )

    # n-subjettiness
    nsubjetiness_2over1_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Nsubjettiness2over1",
        call=f"quantities::fatjet::nsubjettiness_ratio({{df}}, {{output}}, {{input}}, {fatjet_position})",
        input=[fatjet_tau_2_nanoaod, fatjet_tau_1_nanoaod, good_fatjet_index],
        output=[fatjet_nsubjettiness_2over1],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )
    nsubjettiness_3over2_producer = Producer(
        name=f"{producer_prefix}{fatjet_position}Nsubjettiness3over2",
        call=f"quantities::fatjet::nsubjettiness_ratio({{df}}, {{output}}, {{input}}, {fatjet_position})",
        input=[fatjet_tau_3_nanoaod, fatjet_tau_2_nanoaod, good_fatjet_index],
        output=[fatjet_nsubjettiness_3over2],
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
    )

    # create the producer group
    fatjet_producer_group = ProducerGroup(
        name=f"{producer_prefix}{fatjet_position}BasicQuantities",
        call=None,
        input=None,
        output=None,
        scopes=["mt", "et", "tt", "em", "mm", "ee"],
        subproducers=[
            p4_producer,
            pt_producer,
            eta_producer,
            phi_producer,
            mass_producer,
            mass_softdrop_producer,
            mass_particlenet_producer,
            pnet_qcd_producer,
            pnet_xbb_vs_qcd_producer,
            pnet_xte_vs_qcd_producer,
            pnet_xtm_vs_qcd_producer,
            pnet_xtt_vs_qcd_producer,
            nsubjetiness_2over1_producer,
            nsubjettiness_3over2_producer,
        ],
    )

    return fatjet_producer_group



#
# Jet energy calibration and resolution correction
#


# create jet energy correction producers for AK8 jets
FatJetEnergyCorrection_data, FatJetEnergyCorrection, RenameFatJetsData = jerc_producer_factory(
    input={
        "jet_pt": nanoAOD.FatJet_pt,
        "jet_eta": nanoAOD.FatJet_eta,
        "jet_phi": nanoAOD.FatJet_phi,
        "jet_mass": nanoAOD.FatJet_mass,
        "jet_area": nanoAOD.FatJet_area,
        "jet_raw_factor": nanoAOD.FatJet_rawFactor,
        "jet_id": nanoAOD.FatJet_ID,
        "gen_jet_pt": nanoAOD.GenJetAK8_pt,
        "gen_jet_eta": nanoAOD.GenJetAK8_eta,
        "gen_jet_phi": nanoAOD.GenJetAK8_phi,
        "rho": nanoAOD.rho_v12,
    },
    output={
        "jet_pt_corrected": q.FatJet_pt_corrected,
        "jet_mass_corrected": q.FatJet_mass_corrected,
    },
    scopes=GLOBAL_SCOPES,
    producer_prefix="FatJet",
    config_parameter_prefix="fatjet",
)


#
# Base fatjet selection
#


# create producer for transverse momentum cut
FatJetPtCut = Producer(
    name="FatJetPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_fatjet_pt})",
    input=[q.FatJet_pt_corrected],
    output=[],
    scopes=["global"],
)

# create producer for eta cut
FatJetEtaCut = Producer(
    name="FatJetEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_fatjet_eta})",
    input=[nanoAOD.FatJet_eta],
    output=[],
    scopes=["global"],
)

# create producer for cut on passed woking point of the jet identification
FatJetIDCut = Producer(
    name="FatJetIDCut",
    call="physicsobject::jet::CutID({df}, {output}, {input}, {fatjet_id})",
    input=[nanoAOD.FatJet_ID],
    output=[q.fatjet_id_mask],
    scopes=["global"],
)

# producer for mask of selected fatjets
GoodFatJets = ProducerGroup(
    name="GoodFatJets",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.good_fatjets_mask],
    scopes=["global"],
    subproducers=[FatJetPtCut, FatJetEtaCut, FatJetIDCut],
)

# producer for pt-ordered index list of selected fatjets without overlap vetoes
FatJetCollection = ProducerGroup(
    name="FatJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.fatjet_index_no_veto],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

#
# Fatjet four-vector quantities
#

FatJetLV = Producer(
    name="FatJetLV",
    call="lorentzvectors::BuildP4Collection({df}, {output}, {input})",
    input=[
        q.Fatjet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
        q.fatjet_index_no_veto,
    ],
    output=[q.fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPt = Producer(
    name="FatJetPt",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[
        q.Fatjet_pt_corrected,
        q.fatjet_index_no_veto,
    ],
    output=[q.fatjet_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetEta = Producer(
    name="FatJetPt",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[
        nanoAOD.FatJet_eta,
        q.fatjet_index_no_veto,
    ],
    output=[q.fatjet_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPhi = Producer(
    name="FatJetPhi",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[
        nanoAOD.FatJet_phi,
        q.fatjet_index_no_veto,
    ],
    output=[q.fatjet_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetMass = Producer(
    name="FatJetMass",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[
        q.FatJet_mass_corrected,
        q.fatjet_index_no_veto,
    ],
    output=[q.fatjet_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)


#
# Fatjet mass reconstruction (softdrop, particleNet regression)
#


FatJetMassSD = Producer(
    name="FatJetMassSD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_msoftdrop, q.fatjet_index_no_veto],
    output=[q.fatjet_mass_sd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetMassParticleNet = Producer(
    name="FatJetMassParticleNet",
    call="fatjet::quantities::mass_particlenet({df}, {output}, {input})",
    input=[nanoAOD.FatJet_mass_corrected, nanoAOD.FatJet_particleNet_massCorr, q.fatjet_index_no_veto],
    output=[q.fatjet_mass_pnet],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)


#
# Fatjet particleNet scores
#


FatJetPNetQCD = Producer(
    name="FatJetPNetQCD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_particleNet_QCD, q.fatjet_index_no_veto],
    output=[q.fatjet_pnet_qcd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPNetXbbVsQCD = Producer(
    name="FatJetPNetXbbVsQCD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_particleNet_XbbVsQCD, q.fatjet_index_no_veto],
    output=[q.fatjet_pnet_xbb_vs_qcd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPNetXteVsQCD = Producer(
    name="FatJetPNetXteVsQCD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_particleNet_XteVsQCD, q.fatjet_index_no_veto],
    output=[q.fatjet_pnet_xte_vs_qcd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPNetXtmVsQCD = Producer(
    name="FatJetPNetXtmVsQCD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_particleNet_XtmVsQCD, q.fatjet_index_no_veto],
    output=[q.fatjet_pnet_xtm_vs_qcd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetPNetXttVsQCD = Producer(
    name="FatJetPNetXttVsQCD",
    call="basefunctions::take<float>({df}, {output}, {input})",
    input=[nanoAOD.FatJet_particleNet_XttVsQCD, q.fatjet_index_no_veto],
    output=[q.fatjet_pnet_xtt_vs_qcd],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)


#
# Fatjet-electron matching
#


FatJetElectronMatchIndex = Producer(
    name="FatJetElectronMatchIndex",
    call="fatjet::matching::match_object({df}, {output}, {input}, {max_delta_r_fatjet_electron})",
    input=[
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.fatjet_index_no_veto,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        q.loose_electron_index,
    ],
    output=[q.fatjet_electron_match_index],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetNElectronMatches = Producer(
    name="FatJetNElectronMatches",
    call="fatjet::matching::count_matches({df}, {output}, {input})",
    input=[q.fatjet_electron_match_index],
    output=[q.fatjet_n_electron_matches],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetMatchedElectron1Quantities = fatjet_matched_object_quantities_producer_factory(
    input={
        "match_index": q.fatjet_electron_match_index,
        "other_pt": nanoAOD.Electron_pt,
        "other_eta": nanoAOD.Electron_eta,
        "other_phi": nanoAOD.Electron_phi,
        "other_mass": nanoAOD.Electron_mass,
    },
    output={
        "matched_object_pt": q.fatjet_matched_electron_pt_1,
        "matched_object_eta": q.fatjet_matched_electron_eta_1,
        "matched_object_phi": q.fatjet_matched_electron_phi_1,
        "matched_object_mass": q.fatjet_matched_electron_mass_1,
        "matched_object_charge": q.fatjet_matched_electron_charge_1,
    },
    position=0,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    producer_prefix="FatJetMatchedElectron",
)

FatJetMatchedElectron2Quantities = fatjet_matched_object_quantities_producer_factory(
    input={
        "match_index": q.fatjet_electron_match_index,
        "other_pt": nanoAOD.Electron_pt,
        "other_eta": nanoAOD.Electron_eta,
        "other_phi": nanoAOD.Electron_phi,
        "other_mass": nanoAOD.Electron_mass,
    },
    output={
        "matched_object_pt": q.fatjet_matched_electron_pt_2,
        "matched_object_eta": q.fatjet_matched_electron_eta_2,
        "matched_object_phi": q.fatjet_matched_electron_phi_2,
        "matched_object_mass": q.fatjet_matched_electron_mass_2,
        "matched_object_charge": q.fatjet_matched_electron_charge_2,
    },
    position=1,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    producer_prefix="FatJetMatchedElectron",
)


#
# Fatjet-muon matching
#


FatJetMuonMatchIndex = Producer(
    name="FatJetMuonMatchIndex",
    call="fatjet::matching::match_object({df}, {output}, {input}, {max_delta_r_fatjet_electron})",
    input=[
        q.fatjet_eta,
        q.fatjet_phi,
        q.fatjet_index_no_veto,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        q.loose_muon_index,
    ],
    output=[q.fatjet_muon_match_index],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetNMuonMatches = Producer(
    name="FatJetNMuonMatches",
    call="fatjet::matching::count_matches({df}, {output}, {input})",
    input=[q.fatjet_muon_match_index],
    output=[q.fatjet_n_muon_matches],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJetMatchedMuon1Quantities = fatjet_matched_object_quantities_producer_factory(
    input={
        "match_index": q.fatjet_muon_match_index,
        "other_pt": nanoAOD.Muon_pt,
        "other_eta": nanoAOD.Muon_eta,
        "other_phi": nanoAOD.Muon_phi,
        "other_mass": nanoAOD.Muon_mass,
    },
    output={
        "matched_object_pt": q.fatjet_matched_muon_pt_1,
        "matched_object_eta": q.fatjet_matched_muon_eta_1,
        "matched_object_phi": q.fatjet_matched_muon_phi_1,
        "matched_object_mass": q.fatjet_matched_muon_mass_1,
        "matched_object_charge": q.fatjet_matched_muon_charge_1,
    },
    position=0,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    producer_prefix="FatJetMatchedMuon",
)

FatJetMatchedMuon2Quantities = fatjet_matched_object_quantities_producer_factory(
    input={
        "match_index": q.fatjet_muon_match_index,
        "other_pt": nanoAOD.Muon_pt,
        "other_eta": nanoAOD.Muon_eta,
        "other_phi": nanoAOD.Muon_phi,
        "other_mass": nanoAOD.Muon_mass,
    },
    output={
        "matched_object_pt": q.fatjet_matched_muon_pt_2,
        "matched_object_eta": q.fatjet_matched_muon_eta_2,
        "matched_object_phi": q.fatjet_matched_muon_phi_2,
        "matched_object_mass": q.fatjet_matched_muon_mass_2,
        "matched_object_charge": q.fatjet_matched_muon_charge_2,
    },
    position=1,
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    producer_prefix="FatJetMatchedMuon",
)


####################
# Set of producers to apply a veto of fatjets overlapping with ditaupair candidates and ordering fatjets by their pt
# 1. check all fatjets vs the two lepton candidates, if they are not within deltaR = 0.5, keep them --> mask
# 2. Combine mask with good_fatjets_mask
# 3. Generate FatJetCollection, an RVec containing all indices of good FatJets in pt order
# 4. generate fatjet quantity outputs
####################

VetoOverlappingFatJets = Producer(
    name="VetoOverlappingFatJets",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, q.p4_1, q.p4_2],
    output=[q.fatjet_overlap_veto_mask],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
VetoOverlappingFatJets_boosted = Producer(
    name="VetoOverlappingFatJets_boosted",
    call="jet::VetoOverlappingJets({df}, {output}, {input}, {deltaR_fatjet_veto})",
    input=[nanoAOD.FatJet_eta, nanoAOD.FatJet_phi, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.fatjet_overlap_veto_mask_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

GoodFatJetsWithVeto = ProducerGroup(
    name="GoodJetsWithVeto",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_fatjets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingFatJets],
)
GoodFatJetsWithVeto_boosted = ProducerGroup(
    name="GoodJetsWithVeto_boosted",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.good_fatjets_mask],
    output=[],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[VetoOverlappingFatJets_boosted],
)

FatJetCollection = ProducerGroup(
    name="FatJetCollection",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.good_fatjet_collection],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodFatJetsWithVeto],
)
FatJetCollection_boosted = ProducerGroup(
    name="FatJetCollection_boosted",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected],
    output=[q.good_fatjet_collection_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
    subproducers=[GoodFatJetsWithVeto_boosted],
)
FatJetCollectionWithoutVeto = Producer(
    name="FatJetCollectionWithoutVeto",
    call="jet::OrderJetsByPt({df}, {output}, {input})",
    input=[q.FatJet_pt_corrected, q.good_fatjets_mask],
    output=[q.good_fatjet_collection_without_veto],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

##########################
# Basic FatJet Quantities
# n_fatjets, pt, eta, phi, b-tag value
##########################

LVFatJet1 = Producer(
    name="LVFatJet1",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.fatjet_p4_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
LVFatJet2 = Producer(
    name="LVFatJet2",
    call="lorentzvectors::build({df}, {input_vec}, 1, {output})",
    input=[
        q.good_fatjet_collection,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.fatjet_p4_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

NumberOfFatJets = Producer(
    name="NumberOfFatJets",
    call="quantities::jet::NumberOfJets({df}, {output}, {input})",
    input=[q.good_fatjet_collection],
    output=[q.nfatjets],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
NumberOfFatJets_boosted = Producer(
    name="NumberOfFatJets_boosted",
    call="quantities::jet::NumberOfJets({df}, {output}, {input})",
    input=[q.good_fatjet_collection_boosted],
    output=[q.nfatjets_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)

FatJet1BasicQuantities = single_fatjet_producer_factory(
    input={
        "good_fatjet_index": q.good_fatjet_collection,
        "fatjet_pt_nanoaod": q.FatJet_pt_corrected,
        "fatjet_eta_nanoaod": nanoAOD.FatJet_eta,
        "fatjet_phi_nanoaod": nanoAOD.FatJet_phi,
        "fatjet_mass_nanoaod": q.FatJet_mass_corrected,
        "fatjet_mass_softdrop_nanoaod": nanoAOD.FatJet_msoftdrop,
        "fatjet_particlenet_mass_corr_nanoaod": nanoAOD.FatJet_particleNet_massCorr,
        "fatjet_particlenet_qcd_nanoaod": nanoAOD.FatJet_particleNet_QCD,
        "fatjet_particlenet_xbb_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XbbVsQCD,
        "fatjet_particlenet_xte_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XteVsQCD,
        "fatjet_particlenet_xtm_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XtmVsQCD,
        "fatjet_particlenet_xtt_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XttVsQCD,
        "fatjet_tau_1_nanoaod": nanoAOD.FatJet_tau1,
        "fatjet_tau_2_nanoaod": nanoAOD.FatJet_tau2,
        "fatjet_tau_3_nanoaod": nanoAOD.FatJet_tau3,
    },
    output={
        "fatjet_p4": q.fatjet_p4_1,
        "fatjet_pt": q.fj_pt_1,
        "fatjet_eta": q.fj_eta_1,
        "fatjet_phi": q.fj_phi_1,
        "fatjet_mass": q.fj_mass_1,
        "fatjet_mass_softdrop": q.fj_msoftdrop_1,
        "fatjet_mass_particlenet": q.fj_mass_pnet_1,
        "fatjet_particlenet_qcd": q.fj_pnet_qcd_1,
        "fatjet_particlenet_xbb_vs_qcd": q.fj_pnet_xbb_vs_qcd_1,
        "fatjet_particlenet_xte_vs_qcd": q.fj_pnet_xte_vs_qcd_1,
        "fatjet_particlenet_xtm_vs_qcd": q.fj_pnet_xtm_vs_qcd_1,
        "fatjet_particlenet_xtt_vs_qcd": q.fj_pnet_xtt_vs_qcd_1,
        "fatjet_nsubjettiness_2over1": q.fj_nsubjettiness_2over1_1,
        "fatjet_nsubjettiness_3over2": q.fj_nsubjettiness_3over2_1,
    },
    fatjet_position=0,
)

FatJet2BasicQuantities = single_fatjet_producer_factory(
    input={
        "good_fatjet_index": q.good_fatjet_collection,
        "fatjet_pt_nanoaod": q.FatJet_pt_corrected,
        "fatjet_eta_nanoaod": nanoAOD.FatJet_eta,
        "fatjet_phi_nanoaod": nanoAOD.FatJet_phi,
        "fatjet_mass_nanoaod": q.FatJet_mass_corrected,
        "fatjet_mass_softdrop_nanoaod": nanoAOD.FatJet_msoftdrop,
        "fatjet_particlenet_mass_corr_nanoaod": nanoAOD.FatJet_particleNet_massCorr,
        "fatjet_particlenet_qcd_nanoaod": nanoAOD.FatJet_particleNet_QCD,
        "fatjet_particlenet_xbb_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XbbVsQCD,
        "fatjet_particlenet_xte_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XteVsQCD,
        "fatjet_particlenet_xtm_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XtmVsQCD,
        "fatjet_particlenet_xtt_vs_qcd_nanoaod": nanoAOD.FatJet_particleNet_XttVsQCD,
        "fatjet_tau_1_nanoaod": nanoAOD.FatJet_tau1,
        "fatjet_tau_2_nanoaod": nanoAOD.FatJet_tau2,
        "fatjet_tau_3_nanoaod": nanoAOD.FatJet_tau3,
    },
    output={
        "fatjet_p4": q.fatjet_p4_2,
        "fatjet_pt": q.fj_pt_2,
        "fatjet_eta": q.fj_eta_2,
        "fatjet_phi": q.fj_phi_2,
        "fatjet_mass": q.fj_mass_2,
        "fatjet_mass_softdrop": q.fj_msoftdrop_2,
        "fatjet_mass_particlenet": q.fj_mass_pnet_2,
        "fatjet_particlenet_qcd": q.fj_pnet_qcd_2,
        "fatjet_particlenet_xbb_vs_qcd": q.fj_pnet_xbb_vs_qcd_2,
        "fatjet_particlenet_xte_vs_qcd": q.fj_pnet_xte_vs_qcd_2,
        "fatjet_particlenet_xtm_vs_qcd": q.fj_pnet_xtm_vs_qcd_2,
        "fatjet_particlenet_xtt_vs_qcd": q.fj_pnet_xtt_vs_qcd_2,
        "fatjet_nsubjettiness_2over1": q.fj_nsubjettiness_2over1_2,
        "fatjet_nsubjettiness_3over2": q.fj_nsubjettiness_3over2_2,
    },
    fatjet_position=1,
)

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
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.bpair_fatjet,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.matched_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_pt = Producer(
    name="fj_matched_pt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_eta = Producer(
    name="fj_matched_eta",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_phi = Producer(
    name="fj_matched_phi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_mass = Producer(
    name="fj_matched_mass",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.matched_fatjet_p4],
    output=[q.fj_matched_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_msoftdrop = Producer(
    name="fj_matched_msoftdrop",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.bpair_fatjet],
    output=[q.fj_matched_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_matched_particleNet_XbbvsQCD = Producer(
    name="fj_matched_particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_PNet_Xbb_v12, nanoAOD.FatJet_PNet_QCD_v12, q.bpair_fatjet],
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
        nanoAOD.FatJet_PNet_Xbb_v12, 
        nanoAOD.FatJet_PNet_QCD_v12,
    ],
    output=[q.Xbb_fatjet],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVXbbFatJet = Producer(
    name="LVXbbFatJet",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.Xbb_fatjet,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.Xbb_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_pt = Producer(
    name="fj_Xbb_pt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_eta = Producer(
    name="fj_Xbb_eta",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_eta],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_phi = Producer(
    name="fj_Xbb_phi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_phi],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_mass = Producer(
    name="fj_Xbb_mass",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4],
    output=[q.fj_Xbb_mass],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_msoftdrop = Producer(
    name="fj_Xbb_msoftdrop",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.Xbb_fatjet],
    output=[q.fj_Xbb_msoftdrop],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_particleNet_XbbvsQCD = Producer(
    name="fj_Xbb_particleNet_XbbvsQCD",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_PNet_Xbb_v12, nanoAOD.FatJet_PNet_QCD_v12, q.Xbb_fatjet],
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
    call="quantities::fatjet::hadflavor({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_hadronFlavor, q.Xbb_fatjet],
    output=[q.fj_Xbb_hadflavor],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nBhad = Producer(
    name="fj_Xbb_nBhad",
    call="quantities::fatjet::nHadrons({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nBHadrons, q.Xbb_fatjet],
    output=[q.fj_Xbb_nBhad],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nChad = Producer(
    name="fj_Xbb_nChad",
    call="quantities::fatjet::nHadrons({df}, {output}, {input}, 0)",
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
        nanoAOD.FatJet_PNet_Xbb_v12, 
        nanoAOD.FatJet_PNet_QCD_v12,
    ],
    output=[q.Xbb_fatjet_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
LVXbbFatJet_boosted = Producer(
    name="LVXbbFatJet_boosted",
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.Xbb_fatjet_boosted,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.Xbb_fatjet_p4_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_pt_boosted = Producer(
    name="fj_Xbb_pt_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_pt_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_eta_boosted = Producer(
    name="fj_Xbb_eta_boosted",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_eta_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_phi_boosted = Producer(
    name="fj_Xbb_phi_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_phi_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_mass_boosted = Producer(
    name="fj_Xbb_mass_boosted",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.Xbb_fatjet_p4_boosted],
    output=[q.fj_Xbb_mass_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_msoftdrop_boosted = Producer(
    name="fj_Xbb_msoftdrop_boosted",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_msoftdrop, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_msoftdrop_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_particleNet_XbbvsQCD_boosted = Producer(
    name="fj_Xbb_particleNet_XbbvsQCD_boosted",
    call="quantities::fatjet::particleNet_XbbvsQCD({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_PNet_Xbb_v12, nanoAOD.FatJet_PNet_QCD_v12, q.Xbb_fatjet_boosted],
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
    call="quantities::fatjet::hadflavor({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_hadronFlavor, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_hadflavor_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nBhad_boosted = Producer(
    name="fj_Xbb_nBhad_boosted",
    call="quantities::fatjet::nHadrons({df}, {output}, {input}, 0)",
    input=[nanoAOD.FatJet_nBHadrons, q.Xbb_fatjet_boosted],
    output=[q.fj_Xbb_nBhad_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_Xbb_nChad_boosted = Producer(
    name="fj_Xbb_nChad_boosted",
    call="quantities::fatjet::nHadrons({df}, {output}, {input}, 0)",
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
    call="lorentzvectors::build({df}, {input_vec}, 0, {output})",
    input=[
        q.good_fatjet_collection_without_veto,
        q.FatJet_pt_corrected,
        nanoAOD.FatJet_eta,
        nanoAOD.FatJet_phi,
        q.FatJet_mass_corrected,
    ],
    output=[q.leading_fatjet_p4],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_leading_pt = Producer(
    name="fj_leading_pt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.leading_fatjet_p4],
    output=[q.fj_leading_pt],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
fj_leading_msoftdrop = Producer(
    name="fj_leading_msoftdrop",
    call="quantities::fatjet::msoftdrop({df}, {output}, {input}, 0)",
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