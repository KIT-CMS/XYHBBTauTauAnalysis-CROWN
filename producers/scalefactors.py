from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
from code_generation.producer import ExtendedVectorProducer


############################
# Muon ID, ISO SF
# The readout is done via correctionlib
############################

Muon_1_ID_SF = Producer(
    name="MuonID_SF",
    call="""physicsobject::muon::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_id_sf_name}", 
        "{muon_id_sf_variation}")
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_mu_1],
    scopes=["mt", "mm"],
)
Muon_1_Iso_SF = Producer(
    name="MuonIso_SF",
    call="""physicsobject::muon::scalefactor::Iso(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_iso_sf_name}", 
        "{muon_iso_sf_variation}")
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_mu_1],
    scopes=["mt", "mm"],
)
Muon_2_ID_SF = Producer(
    name="MuonID_SF",
    call="""physicsobject::muon::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_id_sf_name}", 
        "{muon_id_sf_variation}")
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_mu_2],
    scopes=["em", "mm"],
)
Muon_2_Iso_SF = Producer(
    name="MuonIso_SF",
    call="""physicsobject::muon::scalefactor::Iso(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_iso_sf_name}", 
        "{muon_iso_sf_variation}")
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_mu_2],
    scopes=["em", "mm"],
)
MuonIDIso_SF = ProducerGroup(
    name="MuonIDIso_SF",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "em", "mm"],
    subproducers={
        "mt": [
            Muon_1_ID_SF,
            Muon_1_Iso_SF,
        ],
        "em": [
            Muon_2_ID_SF,
            Muon_2_Iso_SF,
        ],
        "mm": [
            Muon_1_ID_SF,
            Muon_1_Iso_SF,
            Muon_2_ID_SF,
            Muon_2_Iso_SF,
        ],
    },
)

Muon_1_Reco_SF_boosted = Producer(
    name="MuonReco_SF_boosted",
    call='scalefactor::muon::reco({df}, correctionManager, {input}, "{muon_reco_sf_variation}", {output}, "{muon_sf_file}", "{muon_reco_sf_name}")',
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.reco_wgt_mu_boosted_1],
    scopes=["mt"],
)
Muon_1_ID_SF_boosted = Producer(
    name="MuonID_SF_boosted",
    call="""physicsobject::muon::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_id_sf_name}", 
        "{muon_id_sf_variation}")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.id_wgt_mu_boosted_1],
    scopes=["mt"],
)
Muon_1_Iso_SF_boosted = Producer(
    name="MuonIso_SF_boosted",
    call="""physicsobject::muon::scalefactor::Iso(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{muon_sf_file}", 
        "{muon_iso_sf_name}", 
        "{muon_iso_sf_variation}")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.iso_wgt_mu_boosted_1],
    scopes=["mt"],
)
Muon_SF_boosted = ProducerGroup(
    name="Muon_SF_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["mt"],
    subproducers={
        "mt": [
            # Muon_1_Reco_SF_boosted,
            Muon_1_ID_SF_boosted,
            Muon_1_Iso_SF_boosted,
        ],
    },
)

############################
# Tau ID/ISO SF
# The readout is done via correctionlib
############################

