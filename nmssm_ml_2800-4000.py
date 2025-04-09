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
                    "2800",
                    "3000",
                    "3500",
                    "4000",
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
                    "1800",
                    "2000",
                    "2200",
                    "2400",
                    "2500",
                    "2600",
                    "2800",
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
                    ("2800", "60"),
                    ("2800", "70"),
                    ("2800", "80"),
                    ("2800", "90"),
                    ("2800", "100"),
                    ("2800", "125"),
                    ("2800", "150"),
                    ("2800", "250"),
                    ("2800", "300"),
                    ("2800", "400"),
                    ("2800", "500"),
                    ("2800", "600"),
                    ("2800", "700"),
                    ("2800", "800"),
                    ("2800", "900"),
                    ("2800", "1000"),
                    ("2800", "1100"),
                    ("2800", "1200"),
                    ("2800", "1300"),
                    ("2800", "1400"),
                    ("2800", "1600"),
                    ("2800", "1800"),
                    ("2800", "2000"),
                    ("2800", "2200"),
                    ("2800", "2400"),
                    ("2800", "2500"),
                    ("2800", "2600"),
                    ("3000", "60"),
                    ("3000", "70"),
                    ("3000", "80"),
                    ("3000", "90"),
                    ("3000", "100"),
                    ("3000", "125"),
                    ("3000", "150"),
                    ("3000", "250"),
                    ("3000", "300"),
                    ("3000", "400"),
                    ("3000", "500"),
                    ("3000", "600"),
                    ("3000", "700"),
                    ("3000", "800"),
                    ("3000", "900"),
                    ("3000", "1000"),
                    ("3000", "1100"),
                    ("3000", "1200"),
                    ("3000", "1300"),
                    ("3000", "1400"),
                    ("3000", "1600"),
                    ("3000", "1800"),
                    ("3000", "2000"),
                    ("3000", "2200"),
                    ("3000", "2400"),
                    ("3000", "2500"),
                    ("3000", "2600"),
                    # ("3000", "2800"), # Y(bb)H(tt) sample does not exist for this mass combination (yet)
                    ("3500", "60"),
                    ("3500", "70"),
                    ("3500", "80"),
                    ("3500", "90"),
                    ("3500", "100"),
                    ("3500", "125"),
                    ("3500", "150"),
                    ("3500", "250"),
                    ("3500", "300"),
                    ("3500", "400"),
                    ("3500", "500"),
                    ("3500", "600"),
                    ("3500", "700"),
                    ("3500", "800"),
                    ("3500", "900"),
                    ("3500", "1000"),
                    ("3500", "1100"),
                    ("3500", "1200"),
                    ("3500", "1300"),
                    ("3500", "1400"),
                    ("3500", "1600"),
                    ("3500", "1800"),
                    ("3500", "2000"),
                    ("3500", "2200"),
                    ("3500", "2400"),
                    ("3500", "2500"),
                    ("3500", "2600"),
                    ("3500", "2800"),
                    ("4000", "60"),
                    ("4000", "70"),
                    ("4000", "80"),
                    ("4000", "90"),
                    ("4000", "100"),
                    ("4000", "125"),
                    ("4000", "150"),
                    ("4000", "250"),
                    ("4000", "300"),
                    ("4000", "400"),
                    ("4000", "500"),
                    ("4000", "600"),
                    ("4000", "700"),
                    ("4000", "800"),
                    ("4000", "900"),
                    ("4000", "1000"),
                    ("4000", "1100"),
                    ("4000", "1200"),
                    ("4000", "1300"),
                    ("4000", "1400"),
                    ("4000", "1600"),
                    ("4000", "1800"),
                    ("4000", "2000"),
                    ("4000", "2200"),
                    ("4000", "2400"),
                    ("4000", "2500"),
                    ("4000", "2600"),
                    ("4000", "2800"),
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
