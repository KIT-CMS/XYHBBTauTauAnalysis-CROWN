from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of general producers for BBPair Quantities
####################

bpair_pt_1 = Producer(
    name="bpair_pt_1",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_pt_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_2 = Producer(
    name="bpair_pt_2",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_pt_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_1 = Producer(
    name="bpair_eta_1",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_eta_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_2 = Producer(
    name="bpair_eta_2",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_eta_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_1 = Producer(
    name="bpair_phi_1",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_phi_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_2 = Producer(
    name="bpair_phi_2",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_phi_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_1 = Producer(
    name="bpair_mass_1",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_mass_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_2 = Producer(
    name="bpair_mass_2",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_mass_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_btag_value_1 = Producer(
    name="bpair_btag_value_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_discriminator, q.dibjetpair],
    output=[q.bpair_btag_value_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_btag_value_2 = Producer(
    name="bpair_btag_value_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.dibjetpair],
    output=[q.bpair_btag_value_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_1 = Producer(
    name="bpair_bRegRes_1",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair],
    output=[q.bpair_reg_res_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_2 = Producer(
    name="bpair_bRegRes_2",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair],
    output=[q.bpair_reg_res_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
p4_bpair = Producer(
    name="p4_bpair",
    call="lorentzvector::Sum({df}, {output}, {input})",
    input=[q.bpair_p4_1, q.bpair_p4_2],
    output=[q.p4_bpair],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
bpair_m_inv = Producer(
    name="bpair_m_inv",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.p4_bpair],
    output=[q.bpair_m_inv],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_dijet = Producer(
    name="bpair_pt_dijet",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.p4_bpair],
    output=[q.bpair_pt_dijet],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_deltaR = Producer(
    name="bpair_deltaR",
    call="quantities::DeltaR({df}, {output}, {input})",
    input=[q.bpair_p4_1, q.bpair_p4_2],
    output=[q.bpair_deltaR],
    scopes=["mt", "et", "tt", "mm"],
)

UnrollBjetLV1Run2 = ProducerGroup(
    name="UnrollBjetLV1Run2",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_1,
        bpair_eta_1,
        bpair_phi_1,
        bpair_mass_1,
        bpair_btag_value_1,
        bpair_bRegRes_1,
    ],
)
UnrollBjetLV2Run2 = ProducerGroup(
    name="UnrollBjetLV2Run2",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_2,
        bpair_eta_2,
        bpair_phi_2,
        bpair_mass_2,
        bpair_btag_value_2,
        bpair_bRegRes_2,
    ],
)
UnrollBjetLV1Run3 = ProducerGroup(
    name="UnrollBjetLV1Run3",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_1,
        bpair_eta_1,
        bpair_phi_1,
        bpair_mass_1,
        bpair_btag_value_1,
    ],
)
UnrollBjetLV2Run3 = ProducerGroup(
    name="UnrollBjetLV2Run3",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_2,
        bpair_eta_2,
        bpair_phi_2,
        bpair_mass_2,
        bpair_btag_value_2,
    ],
)
DiBjetPairQuantitiesRun2 = ProducerGroup(
    name="DiBjetPairQuantitiesRun2",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1Run2,
        UnrollBjetLV2Run2,
        p4_bpair,
        bpair_m_inv,
        bpair_pt_dijet,
        bpair_deltaR,
    ],
)
DiBjetPairQuantitiesRun3 = ProducerGroup(
    name="DiBjetPairQuantitiesRun3",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1Run3,
        UnrollBjetLV2Run3,
        p4_bpair,
        bpair_m_inv,
        bpair_pt_dijet,
        bpair_deltaR,
    ],
)

####################
# Set of general producers for BBPair Quantities based on boosted tau pair
####################

bpair_pt_1_boosted = Producer(
    name="bpair_pt_1_boosted",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_pt_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_2_boosted = Producer(
    name="bpair_pt_2_boosted",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_pt_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_1_boosted = Producer(
    name="bpair_eta_1_boosted",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_eta_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_2_boosted = Producer(
    name="bpair_eta_2_boosted",
    call="lorentzvector::GetEta({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_eta_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_1_boosted = Producer(
    name="bpair_phi_1_boosted",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_phi_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_2_boosted = Producer(
    name="bpair_phi_2_boosted",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_phi_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_1_boosted = Producer(
    name="bpair_mass_1_boosted",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_mass_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_2_boosted = Producer(
    name="bpair_mass_2_boosted",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_mass_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_btag_value_1_boosted = Producer(
    name="bpair_btag_value_1_boosted",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_discriminator, q.dibjetpair_boosted],
    output=[q.bpair_btag_value_1_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_btag_value_2_boosted = Producer(
    name="bpair_btag_value_2_boosted",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_discriminator, q.dibjetpair_boosted],
    output=[q.bpair_btag_value_2_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_1_boosted = Producer(
    name="bpair_bRegRes_1_boosted",
    call="event::quantity::Get<float>({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair_boosted],
    output=[q.bpair_reg_res_1_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_2_boosted = Producer(
    name="bpair_bRegRes_2_boosted",
    call="event::quantity::Get<float>({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair_boosted],
    output=[q.bpair_reg_res_2_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
p4_bpair_boosted = Producer(
    name="p4_bpair_boosted",
    call="lorentzvector::Sum({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted, q.bpair_p4_2_boosted],
    output=[q.p4_bpair_boosted],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
bpair_m_inv_boosted = Producer(
    name="bpair_m_inv_boosted",
    call="lorentzvector::GetMass({df}, {output}, {input})",
    input=[q.p4_bpair_boosted],
    output=[q.bpair_m_inv_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_dijet_boosted = Producer(
    name="bpair_pt_dijet_boosted",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.p4_bpair_boosted],
    output=[q.bpair_pt_dijet_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_deltaR_boosted = Producer(
    name="bpair_deltaR_boosted",
    call="quantities::DeltaR({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted, q.bpair_p4_2_boosted],
    output=[q.bpair_deltaR_boosted],
    scopes=["mt", "et", "tt", "mm"],
)

UnrollBjetLV1Run2_boosted = ProducerGroup(
    name="UnrollBjetLV1_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_1_boosted,
        bpair_eta_1_boosted,
        bpair_phi_1_boosted,
        bpair_mass_1_boosted,
        bpair_btag_value_1_boosted,
        bpair_bRegRes_1_boosted,
    ],
)
UnrollBjetLV2Run2_boosted = ProducerGroup(
    name="UnrollBjetLV2_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_2_boosted,
        bpair_eta_2_boosted,
        bpair_phi_2_boosted,
        bpair_mass_2_boosted,
        bpair_btag_value_2_boosted,
        bpair_bRegRes_2_boosted,
    ],
)
UnrollBjetLV1Run3_boosted = ProducerGroup(
    name="UnrollBjetLV1_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_1_boosted,
        bpair_eta_1_boosted,
        bpair_phi_1_boosted,
        bpair_mass_1_boosted,
        bpair_btag_value_1_boosted,
    ],
)
UnrollBjetLV2Run3_boosted = ProducerGroup(
    name="UnrollBjetLV2_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "mm"],
    subproducers=[
        bpair_pt_2_boosted,
        bpair_eta_2_boosted,
        bpair_phi_2_boosted,
        bpair_mass_2_boosted,
        bpair_btag_value_2_boosted,
    ],
)

DiBjetPairQuantitiesRun2_boosted = ProducerGroup(
    name="DiBjetPairQuantities_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1Run2_boosted,
        UnrollBjetLV2Run2_boosted,
        p4_bpair_boosted,
        bpair_m_inv_boosted,
        bpair_pt_dijet_boosted,
        bpair_deltaR_boosted,
    ],
)

DiBjetPairQuantitiesRun3_boosted = ProducerGroup(
    name="DiBjetPairQuantities_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1Run3_boosted,
        UnrollBjetLV2Run3_boosted,
        p4_bpair_boosted,
        bpair_m_inv_boosted,
        bpair_pt_dijet_boosted,
        bpair_deltaR_boosted,
    ],
)