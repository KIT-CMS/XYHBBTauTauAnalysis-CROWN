from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of electrons
####################

ElectronPtCorrectionEmbedding = Producer(
    name="ElectronPtCorrectionEmbedding",
    call='embedding::electron::PtCorrection({df}, correctionManager, {output}, {input}, "{embedding_electron_es_sf_file}", "{ele_ES_json_name}", "{ele_energyscale_barrel}", "{ele_energyscale_endcap}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
    ],
    output=[q.Electron_pt_corrected],
    scopes=["global"],
)
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
    scopes=["global"],
)

RenameElectronPt = Producer(
    name="RenameElectronPt",
    call="event::quantity::Rename<ROOT::RVec<float>>({df}, {output}, {input})",
    input=[nanoAOD.Electron_pt],
    output=[q.Electron_pt_corrected],
    scopes=["global"],
)
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
    scopes=["global"],
)
ElectronEtaCut = Producer(
    name="ElectronEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_eta})",
    input=[nanoAOD.Electron_eta],
    output=[],
    scopes=["global"],
)
ElectronDxyCut = Producer(
    name="ElectronDxyCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_dxy})",
    input=[nanoAOD.Electron_dxy],
    output=[],
    scopes=["global"],
)
ElectronDzCut = Producer(
    name="ElectronDzCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_electron_max_abs_dz})",
    input=[nanoAOD.Electron_dz],
    output=[],
    scopes=["global"],
)
ElectronIDCut = Producer(
    name="ElectronIDCut",
    call='physicsobject::CutEqual<bool>({df}, {output}, \"{loose_electron_id}\", true)',
    input=[],
    output=[],
    scopes=["global"],
)
ElectronIsoCut = Producer(
    name="ElectronIsoCut",
    call="physicsobject::CutMax<float>({df}, {output}, {input}, {loose_electron_iso})",
    input=[nanoAOD.Electron_iso],
    output=[],
    scopes=["global"],
)
GoodElectrons = Producer(
    name="GoodElectrons",
    call="xyh::object_selection::electron({df}, {output}, {input}, \"{tight_electron_id}\",  \"{tight_electron_id}\", {tight_electron_min_pt}, {tight_electron_max_abs_eta}, {tight_electron_max_abs_dxy}, {tight_electron_max_abs_dz}, {tight_electron_max_iso})",
    input=[
        q.Electron_pt_corrected,
        nanoAOD.Electron_eta,
        nanoAOD.Electron_dxy,
        nanoAOD.Electron_dz,
        nanoAOD.Electron_iso,
    ],
    output=[q.good_electrons_mask],
    scopes=["em", "et", "ee"],
)
VetoElectrons = Producer(
    name="VetoElectrons",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask],
    scopes=["em", "et", "ee"],
)
VetoElectrons_boosted = Producer(
    name="VetoElectrons_boosted",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.boosteddileptonpair],
    output=[q.veto_electrons_boosted_mask],
    scopes=["em", "et", "ee"],
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
    scopes=["em", "et", "mt", "tt", "mm", "ee"],
)
BoostedExtraElectronsVeto = Producer(
    name="BoostedExtraElectronsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "et": [q.veto_electrons_boosted_mask],
    },
    output=[q.boosted_electron_veto_flag],
    scopes=["et"],
)
NumberOfGoodElectrons = Producer(
    name="NumberOfGoodElectrons",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_electrons_mask],
    output=[q.nelectrons],
    scopes=["et", "em", "ee"],
)

####################
# Set of producers used for di-electron veto
####################

DiElectronVetoPtCut = Producer(
    name="DiElectronVetoPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_dielectronveto_pt})",
    input=[q.Electron_pt_corrected],
    output=[],
    scopes=["global"],
)
DiElectronVetoIDCut = Producer(
    name="DiElectronVetoIDCut",
    call='physicsobject::CutMin<UChar_t>({df}, {output}, {input}, {dielectronveto_id_wp})',
    input=[nanoAOD.Electron_cutBased],
    output=[],
    scopes=["global"],
)
DiElectronVetoElectrons = ProducerGroup(
    name="DiElectronVetoElectrons",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=ElectronEtaCut.output
    + ElectronDxyCut.output
    + ElectronDzCut.output
    + ElectronIsoCut.output,
    output=[],
    scopes=["global"],
    subproducers=[
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
    scopes=["global"],
    subproducers=[DiElectronVetoElectrons],
)
