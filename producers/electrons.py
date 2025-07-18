"""
Producers for electron energy scale corrections, object selections, and vetoes.
"""

from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ..constants import EE_SCOPES, ET_SCOPES, ELECTRON_SCOPES, SCOPES, GLOBAL_SCOPES


#
# ENERGY SCALE CORRECTIONS
#


# corrections in embedding samples
ElectronPtCorrectionEmbedding = Producer(
    name="ElectronPtCorrectionEmbedding",
    call='embedding::electron::PtCorrection({df}, correctionManager, {output}, {input}, "{embedding_electron_es_sf_file}", "{ele_ES_json_name}", "{ele_energyscale_barrel}", "{ele_energyscale_endcap}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
    ],
    output=[q.Electron_pt_corrected],
    scopes=GLOBAL_SCOPES,
)

# corrections in MC samples in Run 2, for which an additional scale factor file needs to be provided
ElectronPtCorrectionMCRun2 = Producer(
    name="ElectronPtCorrectionMCRun2",
    call='physicsobject::electron::PtCorrectionMC({df}, correctionManager, {output}, {input}, "{ele_es_file}", "{ele_es_era}", "{ele_es_variation}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_seedGain,
        nanoAOD.Electron_dEsigmaUp,
        nanoAOD.Electron_dEsigmaDown,
    ],
    output=[q.Electron_pt_corrected],
    scopes=GLOBAL_SCOPES,
)

# electron scale correction for data in Run 3
ElectronPtCorrectionDataRun3 = Producer(
    name="ElectronPtCorrectionDataRun3",
    call='physicsobject::electron::PtCorrectionDataFromCorrectionlib({df}, correctionManager, {output}, {input}, "{ele_es_file}", "{ele_es_sf_data_name}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_deltaEtaSC,
        nanoAOD.Electron_seedGain,
        nanoAOD.Electron_r9,
        nanoAOD.run
    ],
    output=[q.Electron_pt_corrected],
    scopes=GLOBAL_SCOPES,
)

# event seed for initializing the smearing
ElectronPtSmearingSeed = Producer(
    name="ElectronPtSmearingSeed",
    call="event::quantity::GenerateEventSeed({df}, {output}, {input}, {ele_es_master_seed})",
    input=[
        nanoAOD.luminosityBlock,
        nanoAOD.run,
        nanoAOD.event,
    ],
    output=[],
    scopes=GLOBAL_SCOPES,
)

# electron scale and resolution correction for MC in Run 3
ElectronPtCorrectionMCRun3 = ProducerGroup(
    name="ElectronPtCorrectionMCRun3",
    call='physicsobject::electron::PtCorrectionMCFromCorrectionlib({df}, correctionManager, {output}, {input}, "{ele_es_file}", "{ele_es_sf_mc_name}", "{ele_es_variation}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_deltaEtaSC,
        nanoAOD.Electron_r9,
    ],
    output=[q.Electron_pt_corrected],
    scopes=GLOBAL_SCOPES,
    subproducers=[ElectronPtSmearingSeed],
)

# dummy corrections for cases in which corrections are already applied on NanoAOD level (just rename column)
RenameElectronPt = Producer(
    name="RenameElectronPt",
    call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
    input=[nanoAOD.Electron_pt],
    output=[q.Electron_pt_corrected],
    scopes=GLOBAL_SCOPES,
)


#
# OBJECT SELECTION
#


# selection mask for loose electrons (mainly used to evaluate veto masks)
BaseElectrons = Producer(
    name="BaseElectrons",
    call="xyh::object_selection::electron({df}, {output}, {input}, \"{loose_electron_id}\", {loose_electron_min_pt}, {loose_electron_max_abs_eta}, {loose_electron_max_abs_dxy}, {loose_electron_max_abs_dz}, {loose_electron_max_iso})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_dxy,
        nanoAOD.Electron_dz,
        nanoAOD.Electron_iso,
    ],
    output=[q.base_electrons_mask],
    scopes=GLOBAL_SCOPES,
)

# selection mask for tight electrons (final state tau candidates)
GoodElectrons = Producer(
    name="GoodElectrons",
    call="xyh::object_selection::electron({df}, {output}, {input}, \"{tight_electron_id}\", {tight_electron_min_pt}, {tight_electron_max_abs_eta}, {tight_electron_max_abs_dxy}, {tight_electron_max_abs_dz}, {tight_electron_max_iso})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_dxy,
        nanoAOD.Electron_dz,
        nanoAOD.Electron_iso,
    ],
    output=[q.good_electrons_mask],
    scopes=ELECTRON_SCOPES,
)

# count number of selected electrons
NumberOfGoodElectrons = Producer(
    name="NumberOfGoodElectrons",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_electrons_mask],
    output=[q.nelectrons],
    scopes=ELECTRON_SCOPES,
)


#
# EXTRA-ELECTRON VETO
#


# mask for veto electrons, excluding the selected electron from the di-tau pair for the resolved selection
VetoElectrons = Producer(
    name="VetoElectrons",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask],
    scopes=ELECTRON_SCOPES,
)

# mask for veto electrons, excluding the selected electron from the di-tau pair for the boosted selection
VetoElectrons_boosted = Producer(
    name="VetoElectrons_boosted",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.boosteddileptonpair],
    output=[q.veto_electrons_boosted_mask],
    scopes=ELECTRON_SCOPES,
)

# mask for veto electrons, excluding the selected electrons from the di-tau pair (ee) for the boosted selection
VetoSecondElectron = Producer(
    name="VetoSecondElectron",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {second_electron_index_in_pair})",
    input=[q.veto_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask_2],
    scopes=EE_SCOPES,
)

# extra-electron veto for the different channels for the resolved selection
ExtraElectronsVeto = Producer(
    name="ExtraElectronsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "em": [q.veto_electrons_mask],
        "et": [q.veto_electrons_mask],
        "mt": [q.base_electrons_mask],
        "tt": [q.base_electrons_mask],
        "mm": [q.base_electrons_mask],
        "ee": [q.veto_electrons_mask_2],
    },
    output=[q.electron_veto_flag],
    scopes=SCOPES,
)

# extra-electron veto for the different channels for the boosted selection
BoostedExtraElectronsVeto = Producer(
    name="BoostedExtraElectronsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "et": [q.veto_electrons_boosted_mask],
    },
    output=[q.boosted_electron_veto_flag],
    scopes=ET_SCOPES,
)


#
# DI-ELECTRON VETO
#


DiElectronVeto = Producer(
    name="DiElectronVeto",
    call="xyh::vetoes::dielectron({df}, {output}, {input}, {diele_electron_min_pt}, {diele_electron_max_abs_eta}, {diele_electron_max_iso}, {diele_electron_max_abs_dxy}, {diele_electron_max_abs_dz}, {diele_electron_id_wp}, {diele_electron_min_delta_r})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_iso,
        nanoAOD.Electron_dxy,
        nanoAOD.Electron_dz,
        nanoAOD.Electron_cutBased,
        nanoAOD.Electron_charge,
    ],
    output=[q.dielectron_veto],
    scopes=GLOBAL_SCOPES,
)
