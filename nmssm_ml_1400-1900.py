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
                    "1400",
                    "1500",
                    "1600",
                    "1700",
                    "1800",
                    "1900",
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
                    "1200",
                    "1300",
                    "1400",
                    "1600",
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
                    ("1400", "60"),
                    ("1400", "70"),
                    ("1400", "80"),
                    ("1400", "90"),
                    ("1400", "100"),
                    ("1400", "125"),
                    ("1400", "150"),
                    ("1400", "250"),
                    ("1400", "300"),
                    ("1400", "400"),
                    ("1400", "500"),
                    ("1400", "600"),
                    ("1400", "700"),
                    ("1400", "800"),
                    ("1400", "900"),
                    ("1400", "1000"),
                    ("1400", "1100"),
                    ("1400", "1200"),
                    ("1500", "60"),
                    ("1500", "70"),
                    ("1500", "80"),
                    ("1500", "90"),
                    ("1500", "100"),
                    ("1500", "125"),
                    ("1500", "150"),
                    ("1500", "250"),
                    ("1500", "300"),
                    ("1500", "400"),
                    ("1500", "500"),
                    ("1500", "600"),
                    ("1500", "700"),
                    ("1500", "800"),
                    ("1500", "900"),
                    ("1500", "1000"),
                    ("1500", "1100"),
                    ("1500", "1200"),
                    ("1500", "1300"),
                    ("1600", "60"),
                    ("1600", "70"),
                    ("1600", "80"),
                    ("1600", "90"),
                    ("1600", "100"),
                    ("1600", "125"),
                    ("1600", "150"),
                    ("1600", "250"),
                    ("1600", "300"),
                    ("1600", "400"),
                    ("1600", "500"),
                    ("1600", "600"),
                    ("1600", "700"),
                    ("1600", "800"),
                    ("1600", "900"),
                    ("1600", "1000"),
                    ("1600", "1100"),
                    ("1600", "1200"),
                    ("1600", "1300"),
                    ("1600", "1400"),
                    ("1700", "60"),
                    ("1700", "70"),
                    ("1700", "80"),
                    ("1700", "90"),
                    ("1700", "100"),
                    ("1700", "125"),
                    ("1700", "150"),
                    ("1700", "250"),
                    ("1700", "300"),
                    ("1700", "400"),
                    ("1700", "500"),
                    ("1700", "600"),
                    ("1700", "700"),
                    ("1700", "800"),
                    ("1700", "900"),
                    ("1700", "1000"),
                    ("1700", "1100"),
                    ("1700", "1200"),
                    ("1700", "1300"),
                    ("1700", "1400"),
                    ("1800", "60"),
                    ("1800", "70"),
                    ("1800", "80"),
                    ("1800", "90"),
                    ("1800", "100"),
                    ("1800", "125"),
                    ("1800", "150"),
                    ("1800", "250"),
                    ("1800", "300"),
                    ("1800", "400"),
                    ("1800", "500"),
                    ("1800", "600"),
                    ("1800", "700"),
                    ("1800", "800"),
                    ("1800", "900"),
                    ("1800", "1000"),
                    ("1800", "1100"),
                    ("1800", "1200"),
                    ("1800", "1300"),
                    ("1800", "1400"),
                    ("1800", "1600"),
                    ("1900", "60"),
                    ("1900", "70"),
                    ("1900", "80"),
                    ("1900", "90"),
                    ("1900", "100"),
                    ("1900", "125"),
                    ("1900", "150"),
                    ("1900", "250"),
                    ("1900", "300"),
                    ("1900", "400"),
                    ("1900", "500"),
                    ("1900", "600"),
                    ("1900", "700"),
                    ("1900", "800"),
                    ("1900", "900"),
                    ("1900", "1000"),
                    ("1900", "1100"),
                    ("1900", "1200"),
                    ("1900", "1300"),
                    ("1900", "1400"),
                    ("1900", "1600"),
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
