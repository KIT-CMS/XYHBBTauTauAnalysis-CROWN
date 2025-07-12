"""
Producers for muon object selections and vetoes.
"""

from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ..constants import MT_SCOPES, MUON_SCOPES, GLOBAL_SCOPES


#
# OBJECT SELECTION
#


# loose muons (mainly used to evaluate veto masks)
BaseMuons = Producer(
    name="BaseMuons",
    call="xyh::object_selection::muon({df}, {output}, {input}, \"{loose_muon_id}\", {loose_muon_min_pt}, {loose_muon_max_abs_eta}, {loose_muon_max_abs_dxy}, {loose_muon_max_abs_dz}, {loose_muon_max_iso})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_dxy,
        nanoAOD.Muon_dz,
        nanoAOD.Muon_iso,
    ],
    output=[q.base_muons_mask],
    scopes=GLOBAL_SCOPES,
)

# tight muons (final state tau candidates)
GoodMuons = Producer(
    name="GoodMuons",
    call="xyh::object_selection::muon({df}, {output}, {input}, \"{tight_muon_id}\", {tight_muon_min_pt}, {tight_muon_max_abs_eta}, {tight_muon_max_abs_dxy}, {tight_muon_max_abs_dz}, {tight_muon_max_iso})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_dxy,
        nanoAOD.Muon_dz,
        nanoAOD.Muon_iso,
    ],
    output=[q.good_muons_mask],
    scopes=MUON_SCOPES,
)

# count number of selected muons
NumberOfGoodMuons = Producer(
    name="NumberOfGoodMuons",
    call="physicsobject::Count({df}, {output}, {input})",
    input=[q.good_muons_mask],
    output=[q.nmuons],
    scopes=MUON_SCOPES,
)


#
# EXTRA-MUON VETO
# TODO could be reworked
#


VetoMuons = Producer(
    name="VetoMuons",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {muon_index_in_pair})",
    input=[q.base_muons_mask, q.dileptonpair],
    output=[q.veto_muons_mask],
    scopes=MUON_SCOPES,
)
VetoMuons_boosted = Producer(
    name="VetoMuons_boosted",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {muon_index_in_pair})",
    input=[q.base_muons_mask, q.boosteddileptonpair],
    output=[q.veto_muons_boosted_mask],
    scopes=MUON_SCOPES,
)
VetoSecondMuon = Producer(
    name="VetoSecondMuon",
    call="physicsobject::VetoSingleObject({df}, {output}, {input}, {second_muon_index_in_pair})",
    input=[q.veto_muons_mask, q.dileptonpair],
    output=[q.veto_muons_mask_2],
    scopes=["mm"],
)
ExtraMuonsVeto = Producer(
    name="ExtraMuonsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "mm": [q.veto_muons_mask_2],
        "em": [q.veto_muons_mask],
        "et": [q.base_muons_mask],
        "mt": [q.veto_muons_mask],
        "tt": [q.base_muons_mask],
    },
    output=[q.muon_veto_flag],
    scopes=["em", "et", "mt", "tt", "mm"],
)
BoostedExtraMuonsVeto = Producer(
    name="BoostedExtraMuonsVeto",
    call="physicsobject::Veto({df}, {output}, {input})",
    input={
        "mt": [q.veto_muons_boosted_mask],
    },
    output=[q.boosted_muon_veto_flag],
    scopes=MT_SCOPES,
)


#
# DI-MUON VETO
# TODO could be reworked
#


DiMuonVetoPtCut = Producer(
    name="DiMuonVetoPtCut",
    call="physicsobject::CutMin<float>({df}, {output}, {input}, {min_dimuonveto_pt})",
    input=[nanoAOD.Muon_pt],
    output=[],
    scopes=GLOBAL_SCOPES,
)
DiMuonVetoIDCut = Producer(
    name="DiMuonVetoIDCut",
    call='physicsobject::CutEqual<bool>({df}, {output}, {input}, true)',
    input=[nanoAOD.Muon_id_loose],
    output=[],
    scopes=GLOBAL_SCOPES,
)
MuonEtaCut = Producer(
    name="MuonEtaCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_muon_max_abs_eta})",
    input=[nanoAOD.Muon_eta],
    output=[],
    scopes=GLOBAL_SCOPES,
)
MuonDxyCut = Producer(
    name="MuonDxyCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_muon_max_abs_dxy})",
    input=[nanoAOD.Muon_dxy],
    output=[],
    scopes=GLOBAL_SCOPES,
)
MuonDzCut = Producer(
    name="MuonDzCut",
    call="physicsobject::CutAbsMax<float>({df}, {output}, {input}, {loose_muon_max_abs_dz})",
    input=[nanoAOD.Muon_dz],
    output=[],
    scopes=GLOBAL_SCOPES,
)
MuonIsoCut = Producer(
    name="MuonIsoCut",
    call="physicsobject::CutMax<float>({df}, {output}, {input}, {loose_muon_max_iso})",
    input=[nanoAOD.Muon_iso],
    output=[],
    scopes=GLOBAL_SCOPES,
)
DiMuonVetoMuons = ProducerGroup(
    name="DiMuonVetoMuons",
    call='physicsobject::CombineMasks({df}, {output}, {input}, "all_of")',
    input=[],
    output=[],
    scopes=GLOBAL_SCOPES,
    subproducers=[
        MuonEtaCut,
        MuonDxyCut,
        MuonDzCut,
        MuonIsoCut,
        DiMuonVetoPtCut,
        DiMuonVetoIDCut,
    ],
)
DiMuonVeto = ProducerGroup(
    name="DiMuonVeto",
    call="physicsobject::LeptonPairVeto({df}, {output}, {input}, {dileptonveto_dR})",
    input=[
        nanoAOD.Muon_pt,
        nanoAOD.Muon_eta,
        nanoAOD.Muon_phi,
        nanoAOD.Muon_mass,
        nanoAOD.Muon_charge,
    ],
    output=[q.dimuon_veto],
    scopes=GLOBAL_SCOPES,
    subproducers=[DiMuonVetoMuons],
)
