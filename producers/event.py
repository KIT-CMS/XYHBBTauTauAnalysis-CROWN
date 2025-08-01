from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import BaseFilter, Producer, ProducerGroup, VectorProducer
from .electrons import DiElectronVeto
from .muons import DiMuonVeto

####################
# Set of general producers for event quantities
####################

RunLumiEventFilter = VectorProducer(
    name="RunLumiEventFilter",
    call='event::filter::Quantity<{RunLumiEventFilter_Quantity_Types}>({df}, "RunLumiEventFilter", "{RunLumiEventFilter_Quantities}", {vec_open}{RunLumiEventFilter_Selections}{vec_close})',
    input=[],
    output=None,
    scopes=["global"],
    vec_configs=[
        "RunLumiEventFilter_Quantities",
        "RunLumiEventFilter_Quantity_Types",
        "RunLumiEventFilter_Selections",
    ],
)

JSONFilter = BaseFilter(
    name="JSONFilter",
    call='event::filter::GoldenJSON({df}, correctionManager, "GoldenJSONFilter", {input}, "{golden_json_file}")',
    input=[nanoAOD.run, nanoAOD.luminosityBlock],
    scopes=["global"],
)

PrefireWeight = Producer(
    name="PrefireWeight",
    call="event::quantity::Rename<Float_t>({df}, {output}, {input})",
    input=[nanoAOD.prefireWeight],
    output=[q.prefireweight],
    scopes=["global"],
)

is_data = Producer(
    name="isData",
    input=[],
    call="event::quantity::Define({df}, {output}, {is_data})",
    output=[q.is_data],
    scopes=["global"],
)

is_embedding = Producer(
    name="is_embedding",
    call="event::quantity::Define({df}, {output}, {is_embedding})",
    input=[],
    output=[q.is_embedding],
    scopes=["global"],
)
is_ttbar = Producer(
    name="is_ttbar",
    call="event::quantity::Define({df}, {output}, {is_ttbar})",
    input=[],
    output=[q.is_ttbar],
    scopes=["global"],
)
is_dyjets = Producer(
    name="is_dyjets",
    call="event::quantity::Define({df}, {output}, {is_dyjets})",
    input=[],
    output=[q.is_dyjets],
    scopes=["global"],
)
is_wjets = Producer(
    name="is_wjets",
    call="event::quantity::Define({df}, {output}, {is_wjets})",
    input=[],
    output=[q.is_wjets],
    scopes=["global"],
)
is_ggh_htautau = Producer(
    name="is_ggh_htautau",
    call="event::quantity::Define({df}, {output}, {is_ggh_htautau})",
    input=[],
    output=[q.is_ggh_htautau],
    scopes=["global"],
)
is_vbf_htautau = Producer(
    name="is_vbf_htautau",
    call="event::quantity::Define({df}, {output}, {is_vbf_htautau})",
    input=[],
    output=[q.is_vbf_htautau],
    scopes=["global"],
)
is_diboson = Producer(
    name="is_diboson",
    call="event::quantity::Define({df}, {output}, {is_diboson})",
    input=[],
    output=[q.is_diboson],
    scopes=["global"],
)
is_ggh_hbb = Producer(
    name="is_ggh_hbb",
    call="event::quantity::Define({df}, {output}, {is_ggh_hbb})",
    input=[],
    output=[q.is_ggh_hbb],
    scopes=["global"],
)
is_vbf_hbb = Producer(
    name="is_vbf_hbb",
    call="event::quantity::Define({df}, {output}, {is_vbf_hbb})",
    input=[],
    output=[q.is_vbf_hbb],
    scopes=["global"],
)
is_rem_hbb = Producer(
    name="is_rem_hbb",
    call="event::quantity::Define({df}, {output}, {is_rem_hbb})",
    input=[],
    output=[q.is_rem_hbb],
    scopes=["global"],
)
is_embedding_mc = Producer(
    name="is_embedding_mc",
    call="event::quantity::Define({df}, {output}, {is_embedding_mc})",
    input=[],
    output=[q.is_embedding_mc],
    scopes=["global"],
)
is_singletop = Producer(
    name="is_singletop",
    call="event::quantity::Define({df}, {output}, {is_singletop})",
    input=[],
    output=[q.is_singletop],
    scopes=["global"],
)
is_rem_htautau = Producer(
    name="is_singletop",
    call="event::quantity::Define({df}, {output}, {is_rem_htautau})",
    input=[],
    output=[q.is_rem_htautau],
    scopes=["global"],
)
is_electroweak_boson = Producer(
    name="is_singletop",
    call="event::quantity::Define({df}, {output}, {is_electroweak_boson})",
    input=[],
    output=[q.is_electroweak_boson],
    scopes=["global"],
)

SampleFlags = ProducerGroup(
    name="SampleFlags",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[
        is_data,
        is_embedding,
        is_ttbar,
        is_dyjets,
        is_wjets,
        is_ggh_htautau,
        is_vbf_htautau,
        is_diboson,
        is_ggh_hbb,
        is_vbf_hbb,
        is_rem_hbb,
        is_embedding_mc,
        is_singletop,
        is_rem_htautau,
        is_electroweak_boson,
    ],
)

