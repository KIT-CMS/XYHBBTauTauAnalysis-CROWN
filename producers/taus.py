"""
Producers for hadronic tau energy scale corrections and object selections.
"""

from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup
from ..constants import HAD_TAU_SCOPES


#
# ENERGY SCALE CORRECTIONS
#

# tau pt correction for Run 2
TauPtCorrectionRun2 = Producer(
    name="TauPtCorrectionRun2",
    call="""
        physicsobject::tau::PtCorrectionMC(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_ES_json_name}",
            "{tau_id_algorithm}",
            "{tau_elefake_es_DM0_barrel}",
            "{tau_elefake_es_DM1_barrel}",
            "{tau_elefake_es_DM0_endcap}",
            "{tau_elefake_es_DM1_endcap}",
            "{tau_mufake_es}",
            "{tau_ES_shift_DM0}",
            "{tau_ES_shift_DM1}",
            "{tau_ES_shift_DM10}",
            "{tau_ES_shift_DM11}"
        )
    """,
    input=[
        nanoAOD.Tau_pt,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_genPartFlav,
    ],
    output=[q.Tau_pt_corrected],
    scopes=HAD_TAU_SCOPES,
)

# tau pt correction for Run 3
TauPtCorrectionRun3 = Producer(
    name="TauPtCorrectionRun3",
    call="""
        physicsobject::tau::PtCorrectionMC(
            {df},
            correctionManager,
            {output},
            {input},
            "{tau_sf_file}",
            "{tau_ES_json_name}",
            "{tau_id_algorithm}",
            "{tau_elefake_es_DM0_barrel}",
            "{tau_elefake_es_DM1_barrel}",
            "{tau_elefake_es_DM0_endcap}",
            "{tau_elefake_es_DM1_endcap}",
            "{tau_mufake_es}",
            "{tau_ES_shift_DM0}",
            "{tau_ES_shift_DM1}",
            "{tau_ES_shift_DM10}",
            "{tau_ES_shift_DM11}",
            "{tau_es_vs_jet_wp}",
            "{tau_es_vs_ele_wp}"
        )
    """,
    input=[
        nanoAOD.Tau_pt,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_genPartFlav,
    ],
    output=[q.Tau_pt_corrected],
    scopes=HAD_TAU_SCOPES,
)

# pt correction for hadronic taus in embedding samples
TauPtCorrection_byValue = Producer(
    name="TauPtCorrection",
    call="embedding::tau::PtCorrection_byValue({df}, {output}, {input}, {tau_ES_shift_DM0}, {tau_ES_shift_DM1}, {tau_ES_shift_DM10}, {tau_ES_shift_DM11})",
    input=[
        nanoAOD.Tau_pt,
        nanoAOD.Tau_decayMode,
    ],
    output=[q.Tau_pt_corrected],
    scopes=HAD_TAU_SCOPES,
)

# pt correction for electrons that fake hadronic taus
TauPtCorrection_eleFake = Producer(
    name="TauPtCorrection_eleFake",
    call='physicsobject::tau::PtCorrectionMC_eleFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_elefake_es_DM0_barrel}", "{tau_elefake_es_DM1_barrel}", "{tau_elefake_es_DM0_endcap}", "{tau_elefake_es_DM1_endcap}")',
    input=[
        nanoAOD.Tau_pt,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_genPartFlav,
    ],
    output=[q.Tau_pt_ele_corrected],
    scopes=HAD_TAU_SCOPES,
)

# pt correction for muons that fake hadronic taus 
TauPtCorrection_muFake = Producer(
    name="TauPtCorrection_muFake",
    call='physicsobject::tau::PtCorrectionMC_muFake({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_mufake_es}")',
    input=[
        q.Tau_pt_ele_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_genPartFlav,
    ],
    output=[q.Tau_pt_ele_mu_corrected],
    scopes=HAD_TAU_SCOPES,
)

# pt correction for genuine hadronic taus 
TauPtCorrection_genTau = Producer(
    name="TauPtCorrection_genTau",
    call='physicsobject::tau::PtCorrectionMC_genuineTau({df}, correctionManager, {output}, {input}, "{tau_sf_file}", "{tau_ES_json_name}", "{tau_id_algorithm}", "{tau_ES_shift_DM0}", "{tau_ES_shift_DM1}", "{tau_ES_shift_DM10}", "{tau_ES_shift_DM11}")',
    input=[
        q.Tau_pt_ele_mu_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_genPartFlav,
    ],
    output=[q.Tau_pt_corrected],
    scopes=HAD_TAU_SCOPES,
)

