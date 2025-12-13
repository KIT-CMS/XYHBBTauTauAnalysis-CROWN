from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, ExtendedVectorProducer

# resolved tautau analysis
Transform_njets = Producer(
    name="Transform_njets",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "i")',
    input=[
        q.n_jets,
    ],
    output=[q.transformed_njets],
    scopes=["mt"],
)
Transform_nbtag = Producer(
    name="Transform_nbtag",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "i")',
    input=[
        q.n_bjets,
    ],
    output=[q.transformed_nbtag],
    scopes=["mt"],
)
Transform_nfatjets = Producer(
    name="Transform_nfatjets",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "i")',
    input=[
        q.nfatjets,
    ],
    output=[q.transformed_nfatjets],
    scopes=["mt"],
)
Transform_pt_1 = Producer(
    name="Transform_pt_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.pt_1,
    ],
    output=[q.transformed_pt_1],
    scopes=["mt"],
)
Transform_pt_2 = Producer(
    name="Transform_pt_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.pt_2,
    ],
    output=[q.transformed_pt_2],
    scopes=["mt"],
)
Transform_eta_1 = Producer(
    name="Transform_eta_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.eta_1,
    ],
    output=[q.transformed_eta_1],
    scopes=["mt"],
)
Transform_eta_2 = Producer(
    name="Transform_eta_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.eta_2,
    ],
    output=[q.transformed_eta_2],
    scopes=["mt"],
)
Transform_deltaR_ditaupair = Producer(
    name="Transform_deltaR_ditaupair",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.deltaR_ditaupair,
    ],
    output=[q.transformed_deltaR_ditaupair],
    scopes=["mt"],
)
Transform_m_vis = Producer(
    name="Transform_m_vis",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.m_vis,
    ],
    output=[q.transformed_m_vis],
    scopes=["mt"],
)
Transform_m_fastmtt = Producer(
    name="Transform_m_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.m_fastmtt,
    ],
    output=[q.transformed_m_fastmtt],
    scopes=["mt"],
)
Transform_pt_fastmtt = Producer(
    name="Transform_pt_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.pt_fastmtt,
    ],
    output=[q.transformed_pt_fastmtt],
    scopes=["mt"],
)
Transform_eta_fastmtt = Producer(
    name="Transform_eta_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.eta_fastmtt,
    ],
    output=[q.transformed_eta_fastmtt],
    scopes=["mt"],
)
Transform_bpair_pt_1 = Producer(
    name="Transform_bpair_pt_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_pt_1,
    ],
    output=[q.transformed_bpair_pt_1],
    scopes=["mt"],
)
Transform_bpair_eta_1 = Producer(
    name="Transform_bpair_eta_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_eta_1,
    ],
    output=[q.transformed_bpair_eta_1],
    scopes=["mt"],
)
Transform_bpair_btag_value_1 = Producer(
    name="Transform_bpair_btag_value_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_btag_value_1,
    ],
    output=[q.transformed_bpair_btag_value_1],
    scopes=["mt"],
)
Transform_bpair_pt_2 = Producer(
    name="Transform_bpair_pt_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_pt_2,
    ],
    output=[q.transformed_bpair_pt_2],
    scopes=["mt"],
)
Transform_bpair_eta_2 = Producer(
    name="Transform_bpair_eta_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_eta_2,
    ],
    output=[q.transformed_bpair_eta_2],
    scopes=["mt"],
)
Transform_bpair_btag_value_2 = Producer(
    name="Transform_bpair_btag_value_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_btag_value_2,
    ],
    output=[q.transformed_bpair_btag_value_2],
    scopes=["mt"],
)
Transform_bpair_m_inv = Producer(
    name="Transform_bpair_m_inv",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_m_inv,
    ],
    output=[q.transformed_bpair_m_inv],
    scopes=["mt"],
)
Transform_bpair_deltaR = Producer(
    name="Transform_bpair_deltaR",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_deltaR,
    ],
    output=[q.transformed_bpair_deltaR],
    scopes=["mt"],
)
Transform_bpair_pt_dijet = Producer(
    name="Transform_bpair_pt_dijet",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.bpair_pt_dijet,
    ],
    output=[q.transformed_bpair_pt_dijet],
    scopes=["mt"],
)
Transform_fj_Xbb_pt = Producer(
    name="Transform_fj_Xbb_pt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.fj_Xbb_pt,
    ],
    output=[q.transformed_fj_Xbb_pt],
    scopes=["mt"],
)
Transform_fj_Xbb_eta = Producer(
    name="Transform_fj_Xbb_eta",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.fj_Xbb_eta,
    ],
    output=[q.transformed_fj_Xbb_eta],
    scopes=["mt"],
)
Transform_fj_Xbb_msoftdrop = Producer(
    name="Transform_fj_Xbb_msoftdrop",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.fj_Xbb_msoftdrop,
    ],
    output=[q.transformed_fj_Xbb_msoftdrop],
    scopes=["mt"],
)
Transform_fj_Xbb_nsubjettiness_2over1 = Producer(
    name="Transform_fj_Xbb_nsubjettiness_2over1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.fj_Xbb_nsubjettiness_2over1,
    ],
    output=[q.transformed_fj_Xbb_nsubjettiness_2over1],
    scopes=["mt"],
)
Transform_fj_Xbb_nsubjettiness_3over2 = Producer(
    name="Transform_fj_Xbb_nsubjettiness_3over2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.fj_Xbb_nsubjettiness_3over2,
    ],
    output=[q.transformed_fj_Xbb_nsubjettiness_3over2],
    scopes=["mt"],
)
Transform_met = Producer(
    name="Transform_met",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.met,
    ],
    output=[q.transformed_met],
    scopes=["mt"],
)
Transform_mass_tautaubb = Producer(
    name="Transform_mass_tautaubb",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.mass_tautaubb,
    ],
    output=[q.transformed_mass_tautaubb],
    scopes=["mt"],
)
Transform_pt_tautaubb = Producer(
    name="Transform_pt_tautaubb",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.pt_tautaubb,
    ],
    output=[q.transformed_pt_tautaubb],
    scopes=["mt"],
)
Transform_kinfit_mX = Producer(
    name="Transform_kinfit_mX",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.kinfit_mX,
    ],
    output=[q.transformed_kinfit_mX],
    scopes=["mt"],
)
Transform_kinfit_mY = Producer(
    name="Transform_kinfit_mY",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.kinfit_mY,
    ],
    output=[q.transformed_kinfit_mY],
    scopes=["mt"],
)
Transform_kinfit_chi2 = Producer(
    name="Transform_kinfit_chi2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.kinfit_chi2,
    ],
    output=[q.transformed_kinfit_chi2],
    scopes=["mt"],
)
Transform_mt_1 = Producer(
    name="Transform_mt_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file}", "f")',
    input=[
        q.mt_1,
    ],
    output=[q.transformed_mt_1],
    scopes=["mt"],
)
DefineMassXColumns = ExtendedVectorProducer(
    name="DefineMassXColumns",
    call='ml::DefineMassColumns({df}, {output}, "{masses_transformation_file}", "{massX_value}", "X")',
    input=[],
    output="massX_output",
    scope=["mt"],
    vec_config="massX_definitions",
)
DefineMassYColumns = ExtendedVectorProducer(
    name="DefineMassYColumns",
    call='ml::DefineMassColumns({df}, {output}, "{masses_transformation_file}", "{massY_value}", "Y")',
    input=[],
    output="massY_output",
    scope=["mt"],
    vec_config="massY_definitions",
)

