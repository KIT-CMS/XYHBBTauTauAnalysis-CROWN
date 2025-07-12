"""
Producers for electron energy scale corrections, object selections, and vetoes.
"""

from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ..constants import ET_SCOPES, ELECTRON_SCOPES, SCOPES, GLOBAL_SCOPES


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

# corrections in MC samples
ElectronPtCorrectionMC = Producer(
    name="ElectronPtCorrectionMC",
    call='physicsobject::electron::PtCorrectionMC({df}, correctionManager, {output}, {input}, {ele_es_file}, {ele_es_era}, "{ele_es_variation}")',
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

# dummy corrections in data and for cases in which corrections are already applied on NANOAOD level (just rename column)
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


#
# EXTRA-ELECTRON VETO
# TODO could be reworked
#


VetoElectrons = Producer(
    name="VetoElectrons",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask],
    scopes=ELECTRON_SCOPES,
)
VetoElectrons_boosted = Producer(
    name="VetoElectrons_boosted",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.boosteddileptonpair],
    output=[q.veto_electrons_boosted_mask],
    scopes=ELECTRON_SCOPES,
)
VetoSecondElectron = Producer(
    name="VetoSecondElectron",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {second_electron_index_in_pair})",
    input=[q.veto_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask_2],
    scopes=["ee"],
)
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
BoostedExtraElectronsVeto = Producer(
    name="BoostedExtraElectronsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "et": [q.veto_electrons_boosted_mask],
    },
    output=[q.boosted_electron_veto_flag],
    scopes=ET_SCOPES,
)
NumberOfGoodElectrons = Producer(
    name="NumberOfGoodElectrons",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_electrons_mask],
    output=[q.nelectrons],
    scopes=ELECTRON_SCOPES,
)


#
# DI-ELECTRON VETO
# TODO could be reworked
#


DiElectronVetoPtCut = Producer(
    name="DiElectronVetoPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_dielectronveto_pt})",
    input=[q.Electron_pt_corrected],
    output=[],
    scopes=GLOBAL_SCOPES,
)
DiElectronVetoIDCut = Producer(
    name="DiElectronVetoIDCut",
    call='physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {dielectronveto_id_wp})',
    input=[nanoAOD.Electron_cutBased],
    output=[],
    scopes=GLOBAL_SCOPES,
)
ElectronEtaCut = Producer(
    name="ElectronEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_eta})",
    input=[nanoAOD.Electron_eta],
    output=[],
    scopes=GLOBAL_SCOPES,
)
ElectronDxyCut = Producer(
    name="ElectronDxyCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_dxy})",
    input=[nanoAOD.Electron_dxy],
    output=[],
    scopes=GLOBAL_SCOPES,
)
ElectronDzCut = Producer(
    name="ElectronDzCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_dz})",
    input=[nanoAOD.Electron_dz],
    output=[],
    scopes=GLOBAL_SCOPES,
)
ElectronIsoCut = Producer(
    name="ElectronIsoCut",
    call="physicsobject::CutMax<float>({df}, {output}, {input}, {loose_electron_max_iso})",
    input=[nanoAOD.Electron_iso],
    output=[],
    scopes=GLOBAL_SCOPES,
)
DiElectronVetoElectrons = ProducerGroup(
    name="DiElectronVetoElectrons",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[],
    scopes=GLOBAL_SCOPES,
    subproducers=[
        ElectronEtaCut,
        ElectronDxyCut,
        ElectronDzCut,
        ElectronIsoCut,
        DiElectronVetoPtCut,
        DiElectronVetoIDCut,
    ],
)
DiElectronVeto = ProducerGroup(
    name="DiElectronVeto",
    call="physicsobject::LeptonPairVeto({df}, {output}, {input}, {dileptonveto_dR})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_phi,
        nanoAOD.Electron_mass,
        nanoAOD.Electron_charge,
    ],
    output=[q.dielectron_veto],
    scopes=GLOBAL_SCOPES,
    subproducers=[DiElectronVetoElectrons],
)
