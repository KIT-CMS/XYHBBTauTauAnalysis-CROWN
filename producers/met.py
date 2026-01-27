from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from analysis_configurations.quantities import nanoAODv12_run3
from code_generation.producer import Producer, ProducerGroup

from ..constants import GLOBAL_SCOPES, SCOPES


#
# HELPER FUNCTIONS
#


def met_cov_producers(
    name: str,
    input_quantities: dict[str, str],
    output_quantities: dict[str, str],
    scopes: list[str],
):
    """
    Generic function that generates a producer group for MET covariance matrix
    elements.

    The `input_quantities` dictionary must contain the input `NANOAOD` columns:
    - `met_cov_xx`: The $xx$ component of the MET covariance matrix.
    - `met_cov_xy`: The $xy$ component of the MET covariance matrix.
    - `met_cov_yy`: The $yy$ component of the MET covariance matrix.

    The `output_quantities` dictionary must contain the output columns in the
    NTuple:

    - `met_cov_00`: The $xx$ component of the MET covariance matrix.
    - `met_cov_01`: The $xy$ component of the MET covariance matrix.
    - `met_cov_10`: The $xy$ component of the MET covariance matrix.
    - `met_cov_11`: The $yy$ component of the MET covariance matrix.
    """

    # Get the input and output quantities
    met_cov_xx = input_quantities["met_cov_xx"]
    met_cov_xy = input_quantities["met_cov_xy"]
    met_cov_yy = input_quantities["met_cov_yy"]
    met_cov_00 = output_quantities["met_cov_00"]
    met_cov_01 = output_quantities["met_cov_01"]
    met_cov_10 = output_quantities["met_cov_10"]
    met_cov_11 = output_quantities["met_cov_11"]

    # Create the MET covariance matrix producers
    producers = []
    for input, output, subproducer_name in [
        (met_cov_xx, met_cov_00, "Cov00"),
        (met_cov_xy, met_cov_01, "Cov01"),
        (met_cov_xy, met_cov_10, "Cov10"),
        (met_cov_yy, met_cov_11, "Cov11"),
    ]:
        producers.append(
            Producer(
                name=f"{name}_{subproducer_name}",
                call="event::quantity::Rename<float>({df}, {output}, {input})",
                input=[input],
                output=[output],
                scopes=scopes,
            )
        )

    # Create a producer group for the MET covariance matrix elements
    producer_group = ProducerGroup(
        name=name,
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=producers,
    )

    return producer_group


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

# PF MET covariance matrix elements (2016-2018 v9+v12, 2022-2023 v12)
MetCov = met_cov_producers(
    name="MetCov",
    input_quantities={
        "met_cov_xx": nanoAODv12_run3.MET_covXX,
        "met_cov_xy": nanoAODv12_run3.MET_covXX,
        "met_cov_yy": nanoAODv12_run3.MET_covYY,
    },
    output_quantities={
        "met_cov_00": q.metcov00,
        "met_cov_01": q.metcov01,
        "met_cov_10": q.metcov10,
        "met_cov_11": q.metcov11,
    },
    scopes=GLOBAL_SCOPES,
)

# PUPPI MET covariance matrix elements (2024 v15)
PuppiMetCov = met_cov_producers(
    name="PuppiMetCov",
    input_quantities={
        "met_cov_xx": nanoAOD.PuppiMET_covXX,
        "met_cov_xy": nanoAOD.PuppiMET_covXX,
        "met_cov_yy": nanoAOD.PuppiMET_covYY,
    },
    output_quantities={
        "met_cov_00": q.metcov00,
        "met_cov_01": q.metcov01,
        "met_cov_10": q.metcov10,
        "met_cov_11": q.metcov11,
    },
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
        MetCov,
        MetSumEt,
    ],
)


#
# PROPAGATION OF ENERGY SCALE CORRECTIONS AND RECOIL CORRECTIONS
#


# Correct MET for corrections in lepton energy scale
PropagateLeptonsToMET = Producer(
    name="PropagateLeptonsToMet",
    call="lorentzvector::PropagateToMET({df}, {output}, {input}, {propagate_leptons_to_met})",
    input=[q.met_p4_uncorrected, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
    output=[q.met_p4_leptoncorrected],
    scopes=SCOPES,
)

# Correct MET for corrections in jet energy scale
PropagateJetsToMET = Producer(
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
    output=[q.met_p4_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

# Recoil correction evaluation via correctionlib
RecoilCorrectionMET = Producer(
    name="RecoilCorrectionMET",
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

# Producer group to trigger production of all MET corrections
METCorrections = ProducerGroup(
    name="METCorrections",
    call=None,
    input=None,
    output=None,
    scopes=SCOPES,
    subproducers=[
        PropagateLeptonsToMET,
        PropagateJetsToMET,
        RecoilCorrectionMET,
    ],
)

#
# RENAME PRODUCERS
#


# Dummy producer to rename the MET if recoil corrections are applied to the
# sample
RenameMET = Producer(
    name="RenameMET",
    call="event::quantity::Rename<ROOT::Math::PtEtaPhiMVector>({df}, {output}, {input})",
    input=[q.met_p4_jetcorrected],
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

METQuantities = ProducerGroup(
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