Tau_1_VsJetTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsJetTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsJet_tt(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsjet_tau_id_WP}", 
        "{tau_vsjet_vseleWP}", 
        "{tau_vsjet_sf_dependence}", 
        "{tau_sf_vsjet_tauDM0}", 
        "{tau_sf_vsjet_tauDM1}", 
        "{tau_sf_vsjet_tauDM10}", 
        "{tau_sf_vsjet_tauDM11}")
        """,
    input=[q.pt_1, q.tau_decaymode_1, q.gen_match_1],
    output="tau_1_vsjet_sf_outputname",
    scope=["tt"],
    vec_config="vsjet_tau_id_sf",
)
Tau_1_VsEleTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsEleTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsEle(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsele_tau_id_WP}", 
        "{tau_sf_vsele_barrel}", 
        "{tau_sf_vsele_endcap}")
        """,
    input=[q.eta_1, q.gen_match_1],
    output="tau_1_vsele_sf_outputname",
    scope=["tt"],
    vec_config="vsele_tau_id",
)
Tau_1_VsMuTauID_SF = ExtendedVectorProducer(
    name="Tau_1_VsMuTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsMu(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsmu_tau_id_WP}", 
        "{tau_sf_vsmu_wheel1}", 
        "{tau_sf_vsmu_wheel2}", 
        "{tau_sf_vsmu_wheel3}", 
        "{tau_sf_vsmu_wheel4}", 
        "{tau_sf_vsmu_wheel5}")
        """,
    input=[q.eta_1, q.gen_match_1],
    output="tau_1_vsmu_sf_outputname",
    scope=["tt"],
    vec_config="vsmu_tau_id",
)
Tau_2_VsJetTauID_lt_SF = ExtendedVectorProducer(
    name="Tau_2_VsJetTauID_lt_SF",
    call="""physicsobject::tau::scalefactor::Id_vsJet_lt(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        {vec_open}{tau_dms}{vec_close}, 
        "{vsjet_tau_id_WP}", 
        "{tau_vsjet_vseleWP}", 
        "{tau_vsjet_sf_dependence}", 
        "{tau_sf_vsjet_tau30to35}", 
        "{tau_sf_vsjet_tau35to40}", 
        "{tau_sf_vsjet_tau40to500}", 
        "{tau_sf_vsjet_tau500to1000}", 
        "{tau_sf_vsjet_tau1000toinf}")
        """,
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["et", "mt"],
    vec_config="vsjet_tau_id_sf",
)
Tau_2_VsJetTauID_tt_SF = ExtendedVectorProducer(
    name="Tau_2_VsJetTauID_tt_SF",
    call="""physicsobject::tau::scalefactor::Id_vsJet_tt(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsjet_tau_id_WP}", 
        "{tau_vsjet_vseleWP}", 
        "{tau_vsjet_sf_dependence}", 
        "{tau_sf_vsjet_tauDM0}", 
        "{tau_sf_vsjet_tauDM1}", 
        "{tau_sf_vsjet_tauDM10}", 
        "{tau_sf_vsjet_tauDM11}")
        """,
    input=[q.pt_2, q.tau_decaymode_2, q.gen_match_2],
    output="tau_2_vsjet_sf_outputname",
    scope=["tt"],
    vec_config="vsjet_tau_id_sf",
)
Tau_2_VsEleTauID_SF = ExtendedVectorProducer(
    name="Tau_2_VsEleTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsEle(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsele_tau_id_WP}", 
        "{tau_sf_vsele_barrel}", 
        "{tau_sf_vsele_endcap}")
        """,
    input=[q.eta_2, q.gen_match_2],
    output="tau_2_vsele_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="vsele_tau_id",
)
Tau_2_VsMuTauID_SF = ExtendedVectorProducer(
    name="Tau_2_VsMuTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsMu(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "{tau_id_discriminator}", 
        "{vsmu_tau_id_WP}", 
        "{tau_sf_vsmu_wheel1}", 
        "{tau_sf_vsmu_wheel2}", 
        "{tau_sf_vsmu_wheel3}", 
        "{tau_sf_vsmu_wheel4}", 
        "{tau_sf_vsmu_wheel5}")
        """,
    input=[q.eta_2, q.gen_match_2],
    output="tau_2_vsmu_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="vsmu_tau_id",
)
TauID_SF = ProducerGroup(
    name="TauID_SF",
    call=None,
    input=None,
    output=None,
    scopes=["tt", "mt", "et"],
    subproducers={
        "tt": [
            Tau_1_VsJetTauID_SF,
            Tau_1_VsEleTauID_SF,
            Tau_1_VsMuTauID_SF,
            Tau_2_VsJetTauID_tt_SF,
            Tau_2_VsEleTauID_SF,
            Tau_2_VsMuTauID_SF,
        ],
        "mt": [
            Tau_2_VsJetTauID_lt_SF,
            Tau_2_VsEleTauID_SF,
            Tau_2_VsMuTauID_SF,
        ],
        "et": [
            Tau_2_VsJetTauID_lt_SF,
            Tau_2_VsEleTauID_SF,
            Tau_2_VsMuTauID_SF,
        ],
    },
)

Tau_1_oldIsoTauID_tt_SF = ExtendedVectorProducer(
    name="Tau_1_oldIsoTauID_tt_SF",
    call='scalefactor::tau::id_mva_vsJet_tt({df}, correctionManager, {input}, {vec_open}{boostedtau_dms}{vec_close}, "{iso_boostedtau_id_WP}", "{boostedtau_sf_iso_tauDM0}", "{boostedtau_sf_iso_tauDM1}", "{boostedtau_sf_iso_tauDM10}", "{boostedtau_sf_iso_tauDM11}", "{boostedtau_iso_sf_dependence}", "", {output}, "{boostedtau_sf_file}", "{boostedtau_id_discriminator}")',
    input=[q.boosted_pt_1, q.boosted_tau_decaymode_1, q.boosted_gen_match_1],
    output="boostedtau_1_iso_sf_outputname",
    scope=["tt"],
    vec_config="iso_boostedtau_id",
)
Tau_1_antiEleTauID_SF = ExtendedVectorProducer(
    name="Tau_1_antiEleTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsEle(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{boostedtau_sf_file}", 
        "{boostedtau_id_discriminator}", 
        "{antiele_boostedtau_id_WP}", 
        "{boostedtau_sf_antiele_barrel}", 
        "{boostedtau_sf_antiele_endcap}")
        """,
    input=[q.boosted_eta_1, q.boosted_gen_match_1],
    output="boostedtau_1_antiele_sf_outputname",
    scope=["tt"],
    vec_config="antiele_boostedtau_id",
)
Tau_1_antiMuTauID_SF = ExtendedVectorProducer(
    name="Tau_1_antiMuTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsMu(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{boostedtau_sf_file}", 
        "{boostedtau_id_discriminator}", 
        "{antimu_boostedtau_id_WP}", 
        "{boostedtau_sf_antimu_wheel1}", 
        "{boostedtau_sf_antimu_wheel2}", 
        "{boostedtau_sf_antimu_wheel3}", 
        "{boostedtau_sf_antimu_wheel4}", 
        "{boostedtau_sf_antimu_wheel5}")
        """,
    input=[q.boosted_eta_1, q.boosted_gen_match_1],
    output="boostedtau_1_antimu_sf_outputname",
    scope=["tt"],
    vec_config="antimu_boostedtau_id",
)
Tau_2_oldIsoTauID_tt_SF = ExtendedVectorProducer(
    name="Tau_2_oldIsoTauID_tt_SF",
    call='scalefactor::tau::id_mva_vsJet_tt({df}, correctionManager, {input}, {vec_open}{boostedtau_dms}{vec_close}, "{iso_boostedtau_id_WP}", "{boostedtau_sf_iso_tauDM0}", "{boostedtau_sf_iso_tauDM1}", "{boostedtau_sf_iso_tauDM10}", "{boostedtau_sf_iso_tauDM11}", "{boostedtau_iso_sf_dependence}", "", {output}, "{boostedtau_sf_file}", "{boostedtau_id_discriminator}")',
    input=[q.boosted_pt_2, q.boosted_tau_decaymode_2, q.boosted_gen_match_2],
    output="boostedtau_2_iso_sf_outputname",
    scope=["tt"],
    vec_config="iso_boostedtau_id",
)
Tau_2_oldIsoTauID_lt_SF = ExtendedVectorProducer(
    name="Tau_2_oldIsoTauID_lt_SF",
    call='scalefactor::tau::id_mva_vsJet_lt({df}, correctionManager, {input}, {vec_open}{boostedtau_dms}{vec_close}, "{iso_boostedtau_id_WP}", "{boostedtau_sf_iso_tau30to35}", "{boostedtau_sf_iso_tau35to40}", "{boostedtau_sf_iso_tau40to500}", "{boostedtau_sf_iso_tau500to1000}", "{boostedtau_sf_iso_tau1000toinf}", "{boostedtau_iso_sf_dependence}", "", {output}, "{boostedtau_sf_file}", "{boostedtau_id_discriminator}")',
    input=[q.boosted_pt_2, q.boosted_tau_decaymode_2, q.boosted_gen_match_2],
    output="boostedtau_2_iso_sf_outputname",
    scope=["et", "mt"],
    vec_config="iso_boostedtau_id",
)
Tau_2_antiEleTauID_SF = ExtendedVectorProducer(
    name="Tau_2_antiEleTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsEle(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{boostedtau_sf_file}", 
        "{boostedtau_id_discriminator}", 
        "{antiele_boostedtau_id_WP}", 
        "{boostedtau_sf_antiele_barrel}", 
        "{boostedtau_sf_antiele_endcap}")
        """,
    input=[q.boosted_eta_2, q.boosted_gen_match_2],
    output="boostedtau_2_antiele_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="antiele_boostedtau_id",
)
Tau_2_antiMuTauID_SF = ExtendedVectorProducer(
    name="Tau_2_antiMuTauID_SF",
    call="""physicsobject::tau::scalefactor::Id_vsMu(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{boostedtau_sf_file}", 
        "{boostedtau_id_discriminator}", 
        "{antimu_boostedtau_id_WP}", 
        "{boostedtau_sf_antimu_wheel1}", 
        "{boostedtau_sf_antimu_wheel2}", 
        "{boostedtau_sf_antimu_wheel3}", 
        "{boostedtau_sf_antimu_wheel4}", 
        "{boostedtau_sf_antimu_wheel5}")
        """,
    input=[q.boosted_eta_2, q.boosted_gen_match_2],
    output="boostedtau_2_antimu_sf_outputname",
    scope=["et", "mt", "tt"],
    vec_config="antimu_boostedtau_id",
)
BoostedTauID_SF = ProducerGroup(
    name="BoostedTauID_SF",
    call=None,
    input=None,
    output=None,
    scopes=["tt", "mt", "et"],
    subproducers={
        "tt": [
            Tau_1_VsJetTauID_SF,
            Tau_1_VsEleTauID_SF,
            Tau_1_VsMuTauID_SF,
            Tau_2_oldIsoTauID_tt_SF,
            Tau_2_antiEleTauID_SF,
            Tau_2_antiMuTauID_SF,
        ],
        "mt": [
            Tau_2_oldIsoTauID_lt_SF,
            Tau_2_antiEleTauID_SF,
            Tau_2_antiMuTauID_SF,
        ],
        "et": [
            Tau_2_oldIsoTauID_lt_SF,
            Tau_2_antiEleTauID_SF,
            Tau_2_antiMuTauID_SF,
        ],
    },
)

