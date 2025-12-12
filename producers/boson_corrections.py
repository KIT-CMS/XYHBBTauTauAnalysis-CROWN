
from code_generation.producer import Producer, ProducerGroup
from ..quantities import output as q
from ..quantities import nanoAOD

from ..constants import GLOBAL_SCOPES, SCOPES


#
# GENERATOR BOSON QUANTITIES
#
# Needed as inputs for Z pt and recoil corrections
#

GenBosonP4 = Producer(
    name="GenBosonP4",
    call="genparticles::GetBoson({df}, {output}, {input}, {is_data})",
    input=[
        nanoAOD.GenPart_pt,
        nanoAOD.GenPart_eta,
        nanoAOD.GenPart_phi,
        nanoAOD.GenPart_mass,
        nanoAOD.GenPart_pdgId,
        nanoAOD.GenPart_status,
        nanoAOD.GenPart_statusFlags,
    ],
    output=[q.gen_boson_p4],
    scopes=GLOBAL_SCOPES,
)

GenBosonPt = Producer(
    name="GenBosonPt",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.gen_boson_p4],
    output=[q.gen_boson_pt],
    scopes=GLOBAL_SCOPES,
)

GenBosonQuantities = ProducerGroup(
    name="GenBosonQuantities",
    call=None,
    input=None,
    output=None,
    scopes=GLOBAL_SCOPES,
    subproducers=[GenBosonP4, GenBosonPt],
)

#
# Z PT REWEIGHTING
#

ZPtReweighting = Producer(
    name="ZPtReweighting",
    call=(
        """
        event::reweighting::ZPtWeight(
            {df},
            correctionManager,
            {output},
            {input},
            \"{zpt_weight_order}\",
            \"{zpt_weight_file}\",
            \"{zpt_weight_variation}\"
        )
        """
    ),
    input=[q.gen_boson_pt],
    output=[q.ZPtMassReweightWeight],
    scopes=SCOPES,
)


#
# RECOIL CORRECTIONS
#

BosonRecoilCorrection = Producer(
    name="BosonRecoilCorrection",
    call=(
        """
        met::applyRecoilCorrections(
            {df},
            correctionManager,
            {output},
            {input},
            \"{recoil_correction_file}\",
            \"{recoil_correction_order}\",
            \"{recoil_correction_variation}\",
            \"{recoil_correction_apply}\",
            \"{recoil_correction_is_wjets}\"
        )
        """
    ),
    input=[
        q.met_p4_uncorrected,
        q.gen_boson_p4,
        q.gen_vis_boson_p4,
        q.njets,
    ],
    output=[q.met_p4],
    scopes=SCOPES,
)
