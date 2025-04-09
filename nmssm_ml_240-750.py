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
                    "240",
                    "280",
                    "300",
                    "320",
                    "360",
                    "400",
                    "450",
                    "500",
                    "550",
                    "600",
                    "650",
                    "700",
                    "750",
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
                    ("240", "60"),
                    ("240", "70"),
                    ("240", "80"),
                    ("240", "90"),
                    ("240", "100"),
                    ("280", "60"),
                    ("280", "70"),
                    ("280", "80"),
                    ("280", "90"),
                    ("280", "100"),
                    ("280", "125"),
                    ("280", "150"),
                    ("300", "60"),
                    ("300", "70"),
                    ("300", "80"),
                    ("300", "90"),
                    ("300", "100"),
                    ("300", "125"),
                    ("300", "150"),
                    ("320", "60"),
                    ("320", "70"),
                    ("320", "80"),
                    ("320", "90"),
                    ("320", "100"),
                    ("320", "125"),
                    ("320", "150"),
                    ("360", "60"),
                    ("360", "70"),
                    ("360", "80"),
                    ("360", "90"),
                    ("360", "100"),
                    ("360", "125"),
                    ("360", "150"),
                    ("400", "60"),
                    ("400", "70"),
                    ("400", "80"),
                    ("400", "90"),
                    ("400", "100"),
                    ("400", "125"),
                    ("400", "150"),
                    ("400", "250"),
                    ("450", "60"),
                    ("450", "70"),
                    ("450", "80"),
                    ("450", "90"),
                    ("450", "100"),
                    ("450", "125"),
                    ("450", "150"),
                    ("450", "250"),
                    ("450", "300"),
                    ("500", "60"),
                    ("500", "70"),
                    ("500", "80"),
                    ("500", "90"),
                    ("500", "100"),
                    ("500", "125"),
                    ("500", "150"),
                    ("500", "250"),
                    ("500", "300"),
                    ("550", "60"),
                    ("550", "70"),
                    ("550", "80"),
                    ("550", "90"),
                    ("550", "100"),
                    ("550", "125"),
                    ("550", "150"),
                    ("550", "250"),
                    ("550", "300"),
                    ("550", "400"),
                    ("600", "60"),
                    ("600", "70"),
                    ("600", "80"),
                    ("600", "90"),
                    ("600", "100"),
                    ("600", "125"),
                    ("600", "150"),
                    ("600", "250"),
                    ("600", "300"),
                    ("600", "400"),
                    ("650", "60"),
                    ("650", "70"),
                    ("650", "80"),
                    ("650", "90"),
                    ("650", "100"),
                    ("650", "125"),
                    ("650", "150"),
                    ("650", "250"),
                    ("650", "300"),
                    ("650", "400"),
                    ("650", "500"),
                    ("700", "60"),
                    ("700", "70"),
                    ("700", "80"),
                    ("700", "90"),
                    ("700", "100"),
                    ("700", "125"),
                    ("700", "150"),
                    ("700", "250"),
                    ("700", "300"),
                    ("700", "400"),
                    ("700", "500"),
                    ("750", "60"),
                    ("750", "70"),
                    ("750", "80"),
                    ("750", "90"),
                    ("750", "100"),
                    ("750", "125"),
                    ("750", "150"),
                    ("750", "250"),
                    ("750", "300"),
                    ("750", "400"),
                    ("750", "500"),
                    ("750", "600"),
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