MTTransformVars = ProducerGroup(
    name="MTTransformVars",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        Transform_njets,
        Transform_nbtag,
        Transform_nfatjets,
        Transform_pt_1,
        Transform_pt_2,
        Transform_eta_1,
        Transform_eta_2,
        Transform_deltaR_ditaupair,
        Transform_m_vis,
        Transform_m_fastmtt,
        Transform_pt_fastmtt,
        Transform_eta_fastmtt,
        Transform_bpair_pt_1,
        Transform_bpair_eta_1,
        Transform_bpair_btag_value_1,
        Transform_bpair_pt_2,
        Transform_bpair_eta_2,
        Transform_bpair_btag_value_2,
        Transform_bpair_m_inv,
        Transform_bpair_deltaR,
        Transform_bpair_pt_dijet,
        Transform_fj_Xbb_pt,
        Transform_fj_Xbb_eta,
        Transform_fj_Xbb_msoftdrop,
        Transform_fj_Xbb_nsubjettiness_2over1,
        # Transform_fj_Xbb_nsubjettiness_3over2,
        Transform_met,
        Transform_mass_tautaubb,
        Transform_pt_tautaubb,
        Transform_kinfit_mX,
        Transform_kinfit_mY,
        Transform_kinfit_chi2,
        Transform_mt_1,
    ],
)

