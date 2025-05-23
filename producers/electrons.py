from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for loosest selection of electrons
####################

ElectronPtCorrectionEmbedding = Producer(
    name="ElectronPtCorrectionEmbedding",
    call='physicsobject::electron::PtCorrection({df}, correctionManager, {output}, {input}, "{ele_energyscale_barrel}", "{ele_energyscale_endcap}","{embedding_electron_es_sf_file}", "{ele_ES_json_name}")',
    input=[
        nanoAOD.Electron_pt,
        nanoAOD.Electron_eta,
    ],
    output=[q.Electron_pt_corrected],
    scopes=["global"],
)
ElectronPtCorrectionMC = Producer(
    name="ElectronPtCorrectionMC",
    call='physicsobject::electron::PtCorrectionMC({df}, correctionManager, {output}, {input}, {ele_es_era}, "{ele_es_variation}", {ele_es_file})',
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
    call="basefunctions::rename<ROOT::RVec<float>>({df}, {input}, {output})",
    input=[nanoAOD.Electron_pt],
    output=[q.Electron_pt_corrected],
    scopes=["global"],
)

ElectronPtCut = Producer(
    name="ElectronPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_ele_pt})",
    input=[q.Electron_pt_corrected],
    output=[],
    scopes=["global"],
)
ElectronEtaCut = Producer(
    name="ElectronEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_ele_eta})",
    input=[nanoAOD.Electron_eta],
    output=[],
    scopes=["global"],
)
ElectronDxyCut = Producer(
    name="ElectronDxyCut",
    call="physicsobject::CutDxy({df}, {input}, {output}, {max_ele_dxy})",
    input=[nanoAOD.Electron_dxy],
    output=[],
    scopes=["global"],
)
ElectronDzCut = Producer(
    name="ElectronDzCut",
    call="physicsobject::CutDz({df}, {input}, {output}, {max_ele_dz})",
    input=[nanoAOD.Electron_dz],
    output=[],
    scopes=["global"],
)
ElectronIDCut = Producer(
    name="ElectronIDCut",
    call='physicsobject::electron::CutID({df}, {output}, "{ele_id}")',
    input=[],
    output=[],
    scopes=["global"],
)
ElectronIsoCut = Producer(
    name="ElectronIsoCut",
    call="physicsobject::electron::CutIsolation({df}, {output}, {input}, {max_ele_iso})",
    input=[nanoAOD.Electron_iso],
    output=[],
    scopes=["global"],
)
BaseElectrons = ProducerGroup(
    name="BaseElectrons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[],
    output=[q.base_electrons_mask],
    scopes=["global"],
    subproducers=[
        ElectronPtCut,
        ElectronEtaCut,
        ElectronDxyCut,
        ElectronDzCut,
        ElectronIDCut,
        ElectronIsoCut,
    ],
)

####################
# Set of producers used for more specific selection of electrons in channels
####################

GoodElectronPtCut = Producer(
    name="GoodElectronPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_electron_pt})",
    input=[q.Electron_pt_corrected],
    output=[],
    scopes=["em", "et", "ee"],
)
GoodElectronEtaCut = Producer(
    name="GoodElectronEtaCut",
    call="physicsobject::CutEta({df}, {input}, {output}, {max_electron_eta})",
    input=[nanoAOD.Electron_eta],
    output=[],
    scopes=["em", "et", "ee"],
)
GoodElectronIsoCut = Producer(
    name="GoodElectronIsoCut",
    call="physicsobject::electron::CutIsolation({df}, {output}, {input}, {electron_iso_cut})",
    input=[nanoAOD.Electron_iso],
    output=[],
    scopes=["em", "et", "ee"],
)
GoodElectrons = ProducerGroup(
    name="GoodElectrons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
    input=[q.base_electrons_mask],
    output=[q.good_electrons_mask],
    scopes=["em", "et", "ee"],
    subproducers=[
        GoodElectronPtCut,
        GoodElectronEtaCut,
        GoodElectronIsoCut,
    ],
)

VetoElectrons = Producer(
    name="VetoElectrons",
    call="physicsobject::VetoCandInMask({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask],
    scopes=["em", "et", "ee"],
)
VetoElectrons_boosted = Producer(
    name="VetoElectrons_boosted",
    call="physicsobject::VetoCandInMask({df}, {output}, {input}, {electron_index_in_pair})",
    input=[q.base_electrons_mask, q.boosteddileptonpair],
    output=[q.veto_electrons_boosted_mask],
    scopes=["em", "et", "ee"],
)
VetoSecondElectron = Producer(
    name="VetoSecondElectron",
    call="physicsobject::VetoCandInMask({df}, {output}, {input}, {second_electron_index_in_pair})",
    input=[q.veto_electrons_mask, q.dileptonpair],
    output=[q.veto_electrons_mask_2],
    scopes=["ee"],
)
ExtraElectronsVeto = Producer(
    name="ExtraElectronsVeto",
    call="physicsobject::LeptonVetoFlag({df}, {output}, {input})",
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
    call="physicsobject::LeptonVetoFlag({df}, {output}, {input})",
    input={
        "et": [q.veto_electrons_boosted_mask],
    },
    output=[q.boosted_electron_veto_flag],
    scopes=["et"],
)
NumberOfGoodElectrons = Producer(
    name="NumberOfGoodElectrons",
    call="quantities::NumberOfGoodLeptons({df}, {output}, {input})",
    input=[q.good_electrons_mask],
    output=[q.nelectrons],
    scopes=["et", "em", "ee"],
)

####################
# Set of producers used for di-electron veto
####################

DiElectronVetoPtCut = Producer(
    name="DiElectronVetoPtCut",
    call="physicsobject::CutPt({df}, {input}, {output}, {min_dielectronveto_pt})",
    input=[q.Electron_pt_corrected],
    output=[],
    scopes=["global"],
)
DiElectronVetoIDCut = Producer(
    name="DiElectronVetoIDCut",
    call='v12::physicsobject::electron::CutCBID({df}, {output}, "{dielectronveto_id}", {dielectronveto_id_wp})',
    input=[],
    output=[],
    scopes=["global"],
)
DiElectronVetoElectrons = ProducerGroup(
    name="DiElectronVetoElectrons",
    call="physicsobject::CombineMasks({df}, {output}, {input})",
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
    call="physicsobject::CheckForDiLeptonPairs({df}, {output}, {input}, {dileptonveto_dR})",
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
