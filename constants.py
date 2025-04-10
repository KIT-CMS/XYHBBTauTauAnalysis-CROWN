"""
Constant definitions.
"""


__all__ = [
    "GLOBAL_SCOPES",
    "ET_SCOPES",
    "MT_SCOPES",
    "TT_SCOPES",
    "SL_SCOPES",
    "FH_SCOPES",
    "HAD_TAU_SCOPES",
    "SCOPES",
    "ERAS",
]


# all scopes containing hadronic taus
GLOBAL_SCOPES = ["global"]
ET_SCOPES = ["et"]
MT_SCOPES = ["mt"]
TT_SCOPES = ["tt"]
SL_SCOPES = ET_SCOPES + MT_SCOPES
FH_SCOPES = TT_SCOPES
HAD_TAU_SCOPES = SL_SCOPES + FH_SCOPES
SCOPES = HAD_TAU_SCOPES

ERAS = ["2016preVFP", "2016postVFP", "2017", "2018"]