# dummy pt corrections in data and for cases in which corrections are already applied on NANOAOD level (just rename column)
TauPtCorrection_data = Producer(
    name="TauPtCorrection_data",
    call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
    input=[nanoAOD.Tau_pt],
    output=[q.Tau_pt_corrected],
    scopes=HAD_TAU_SCOPES,
)

# dummy mass corrections in data and for cases in which corrections are already applied on NANOAOD level (just rename column)
TauMassCorrection_data = Producer(
    name="TauMassCorrection_data",
    call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
    input=[nanoAOD.Tau_mass],
    output=[q.Tau_mass_corrected],
    scopes=HAD_TAU_SCOPES,
)

# mass correction derived from the pt correction
TauMassCorrection = Producer(
    name="TauMassCorrection",
    call="physicsobject::MassCorrectionWithPt({df}, {output}, {input})",
    input=[
        nanoAOD.Tau_mass,
        nanoAOD.Tau_pt,
        q.Tau_pt_corrected,
    ],
    output=[q.Tau_mass_corrected],
    scopes=HAD_TAU_SCOPES,
)

# producer group encapsulating tau pt corrections in embedding samples
TauEnergyCorrection_byValue = ProducerGroup(
    name="TauEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=HAD_TAU_SCOPES,
    subproducers=[
        TauPtCorrection_eleFake,
        TauPtCorrection_byValue,
        TauMassCorrection,
    ],
)

# producer group encapsulating all tau energy scale corrections in MC samples
TauEnergyCorrectionMCRun2 = ProducerGroup(
    name="TauEnergyCorrectionMCRun2",
    call=None,
    input=None,
    output=None,
    scopes=HAD_TAU_SCOPES,
    subproducers=[
        TauPtCorrection_eleFake,
        TauPtCorrection_muFake,
        TauPtCorrection_genTau,
        TauMassCorrection,
    ],
)

# producer group encapsulating all tau energy scale corrections in Run 3 MC samples
TauEnergyCorrectionMCRun3 = ProducerGroup(
    name="TauEnergyCorrectionMCRun3",
    call=None,
    input=None,
    output=None,
    scopes=HAD_TAU_SCOPES,
    subproducers=[
        TauPtCorrectionRun3,
        TauMassCorrection,
    ],
)

# producer group encapsulating all tau energy scale corrections in embedding samples
TauEnergyCorrection_Embedding = ProducerGroup(
    name="TauEnergyCorrection_Embedding",
    call=None,
    input=None,
    output=None,
    scopes=HAD_TAU_SCOPES,
    subproducers=[
        TauPtCorrection_byValue,
        TauMassCorrection,
    ],
)

# producer group encapsulating dummy tau energy scale corrections in data
TauEnergyCorrection_data = ProducerGroup(
    name="TauEnergyCorrection",
    call=None,
    input=None,
    output=None,
    scopes=HAD_TAU_SCOPES,
    subproducers=[
        TauPtCorrection_data,
        TauMassCorrection_data,
    ],
)


#
# OBJECT SELECTION
#


# selection masks for tight hadronic taus (final state tau candidates)
GoodTaus = Producer(
    name="GoodTaus",
    call="xyh::object_selection::tau({df}, {output}, {input}, {tight_tau_min_pt}, {tight_tau_max_abs_eta}, {tight_tau_max_abs_dz}, {{{tight_tau_decay_modes}}}, {tight_tau_id_vs_jet_wp}, {tight_tau_id_vs_electron_wp}, {tight_tau_id_vs_muon_wp})",
    input=[
        q.Tau_pt_corrected,
        nanoAOD.Tau_eta,
        nanoAOD.Tau_dz,
        nanoAOD.Tau_decayMode,
        nanoAOD.Tau_idDeepTau2018v2p5VSjet,
        nanoAOD.Tau_idDeepTau2018v2p5VSe,
        nanoAOD.Tau_idDeepTau2018v2p5VSmu,
    ],
    output=[q.good_taus_mask],
    scopes=HAD_TAU_SCOPES,
)

# count number of selected hadronic taus
NumberOfGoodTaus = Producer(
    name="NumberOfGoodTaus",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_taus_mask],
    output=[q.ntaus],
    scopes=HAD_TAU_SCOPES,
)