Evaluate_PNN = ExtendedVectorProducer(
    name="Evaluate_PNN",
    call='ml::sofie::NMSSMEvaluate_ONNX({df}, {input_vec}, {output}, "{model_file}", "{massX_parameter}", "{massY_parameter}")',
    input=[
        q.transformed_njets,
        q.transformed_nbtag,
        q.transformed_nfatjets,
        q.transformed_pt_1,
        q.transformed_pt_2,
        q.transformed_eta_1,
        q.transformed_eta_2,
        q.transformed_deltaR_ditaupair,
        q.transformed_m_vis,
        q.transformed_m_fastmtt,
        q.transformed_pt_fastmtt,
        q.transformed_eta_fastmtt,
        q.transformed_bpair_pt_1,
        q.transformed_bpair_eta_1,
        q.transformed_bpair_btag_value_1,
        q.transformed_bpair_pt_2,
        q.transformed_bpair_eta_2,
        q.transformed_bpair_btag_value_2,
        q.transformed_bpair_m_inv,
        q.transformed_bpair_deltaR,
        q.transformed_bpair_pt_dijet,
        q.transformed_fj_Xbb_pt,
        q.transformed_fj_Xbb_eta,
        q.transformed_fj_Xbb_msoftdrop,
        q.transformed_fj_Xbb_nsubjettiness_2over1,
        # q.transformed_fj_Xbb_nsubjettiness_3over2,
        q.transformed_met,
        q.transformed_mass_tautaubb,
        q.transformed_pt_tautaubb,
        q.transformed_kinfit_mX,
        q.transformed_kinfit_mY,
        q.transformed_kinfit_chi2,
        q.transformed_mt_1,
        # q.massX,
        # q.massY,
    ],
    output=["pnn_output_vector", "predicted_class", "predicted_max_value"],
    scope=["mt"],
    vec_config="pnn_mass_parameters",
)

Evaluate_PNN_ORT = ExtendedVectorProducer(
    name="Evaluate_PNN_ORT",
    call='ml::PNNEvaluate_ORT<34>({df}, onnxSessionManager, {output}, "{model_file}", "{massX_parameter}", "{massY_parameter}", {input_vec})',
    input=[
        q.transformed_njets,
        q.transformed_nbtag,
        q.transformed_nfatjets,
        q.transformed_pt_1,
        q.transformed_pt_2,
        q.transformed_eta_1,
        q.transformed_eta_2,
        q.transformed_deltaR_ditaupair,
        q.transformed_m_vis,
        q.transformed_m_fastmtt,
        q.transformed_pt_fastmtt,
        q.transformed_eta_fastmtt,
        q.transformed_bpair_pt_1,
        q.transformed_bpair_eta_1,
        q.transformed_bpair_btag_value_1,
        q.transformed_bpair_pt_2,
        q.transformed_bpair_eta_2,
        q.transformed_bpair_btag_value_2,
        q.transformed_bpair_m_inv,
        q.transformed_bpair_deltaR,
        q.transformed_bpair_pt_dijet,
        q.transformed_fj_Xbb_pt,
        q.transformed_fj_Xbb_eta,
        q.transformed_fj_Xbb_msoftdrop,
        q.transformed_fj_Xbb_nsubjettiness_2over1,
        # q.transformed_fj_Xbb_nsubjettiness_3over2,
        q.transformed_met,
        q.transformed_mass_tautaubb,
        q.transformed_pt_tautaubb,
        q.transformed_kinfit_mX,
        q.transformed_kinfit_mY,
        q.transformed_kinfit_chi2,
        q.transformed_mt_1,
        # q.massX,
        # q.massY,
    ],
    output=["pnn_output_vector", "predicted_class", "predicted_max_value"],
    scope=["mt"],
    vec_config="pnn_mass_parameters",
)

