from __future__ import annotations  # needed for type annotations in > python 3.7
from typing import List, Union
from .producers import pairquantities as pairquantities
from .producers import ml as ml
from .quantities import output as q
from code_generation.friend_trees import FriendTreeConfiguration
from code_generation.modifiers import EraModifier


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
    quantities_map: Union[str, None] = None,
):

    configuration = FriendTreeConfiguration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
        quantities_map,
    )

    # fake factor configurations
    configuration.add_config_parameters(
        ["mt"],
        {
            "masses_transformation_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/ml/nmssm/2018/mt_mass_transformation.json",
                }
            ),
            "model_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/ml/nmssm/2018/resolved_mt_best_pnn_EVTID.onnx",
                }
            ),
            "feature_transformation_file": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/ml/nmssm/2018/resolved_mt_feature_transformation_EVTID.json",
                }
            ),
            "model_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/ml/nmssm/2018/boosted_mt_best_pnn_EVTID.onnx",
                }
            ),
            "feature_transformation_file_boosted": EraModifier(
                {
                    "2016preVFP": "",
                    "2016postVFP": "",
                    "2017": "",
                    "2018": "payloads/ml/nmssm/2018/boosted_mt_feature_transformation_EVTID.json",
                }
            ),
            "massX_definitions": [
                {
                    "massX_value": massX,
                    "massX_output": "massX_{massX}".format(massX=massX),
                }
                for massX in [
                    "800",
                    "850",
                    "900",
                    "950",
                    "1000",
                    "1100",
                    "1200",
                    "1300",
                ]
            ],
            "massY_definitions": [
                {
                    "massY_value": massY,
                    "massY_output": "massY_{massY}".format(massY=massY),
                }
                for massY in [
                    "60",
                    "70",
                    "80",
                    "90",
                    "100",
                    "125",
                    "150",
                    "250",
                    "300",
                    "400",
                    "500",
                    "600",
                    "700",
                    "800",
                    "900",
                    "1000",
                    "1100",
                ]
            ],
            "pnn_mass_parameters": [
                {
                    "massX_parameter": massX,
                    "massY_parameter": massY,
                    "pnn_output_vector": "pnn_output_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                    "boosted_pnn_output_vector": "boosted_pnn_output_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                    "predicted_class": "max_index_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                    "predicted_max_value": "max_score_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                    "boosted_predicted_class": "boosted_max_index_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                    "boosted_predicted_max_value": "boosted_max_score_{massX}_{massY}".format(
                        massX=massX, massY=massY
                    ),
                }
                for massX, massY in [
                    ("800", "60"),
                    ("800", "70"),
                    ("800", "80"),
                    ("800", "90"),
                    ("800", "100"),
                    ("800", "125"),
                    ("800", "150"),
                    ("800", "250"),
                    ("800", "300"),
                    ("800", "400"),
                    ("800", "500"),
                    ("800", "600"),
                    ("850", "60"),
                    ("850", "70"),
                    ("850", "80"),
                    ("850", "90"),
                    ("850", "100"),
                    ("850", "125"),
                    ("850", "150"),
                    ("850", "250"),
                    ("850", "300"),
                    ("850", "400"),
                    ("850", "500"),
                    ("850", "600"),
                    ("850", "700"),
                    ("900", "60"),
                    ("900", "70"),
                    ("900", "80"),
                    ("900", "90"),
                    ("900", "100"),
                    ("900", "125"),
                    ("900", "150"),
                    ("900", "250"),
                    ("900", "300"),
                    ("900", "400"),
                    ("900", "500"),
                    ("900", "600"),
                    ("900", "700"),
                    ("950", "60"),
                    ("950", "70"),
                    ("950", "80"),
                    ("950", "90"),
                    ("950", "100"),
                    ("950", "125"),
                    ("950", "150"),
                    ("950", "250"),
                    ("950", "300"),
                    ("950", "400"),
                    ("950", "500"),
                    ("950", "600"),
                    ("950", "700"),
                    ("950", "800"),
                    ("1000", "60"),
                    ("1000", "70"),
                    ("1000", "80"),
                    ("1000", "90"),
                    ("1000", "100"),
                    ("1000", "125"),
                    ("1000", "150"),
                    ("1000", "250"),
                    ("1000", "300"),
                    ("1000", "400"),
                    ("1000", "500"),
                    ("1000", "600"),
                    ("1000", "700"),
                    ("1000", "800"),
                    ("1100", "60"),
                    ("1100", "70"),
                    ("1100", "80"),
                    ("1100", "90"),
                    ("1100", "100"),
                    ("1100", "125"),
                    ("1100", "150"),
                    ("1100", "250"),
                    ("1100", "300"),
                    ("1100", "400"),
                    ("1100", "500"),
                    ("1100", "600"),
                    ("1100", "700"),
                    ("1100", "800"),
                    ("1100", "900"),
                    ("1200", "60"),
                    ("1200", "70"),
                    ("1200", "80"),
                    ("1200", "90"),
                    ("1200", "100"),
                    ("1200", "125"),
                    ("1200", "150"),
                    ("1200", "250"),
                    ("1200", "300"),
                    ("1200", "400"),
                    ("1200", "500"),
                    ("1200", "600"),
                    ("1200", "700"),
                    ("1200", "800"),
                    ("1200", "900"),
                    ("1200", "1000"),
                    ("1300", "60"),
                    ("1300", "70"),
                    ("1300", "80"),
                    ("1300", "90"),
                    ("1300", "100"),
                    ("1300", "125"),
                    ("1300", "150"),
                    ("1300", "250"),
                    ("1300", "300"),
                    ("1300", "400"),
                    ("1300", "500"),
                    ("1300", "600"),
                    ("1300", "700"),
                    ("1300", "800"),
                    ("1300", "900"),
                    ("1300", "1000"),
                    ("1300", "1100"),
                ]
            ],
        },
    )

    configuration.add_producers(
        ["mt"],
        [
            ml.DefineMassXColumns,
            ml.DefineMassYColumns,
            ml.MTTransformVars,
            ml.BoostedMTTransformVars,
            # ml.Evaluate_PNN,
            # ml.Evaluate_PNN_boosted,
            ml.Evaluate_PNN_ORT,
            ml.Evaluate_PNN_ORT_boosted,
        ],
    )

    configuration.add_outputs(
        ["mt"],
        [
            # ml.Evaluate_PNN.output_group,
            # ml.Evaluate_PNN_boosted.output_group,
            ml.Evaluate_PNN_ORT.output_group,
            ml.Evaluate_PNN_ORT_boosted.output_group,
        ],
    )

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
