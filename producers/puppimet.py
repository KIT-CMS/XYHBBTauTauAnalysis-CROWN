from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

from ..constants import GLOBAL_SCOPES, SCOPES


#
# UNCORRECTED MET QUANTITIES
#

BuildMetVector_uncorrected = Producer(
    name="BuildMetVector_uncorrected",
    call="lorentzvector::BuildMET({df}, {output}, {input})",
    input=[
        nanoAOD.PuppiMET_pt,
        nanoAOD.PuppiMET_phi,
    ],
    output=[q.met_p4_uncorrected],
    scopes=GLOBAL_SCOPES,
)

MetCov00 = Producer(
    name="MetCov00",
    call="event::quantity::Rename<float>({df}, {output}, {input})",
    input=[
        nanoAOD.MET_covXX,
    ],
    output=[q.metcov00],
    scopes=GLOBAL_SCOPES,
)

MetCov01 = Producer(
    name="MetCov01",
    call="event::quantity::Rename<float>({df}, {output}, {input})",
    input=[
        nanoAOD.MET_covXY,
    ],
    output=[q.metcov01],
    scopes=GLOBAL_SCOPES,
)

MetCov10 = Producer(
    name="MetCov10",
    call="event::quantity::Rename<float>({df}, {output}, {input})",
    input=[
        nanoAOD.MET_covXY,
    ],
    output=[q.metcov10],
    scopes=GLOBAL_SCOPES,
)

MetCov11 = Producer(
    name="MetCov11",
    call="event::quantity::Rename<float>({df}, {output}, {input})",
    input=[
        nanoAOD.MET_covYY,
    ],
    output=[q.metcov11],
    scopes=GLOBAL_SCOPES,
)

MetSumEt = Producer(
    name="MetSumEt",
    call="event::quantity::Rename<float>({df}, {output}, {input})",
    input=[
        nanoAOD.PuppiMET_sumEt,
    ],
    output=[q.metSumEt],
    scopes=GLOBAL_SCOPES,
)

MetPt_uncorrected = Producer(
    name="MetPt_uncorrected",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.met_p4_uncorrected],
    output=[q.met_uncorrected],
    scopes=GLOBAL_SCOPES,
)

MetPhi_uncorrected = Producer(
    name="MetPhi_uncorrected",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.met_p4_uncorrected],
    output=[q.metphi_uncorrected],
    scopes=GLOBAL_SCOPES,
)

MetQuantitiesUncorrected = ProducerGroup(
    name="MetQuantitiesUncorrected",
    call=None,
    input=None,
    output=None,
    scopes=GLOBAL_SCOPES,
    subproducers=[
        BuildMetVector_uncorrected,
        MetPt_uncorrected,
        MetPhi_uncorrected,
        MetCov00,
        MetCov01,
        MetCov10,
        MetCov11,
        MetSumEt,
    ],
)


#
# RENAME PRODUCERS
#


# Dummy producer to rename the MET if no recoil corrections are applied to the sample
RenameMet = Producer(
    name="RenameMet",
    call="event::quantity::Rename<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input})",
    input=[q.met_p4_uncorrected],
    output=[q.met_p4_recoilcorrected],
    scopes=SCOPES,
)


#
# CORRECTED MET QUANTITIES
#


MetPt = Producer(
    name="MetPt",
    call="lorentzvector::GetPt({df}, {output}, {input})",
    input=[q.met_p4_recoilcorrected],
    output=[q.met],
    scopes=SCOPES,
)

MetPhi = Producer(
    name="MetPhi",
    call="lorentzvector::GetPhi({df}, {output}, {input})",
    input=[q.met_p4_recoilcorrected],
    output=[q.metphi],
    scopes=SCOPES,
)

MetQuantities = ProducerGroup(
    name="MetQuantities",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=[
        MetPt,
        MetPhi,
    ],
)
