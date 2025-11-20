"""
Constant definitions.
"""


__all__ = [
    "GLOBAL_SCOPES",
    "ET_SCOPES",
    "MT_SCOPES",
    "TT_SCOPES",
    "EM_SCOPES",
    "EE_SCOPES",
    "MM_SCOPES",
    "ELECTRON_SCOPES",
    "MUON_SCOPES",
    "SL_SCOPES",
    "FH_SCOPES",
    "FL_SCOPES",
    "HAD_TAU_SCOPES",
    "SCOPES",
    "ERAS",
]


# all scopes containing hadronic taus
GLOBAL_SCOPES = ["global"]
ET_SCOPES = ["et"]
MT_SCOPES = ["mt"]
TT_SCOPES = ["tt"]
EM_SCOPES = ["em"]
EE_SCOPES = ["ee"]
MM_SCOPES = ["mm"]
ELECTRON_SCOPES = ET_SCOPES + EM_SCOPES + EE_SCOPES
MUON_SCOPES = MT_SCOPES + EM_SCOPES + MM_SCOPES
SL_SCOPES = ET_SCOPES + MT_SCOPES
FH_SCOPES = TT_SCOPES
FL_SCOPES = EM_SCOPES + EE_SCOPES + MM_SCOPES
HAD_TAU_SCOPES = SL_SCOPES + FH_SCOPES
SCOPES = SL_SCOPES + FH_SCOPES + FL_SCOPES

# eras for Run 2 and Run 3
ERAS_RUN2 = ["2016preVFP", "2016postVFP", "2017", "2018"]
ERAS_RUN3 = ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]
ERAS = ERAS_RUN2 + ERAS_RUN3

# correctionlib campaigns
CORRECTIONLIB_CAMPAIGNS = {
    **{
        _era: f"{_era}_UL"
        for _era in ERAS_RUN2
    },
    "2022preEE": "2022_Summer22",
    "2022postEE": "2022_Summer22EE",
    "2023preBPix": "2023_Summer23",
    "2023postBPix": "2023_Summer23BPix",
}
