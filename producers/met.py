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
# PROPAGATION OF ENERGY SCALE CORRECTIONS
#


PropagateLeptonsToMet = Producer(
    name="PropagateLeptonsToMet",
    call="lorentzvector::PropagateToMET({df}, {output}, {input}, {propagate_leptons_to_met})",
    input=[q.met_p4_uncorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
    output=[q.met_p4_leptoncorrected],
    scopes=SCOPES,
)

PropagateJetsToMet = Producer(
    name="PropagateJetsToMet",
    call="physicsobject::PropagateToMET({df}, {output}, {input}, {propagate_jets_to_met}, {jet_to_met_propagation_pt_min})",
    input=[
        q.met_p4_leptoncorrected,
        q.Jet_pt_corrected,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_mass,
    ],
    output=[q.pfmet_p4_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)


#
# RECOIL CORRECTIONS
#


# Recoil correction evaluation via correctionlib
BosonRecoilCorrection = Producer(
    name="BosonRecoilCorrection",
    call=(
        """
        met::RecoilCorrection(
            {df},
            correctionManager,
            {output},
            {input},
            \"{recoil_correction_file}\",
            \"{recoil_correction_name}\",
            \"{recoil_correction_method}\",
            \"{recoil_correction_order}\",
            \"{recoil_correction_variation}\",
            {apply_recoil_correction}
        )
        """
    ),
    input=[
        q.met_p4_jetcorrected,
        q.gen_boson_p4,
        q.gen_vis_boson_p4,
        q.n_jets,
    ],
    output=[q.met_p4_recoilcorrected],
    scopes=SCOPES,
)


#
# RENAME PRODUCERS
#


# Dummy producer to rename the MET if no lepton and recoil corrections are
# applied to the sample
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