#########################
# Electron ID/ISO SF
#########################
Ele_1_Reco_SF = Producer(
    name="Ele_1_Reco_SF",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_reco_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_reco_sf_variation}")
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.reco_wgt_ele_1],
    scopes=["em", "ee", "et"],
)
Ele_2_Reco_SF = Producer(
    name="Ele_2_Reco_SF",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_reco_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_reco_sf_variation}")
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.reco_wgt_ele_2],
    scopes=["ee"],
)
Ele_1_IDWP90_SF = Producer(
    name="Ele_1_IDWP90_SF",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_id_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_id_sf_variation}")
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_ele_wp90nonIso_1],
    scopes=["em", "ee", "et"],
)
Ele_2_IDWP90_SF = Producer(
    name="Ele_2_IDWP90_SF",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_id_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_id_sf_variation}")
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_ele_wp90nonIso_2],
    scopes=["ee"],
)
EleID_SF = ProducerGroup(
    name="EleID_SF",
    call=None,
    input=None,
    output=None,
    scopes=["em", "ee", "et"],
    subproducers={
        "em": [Ele_1_Reco_SF, Ele_1_IDWP90_SF],
        "ee": [
            Ele_1_Reco_SF,
            Ele_2_Reco_SF,
            Ele_1_IDWP90_SF,
            Ele_2_IDWP90_SF,
        ],
        "et": [Ele_1_Reco_SF, Ele_1_IDWP90_SF],
    },
)
Ele_1_Reco_SF_boosted = Producer(
    name="Ele_1_Reco_SF_boosted",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_reco_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_reco_sf_variation}")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.reco_wgt_ele_boosted_1],
    scopes=["et"],
)
Ele_1_IDWP90_SF_boosted = Producer(
    name="Ele_1_IDWP90_SF_boosted",
    call="""physicsobject::electron::scalefactor::Id(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{ele_sf_year_id}", 
        "{ele_id_sf_name}", 
        "{ele_sf_file}", 
        "{ele_sf_cset_name}", 
        "{ele_id_sf_variation}")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.id_wgt_ele_boosted_wp90nonIso_1],
    scopes=["et"],
)
EleID_SF_boosted = ProducerGroup(
    name="EleID_SF_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et"],
    subproducers={
        "et": [Ele_1_Reco_SF_boosted, Ele_1_IDWP90_SF_boosted],
    },
)

###################################
# Trigger Scalefactors coming from our measurements
###################################


#
# SINGLE MUON TRIGGER SCALE FACTORS
#


# single muon trigger scale factor
SingleMuTriggerSF = ExtendedVectorProducer(
    name="SingleMuTriggerSF",
    call='physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{muon_sf_file}", "{m_trigger_sf_name}", "{m_trigger_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="m_trigger_flagname",
    scope=["mt"],
    vec_config="single_mu_trigger_sf",
)


#
# DOUBLE MUON-TAU TRIGGER SCALE FACTORS
#


# muon leg scale factor
DoubleMuTauTriggerLeg1SF = ExtendedVectorProducer(
    name="DoubleMuTauTriggerLeg1SF",
    call='physicsobject::muon::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{mt_trigger_leg1_sf_file}", "{mt_trigger_leg1_sf_name}", "{mt_trigger_leg1_variation}")',
    input=[
        q.pt_1,
        q.eta_1,
    ],
    output="mt_trigger_leg1_flagname",
    scope=["mt"],
    vec_config="double_mutau_trigger_leg1_sf",
)

# tau leg scale factor (for the Medium DeepTau WP)
DoubleMuTauTriggerLeg2SF = ExtendedVectorProducer(
    name="GenerateMuTauCrossTriggerLeg2SF",
    call='physicsobject::tau::scalefactor::Trigger({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "tau_trigger", "{mt_trigger_leg2_sf_name}", "Medium", "sf", "{mt_trigger_leg2_variation}")',
    input=[
        q.pt_2,
        q.tau_decaymode_2,
    ],
    output="mt_trigger_leg2_flagname",
    scope=["mt"],
    vec_config="double_mutau_trigger_leg2_sf",
)

BoostedMTGenerateSingleMuonTriggerSF_MC = ExtendedVectorProducer(
    name="BoostedMTGenerateSingleMuonTriggerSF_MC",
    call='scalefactor::muon::trigger({df}, correctionManager, {input}, "{muon_trg_sf_variation}", {output}, "{muon_sf_file}", "{muon_trigger_sf_name}")',
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output="flagname",
    scope=["mt"],
    vec_config="boosted_singlemuon_trigger_sf_mc",
)

ETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(
    name="ETGenerateSingleElectronTriggerSF_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_trigger_sf}", 
        "mc", 
        {mc_electron_trg_extrapolation})
        """,
    input=[q.pt_1, q.eta_1],
    output="flagname",
    scope=["et", "ee"],
    vec_config="singlelectron_trigger_sf_mc",
)
BoostedETGenerateSingleElectronTriggerSF_MC = ExtendedVectorProducer(
    name="BoostedETGenerateSingleElectronTriggerSF_MC",
    call='scalefactor::electron::trigger({df}, correctionManager, {input}, "{ele_trg_sf_variation}", {output}, "{ele_trg_sf_file}", "{ele_trg_sf_name}")',
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output="flagname",
    scope=["et"],
    vec_config="boosted_singleelectron_trigger_sf_mc",
)