MetFilter = VectorProducer(
    name="MetFilter",
    call='event::filter::Flag({df}, "{met_filters}", "{met_filters}")',
    input=[],
    output=None,
    scopes=["global"],
    vec_configs=["met_filters"],
)

Lumi = Producer(
    name="Lumi",
    call="event::quantity::Rename<UInt_t>({df}, {output}, {input})",
    input=[nanoAOD.luminosityBlock],
    output=[q.lumi],
    scopes=["global"],
)

npartons = Producer(
    name="npartons",
    call="event::quantity::Rename<UChar_t>({df}, {output}, {input})",
    input=[nanoAOD.LHE_Njets],
    output=[q.npartons],
    scopes=["global"],
)

PUweights = Producer(
    name="PUweights",
    call="""event::reweighting::Pileup(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{PU_reweighting_file}", 
        "{PU_reweighting_era}", 
        "{PU_reweighting_variation}")
        """,
    input=[nanoAOD.Pileup_nTrueInt],
    output=[q.puweight],
    scopes=["global"],
)

ZPtMassReweighting = Producer(
    name="ZPtMassReweighting",
    call='event::reweighting::ZPtMass({df}, {output}, {input}, "{zptmass_file}", "{zptmass_functor}", "{zptmass_arguments}")',
    input=[
        q.recoil_genboson_p4_vec,
    ],
    output=[q.ZPtMassReweightWeight],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)

TopPtReweighting = Producer(
    name="TopPtReweighting",
    call="event::reweighting::TopPt({df}, {output}, {input})",
    input=[
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_statusFlags,
        nanoAOD.GenParticle_pt,
    ],
    output=[q.topPtReweightWeight],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)

DiLeptonVeto = ProducerGroup(
    name="DiLeptonVeto",
    call='event::CombineFlags({df}, {output}, {input}, "any_of")',
    input=[],
    output=[q.dilepton_veto],
    scopes=["global"],
    subproducers=[DiElectronVeto, DiMuonVeto],
)

JetVetoMapVeto = Producer(
    name="JetVetoMapVeto",
    call="""
    xyh::vetoes::jet_vetomap(
        {df},
        correctionManager,
        {output},
        {input},
        "{jet_veto_map_file}",
        "{jet_veto_map_name}",
        "{jet_veto_map_type}",
        {jet_veto_min_pt},
        {jet_veto_id_wp},
        {jet_veto_max_em_frac},
        {jet_veto_min_delta_r_jet_muon}
    )
    """,
    input=[
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_ID_corrected,
        nanoAOD.Jet_chEmEF,
        nanoAOD.Jet_neEmEF,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_isPFcand,
    ],
    output=[q.jet_vetomap_veto],
    scopes=["global"],
)

GGH_NNLO_Reweighting = Producer(
    name="GGH_NNLO_Reweighting",
    call='htxs::ggHNNLOWeights({df}, {output}, "{ggHNNLOweightsRootfile}", "{ggH_generator}", {input})',
    input=[nanoAOD.HTXS_Higgs_pt, nanoAOD.HTXS_njets30],
    output=[q.ggh_NNLO_weight],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)

GGH_WG1_Uncertainties = Producer(
    name="GGH_WG1_Uncertainties",
    call="htxs::ggH_WG1_uncertainties({df}, {output_vec}, {input})",
    input=[
        nanoAOD.HTXS_stage_1_pTjet30,
        nanoAOD.HTXS_Higgs_pt,
        nanoAOD.HTXS_njets30,
    ],  # using non-updated stage1 flag required by the used macro
    output=[
        q.THU_ggH_Mu,
        q.THU_ggH_Res,
        q.THU_ggH_Mig01,
        q.THU_ggH_Mig12,
        q.THU_ggH_VBF2j,
        q.THU_ggH_VBF3j,
        q.THU_ggH_PT60,
        q.THU_ggH_PT120,
        q.THU_ggH_qmtop,
    ],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)

QQH_WG1_Uncertainties = Producer(
    name="QQH_WG1_Uncertainties",
    call="htxs::qqH_WG1_uncertainties({df}, {output_vec}, {input})",
    input=[
        nanoAOD.HTXS_stage1_1_fine_cat_pTjet30GeV
    ],  # using fine stage1.1 flag required by the used macro
    output=[
        q.THU_qqH_TOT,
        q.THU_qqH_PTH200,
        q.THU_qqH_Mjj60,
        q.THU_qqH_Mjj120,
        q.THU_qqH_Mjj350,
        q.THU_qqH_Mjj700,
        q.THU_qqH_Mjj1000,
        q.THU_qqH_Mjj1500,
        q.THU_qqH_25,
        q.THU_qqH_JET01,
    ],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)
LHE_Scale_weight = Producer(
    name="LHE_Scale_weight",
    call="event::reweighting::LHEscale({df}, {output}, {input}, {muR}, {muF})",
    input=[nanoAOD.LHEScaleWeight],
    output=[q.lhe_scale_weight],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)
NMSSM_LHE_Scale_weight = Producer(
    name="NMSSM_LHE_Scale_weight",
    call="reweighting::nmssm_lhe_scale_weights({df}, {output}, {input}, {muR}, {muF})",
    input=[nanoAOD.LHEScaleWeight],
    output=[q.lhe_scale_weight],
    scopes=["global", "em", "et", "mt", "tt", "mm", "ee"],
)