# boosted tautau analysis
Transform_njets_boosted = Producer(
    name="Transform_njets_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "i")',
    input=[
        q.n_jets_boosted,
    ],
    output=[q.transformed_njets_boosted],
    scopes=["mt"],
)
Transform_nbtag_boosted = Producer(
    name="Transform_nbtag_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "i")',
    input=[
        q.n_bjets_boosted,
    ],
    output=[q.transformed_nbtag_boosted],
    scopes=["mt"],
)
Transform_nfatjets_boosted = Producer(
    name="Transform_nfatjets_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "i")',
    input=[
        q.nfatjets_boosted,
    ],
    output=[q.transformed_nfatjets_boosted],
    scopes=["mt"],
)
Transform_boosted_pt_1 = Producer(
    name="Transform_boosted_pt_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_pt_1,
    ],
    output=[q.transformed_boosted_pt_1],
    scopes=["mt"],
)
Transform_boosted_pt_2 = Producer(
    name="Transform_boosted_pt_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_pt_2,
    ],
    output=[q.transformed_boosted_pt_2],
    scopes=["mt"],
)
Transform_boosted_eta_1 = Producer(
    name="Transform_boosted_eta_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_eta_1,
    ],
    output=[q.transformed_boosted_eta_1],
    scopes=["mt"],
)
Transform_boosted_eta_2 = Producer(
    name="Transform_boosted_eta_2",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_eta_2,
    ],
    output=[q.transformed_boosted_eta_2],
    scopes=["mt"],
)
Transform_boosted_deltaR_ditaupair = Producer(
    name="Transform_boosted_deltaR_ditaupair",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_deltaR_ditaupair,
    ],
    output=[q.transformed_boosted_deltaR_ditaupair],
    scopes=["mt"],
)
Transform_boosted_m_vis = Producer(
    name="Transform_boosted_m_vis",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_m_vis,
    ],
    output=[q.transformed_boosted_m_vis],
    scopes=["mt"],
)
Transform_boosted_m_fastmtt = Producer(
    name="Transform_boosted_m_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_m_fastmtt,
    ],
    output=[q.transformed_boosted_m_fastmtt],
    scopes=["mt"],
)
Transform_boosted_pt_fastmtt = Producer(
    name="Transform_boosted_pt_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_pt_fastmtt,
    ],
    output=[q.transformed_boosted_pt_fastmtt],
    scopes=["mt"],
)
Transform_boosted_eta_fastmtt = Producer(
    name="Transform_boosted_eta_fastmtt",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_eta_fastmtt,
    ],
    output=[q.transformed_boosted_eta_fastmtt],
    scopes=["mt"],
)
Transform_bpair_pt_1_boosted = Producer(
    name="Transform_bpair_pt_1_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_pt_1_boosted,
    ],
    output=[q.transformed_bpair_pt_1_boosted],
    scopes=["mt"],
)
Transform_bpair_eta_1_boosted = Producer(
    name="Transform_bpair_eta_1_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_eta_1_boosted,
    ],
    output=[q.transformed_bpair_eta_1_boosted],
    scopes=["mt"],
)
Transform_bpair_btag_value_1_boosted = Producer(
    name="Transform_bpair_btag_value_1_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_btag_value_1_boosted,
    ],
    output=[q.transformed_bpair_btag_value_1_boosted],
    scopes=["mt"],
)
Transform_bpair_pt_2_boosted = Producer(
    name="Transform_bpair_pt_2_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_pt_2_boosted,
    ],
    output=[q.transformed_bpair_pt_2_boosted],
    scopes=["mt"],
)
Transform_bpair_eta_2_boosted = Producer(
    name="Transform_bpair_eta_2_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_eta_2_boosted,
    ],
    output=[q.transformed_bpair_eta_2_boosted],
    scopes=["mt"],
)
Transform_bpair_btag_value_2_boosted = Producer(
    name="Transform_bpair_btag_value_2_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_btag_value_2_boosted,
    ],
    output=[q.transformed_bpair_btag_value_2_boosted],
    scopes=["mt"],
)
Transform_bpair_m_inv_boosted = Producer(
    name="Transform_bpair_m_inv_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_m_inv_boosted,
    ],
    output=[q.transformed_bpair_m_inv_boosted],
    scopes=["mt"],
)
Transform_bpair_deltaR_boosted = Producer(
    name="Transform_bpair_deltaR_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_deltaR_boosted,
    ],
    output=[q.transformed_bpair_deltaR_boosted],
    scopes=["mt"],
)
Transform_bpair_pt_dijet_boosted = Producer(
    name="Transform_bpair_pt_dijet_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.bpair_pt_dijet_boosted,
    ],
    output=[q.transformed_bpair_pt_dijet_boosted],
    scopes=["mt"],
)
Transform_fj_Xbb_pt_boosted = Producer(
    name="Transform_fj_Xbb_pt_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.fj_Xbb_pt_boosted,
    ],
    output=[q.transformed_fj_Xbb_pt_boosted],
    scopes=["mt"],
)
Transform_fj_Xbb_eta_boosted = Producer(
    name="Transform_fj_Xbb_eta_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.fj_Xbb_eta_boosted,
    ],
    output=[q.transformed_fj_Xbb_eta_boosted],
    scopes=["mt"],
)
Transform_fj_Xbb_msoftdrop_boosted = Producer(
    name="Transform_fj_Xbb_msoftdrop_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.fj_Xbb_msoftdrop_boosted,
    ],
    output=[q.transformed_fj_Xbb_msoftdrop_boosted],
    scopes=["mt"],
)
Transform_fj_Xbb_nsubjettiness_2over1_boosted = Producer(
    name="Transform_fj_Xbb_nsubjettiness_2over1_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.fj_Xbb_nsubjettiness_2over1_boosted,
    ],
    output=[q.transformed_fj_Xbb_nsubjettiness_2over1_boosted],
    scopes=["mt"],
)
Transform_fj_Xbb_nsubjettiness_3over2_boosted = Producer(
    name="Transform_fj_Xbb_nsubjettiness_3over2_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.fj_Xbb_nsubjettiness_3over2_boosted,
    ],
    output=[q.transformed_fj_Xbb_nsubjettiness_3over2_boosted],
    scopes=["mt"],
)
Transform_met_boosted = Producer(
    name="Transform_met_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.met_boosted,
    ],
    output=[q.transformed_met_boosted],
    scopes=["mt"],
)
Transform_boosted_mass_tautaubb = Producer(
    name="Transform_boosted_mass_tautaubb",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_mass_tautaubb,
    ],
    output=[q.transformed_boosted_mass_tautaubb],
    scopes=["mt"],
)
Transform_boosted_pt_tautaubb = Producer(
    name="Transform_boosted_pt_tautaubb",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_pt_tautaubb,
    ],
    output=[q.transformed_boosted_pt_tautaubb],
    scopes=["mt"],
)
Transform_kinfit_mX_boosted = Producer(
    name="Transform_kinfit_mX_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.kinfit_mX_boosted,
    ],
    output=[q.transformed_kinfit_mX_boosted],
    scopes=["mt"],
)
Transform_kinfit_mY_boosted = Producer(
    name="Transform_kinfit_mY_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.kinfit_mY_boosted,
    ],
    output=[q.transformed_kinfit_mY_boosted],
    scopes=["mt"],
)
Transform_kinfit_chi2_boosted = Producer(
    name="Transform_kinfit_chi2_boosted",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.kinfit_chi2_boosted,
    ],
    output=[q.transformed_kinfit_chi2_boosted],
    scopes=["mt"],
)
Transform_boosted_mt_1 = Producer(
    name="Transform_boosted_mt_1",
    call='ml::StandardTransformer({df}, {input}, {output}, "{feature_transformation_file_boosted}", "f")',
    input=[
        q.boosted_mt_1,
    ],
    output=[q.transformed_boosted_mt_1],
    scopes=["mt"],
)