TTGenerateDoubleTauTriggerSF_MC_1 = Producer(
    name="TTGenerateDoubleTauTriggerSF_MC_1",
    call="""physicsobject::tau::scalefactor::Trigger(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "tau_trigger", 
        "{ditau_trigger_type}", 
        "{ditau_trigger_wp}", 
        "{ditau_trigger_corrtype}", 
        "{ditau_trigger_syst}")
        """,
    input=[q.pt_1, q.tau_decaymode_1],
    output=[q.trg_wgt_double_tau_1],
    scopes=["tt"],
)
TTGenerateDoubleTauTriggerSF_MC_2 = Producer(
    name="TTGenerateDoubleTauTriggerSF_MC_2",
    call="""physicsobject::tau::scalefactor::Trigger(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{tau_sf_file}", 
        "tau_trigger", 
        "{ditau_trigger_type}", 
        "{ditau_trigger_wp}", 
        "{ditau_trigger_corrtype}", 
        "{ditau_trigger_syst}")
        """,
    input=[q.pt_2, q.tau_decaymode_2],
    output=[q.trg_wgt_double_tau_2],
    scopes=["tt"],
)
TTGenerateDoubleTauTriggerSF_MC = ProducerGroup(
    name="TTGenerateDoubleTauTriggerSF_MC",
    call=None,
    input=None,
    output=None,
    scopes=["tt"],
    subproducers=[
        TTGenerateDoubleTauTriggerSF_MC_1,
        TTGenerateDoubleTauTriggerSF_MC_2,
    ],
)
BoostedTTGenerateFatjetTriggerSF_MC = Producer(
    name="BoostedTTGenerateFatjetTriggerSF_MC",
    call='scalefactor::fatjet::trigger({df}, correctionManager, {input}, {output}, "{fatjet_trigger_sf_file}", "{fatjet_trigger_sf_name}", "{fatjet_trigger_sf_syst}")',
    input=[q.fj_leading_pt, q.fj_leading_msoftdrop],
    output=[q.trg_wgt_fatjet],
    scopes=["tt"],
)

