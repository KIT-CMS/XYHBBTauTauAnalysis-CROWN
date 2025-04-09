"""
Constant definitions.
"""


__all__ = [
    "GLOBAL_SCOPES",
    "SL_SCOPES",
    "FH_SCOPES",
    "HAD_TAU_SCOPES",
    "SCOPES",
    "ERAS",
]


# all scopes containing hadronic taus
GLOBAL_SCOPES = ["global"]
SL_SCOPES = ["et", "mt"]
FH_SCOPES = ["tt"]
HAD_TAU_SCOPES = SL_SCOPES + FH_SCOPES
SCOPES = HAD_TAU_SCOPES

ERAS = ["2016preVFP", "2016postVFP", "2017", "2018"]