BoostedMTTransformVars = ProducerGroup(
    name="BoostedMTTransformVars",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers=[
        Transform_njets_boosted,
        Transform_nbtag_boosted,
        Transform_nfatjets_boosted,
        Transform_boosted_pt_1,
        Transform_boosted_pt_2,
        Transform_boosted_eta_1,
        Transform_boosted_eta_2,
        Transform_boosted_deltaR_ditaupair,
        Transform_boosted_m_vis,
        Transform_boosted_m_fastmtt,
        Transform_boosted_pt_fastmtt,
        Transform_boosted_eta_fastmtt,
        Transform_bpair_pt_1_boosted,
        Transform_bpair_eta_1_boosted,
        Transform_bpair_btag_value_1_boosted,
        Transform_bpair_pt_2_boosted,
        Transform_bpair_eta_2_boosted,
        Transform_bpair_btag_value_2_boosted,
        Transform_bpair_m_inv_boosted,
        Transform_bpair_deltaR_boosted,
        Transform_bpair_pt_dijet_boosted,
        Transform_fj_Xbb_pt_boosted,
        Transform_fj_Xbb_eta_boosted,
        Transform_fj_Xbb_msoftdrop_boosted,
        Transform_fj_Xbb_nsubjettiness_2over1_boosted,
        # Transform_fj_Xbb_nsubjettiness_3over2_boosted,
        Transform_met_boosted,
        Transform_boosted_mass_tautaubb,
        Transform_boosted_pt_tautaubb,
        Transform_kinfit_mX_boosted,
        Transform_kinfit_mY_boosted,
        Transform_kinfit_chi2_boosted,
        Transform_boosted_mt_1,
    ],
)

