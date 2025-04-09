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
                    "2000",
                    "2200",
                    "2400",
                    "2500",
                    "2600",
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
                    ("2000", "60"),
                    ("2000", "70"),
                    ("2000", "80"),
                    ("2000", "90"),
                    ("2000", "100"),
                    ("2000", "125"),
                    ("2000", "150"),
                    ("2000", "250"),
                    ("2000", "300"),
                    ("2000", "400"),
                    ("2000", "500"),
                    ("2000", "600"),
                    ("2000", "700"),
                    ("2000", "800"),
                    ("2000", "900"),
                    ("2000", "1000"),
                    ("2000", "1100"),
                    ("2000", "1200"),
                    ("2000", "1300"),
                    ("2000", "1400"),
                    ("2000", "1600"),
                    ("2000", "1800"),
                    ("2200", "60"),
                    ("2200", "70"),
                    ("2200", "80"),
                    ("2200", "90"),
                    ("2200", "100"),
                    ("2200", "125"),
                    ("2200", "150"),
                    ("2200", "250"),
                    ("2200", "300"),
                    ("2200", "400"),
                    ("2200", "500"),
                    ("2200", "600"),
                    ("2200", "700"),
                    ("2200", "800"),
                    ("2200", "900"),
                    ("2200", "1000"),
                    ("2200", "1100"),
                    ("2200", "1200"),
                    ("2200", "1300"),
                    ("2200", "1400"),
                    ("2200", "1600"),
                    ("2200", "1800"),
                    ("2200", "2000"),
                    ("2400", "60"),
                    ("2400", "70"),
                    ("2400", "80"),
                    ("2400", "90"),
                    ("2400", "100"),
                    ("2400", "125"),
                    ("2400", "150"),
                    ("2400", "250"),
                    ("2400", "300"),
                    ("2400", "400"),
                    ("2400", "500"),
                    ("2400", "600"),
                    ("2400", "700"),
                    ("2400", "800"),
                    ("2400", "900"),
                    ("2400", "1000"),
                    ("2400", "1100"),
                    ("2400", "1200"),
                    ("2400", "1300"),
                    ("2400", "1400"),
                    ("2400", "1600"),
                    ("2400", "1800"),
                    ("2400", "2000"),
                    ("2400", "2200"),
                    ("2500", "60"),
                    ("2500", "70"),
                    ("2500", "80"),
                    ("2500", "90"),
                    ("2500", "100"),
                    ("2500", "125"),
                    ("2500", "150"),
                    ("2500", "250"),
                    ("2500", "300"),
                    ("2500", "400"),
                    ("2500", "500"),
                    ("2500", "600"),
                    ("2500", "700"),
                    ("2500", "800"),
                    ("2500", "900"),
                    ("2500", "1000"),
                    ("2500", "1100"),
                    ("2500", "1200"),
                    ("2500", "1300"),
                    ("2500", "1400"),
                    ("2500", "1600"),
                    ("2500", "1800"),
                    ("2500", "2000"),
                    ("2500", "2200"),
                    ("2600", "60"),
                    ("2600", "70"),
                    ("2600", "80"),
                    ("2600", "90"),
                    ("2600", "100"),
                    ("2600", "125"),
                    ("2600", "150"),
                    ("2600", "250"),
                    ("2600", "300"),
                    ("2600", "400"),
                    ("2600", "500"),
                    ("2600", "600"),
                    ("2600", "700"),
                    ("2600", "800"),
                    ("2600", "900"),
                    ("2600", "1000"),
                    ("2600", "1100"),
                    ("2600", "1200"),
                    ("2600", "1300"),
                    ("2600", "1400"),
                    ("2600", "1600"),
                    ("2600", "1800"),
                    ("2600", "2000"),
                    ("2600", "2200"),
                    ("2600", "2400"),
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