####################################
# Electron and Muon SFs coming from our measurements
####################################
TauEmbeddingMuonIDSF_1_MC = Producer(
    name="TauEmbeddingMuonIDSF_1_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_id_sf}", 
        "mc", 
        {mc_muon_id_extrapolation})
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_mu_1],
    scopes=["mt", "mm"],
)

TauEmbeddingMuonIDSF_2_MC = Producer(
    name="TauEmbeddingMuonIDSF_2_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_id_sf}", 
        "mc", 
        {mc_muon_id_extrapolation})
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_mu_2],
    scopes=["mm", "em"],
)

TauEmbeddingMuonIsoSF_1_MC = Producer(
    name="TauEmbeddingMuonIsoSF_1_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_iso_sf}", 
        "mc", 
        {mc_muon_iso_extrapolation})
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_mu_1],
    scopes=["mt", "mm"],
)

TauEmbeddingMuonIsoSF_2_MC = Producer(
    name="TauEmbeddingMuonIsoSF_2_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_iso_sf}", 
        "mc", 
        {mc_muon_iso_extrapolation})
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_mu_2],
    scopes=["mm", "em"],
)

TauEmbeddingBoostedMuonIDSF_1_MC = Producer(
    name="TauEmbeddingBoostedMuonIDSF_1_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_id_sf}", 
        "mc")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.emb_id_wgt_mu_boosted_1],
    scopes=["mt", "mm"],
)
TauEmbeddingBoostedMuonIsoSF_1_MC = Producer(
    name="TauEmbeddingBoostedMuonIsoSF_1_MC",
    call="""embedding::muon::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_muon_sf_file}", 
        "{mc_muon_iso_sf}", 
        "mc")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.emb_iso_wgt_mu_boosted_1],
    scopes=["mt", "mm"],
)

# Electron ID/Iso/Trigger SFS

TauEmbeddingElectronIDSF_1_MC = Producer(
    name="TauEmbeddingElectronIDSF_1_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_id_sf}", 
        "mc", 
        {mc_electron_id_extrapolation})
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.id_wgt_ele_1],
    scopes=["et", "ee", "em"],
)

TauEmbeddingElectronIDSF_2_MC = Producer(
    name="TauEmbeddingElectronIDSF_2_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_id_sf}", 
        "mc", 
        {mc_electron_id_extrapolation})
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.id_wgt_ele_2],
    scopes=["ee"],
)

TauEmbeddingElectronIsoSF_1_MC = Producer(
    name="TauEmbeddingElectronIsoSF_1_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_iso_sf}", 
        "mc", 
        {mc_electron_iso_extrapolation})
        """,
    input=[q.pt_1, q.eta_1],
    output=[q.iso_wgt_ele_1],
    scopes=["et", "ee", "em"],
)