Evaluate_PNN_boosted = ExtendedVectorProducer(
    name="Evaluate_PNN_boosted",
    call='ml::sofie::NMSSMEvaluate_ONNX({df}, {input_vec}, {output}, "{model_file_boosted}", "{massX_parameter}", "{massY_parameter}")',
    input=[
        q.transformed_njets_boosted,
        q.transformed_nbtag_boosted,
        q.transformed_nfatjets_boosted,
        q.transformed_boosted_pt_1,
        q.transformed_boosted_pt_2,
        q.transformed_boosted_eta_1,
        q.transformed_boosted_eta_2,
        q.transformed_boosted_deltaR_ditaupair,
        q.transformed_boosted_m_vis,
        q.transformed_boosted_m_fastmtt,
        q.transformed_boosted_pt_fastmtt,
        q.transformed_boosted_eta_fastmtt,
        q.transformed_bpair_pt_1_boosted,
        q.transformed_bpair_eta_1_boosted,
        q.transformed_bpair_btag_value_1_boosted,
        q.transformed_bpair_pt_2_boosted,
        q.transformed_bpair_eta_2_boosted,
        q.transformed_bpair_btag_value_2_boosted,
        q.transformed_bpair_m_inv_boosted,
        q.transformed_bpair_deltaR_boosted,
        q.transformed_bpair_pt_dijet_boosted,
        q.transformed_fj_Xbb_pt_boosted,
        q.transformed_fj_Xbb_eta_boosted,
        q.transformed_fj_Xbb_msoftdrop_boosted,
        q.transformed_fj_Xbb_nsubjettiness_2over1_boosted,
        # q.transformed_fj_Xbb_nsubjettiness_3over2_boosted,
        q.transformed_met_boosted,
        q.transformed_boosted_mass_tautaubb,
        q.transformed_boosted_pt_tautaubb,
        q.transformed_kinfit_mX_boosted,
        q.transformed_kinfit_mY_boosted,
        q.transformed_kinfit_chi2_boosted,
        q.transformed_boosted_mt_1,
        # q.massX,
        # q.massY,
    ],
    output=[
        "boosted_pnn_output_vector",
        "boosted_predicted_class",
        "boosted_predicted_max_value",
    ],
    scope=["mt"],
    vec_config="pnn_mass_parameters",
)

Evaluate_PNN_ORT_boosted = ExtendedVectorProducer(
    name="Evaluate_PNN_ORT_boosted",
    call='ml::PNNEvaluate_ORT<34>({df}, onnxSessionManager, {output}, "{model_file_boosted}", "{massX_parameter}", "{massY_parameter}", {input_vec})',
    input=[
        q.transformed_njets_boosted,
        q.transformed_nbtag_boosted,
        q.transformed_nfatjets_boosted,
        q.transformed_boosted_pt_1,
        q.transformed_boosted_pt_2,
        q.transformed_boosted_eta_1,
        q.transformed_boosted_eta_2,
        q.transformed_boosted_deltaR_ditaupair,
        q.transformed_boosted_m_vis,
        q.transformed_boosted_m_fastmtt,
        q.transformed_boosted_pt_fastmtt,
        q.transformed_boosted_eta_fastmtt,
        q.transformed_bpair_pt_1_boosted,
        q.transformed_bpair_eta_1_boosted,
        q.transformed_bpair_btag_value_1_boosted,
        q.transformed_bpair_pt_2_boosted,
        q.transformed_bpair_eta_2_boosted,
        q.transformed_bpair_btag_value_2_boosted,
        q.transformed_bpair_m_inv_boosted,
        q.transformed_bpair_deltaR_boosted,
        q.transformed_bpair_pt_dijet_boosted,
        q.transformed_fj_Xbb_pt_boosted,
        q.transformed_fj_Xbb_eta_boosted,
        q.transformed_fj_Xbb_msoftdrop_boosted,
        q.transformed_fj_Xbb_nsubjettiness_2over1_boosted,
        # q.transformed_fj_Xbb_nsubjettiness_3over2_boosted,
        q.transformed_met_boosted,
        q.transformed_boosted_mass_tautaubb,
        q.transformed_boosted_pt_tautaubb,
        q.transformed_kinfit_mX_boosted,
        q.transformed_kinfit_mY_boosted,
        q.transformed_kinfit_chi2_boosted,
        q.transformed_boosted_mt_1,
        # q.massX,
        # q.massY,
    ],
    output=[
        "boosted_pnn_output_vector",
        "boosted_predicted_class",
        "boosted_predicted_max_value",
    ],
    scope=["mt"],
    vec_config="pnn_mass_parameters",
)
