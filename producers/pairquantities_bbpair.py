from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup, ExtendedVectorProducer

####################
# Set of general producers for BBPair Quantities
####################

bpair_pt_1 = Producer(
    name="bpair_pt_1",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_pt_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_2 = Producer(
    name="bpair_pt_2",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_pt_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_1 = Producer(
    name="bpair_eta_1",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_eta_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_2 = Producer(
    name="bpair_eta_2",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_eta_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_1 = Producer(
    name="bpair_phi_1",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_phi_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_2 = Producer(
    name="bpair_phi_2",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.bpair_p4_2],
    output=[q.bpair_phi_2],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_1 = Producer(
    name="bpair_mass_1",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.bpair_p4_1],
    output=[q.bpair_mass_1],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_2 = Producer(
    name="bpair_mass_2",
    call="quantities::mass({df}, {output}, {input})",
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
    call="quantities::jet::bRegRes({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair],
    output=[q.bpair_reg_res_1],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_2 = Producer(
    name="bpair_bRegRes_2",
    call="quantities::jet::bRegRes({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair],
    output=[q.bpair_reg_res_2],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
p4_bpair = Producer(
    name="p4_bpair",
    call="lorentzvectors::CombineP4s({df}, {output}, {input})",
    input=[q.bpair_p4_1, q.bpair_p4_2],
    output=[q.p4_bpair],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
bpair_m_inv = Producer(
    name="bpair_m_inv",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.p4_bpair],
    output=[q.bpair_m_inv],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_dijet = Producer(
    name="bpair_pt_dijet",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.p4_bpair],
    output=[q.bpair_pt_dijet],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_deltaR = Producer(
    name="bpair_deltaR",
    call="quantities::deltaR({df}, {output}, {input})",
    input=[q.bpair_p4_1, q.bpair_p4_2],
    output=[q.bpair_deltaR],
    scopes=["mt", "et", "tt", "mm"],
)

UnrollBjetLV1 = ProducerGroup(
    name="UnrollBjetLV1",
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
UnrollBjetLV2 = ProducerGroup(
    name="UnrollBjetLV2",
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
DiBjetPairQuantities = ProducerGroup(
    name="DiBjetPairQuantities",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1,
        UnrollBjetLV2,
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
    call="quantities::pt({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_pt_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_2_boosted = Producer(
    name="bpair_pt_2_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_pt_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_1_boosted = Producer(
    name="bpair_eta_1_boosted",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_eta_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_eta_2_boosted = Producer(
    name="bpair_eta_2_boosted",
    call="quantities::eta({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_eta_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_1_boosted = Producer(
    name="bpair_phi_1_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_phi_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_phi_2_boosted = Producer(
    name="bpair_phi_2_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.bpair_p4_2_boosted],
    output=[q.bpair_phi_2_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_1_boosted = Producer(
    name="bpair_mass_1_boosted",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted],
    output=[q.bpair_mass_1_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_mass_2_boosted = Producer(
    name="bpair_mass_2_boosted",
    call="quantities::mass({df}, {output}, {input})",
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
    call="quantities::jet::bRegRes({df}, {output}, {input}, 0)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair_boosted],
    output=[q.bpair_reg_res_1_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
bpair_bRegRes_2_boosted = Producer(
    name="bpair_bRegRes_2_boosted",
    call="quantities::jet::bRegRes({df}, {output}, {input}, 1)",
    input=[nanoAOD.BJet_bRegRes, q.dibjetpair_boosted],
    output=[q.bpair_reg_res_2_boosted],
    scopes=["mt", "et", "tt", "em", "mm", "ee"],
)
p4_bpair_boosted = Producer(
    name="p4_bpair_boosted",
    call="lorentzvectors::CombineP4s({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted, q.bpair_p4_2_boosted],
    output=[q.p4_bpair_boosted],
    scopes=["mt", "et", "tt", "em", "ee", "mm"],
)
bpair_m_inv_boosted = Producer(
    name="bpair_m_inv_boosted",
    call="quantities::mass({df}, {output}, {input})",
    input=[q.p4_bpair_boosted],
    output=[q.bpair_m_inv_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_pt_dijet_boosted = Producer(
    name="bpair_pt_dijet_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.p4_bpair_boosted],
    output=[q.bpair_pt_dijet_boosted],
    scopes=["mt", "et", "tt", "mm"],
)
bpair_deltaR_boosted = Producer(
    name="bpair_deltaR_boosted",
    call="quantities::deltaR({df}, {output}, {input})",
    input=[q.bpair_p4_1_boosted, q.bpair_p4_2_boosted],
    output=[q.bpair_deltaR_boosted],
    scopes=["mt", "et", "tt", "mm"],
)

UnrollBjetLV1_boosted = ProducerGroup(
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
UnrollBjetLV2_boosted = ProducerGroup(
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

DiBjetPairQuantities_boosted = ProducerGroup(
    name="DiBjetPairQuantities_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["mt", "et", "tt", "mm"],
    subproducers=[
        UnrollBjetLV1_boosted,
        UnrollBjetLV2_boosted,
        p4_bpair_boosted,
        bpair_m_inv_boosted,
        bpair_pt_dijet_boosted,
        bpair_deltaR_boosted,
    ],
)