TauEmbeddingElectronIsoSF_2_MC = Producer(
    name="TauEmbeddingElectronIsoSF_2_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_iso_sf}", 
        "mc", 
        {mc_electron_iso_extrapolation})
        """,
    input=[q.pt_2, q.eta_2],
    output=[q.iso_wgt_ele_2],
    scopes=["ee"],
)

TauEmbeddingBoostedElectronIDSF_1_MC = Producer(
    name="TauEmbeddingBoostedElectronIDSF_1_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_id_sf}", 
        "mc")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.id_wgt_ele_boosted_1],
    scopes=["et", "ee", "em"],
)
TauEmbeddingBoostedElectronIsoSF_1_MC = Producer(
    name="TauEmbeddingBoostedElectronIsoSF_1_MC",
    call="""embedding::electron::Scalefactor(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{mc_electron_sf_file}", 
        "{mc_electron_iso_sf}", 
        "mc")
        """,
    input=[q.boosted_pt_1, q.boosted_eta_1],
    output=[q.iso_wgt_ele_boosted_1],
    scopes=["et", "ee", "em"],
)

#########################
# b-tagging SF
#########################
btagging_SF = Producer(
    name="btagging_SF",
    call="""physicsobject::jet::scalefactor::Btagging(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{btag_sf_file}", 
        "{btag_corr_algo}", 
        "{btag_sf_variation}")
        """,
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.BJet_discriminator,
        nanoAOD.Jet_flavour,
        q.good_jets_mask,
        q.good_bjets_mask,
        q.jet_overlap_veto_mask,
    ],
    output=[q.btag_weight],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)
btagging_SF_boosted = Producer(
    name="btagging_SF_boosted",
    call="""physicsobject::jet::scalefactor::Btagging(
        {df}, 
        correctionManager, 
        {output}, 
        {input}, 
        "{btag_sf_file}", 
        "{btag_corr_algo}", 
        "{btag_sf_variation}")
        """,
    input=[
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.BJet_discriminator,
        nanoAOD.Jet_flavour,
        q.good_jets_mask,
        q.good_bjets_mask,
        q.jet_overlap_veto_mask_boosted,
    ],
    output=[q.btag_weight_boosted],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)

#########################
# particleNet tagging SF
#########################
Xbb_tagging_SF = Producer(
    name="Xbb_tagging_SF",
    call='scalefactor::fatjet::pNetXbbSF({df}, correctionManager, {input}, "{pNetXbb_sf_variation}", {output}, "{pNetXbb_sf_file}")',
    input=[
        q.fj_Xbb_pt,
        q.fj_Xbb_nBhad,
        q.fj_Xbb_nChad,
    ],
    output=[q.pNet_Xbb_weight],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)
Xbb_tagging_SF_boosted = Producer(
    name="Xbb_tagging_SF_boosted",
    call='scalefactor::fatjet::pNetXbbSF({df}, correctionManager, {input}, "{pNetXbb_sf_variation}", {output}, "{pNetXbb_sf_file}")',
    input=[
        q.fj_Xbb_pt_boosted,
        q.fj_Xbb_nBhad_boosted,
        q.fj_Xbb_nChad_boosted,
    ],
    output=[q.pNet_Xbb_weight_boosted],
    scopes=["tt", "mt", "et", "mm", "em", "ee"],
)