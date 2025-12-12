from __future__ import annotations  # needed for type annotations in > python 3.7

from typing import List

from .producers import electrons as electrons
from .producers import event as event
from .producers import genparticles as genparticles
from .producers import jets as jets
from .producers import fatjets as fatjets
from .producers import met as met
from .producers import muons as muons
from .producers import pairquantities as pairquantities
from .producers import boson_corrections as boson_corrections
from .producers import pairquantities_bbpair as pairquantities_bbpair
from .producers import pairselection as pairselection
from .producers import scalefactors as scalefactors
from .producers import taus as taus
from .producers import puppimet as puppimet
from .producers import triggers as triggers
from .quantities import nanoAOD, nanoAOD_run2
from .quantities import output as q
from .tau_triggersetup import add_diTauTriggerSetup
from .tau_variations import add_tauVariations
from .jet_variations import add_jetVariations
from .tau_embedding_settings import setup_embedding
from .btag_variations import add_btagVariations
# from .jec_data import add_jetCorrectionData
from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier, SampleModifier
from code_generation.rules import AppendProducer, RemoveProducer, ReplaceProducer
from code_generation.systematics import SystematicShift, SystematicShiftByQuantity

from .constants import ERAS_RUN2, ERAS_RUN3, CORRECTIONLIB_CAMPAIGNS, ET_SCOPES, MT_SCOPES, TT_SCOPES, EE_SCOPES, MM_SCOPES, EM_SCOPES, SL_SCOPES, FH_SCOPES, HAD_TAU_SCOPES, ELECTRON_SCOPES, MUON_SCOPES, SCOPES, GLOBAL_SCOPES
from .helpers import get_for_era


def add_noise_filters_config(configuration: Configuration):
    """
    List of all noise filters to be applied.

    The following recommendations are implemented:

    - Run 2 UltraLegacy: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#UL_data

    - 2022: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC

    - 2023: https://twiki.cern.ch/twiki/bin/viewauth/CMS/MissingETOptionalFiltersRun2#Run_3_2022_and_2023_data_and_MC

    :todo add 2022 and 2023:

    :param configuration: the main configuration object
    :type configuration: Configuration
    """

    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "met_filters": EraModifier(
                {
                    "2016preVFP": [
                        "Flag_goodVertices"
                        "Flag_globalSuperTightHalo2016Filter"
                        "Flag_HBHENoiseFilter"
                        "Flag_HBHENoiseIsoFilter"
                        "Flag_EcalDeadCellTriggerPrimitiveFilter"
                        "Flag_BadPFMuonFilter"
                        "Flag_BadPFMuonDzFilter"
                        "Flag_eeBadScFilter",
                    ],
                    "2016postVFP": [
                        "Flag_goodVertices"
                        "Flag_globalSuperTightHalo2016Filter"
                        "Flag_HBHENoiseFilter"
                        "Flag_HBHENoiseIsoFilter"
                        "Flag_EcalDeadCellTriggerPrimitiveFilter"
                        "Flag_BadPFMuonFilter"
                        "Flag_BadPFMuonDzFilter"
                        "Flag_eeBadScFilter",
                    ],
                    "2017": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2018": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_HBHENoiseFilter",
                        "Flag_HBHENoiseIsoFilter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",
                    ],
                    "2022preEE": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_hfNoisyHitsFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",  # marked as "yellow" in TWiki
                    ],
                    "2022postEE": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_hfNoisyHitsFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",  # marked as "yellow" in TWiki
                    ],
                    "2023preBPix": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_hfNoisyHitsFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",  # marked as "yellow" in TWiki
                    ],
                    "2023postBPix": [
                        "Flag_goodVertices",
                        "Flag_globalSuperTightHalo2016Filter",
                        "Flag_EcalDeadCellTriggerPrimitiveFilter",
                        "Flag_BadPFMuonFilter",
                        "Flag_BadPFMuonDzFilter",
                        "Flag_hfNoisyHitsFilter",
                        "Flag_eeBadScFilter",
                        "Flag_ecalBadCalibFilter",  # marked as "yellow" in TWiki
                    ],
                },
            ),
        },
    )


def add_pileup_reweighting_config(configuration: Configuration):
    """
    Filepaths for pileup reweighting corrections, and additional settings for the producers.

    The files with the correction are obtained from the
    [nanoaod-tools/jsonpog-integration](https://gitlab.cern.ch/nanoaod-tools/jsonpog-integration)
    repository.

    - 2016-2018 and 2022-2023: https://twiki.cern.ch/twiki/bin/view/CMS/PileupJSONFileforData#Centrally_produced_correctionlib

    - 2022-2023: https://twiki.cern.ch/twiki/bin/view/CMS/LumiRecommendationsRun3

    The documentation of the `correctionlib` files can be found here:

    | Era          | Documentation                                                                                          |
    |--------------|--------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2016preVFP_UL_puWeights.html   |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2016postVFP_UL_puWeights.html  |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2017_UL_puWeights.html         |
    | 2018         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2018_UL_puWeights.html         |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2022_Summer22_puWeights.html   |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2022_Summer22EE_puWeights.html |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2023_Summer23_puWeights.html   |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/LUM_2023_Summer23_puWeights.html   |

    :param configuration: the main configuration object
    :type configuration: Configuration
    """
    # pileup reweighting
    configuration.add_config_parameters(
        "global",
        {

            "PU_reweighting_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2016preVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2016postVFP-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2017-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run2-2017-UL-NanoAODv9/2021-09-10/puWeights.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22CDSep23-Summer22-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23CSep23-Summer23-NanoAODv12/2024-01-31/puWeights.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/LUM/Run3-23DSep23-Summer23BPix-NanoAODv12/2024-01-31/puWeights.json.gz",
                },
            ),
            "PU_reweighting_era": EraModifier(
                {
                    "2016preVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2016postVFP": "Collisions16_UltraLegacy_goldenJSON",
                    "2017": "Collisions17_UltraLegacy_goldenJSON",
                    "2018": "Collisions18_UltraLegacy_goldenJSON",
                    "2022preEE": "Collisions2022_355100_357900_eraBCD_GoldenJson",
                    "2022postEE": "Collisions2022_359022_362760_eraEFG_GoldenJson",
                    "2023preBPix": "Collisions2023_366403_369802_eraBC_GoldenJson",
                    "2023postBPix": "Collisions2023_369803_370790_eraD_GoldenJson",
                }
            ),
            "PU_reweighting_variation": "nominal",
        },
    )


def add_mur_muf_weights_config(configuration: Configuration):
    """
    Variations of the weights for renormalization and factorization scale.

    For the nominal samples, the nominal generator weights are applied.
    For the up (down) shift of the scales, the weights corresponding to the
    doubled or the halved value of the corresponding scale are applied.

    :param configuration: the main configuration object
    :type configuration: Configuration
    """
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "muR": 1.0,
            "muF": 1.0,
        },
    )


def add_golden_json_config(configuration: Configuration):
    """
    Filepaths to the `GoldenJSON` files to select certified data events.

    - 2022: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Year_2022

    - 2023: https://twiki.cern.ch/twiki/bin/view/CMS/PdmVRun3Analysis#Year_2023

    :param configuration: the main configuration object
    :type configuration: Configuration
    """
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "golden_json_file": EraModifier(
                {
                    "2016preVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2016postVFP": "data/golden_json/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt",
                    "2017": "data/golden_json/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt",
                    "2018": "data/golden_json/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt",
                    "2022preEE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    "2022postEE": "data/golden_json/Cert_Collisions2022_355100_362760_Golden.json",
                    "2023preBPix": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                    "2023postBPix": "data/golden_json/Cert_Collisions2023_366442_370790_Golden.json",
                }
            ),
        },
    )


def add_electron_config(configuration: Configuration):
    """
    Selection requirements and corrections for electrons.

    The corrections include scale factors for reconstruction and identification
    efficiencies at the working points used for electrons in this analysis. Separate corrections to
    electrons in $\mu \to \tau$-embedded events are defined as well.

    This function adds configuration parameters for two types of muon collections:

    - The loose collection contains electrons selected with loose requirements. They are mainly used to
      veto additional electrons in events and to remove electron-jet overlaps.

    - The tight collection contains electrons that are candidates for electron+hadronic tau pairs.

    The tight collection is a subset of the loose collection.

    The following recommendations and corrections are implemented:

    - [EGamma UL 2016-2018](https://twiki.cern.ch/twiki/bin/view/CMS/EgammaUL2016To2018)

    - [EGamma Run 2 recommendations](https://twiki.cern.ch/twiki/bin/view/CMS/EgammaRunIIRecommendations)

    - [EGamma Run 3 recommendations](https://twiki.cern.ch/twiki/bin/view/CMS/EgammaRunIIIRecommendations)

    Correction factors are obtained from the
    [nanoaod-tools/jsonpog-integration](gitlab.cern.ch/nanoaod-tools/jsonpog-integration) repository.

    The `correctionlib` documentation can be found here:

    - https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2023_Summer23_electron.html

    :todo add 2022 and 2023:

    The documentation of the electron reconstruction and identification corrections can be found here:

    | Era          | Documentation                                                                                           |
    |--------------|---------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2016preVFP_UL_electron.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2016postVFP_UL_electron.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2017_UL_electron.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2018_UL_electron.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2022_Summer22_electron.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2022_Summer22EE_electron.html   |
    | 2022preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2023_Summer23_electron.html     |
    | 2022postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/EGM_2023_Summer23BPix_electron.html |

    :param configuration: the main configuration object
    :type configuration: Configuration

    :param electron_id_loose: name of the electron ID for the loose electron collection; default: `"Electron_mvaNoIso_WP90"`.
    :type electron_id_loose: str

    :param electron_id_loose_corrlib: name of the electron ID for the loose electron collection in the EGM correctionlib file; default: `"wp90noiso"`.
    :type electron_id_loose: str
    """

    # Loose electrons, mainly used for vetoes
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "loose_electron_min_pt": 10.0,
            "loose_electron_max_abs_eta": 2.5,
            "loose_electron_max_abs_dxy": 0.045,
            "loose_electron_max_abs_dz": 0.2,
            "loose_electron_max_iso": 0.25,
            "loose_electron_id": "Electron_mvaNoIso_WP90",  # NanoAOD v9: Electron_mvaFall17V2noIso_WP90
        },
    )

    # Loose electrons and spatial separation for the di-electron veto
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "diele_electron_min_pt": 15.0,
            "diele_electron_max_abs_eta": 2.5,
            "diele_electron_max_abs_dxy": 0.045,
            "diele_electron_max_abs_dz": 0.2,
            "diele_electron_max_iso": 0.25,
            "diele_electron_id_wp": 1,  # cut-based electron ID, 'veto' working point
            "diele_electron_min_delta_r": 0.15,  # cut-based electron ID, 'veto' working point
        },
    )

    # Tight electrons, mainly used as candidates for dilepton pairs
    configuration.add_config_parameters(
        ELECTRON_SCOPES,
        {
            "tight_electron_min_pt": 25.0,
            "tight_electron_max_abs_eta": 2.5,
            "tight_electron_max_abs_dxy": 0.045,
            "tight_electron_max_abs_dz": 0.2,
            "tight_electron_max_iso": 0.4,
            "tight_electron_id": "Electron_mvaNoIso_WP90",  # NanoAOD v9: Electron_mvaFall17V2noIso_WP90,
        },
    )

    # In the et and em scopes, the first lepton is an electron
    configuration.add_config_parameters(
        ET_SCOPES + EM_SCOPES,
        {
            "electron_index_in_pair": 0,
        },
    )

    # In the ee scope, the first and the second leptons are electrons
    configuration.add_config_parameters(
        EE_SCOPES,
        {
            "electron_index_in_pair": 0,
            "second_electron_index_in_pair": 1,
        },
    )

    # Electron reconstruction and identification corrections for simulated events
    configuration.add_config_parameters(
        ELECTRON_SCOPES,
        {
            "ele_sf_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2016preVFP-UL-NanoAODv9/2024-07-02/electron.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2016postVFP-UL-NanoAODv9/2024-07-02/electron.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2017-UL-NanoAODv9/2024-07-02/electron.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run2-2018-UL-NanoAODv9/2024-07-02/electron.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electron.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electron.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electron.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electron.json.gz",
                },
            ),
            "ele_sf_cset_name": EraModifier(
                {
                    **{
                        _era: "UL-Electron-ID-SF"
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: "Electron-ID-SF"
                        for _era in ERAS_RUN3
                    }
                }
            ),
            "ele_sf_year_id": EraModifier(
                {
                    **{
                        _era: _era
                        for _era in ERAS_RUN2
                    },
                    "2022preEE": "2022Re-recoBCD",
                    "2022postEE": "2022Re-recoE+PromptFG",
                    "2023preBPix": "2023PromptC",
                    "2023postBPix": "2023PromptD",
                }
            ),
            "ele_reco_sf_name": "RecoAbove20",  # TODO needs to be modified for 2022 and 2023
            "ele_id_sf_name": "wp90noiso",
            "ele_reco_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
            "ele_id_sf_variation": "sf",  # "sf" is nominal, "sfup"/"sfdown" are up/down variations
        },
    )

    # Electron identification and isolation corrections for mu -> tau-embedded events
    configuration.add_config_parameters(
        ELECTRON_SCOPES,
        {
            "mc_electron_sf_file": EraModifier(
                {
                    "2016preVFP": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2016postVFP": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2017": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2018": "data/embedding/electron_2018UL.json.gz",
                    "2022preEE": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2022postEE": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2023preBPix": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2023postBPix": "DOES_NOT_EXIST",  # TODO to be added when available
                },
            ),
            "mc_electron_id_sf": "ID90_pt_eta_bins",
            "mc_electron_iso_sf": "Iso_pt_eta_bins",
            "mc_electron_id_extrapolation": 1.0,  # for nominal case
            "mc_electron_iso_extrapolation": 1.0,  # for nominal case
        },
    )


def add_muon_config(configuration: Configuration):
    """
    Selection requirements and corrections for muons.

    The corrections include scale factors for reconstruction, identification, and isolation
    efficiencies at the working points used for muons in this analysis. Separate corrections to
    muons in $\mu \to \tau$-embedded events are defined as well.

    This function adds configuration parameters for two types of muon collections:

    - The loose collection contains muons selected with loose requirements. They are mainly used to
      veto additional muons in events and to remove muon-jet overlaps.

    - The tight collection contains muons that are candidates for muon+hadronic tau pairs.

    The tight collection is a subset of the loose collection.

    The following recommendations for medium-$p_{\mathrm{T}}$ muons and corrections are implemented:

    - [Muon Recommendations For Analysis](https://muon-wiki.docs.cern.ch/guidelines/recommendations/)

    - [Muon correction recommendations](https://muon-wiki.docs.cern.ch/guidelines/corrections/)

    The relative isolation of the muon has the following working points:

    | ``PFIsoVeryLoose``     | 0.4  |                     |
    | ``PFIsoLoose``         | 0.25 | use for loose muons |
    | ``PFIsoMedium``        | 0.20 |                     |
    | ``PFIsoTight``         | 0.15 | use for tight muons |
    | ``PFIsoVeryTight``     | 0.10 |                     |
    | ``PFIsoVeryVeryTight`` | 0.05 |                     |

    Correction factors are obtained from the
    [nanoaod-tools/jsonpog-integration](gitlab.cern.ch/nanoaod-tools/jsonpog-integration) repository.

    The documentation of the muon reconstruction, identification, and isolation corrections can be found here:

    | Era          | Documentation                                                                                         |
    |--------------|-------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2016preVFP_UL_muon_Z.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2016postVFP_UL_muon_Z.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2017_UL_muon_Z.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2018_UL_muon_Z.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2022_Summer22_muon_Z.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2022_Summer22EE_muon_Z.html   |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2023_Summer23_muon_Z.html     |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/MUO_2023_Summer23BPix_muon_Z.html |

    :param configuration: the main configuration object
    :type configuration: Configuration
    """

    # Loose muons, mainly used for vetoes
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "loose_muon_min_pt": 10.0,
            "loose_muon_max_abs_eta": 2.4,
            "loose_muon_max_abs_dxy": 0.045,
            "loose_muon_max_abs_dz": 0.2,
            "loose_muon_max_iso": 0.25,
            "loose_muon_id": "Muon_mediumId",
        },
    )

    # Loose muons and spatial separation for the di-muon veto
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "dimu_muon_min_pt": 15.0,
            "dimu_muon_max_abs_eta": 2.4,
            "dimu_muon_max_abs_dxy": 0.045,
            "dimu_muon_max_abs_dz": 0.2,
            "dimu_muon_max_iso": 0.25,
            "dimu_muon_min_delta_r": 0.15,
        },
    )

    # Tight muons, mainly used as candidates for dileptons pairs
    configuration.add_config_parameters(
        MUON_SCOPES,
        {
            "tight_muon_min_pt": 20.0,
            "tight_muon_max_abs_eta": 2.4,
            "tight_muon_max_abs_dxy": 0.045,
            "tight_muon_max_abs_dz": 0.2,
            "tight_muon_max_iso": 0.4,
            "tight_muon_id": "Muon_mediumId",
            "muon_index_in_pair": 0,
        },
    )

    # In the mt scope, the first lepton is a muon
    configuration.add_config_parameters(
        MT_SCOPES,
        {
            "muon_index_in_pair": 0,
        },
    )

    # In the em scope, the first lepton is a muon
    configuration.add_config_parameters(
        EM_SCOPES,
        {
            "muon_index_in_pair": 1,
        },
    )

    # In the mm scope, the first and the second leptons are muons 
    configuration.add_config_parameters(
        MM_SCOPES,
        {
            "muon_index_in_pair": 0,
            "second_muon_index_in_pair": 1,
        },
    )

    # Muon reconstruction, identification, and isolation corrections for simulated events
    configuration.add_config_parameters(
        MUON_SCOPES,
        {
            "muon_sf_file": EraModifier(
                {
                    **{
                        _era: f"data/jsonpog-integration/POG/MUO/{_campaign}/muon_Z.json.gz"
                        for _era, _campaign in CORRECTIONLIB_CAMPAIGNS.items()
                        if _era in ERAS_RUN2
                    },
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2016preVFP-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2016postVFP-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2017-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run2-2018-UL-NanoAODv9/2024-07-02/muon_Z.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-14/muon_Z.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-14/muon_Z.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23CSep23-Summer23-NanoAODv12/2025-08-14/muon_Z.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/MUO/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-14/muon_Z.json.gz",
                },
            ),
            "muon_reco_sf_name": EraModifier(
                {
                    **{
                       _era: "NUM_TrackerMuons_DEN_genTracks"
                       for _era in ERAS_RUN2
                    },
                    **{
                        _era: "DOES_NOT_EXIST"  # reconstruction corrections not recommended for 2022+2023
                        for _era in ERAS_RUN3
                    }
                }
            ),
            "muon_id_sf_name": "NUM_MediumID_DEN_TrackerMuons",  # correction for mediumId WP
            "muon_iso_sf_name": "NUM_TightPFIso_DEN_MediumID",  # correction for TightPFIso WP (PF isolation < 0.15)
            "muon_reco_sf_variation": "nominal",  # "nominal" is nominal, "systup"/"systdown" are up/down variations
            "muon_id_sf_variation": "nominal",  # "nominal" is nominal, "systup"/"systdown" are up/down variations
            "muon_iso_sf_variation": "nominal",  # "nominal" is nominal, "systup"/"systdown" are up/down variations
        },
    )

    # Muon identification and isolation corrections for mu -> tau-embedded events
    configuration.add_config_parameters(
        MUON_SCOPES,
        {
            "mc_muon_sf_file": EraModifier(
                {
                    "2016preVFP": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2016postVFP": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2017": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2018": "data/embedding/muon_2018UL.json.gz",
                    "2022preEE": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2022postEE": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2023preBPix": "DOES_NOT_EXIST",  # TODO to be added when available
                    "2023postBPix": "DOES_NOT_EXIST",  # TODO to be added when available
                }
            ),
            "mc_muon_id_sf": "ID_pt_eta_bins",
            "mc_muon_iso_sf": "Iso_pt_eta_bins",
            "mc_muon_id_extrapolation": 1.0,  # for nominal case
            "mc_muon_iso_extrapolation": 1.0,  # for nominal case
        },
    )


def add_hadronic_tau_config(configuration: Configuration, era: str):
    """
    Selection requirements and corrections for hadronic taus.

    The corrections include scale factors for identification efficiencies and corrections of the
    energy scale of the hadronic taus at the working points used for hadronic taus in this analysis.
    Separate corrections to hadronic taus in $\mu \to \tau$-embedded events are defined as well.

    This function adds configuration parameters for two types of muon collections:

    - The loose collection contains muons selected with loose requirements. They are mainly used to
      veto additional muons in events and to remove muon-jet overlaps.

    - The tight collection contains muons that are candidates for muon+hadronic tau pairs.

    The tight collection is a subset of the loose collection.

    The following recommendations for medium-$p_{\mathrm{T}}$ muons and corrections are implemented:

    - [Muon Recommendations For Analysis](https://muon-wiki.docs.cern.ch/guidelines/recommendations/)

    - [Muon correction recommendations](https://muon-wiki.docs.cern.ch/guidelines/corrections/)

    Correction factors are obtained from the
    [nanoaod-tools/jsonpog-integration](gitlab.cern.ch/nanoaod-tools/jsonpog-integration) repository.

    The documentation of the tau identification corrections can be found here:

    | Era          | Documentation                                                                                      |
    |--------------|----------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2016preVFP_UL_tau.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2016postVFP_UL_tau.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2017_UL_tau.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2018_UL_tau.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2022_Summer22_tau.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2022_Summer22EE_tau.html   |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2023_Summer23_tau.html     |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/TAU_2023_Summer23BPix_tau.html |

    :param configuration: the main configuration object
    :type configuration: Configuration

    :param muon_id_loose: name of the muon ID for the loose muon collection; default: `"Muon_mediumId"`.
    :type muon_id_loose: str

    :param muon_id_loose_corrlib: name of the muon ID for the loose muon collection in the MUO correctionlib file; default: `""`.
    :type muon_id_loose: str
    """

    # define the tau identification algorithm to use
    tau_id = EraModifier(
        {
            **{
                _era: "DeepTau2017v2p1"
                for _era in ERAS_RUN2
            },
            **{
                _era: "DeepTau2018v2p5"
                for _era in ERAS_RUN3
            },
        }
    )

    # hadronic tau selection in semileptonic channels
    configuration.add_config_parameters(
        SL_SCOPES,
        {
            "tight_tau_min_pt": 20.0,
            "tight_tau_max_abs_eta": 2.5,
            "tight_tau_max_abs_dz": 0.2,
            "tight_tau_decay_modes": "0, 1, 10, 11",  # needs to be converted in a C++ vector in the code, so set it as string here
            "tight_tau_id_vs_jet_wp": 1,              # VVVLoose working point, looser taus needed for tau misidentification estimate
            "tight_tau_id_vs_electron_wp": 1,         # VVVLoose working point, looser taus needed for tau misidentification estimate
            "tight_tau_id_vs_muon_wp": 1,             # VLoose working point, looser taus needed for tau misidentification estimate
        },
    )
    # hadronic tau selection in fullhadronic channels
    configuration.add_config_parameters(
        FH_SCOPES,
        {
            "tight_tau_min_pt": 20.0,
            "tight_tau_max_abs_eta": 2.5,
            "tight_tau_max_abs_dz": 0.2,
            "tight_tau_decay_modes": "0, 1, 10, 11",  # needs to be converted in a C++ vector in the code, so set it as string here
            "tight_tau_id_vs_jet_wp": 1,              # VVVLoose working point, looser taus needed for tau misidentification estimate
            "tight_tau_id_vs_electron_wp": 1,         # VVVLoose working point, looser taus needed for tau misidentification estimate
            "tight_tau_id_vs_muon_wp": 1,             # VLoose working point, looser taus needed for tau misidentification estimate
        },
    )

    # hadronic tau identification against jets, electrons, and muons
    # recommendations: https://twiki.cern.ch/twiki/bin/viewauth/CMS/TauIDRecommendationForRun2
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            "vsjet_tau_id": [
                {
                    "tau_id_discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSjet"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "vsjet_tau_id_WPbit": bit,
                    "vsjet_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsjet_id_outputname": "id_tau_vsJet_{wp}_1".format(wp=wp),
                    "tau_2_vsjet_id_outputname": "id_tau_vsJet_{wp}_2".format(wp=wp),
                }
                for wp, bit in {
                    "VVVLoose": 1,
                    "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
            "vsele_tau_id": [
                {
                    "tau_id_discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSe"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "vsele_tau_id_WPbit": bit,
                    "vsele_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsele_id_outputname": "id_tau_vsEle_{wp}_1".format(wp=wp),
                    "tau_2_vsele_id_outputname": "id_tau_vsEle_{wp}_2".format(wp=wp),
                }
                for wp, bit in {
                    #"VVVLoose": 1,
                    "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    # "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
            "vsmu_tau_id": [
                {
                    "tau_id_discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSmu"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "vsmu_tau_id_WPbit": bit,
                    "vsmu_tau_id_WP": "{wp}".format(wp=wp),
                    "tau_1_vsmu_id_outputname": "id_tau_vsMu_{wp}_1".format(wp=wp),
                    "tau_2_vsmu_id_outputname": "id_tau_vsMu_{wp}_2".format(wp=wp),
                }
                for wp, bit in {
                    "VLoose": 1,
                    # "Loose": 2,
                    # "Medium": 3,
                    "Tight": 4,
                }.items()
            ],
        },
    )

    # correction files for tau identification/energy scale corrections and tau trigger scale factors
    # TODO for now, preliminary corrections are used for 2022 and 2023, update them as soon as the official corrections are available
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            "tau_ides_sf_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016preVFP-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016postVFP-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2017-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2018-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22CDSep23-Summer22-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2022_preEE.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2022_postEE.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23CSep23-Summer23-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2023_preBPix.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2023_postBPix.json.gz",
                }
            ),
            "tau_trigger_sf_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016preVFP-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2016postVFP-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2017-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run2-2018-UL-NanoAODv9/2024-07-02/tau.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22CDSep23-Summer22-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2022_preEE.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2022_postEE.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23CSep23-Summer23-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2023_preBPix.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/TAU/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-01/tau_DeepTau2018v2p5_2023_postBPix.json.gz",
                }
            ),
            "tau_ES_json_name": "tau_energy_scale",
            "tau_id_algorithm": tau_id,
            "tau_es_vs_jet_wp": "Medium",
            "tau_ES_shift_DM0": "nom",
            "tau_ES_shift_DM1": "nom",
            "tau_ES_shift_DM10": "nom",
            "tau_ES_shift_DM11": "nom",
            "tau_elefake_es_DM0_barrel": "nom",
            "tau_elefake_es_DM0_endcap": "nom",
            "tau_elefake_es_DM1_barrel": "nom",
            "tau_elefake_es_DM1_endcap": "nom",
            "tau_mufake_es": "nom",
        },
    )

    # configure the DeepTau working points for vs jets and vs electrons ID to use for ID and ES
    # corrections
    # the vs electrons WP is different for mt/tt and et channels
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            "tau_ides_sf_vsjet_wp": "Medium",
        }
    )
    configuration.add_config_parameters(
        MT_SCOPES + TT_SCOPES,
        {
            "tau_ides_sf_vsele_wp": "VVLoose",
        }
    )
    configuration.add_config_parameters(
        ET_SCOPES,
        {
            "tau_ides_sf_vsele_wp": "Tight",
        }
    )

    # hadronic tau identification corrections for DeepTau discriminator vs jets
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            # scale factors
            "vsjet_tau_id_sf": [
                {
                    "discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSjet"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "tau1_output_name": "id_wgt_tau_vsJet_{wp}_1".format(
                        wp=wp
                    ),
                    "tau2_output_name": "id_wgt_tau_vsJet_{wp}_2".format(
                        wp=wp
                    ),
                    "vsjet_wp": "{wp}".format(wp=wp),
                }
                for wp, bit in {
                    # "VVVLoose": 1,
                    # "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    "Medium": 5,
                    # "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],
        },
    )

    # the SF dependence and the SF variations for the DeepTau discriminator vs jets are different
    # for Run2 and Run3
    if era in ERAS_RUN2:

        # hadronic tau identification variations in semileptonic channels
        configuration.add_config_parameters(
            SL_SCOPES,
            {
                "tau_id_sf_vsjet_tau30to35_shift": "nom",
                "tau_id_sf_vsjet_tau35to40_shift": "nom",
                "tau_id_sf_vsjet_tau40to500_shift": "nom",
                "tau_id_sf_vsjet_tau500to1000_shift": "nom",
                "tau_id_sf_vsjet_tau1000toinf_shift": "nom",
                "tau_id_sf_vsjet_shift": "nom",
                "tau_id_sf_vsjet_sf_dependence": "dm",  # or "dm", "eta"
            },
        )

        # hadronic tau identification variations in fullhadronic channels
        configuration.add_config_parameters(
            FH_SCOPES,
            {
                "tau_id_sf_vsjet_tau_dm0_shift": "nom",
                "tau_id_sf_vsjet_tau_dm1_shift": "nom",
                "tau_id_sf_vsjet_tau_dm10_shift": "nom",
                "tau_id_sf_vsjet_tau_dm11_shift": "nom",
                "tau_id_sf_vsjet_sf_dependence": "dm",  # or "dm", "eta"
            },
        )

    elif era in ERAS_RUN3:
        # hadronic tau identification variations in all channels
        configuration.add_config_parameters(
            HAD_TAU_SCOPES,
            {
                "tau_id_sf_vsjet_shift": "nom",
                "tau_id_sf_vsjet_sf_dependence": "dm",  # or "dm", "eta"
            },
        )

    # hadronic tau identification corrections for DeepTau discriminator vs electrons
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            # scale factors
            "vsele_tau_id_sf": [
                {
                    "discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSe"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "tau1_output_name": "id_wgt_tau_vsEle_{wp}_1".format(
                        wp=wp
                    ),
                    "tau2_output_name": "id_wgt_tau_vsEle_{wp}_2".format(
                        wp=wp
                    ),
                    "vsele_wp": "{wp}".format(wp=wp),
                }
                for wp, bit in {
                    # "VVVLoose": 1,
                    "VVLoose": 2,
                    # "VLoose": 3,
                    # "Loose": 4,
                    # "Medium": 5,
                    "Tight": 6,
                    # "VTight": 7,
                    # "VVTight": 8,
                }.items()
            ],

            # systematic variations
            "tau_id_sf_vsele_barrel_shift": "nom",  # or "up"/"down" for up/down variation
            "tau_id_sf_vsele_endcap_shift": "nom",  # or "up"/"down" for up/down variation
        },
    )

    # hadronic tau identification corrections for DeepTau discriminator vs muons
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            # scale factors
            "vsmu_tau_id_sf": [
                {
                    "discriminator": EraModifier(
                        {
                            _era: f"{_tau_id}VSmu"
                            for _era, _tau_id in tau_id.modifier_dict.items()
                        }
                    ),
                    "tau1_output_name": "id_wgt_tau_vsMu_{wp}_1".format(
                        wp=wp
                    ),
                    "tau2_output_name": "id_wgt_tau_vsMu_{wp}_2".format(
                        wp=wp
                    ),
                    "vsmu_wp": "{wp}".format(wp=wp),
                    "max_abs_eta": EraModifier(
                        {
                            **{
                                _era: 2.3
                                for _era in ERAS_RUN2
                            },
                            **{
                                _era: 2.4
                                for _era in ERAS_RUN3
                            }
                        }
                    )
                }
                for wp, bit in {
                    "VLoose": 1,
                    # "Loose": 2,
                    # "Medium": 3,
                    "Tight": 4,
                }.items()
            ],

            # systematic variations
            "tau_id_sf_vsmu_wheel1_shift": "nom",  # or "up"/"down" for up/down variation
            "tau_id_sf_vsmu_wheel2_shift": "nom",  # or "up"/"down" for up/down variation
            "tau_id_sf_vsmu_wheel3_shift": "nom",  # or "up"/"down" for up/down variation
            "tau_id_sf_vsmu_wheel4_shift": "nom",  # or "up"/"down" for up/down variation
            "tau_id_sf_vsmu_wheel5_shift": "nom",  # or "up"/"down" for up/down variation
        },
    )


def add_boosted_hadronic_tau_config(configuration: Configuration):

    # boosted hadronic tau selection in semileptonic channels
    configuration.add_config_parameters(
        SL_SCOPES,
        {
            "min_boostedtau_pt": 40.0,
            "max_boostedtau_eta": 2.3,
            # "iso_boostedtau_id_bit": 1,
            # "antiele_boostedtau_id_bit": 1,
            # "antimu_boostedtau_id_bit": 1,
            "boosted_pairselection_min_dR": 0.1,
            "boosted_pairselection_max_dR": 5.0,
        },
    )

    # boosted hadronic tau selection in fullhadronic channels
    configuration.add_config_parameters(
        FH_SCOPES,
        {
            "min_boostedtau_pt": 40.0,
            "max_boostedtau_eta": 2.3,
            # "iso_boostedtau_id_bit": 2,
            # "antiele_boostedtau_id_bit": 2,
            # "antimu_boostedtau_id_bit": 1,
            "boosted_pairselection_min_dR": 0.1,
            "boosted_pairselection_max_dR": 5.0,
        },
    )

    # identification and energy scale corrections for boosted hadronic taus
    configuration.add_config_parameters(
        GLOBAL_SCOPES + HAD_TAU_SCOPES,
        {
            # boosted taus
            "boostedtau_dms": "0,1,10",
            "boostedtau_sf_file": EraModifier(
                {
                    "2016": "data/jsonpog-integration/POG/TAU/2016_Legacy/tau.json.gz",
                    "2017": "data/jsonpog-integration/POG/TAU/2017_ReReco/tau.json.gz",
                    "2018": "data/jsonpog-integration/POG/TAU/2018_ReReco/tau.json.gz",
                    **{
                        _era: "DOES_NOT_EXIST"  # placeholder, as these corrections are not available for Run3
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "boostedtau_ES_json_name": "tau_energy_scale",
            "boostedtau_id_algorithm": "MVAoldDM2017v2",
            "boostedtau_ES_shift_DM0": "nom",
            "boostedtau_ES_shift_DM1": "nom",
            "boostedtau_ES_shift_DM10": "nom",
            "boostedtau_ES_shift_DM11": "nom",
        },
    )

    # boosted hadronic tau identification
    configuration.add_config_parameters(
        HAD_TAU_SCOPES,
        {
            "iso_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "MVAoldDM2017v2",
                    "boostedtau_1_iso_id_outputname": "id_boostedtau_iso_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_iso_sf_outputname": "id_wgt_boostedtau_iso_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_iso_id_outputname": "id_boostedtau_iso_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_iso_sf_outputname": "id_wgt_boostedtau_iso_{wp}_2".format(
                        wp=wp
                    ),
                    "iso_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "iso_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    # "VVLoose": 1,
                    "VLoose": 2,
                    "Loose": 3,
                    "Medium": 4,
                    # "Tight": 5,
                    # "VTight": 6,
                    # "VVTight": 7,
                }.items()
            ],
            "antiele_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "antiEleMVA6",
                    "boostedtau_1_antiele_id_outputname": "id_boostedtau_antiEle_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_antiele_sf_outputname": "id_wgt_boostedtau_antiEle_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_antiele_id_outputname": "id_boostedtau_antiEle_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_antiele_sf_outputname": "id_wgt_boostedtau_antiEle_{wp}_2".format(
                        wp=wp
                    ),
                    "antiele_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "antiele_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    "VLoose": 1,
                    "Loose": 2,
                    # "Medium": 3,
                    # "Tight": 4,
                    # "VTight": 5,
                }.items()
            ],
            "antimu_boostedtau_id": [
                {
                    "boostedtau_id_discriminator": "antiMu3",
                    "boostedtau_1_antimu_id_outputname": "id_boostedtau_antiMu_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_1_antimu_sf_outputname": "id_wgt_boostedtau_antiMu_{wp}_1".format(
                        wp=wp
                    ),
                    "boostedtau_2_antimu_id_outputname": "id_boostedtau_antiMu_{wp}_2".format(
                        wp=wp
                    ),
                    "boostedtau_2_antimu_sf_outputname": "id_wgt_boostedtau_antiMu_{wp}_2".format(
                        wp=wp
                    ),
                    "antimu_boostedtau_id_WP": "{wp}".format(wp=wp),
                    "antimu_boostedtau_id_WPbit": bit,
                }
                for wp, bit in {
                    "Loose": 1,
                    # "Tight": 2,
                }.items()
            ],
            "boostedtau_sf_antiele_barrel": "nom",  # or "up"/"down" for up/down variation
            "boostedtau_sf_antiele_endcap": "nom",  # or "up"/"down" for up/down variation
            "boostedtau_sf_antimu_wheel1": "nom",
            "boostedtau_sf_antimu_wheel2": "nom",
            "boostedtau_sf_antimu_wheel3": "nom",
            "boostedtau_sf_antimu_wheel4": "nom",
            "boostedtau_sf_antimu_wheel5": "nom",
        },
    )

    # boosted hadronic tau identification variations in semileptonic channels
    configuration.add_config_parameters(
        SL_SCOPES,
        {
            "boostedtau_sf_iso_tau30to35": "nom",
            "boostedtau_sf_iso_tau35to40": "nom",
            "boostedtau_sf_iso_tau40to500": "nom",
            "boostedtau_sf_iso_tau500to1000": "nom",
            "boostedtau_sf_iso_tau1000toinf": "nom",
            "boostedtau_iso_sf_dependence": "pt",
        },
    )

    # boosted hadronic tau identification variations in fullhadronic channels
    configuration.add_config_parameters(
        FH_SCOPES,
        {
            "boostedtau_sf_iso_tauDM0": "nom",
            "boostedtau_sf_iso_tauDM1": "nom",
            "boostedtau_sf_iso_tauDM10": "nom",
            "boostedtau_sf_iso_tauDM11": "nom",
            "boostedtau_iso_sf_dependence": "dm",  # or "dm", "eta"
        },
    )


def add_ak4jet_config(configuration: Configuration):
    """
    Selection requirements and corrections for AK4 jets.

    - The `tightLepVeto` working point (corresponds to `jet_id == 6`) is used.

    Recommendations are taken from:

    - [Jet ID Run2 recommendations](https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVUL#Preliminary_Recommendations_for)

    - [Jet ID Run3 recommendations](https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV)

    - [Jet JERC Run3 recommendations](https://cms-jerc.web.cern.ch/Recommendations/)

    Corrections are obtained from the
    [nanoaod-tools/jsonpog-integration](gitlab.cern.ch/nanoaod-tools/jsonpog-integration) repository.

    The documentation of the `correctionlib` files for the jet energy corrections and resolution smearings can be found here:

    | Era          | Documentation                                                                                           |
    |--------------|---------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2016preVFP_UL_jet_jerc.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2016postVFP_UL_jet_jerc.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2017_UL_jet_jerc.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jet_jerc.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22_jet_jerc.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22EE_jet_jerc.html   |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23_jet_jerc.html     |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23BPix_jet_jerc.html |

    :param configuration: the main configuration object
    :type configuration: Configuration
    """

    # JetID recommendations: https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVUL#Preliminary_Recommendations_for
    configuration.add_config_parameters(
        "global",
        {
            "ak4jet_min_pt": 30.0,
            "ak4jet_max_abs_eta": 4.7,
            "ak4jet_id_wp": 2,  # 0 == fail, 2 == pass(tight) & fail(tightLepVeto), 6 == pass(tight) & pass(tightLepVeto)
            "ak4jet_apply_jet_horn_veto": "true",
            "ak4jet_puid_wp": EraModifier(
                {
                    "2016preVFP": 1,  # 0 == fail, 1 == pass(loose), 3 == pass(loose,medium), 7 == pass(loose,medium,tight)
                    "2016postVFP": 1,  # 0 == fail, 1 == pass(loose), 3 == pass(loose,medium), 7 == pass(loose,medium,tight)
                    "2017": 4,  # 0 == fail, 4 == pass(loose), 6 == pass(loose,medium), 7 == pass(loose,medium,tight)
                    "2018": 4,  # 0 == fail, 4 == pass(loose), 6 == pass(loose,medium), 7 == pass(loose,medium,tight)
                    **{
                        _era: 0  # placeholder value as it does not exist for Run3 samples
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "ak4jet_puid_max_pt": EraModifier(
                {
                    **{
                        _era: 50.0  # recommended to apply puID only for jets below 50 GeV
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: 0.0  # placeholder value as it does not exist for Run3 samples
                        for _era in ERAS_RUN3
                    },
                },
            )
        },
    )

    # AK4 jet energy calibration and resolution corrections
    # JEC recommendations: https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
    configuration.add_config_parameters(
        "global",
        {
            "ak4jet_reapplyJES": False,
            "ak4jet_jes_sources": '{""}',
            "ak4jet_jes_shift": 0,
            "ak4jet_jer_master_seed": 42,
            "ak4jet_jer_shift": "nom",  # or '"up"', '"down"'
            "ak4jet_jec_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv9/2025-04-11/jet_jerc.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv9/2025-04-11/jet_jerc.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv9/2025-04-11/jet_jerc.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv9/2025-04-11/jet_jerc.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jet_jerc.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jet_jerc.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07/jet_jerc.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jet_jerc.json.gz",
                },
            ),
            "ak4jet_jer_tag": EraModifier(
                {
                    "2016preVFP": "Summer20UL16APV_JRV3_MC",
                    "2016postVFP": "Summer20UL16_JRV3_MC",
                    "2017": "Summer19UL17_JRV2_MC",
                    "2018": "Summer19UL18_JRV2_MC",
                    "2022preEE": "Summer22_22Sep2023_JRV1_MC",
                    "2022postEE": "Summer22EE_22Sep2023_JRV1_MC",
                    "2023preBPix": "Summer23Prompt23_RunCv1234_JRV1_MC",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_JRV1_MC",
                }
            ),
            "ak4jet_jes_tag_data": "\"\"",
            "ak4jet_jes_tag": EraModifier(
                {
                    "2016preVFP": "Summer19UL16APV_V7_MC",
                    "2016postVFP": "Summer19UL16_V7_MC",
                    "2017": "Summer19UL17_V5_MC",
                    "2018": "Summer19UL18_V5_MC",
                    "2022preEE": "Summer22_22Sep2023_V3_MC",
                    "2022postEE": "Summer22EE_22Sep2023_V3_MC",
                    "2023preBPix": "Summer23Prompt23_V2_MC",
                    "2023postBPix": "Summer23BPixPrompt23_V3_MC",
                }
            ),
            "ak4jet_jec_algo": EraModifier(
                {
                    **{
                        _era: "AK4PFchs"
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: "AK4PFPuppi"
                        for _era in ERAS_RUN3
                    }
                }
            )
        },
    )

    # lepton/tau-jet overlap removal
    configuration.add_config_parameters(
        SCOPES,
        {
            "ak4jet_veto_min_delta_r": 0.4,
        },
    )

    # jet veto configuration
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "jet_veto_map_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv9/2025-04-11/jetvetomaps.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv9/2025-04-11/jetvetomaps.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv9/2025-04-11/jetvetomaps.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv9/2025-04-11/jetvetomaps.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/jetvetomaps.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/jetvetomaps.json.gz",
                },
            ),
            "jet_veto_map_name": EraModifier(
                {
                    **{
                        era: "DOES_NOT_EXIST"
                        for era in ERAS_RUN2
                    },
                    "2022preEE": "Summer22_23Sep2023_RunCD_V1",
                    "2022postEE": "Summer22EE_23Sep2023_RunEFG_V1",
                    "2023preBPix": "Summer23Prompt23_RunC_V1",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_V1",
                },
            ),
            "jet_veto_map_type": "jetvetomap",
            "jet_veto_min_pt": 15.0,
            "jet_veto_id_wp": 2,  # tight
            "jet_veto_max_em_frac": 0.9,
            "jet_veto_min_delta_r_jet_muon": 0.2,
        }
    )


def add_ak8jet_config(configuration: Configuration):
    """
    The documentation of the `correctionlib` files for the jet energy corrections and resolution smearings can be found here:

    | Era          | Documentation                                                                                           |
    |--------------|---------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2016preVFP_UL_jet_jerc.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2016postVFP_UL_jet_jerc.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2017_UL_jet_jerc.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2018_UL_jet_jerc.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22_jet_jerc.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2022_Summer22EE_jet_jerc.html   |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23_jet_jerc.html     |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/JME_2023_Summer23BPix_jet_jerc.html |
    """

    # AK8 jet selection
    # JEC recommendations: https://twiki.cern.ch/twiki/bin/view/CMS/JECDataMC
    configuration.add_config_parameters(
        "global",
        {
            "ak8jet_min_pt": 200.,
            "ak8jet_max_abs_eta": 2.5,
            "ak8jet_id_wp": 2,  # tight & tightLepVeto
            "ak8jet_apply_jet_horn_veto": "true",
            "ak8jet_reapplyJES": False,
            "ak8jet_jes_sources": '{""}',
            "ak8jet_jes_shift": 0,
            "ak8jet_jer_master_seed": 43,
            "ak8jet_jer_shift": "nom",  # or '"up"', '"down"'
            "ak8jet_jec_file": EraModifier(  # TODO use AK4 file for fatjets because it either was is just copied and the fatjet file has no merged uncertainty scheme?
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016preVFP-UL-NanoAODv9/2025-04-11/fatJet_jerc.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2016postVFP-UL-NanoAODv9/2025-04-11/fatJet_jerc.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2017-UL-NanoAODv9/2025-04-11/fatJet_jerc.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run2-2018-UL-NanoAODv9/2025-04-11/fatJet_jerc.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22CDSep23-Summer22-NanoAODv12/2025-09-23/fatJet_jerc.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-10-07/fatJet_jerc.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23CSep23-Summer23-NanoAODv12/2025-10-07/fatJet_jerc.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/JME/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-10-07/fatJet_jerc.json.gz",
                },
            ),
            "ak8jet_jer_tag": EraModifier(
                {
                    "2016preVFP": "Summer20UL16APV_JRV3_MC",
                    "2016postVFP": "Summer20UL16_JRV3_MC",
                    "2017": "Summer19UL17_JRV2_MC",
                    "2018": "Summer19UL18_JRV2_MC",
                    "2022preEE": "Summer22_22Sep2023_JRV1_MC",
                    "2022postEE": "Summer22EE_22Sep2023_JRV1_MC",
                    "2023preBPix": "Summer23Prompt23_RunCv1234_JRV1_MC",
                    "2023postBPix": "Summer23BPixPrompt23_RunD_JRV1_MC",
                }
            ),
            "ak8jet_jes_tag_data": "\"\"",
            "ak8jet_jes_tag": EraModifier(
                {
                    "2016preVFP": "Summer19UL16APV_V7_MC",
                    "2016postVFP": "Summer19UL16_V7_MC",
                    "2017": "Summer19UL17_V5_MC",
                    "2018": "Summer19UL18_V5_MC",
                    "2022preEE": "Summer22_22Sep2023_V3_MC",
                    "2022postEE": "Summer22EE_22Sep2023_V3_MC",
                    "2023preBPix": "Summer23Prompt23_V2_MC",
                    "2023postBPix": "Summer23BPixPrompt23_V3_MC",
                }
            ),
            "ak8jet_jec_algo": "AK8PFPuppi",  # TODO normally "AK8PFPuppi" would be used -> change to AK4 naming to get merged uncertainty scheme?
        },
    )

    # lepton/tau-jet overlap removal
    configuration.add_config_parameters(
        SCOPES,
        {
            "deltaR_fatjet_veto": 0.8,
        },
    )


def add_bjet_config(configuration: Configuration):
    """
    B jet identification and corrections.

    The documentation of the `correctionlib` files for the b jet identification corrections can be found here:

    | Era          | Documentation                                                                                           |
    |--------------|---------------------------------------------------------------------------------------------------------|
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2016preVFP_UL_btagging.html     |
    | 2016postVFP  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2016postVFP_UL_btagging.html    |
    | 2017         | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2017_UL_btagging.html           |
    | 2016preVFP   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2018_UL_btagging.html           |
    | 2022preEE    | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2022_Summer22_btagging.html     |
    | 2022postEE   | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2022_Summer22EE_btagging.html   |
    | 2023preBPix  | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2023_Summer23_btagging.html     |
    | 2023postBPix | https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/summaries/BTV_2023_Summer23BPix_btagging.html |
    """

    # b jet selection
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "bjet_min_pt": 20.,
            "bjet_max_abs_eta": EraModifier(
                {
                    "2016preVFP": 2.4,
                    "2016postVFP": 2.4,
                    **{
                        _era: 2.5
                        for _era in ["2017", "2018"] + ERAS_RUN3
                    },
                }
            ),
        },
    )

    # b jet identification
    # recommendations: https://btv-wiki.docs.cern.ch/ScaleFactors
    configuration.add_config_parameters(
        GLOBAL_SCOPES + SCOPES,
        {
            "bjet_min_deepjet_score": EraModifier(  # medium
                {
                    "2016preVFP": 0.2598,
                    "2016postVFPP": 0.2489,
                    "2017": 0.3040,
                    "2018": 0.2783,
                    "2022preEE": 0.3086,
                    "2022postEE": 0.3196,
                    "2023preBPix": 0.2431,
                    "2023postBPix": 0.2435,
                },
            ),
        },
    )

    # corrections for b jet identification
    configuration.add_config_parameters(
        SCOPES,
        {
            "btag_sf_file": EraModifier(
                {
                    "2016preVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run2-2016preVFP-UL-NanoAODv9/2025-08-19/btagging.json.gz",
                    "2016postVFP": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run2-2016postVFP-UL-NanoAODv9/2025-08-19/btagging.json.gz",
                    "2017": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run2-2017-UL-NanoAODv9/2025-08-19/btagging.json.gz",
                    "2018": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run2-2018-UL-NanoAODv9/2025-08-19/btagging.json.gz",
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-22CDSep23-Summer22-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-23CSep23-Summer23-NanoAODv12/2025-08-20/btagging.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/BTV/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-08-20/btagging.json.gz",
                }
            ),
            "btag_sf_variation": "central",
            "btag_corr_algo": "deepJet_shape",
        },
    )


def add_zpt_weight_config(configuration: Configuration):
    """
    Configuration parameters for Z boson pt reweighting.

    This configuration applies to run 3 eras only. Corrections are read from `correctionlib` files
    provided by the HLepRare group.
    """
    ## all scopes MET selection
    configuration.add_config_parameters(
        SCOPES,
        {
            "zpt_weight_order": SampleModifier(
                {
                    "dyjets": "LO",
                    "dyjets_madgraph": "LO",
                    "dyjets_amcatnlo_ll": "NLO",
                    "dyjets_amcatnlo_tt": "NLO",
                    "dyjets_powheg": "NLO",
                },
                default="DOES_NOT_EXIST",  # placeholder for samples without z pt reweighting
            ),
            "zpt_weight_file": EraModifier(
                {
                    **{
                        _era: f"data/hleprare/DYweightCorrlib/DY_pTll_weights_{_era}_v5.json.gz"
                        for _era in ERAS_RUN3
                    },
                    **{
                        _era: "DOES_NOT_EXIST"  # placeholder for Run 2, for which corrections are provided in a different way
                        for _era in ERAS_RUN2
                    },
                },
            ),
            "zpt_weight_name": "DY_pTll_reweighting",
            "zpt_weight_variation": "nom",
        },
    )


def add_recoil_corrections_config(configuration: Configuration):
    """
    Configuration parameters for recoil corrections.

    This configuration applies to Run 3 eras only. Corrections are read from `correctionlib` files
    provided by the HLepRare group.
    """

    configuration.add_config_parameters(
        SCOPES,
        {
            "recoil_correction_file": EraModifier(
                {
                    **{
                        _era: f"data/hleprare/RecoilCorrlib/Recoil_corrections_{_era}_v5.json.gz"
                        for _era in ERAS_RUN3
                    },
                    **{
                        _era: "DOES_NOT_EXIST"  # placeholder for Run 2, for which corrections are provided in a different way
                        for _era in ERAS_RUN2
                    },
                },
            ),
            "recoil_correction_name": "Recoil_correction",
            "recoil_correction_order": SampleModifier(
                {
                    "dyjets": "LO",
                    "dyjets_madgraph": "LO",
                    "dyjets_amcatnlo_ll": "NLO",
                    "dyjets_amcatnlo_tt": "NLO",
                    "dyjets_powheg": "NLO",
                    "wjets_madgraph": "LO",
                    "wjets_amcatnlo": "NLO",
                },
                default="DOES_NOT_EXIST",  # placeholder for samples without recoil corrections
            ),
            "recoil_correction_method": "QuantileMapHist",
            "recoil_correction_apply": SampleModifier(
                {
                    "dyjets": True,
                    "dyjets_madgraph": True,
                    "dyjets_amcatnlo_ll": True,
                    "dyjets_amcatnlo_tt": True,
                    "dyjets_powheg": True,
                    "wjets_madgraph": True,
                    "wjets_amcatnlo": True,
                },
                default=False,
            ),
            "recoil_correction_is_wjets": SampleModifier(
                {
                    "wjets_madgraph": True,
                    "wjets_amcatnlo": True,
                },
                default=False,
            ),
            "recoil_correction_variation": "nom",
        },
    )


def add_recoil_corrections_config_run2(configuration: Configuration):
    ## all scopes MET selection
    configuration.add_config_parameters(
        SCOPES,
        {
            "propagateLeptons": SampleModifier(
                {"data": False},
                default=True,
            ),
            "propagateJets": SampleModifier(
                {"data": False},
                default=True,
            ),
            "recoil_corrections_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",
                    "2016postVFP": "data/recoil_corrections/Type1_PuppiMET_2016.root",
                    "2017": "data/recoil_corrections/Type1_PuppiMET_2017.root",
                    "2018": "data/recoil_corrections/Type1_PuppiMET_2018.root",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "recoil_systematics_file": EraModifier(
                {
                    "2016preVFP": "data/recoil_corrections/PuppiMETSys_2016.root",
                    "2016postVFP": "data/recoil_corrections/PuppiMETSys_2016.root",
                    "2017": "data/recoil_corrections/PuppiMETSys_2017.root",
                    "2018": "data/recoil_corrections/PuppiMETSys_2018.root",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "applyRecoilCorrections": SampleModifier(
                {
                    "ttbar": False,
                    "singletop": False,
                    "diboson": False,
                    "data": False,
                    "embedding": False,
                    "embedding_mc": False,
                },
                default=True,
            ),
            "apply_recoil_resolution_systematic": False,
            "apply_recoil_response_systematic": False,
            "recoil_systematic_shift_up": False,
            "recoil_systematic_shift_down": False,
            "min_jetpt_met_propagation": 15,
        },
    )


def add_z_pt_reweighting_config_run2(configuration: Configuration):
    """
    Configuration for the Z boson pt reweighting.

    The Run 3 Z boson pt and recoil corrections are documented here: https://indico.cern.ch/event/1495537/contributions/6359516/attachments/3014424/5315938/HLepRare_25.02.14.pdf.

    The corrections are available here: https://gitlab.cern.ch/cms-higgs-leprare/hleprare
    """

    # Z pt reweighting
    configuration.add_config_parameters(
        SCOPES,
        {
            "zptmass_file": EraModifier(
                {
                    "2016preVFP": "data/zpt/htt_scalefactors_legacy_2016.root",
                    "2016postVFP": "data/zpt/htt_scalefactors_legacy_2016.root",
                    "2017": "data/zpt/htt_scalefactors_legacy_2017.root",
                    "2018": "data/zpt/htt_scalefactors_legacy_2018.root",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "zptmass_functor": "zptmass_weight_nom",
            "zptmass_arguments": "z_gen_mass,z_gen_pt",
        },
    )


def build_config(
    era: str,
    sample: str,
    scopes: List[str],
    shifts: List[str],
    available_sample_types: List[str],
    available_eras: List[str],
    available_scopes: List[str],
):

    configuration = Configuration(
        era,
        sample,
        scopes,
        shifts,
        available_sample_types,
        available_eras,
        available_scopes,
    )

    # Set sample flags manually
    # The configuration of is_data and is_embedding is set here for better readability, although
    # it has already been set in the Configuration class.
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "is_data": sample == "data",
            "is_embedding": sample == "embedding",
            "is_mc": sample not in ["data", "embedding"],
        },
    )

    # noise filters
    add_noise_filters_config(configuration)

    # pileup reweighting
    add_pileup_reweighting_config(configuration)

    # golden JSON filter
    add_golden_json_config(configuration)

    # variations of the renormalization and factorization scales
    add_mur_muf_weights_config(configuration)

    # AK4 jet selection and energy/resolution corrections
    add_ak4jet_config(configuration)

    # AK8 jet selection and energy/resolution corrections
    add_ak8jet_config(configuration)

    # electron selection and corrections for reconstruction and identification
    add_electron_config(configuration)

    # muon selection and corrections for reconstruction, identification, and isolation
    add_muon_config(configuration)

    # hadronic tau selection and corrections for identification and energy scale
    add_hadronic_tau_config(configuration, era)

    # b jet selection, identification, and corrections
    add_bjet_config(configuration)

    # Z pt reweighting
    add_zpt_weight_config(configuration)

    # Recoil corrections
    add_recoil_corrections_config(configuration)

    # recoil corrections
    # TODO needs to be refined for run 3, not considered at the moment(https://github.com/kit-cms/XYHBBTauTauAnalysis-CROWN/issues/6)
    #add_recoil_corrections_config(configuration)

    # Z pt reweighting
    # TODO needs to be refined for run 3, not considered at the moment (https://github.com/kit-cms/XYHBBTauTauAnalysis-CROWN/issues/7)
    #add_z_pt_reweighting_config(configuration)

    #
    # LOOSE OBJECT SELECTIONS
    #

    # electron energy scale corrections
    configuration.add_config_parameters(
        GLOBAL_SCOPES,
        {
            "ele_es_master_seed": 44,
            "ele_es_era": EraModifier(
                {
                    "2016preVFP": "2016preVFP",
                    "2016postVFP": "2016postVFP",
                    "2017": "2017",
                    "2018": "2018",
                    **{
                        _era: "DOES_NOT_EXIST"  # not needed for Run 3 producer
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "ele_es_variation": "nom",
            "ele_es_file": EraModifier(
                {
                    **{
                        _era: f"data/electron_energy_scale/{_era}_UL/EGM_ScaleUnc.json.gz"
                        for _era in ERAS_RUN2
                    },
                    "2022preEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22CDSep23-Summer22-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
                    "2022postEE": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-22EFGSep23-Summer22EE-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
                    "2023preBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23CSep23-Summer23-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
                    "2023postBPix": "/cvmfs/cms-griddata.cern.ch/cat/metadata/EGM/Run3-23DSep23-Summer23BPix-NanoAODv12/2025-12-03/electronSS_EtDependent.json.gz",
                }
            ),
            "ele_es_sf_name": EraModifier(
                {
                    **{
                        _era: "UL-EGM_ScaleUnc"  # not needed for Run 2 producer
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: "DOES_NOT_EXIST"  # not needed for Run 3 producer
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "ele_es_sf_data_name": EraModifier(
                {
                    **{
                        _era: "DOES_NOT_EXIST"  # not needed for Run 2 producer
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: "Scale"
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "ele_es_sf_mc_name": EraModifier(
                {
                    **{
                        _era: "DOES_NOT_EXIST"  # not needed for Run 2 producer
                        for _era in ERAS_RUN2
                    },
                    **{
                        _era: "SmearAndSyst"
                        for _era in ERAS_RUN3
                    },
                }
            ),
        },
    )

    # AK8 X->bb jet identification
    configuration.add_config_parameters(
        SCOPES,
        {
            "pNetXbb_sf_file": EraModifier(
                {
                    "2016preVFP": "DOES_NOT_EXIST",
                    "2016postVFP": "DOES_NOT_EXIST",
                    "2017": "DOES_NOT_EXIST",
                    "2018": "payloads/particleNet/pNet_Xbb_SF_2018.json.gz",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    },
                }
            ),
            "pNetXbb_sf_variation": "nominal",
        },
    )

    # gen b pair for NMSSM analysis
    configuration.add_config_parameters(
        SCOPES,
        {
            "bb_truegen_mother_pdgid": SampleModifier(
                {"nmssm_Ybb": 35, "nmssm_Ytautau": 25}, default=-1
            ),
            "bb_truegen_daughter_1_pdgid": 5,
            "bb_truegen_daughter_2_pdgid": 5,
            "gen_bpair_match_deltaR": 0.2,
            "tautau_truegen_mother_pdgid": SampleModifier(
                {"nmssm_Ybb": 25, "nmssm_Ytautau": 35}, default=-1
            ),
            "tautau_truegen_daughter_1_pdgid": 15,
            "tautau_truegen_daughter_2_pdgid": 15,
            "gen_taupair_match_deltaR": 0.2,
            "fatjet_bpair_matching_max_dR": 0.2,
        },
    )

    # Separation for resolved bb and tautau pair selections
    configuration.add_config_parameters(
        SCOPES,
        {
            "pairselection_min_dR": 0.5,
            "bb_pairselection_min_dR": 0.4,
        },
    )


    #
    # TRIGGERS
    #


    # Trigger scale factors for measurements in the embedding workflow
    configuration.add_config_parameters(
        MUON_SCOPES,
        {
            "singlemuon_trigger_sf_mc": [
                {
                    "flagname": "trg_wgt_single_mu24",
                    "mc_trigger_sf": "Trg_IsoMu24_pt_eta_bins",
                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_mu27",
                    "mc_trigger_sf": "Trg_IsoMu27_pt_eta_bins",
                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_mu24ormu27",
                    "mc_trigger_sf": "Trg_IsoMu27_or_IsoMu24_pt_eta_bins",
                    "mc_muon_trg_extrapolation": 1.0,  # for nominal case
                },
            ]
        },
    )

    # Trigger scale factors for measurements in the embedding workflow
    configuration.add_config_parameters(
        ELECTRON_SCOPES,
        {
            "singlelectron_trigger_sf_mc": [
                {
                    "flagname": "trg_wgt_single_ele32",
                    "mc_trigger_sf": "Trg32_Iso_pt_eta_bins",
                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele35",
                    "mc_trigger_sf": "Trg35_Iso_pt_eta_bins",
                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele32orele35",
                    "mc_trigger_sf": "Trg32_or_Trg35_Iso_pt_eta_bins",
                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                },
                {
                    "flagname": "trg_wgt_single_ele27orele32orele35",
                    "mc_trigger_sf": "Trg_Iso_pt_eta_bins",
                    "mc_electron_trg_extrapolation": 1.0,  # for nominal case
                },
            ]
        },
    )

    # Trigger scale factors for electron triggers
    configuration.add_config_parameters(
        ELECTRON_SCOPES,
        {
            "ele_trg_sf_file": EraModifier(
                {
                    "2016preVFP": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL16preVFP.json.gz",
                    "2016postVFP": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL16postVFP.json.gz",
                    "2017": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL17.json.gz",
                    "2018": "payloads/electron_trigger/B2G-22-006_ElecTriggerSF_UL18.json.gz",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    }
                }
            ),
        },
    )
    # Settings for the ditau trigger scale factors on embedding
    configuration.add_config_parameters(
        TT_SCOPES,
        {
            "ditau_trigger_wp": "Medium",
            "ditau_trigger_type": "ditau",
            "ditau_trigger_corrtype": "sf",
            "ditau_trigger_syst": "nom",
        },
    )

    # fatjet trigger settings
    configuration.add_config_parameters(
        SCOPES,
        {
            "fatjet_trigger_sf_file": EraModifier(
                {
                    "2016preVFP": "DOES_NOT_EXIST",
                    "2016postVFP": "DOES_NOT_EXIST",
                    "2017": "DOES_NOT_EXIST",
                    "2018": "payloads/fatjet_trigger/scale_factor__AK8PFJet400_TrimMass30__singlemuon.json",
                    **{
                        _era: "DOES_NOT_EXIST"  # TODO does not exist yet for Run3 samples, include as soon as available
                        for _era in ERAS_RUN3
                    }
                }
            ),
            "fatjet_trigger_sf_name": "SF_AK8PFJet400_TrimMass30",
            "fatjet_trigger_sf_syst": "nominal",
        },
    )


    #
    # ERA-DEPENDENT PRODUCERS
    #
    # Catch correct producers depending on the era.
    #

    # Prefiring weights
    # Correction of this issue is only relevant for 2016 and 2017 data/MC
    prefire_weight_producers = get_for_era(
        {
            ("2016preVFP", "2016postVFP", "2017"): [event.PrefireWeight],
        },
        era,
        default=[],
    )

    # Electron pt correction
    # - In Run 2, a fix must be applied to the already corrected electron pt.
    # - In Run 3, the electon pt is not corrected at NanoAOD level, the full correction is applied
    #   based on correctionlib files.
    electron_pt_correction_mc_producer = get_for_era(
        {
            tuple(ERAS_RUN2): electrons.ElectronPtCorrectionMCRun2,
            tuple(ERAS_RUN3): electrons.ElectronPtCorrectionMCRun3,
        },
        era,
    )

    # Electron pt correction for data
    # - In Run 2, the pt is already corrected, so this is just 
    electron_pt_correction_data_producer = get_for_era(
        {
            tuple(ERAS_RUN2): electrons.RenameElectronPt,
            tuple(ERAS_RUN3): electrons.ElectronPtCorrectionDataRun3,
        },
        era,
    )

    # Tau energy correction on MC
    # The parameters of the correction changed between Run 2 and Run 3, that's why we need two
    # different types of producers here.
    tau_energy_correction_mc_producer = get_for_era(
        {
            tuple(ERAS_RUN2): taus.TauEnergyCorrectionMCRun2,
            tuple(ERAS_RUN3): taus.TauEnergyCorrectionMCRun3,
        },
        era,
    )

    # Jet selection
    # - In Run 2, the CHS collection is used and pileup ID is applied.
    # - In Run 3, the PUPPI collection is used and no pileup ID is applied; the jet ID needs to
    #   be corrected in 2022 and 2023 due to a bug.
    jet_selection_producers = get_for_era(
        {
            tuple(ERAS_RUN2): [
                jets.JetIDRun2,
                jets.GoodJetsWithPUID,
                jets.GoodBJetsWithPUID,
            ],
            tuple(ERAS_RUN3): [
                jets.JetIDRun3NanoV12Corrected,
                jets.GoodJetsWithoutPUID,
                jets.GoodBJetsWithoutPUID,
                jets.GoodJetsCombinedWithoutPUID,
            ],
        },
        era,
    )

    # Jet energy corrections for AK4 jets
    # Different producers are used for Run 2 and Run 3 due to minor differences in the parameters
    # that the corrections depend on.
    jet_energy_correction_producer = get_for_era(
        {
            tuple(ERAS_RUN2): jets.JetEnergyCorrectionRun2,
            tuple(ERAS_RUN3): jets.JetEnergyCorrection,
        },
        era,
    )

    # Jet energy corrections for AK8 jets
    # Different producers are used for Run 2 and Run 3 due to minor differences in the parameters
    # that the corrections depend on.
    fat_jet_energy_correction_producer = get_for_era(
        {
            tuple(ERAS_RUN2): fatjets.FatJetEnergyCorrectionRun2,
            tuple(ERAS_RUN3): fatjets.FatJetEnergyCorrection,
        },
        era,
    )

    # Jet rename for embedding
    # In embedding, the full JEC has already been applied, so no further correction is needed.
    rename_jets_data_producer = get_for_era(
        {
            tuple(ERAS_RUN2): jets.RenameJetsDataRun2,
            tuple(ERAS_RUN3): jets.RenameJetsData,
        },
        era,
    )

    # Fat jet rename for embedding
    # In embedding, the full JEC has already been applied, so no further correction is needed.
    rename_fatjets_data_producer = get_for_era(
        {
            tuple(ERAS_RUN2): fatjets.RenameFatJetsDataRun2,
            tuple(ERAS_RUN3): fatjets.RenameFatJetsData,
        },
        era,
    )

    # Jet vetomaps
    # Vetoing events with jets in regions with known issues is only applied to Run 3 data/MC
    jet_veto_map_producers = get_for_era(
        {
            tuple(ERAS_RUN3): [event.JetVetoMapVeto],
        },
        era,
        default=[],
    )

    # AK8 X -> bb tagging scale factors
    # The X -> bb tagging scale factors only exist for 2018 for now.
    # TODO provide these scale factors for all eras
    xbb_sf_producers = get_for_era(
        {
            "2018": [
                scalefactors.Xbb_tagging_SF,
            ],
        },
        era,
        default=[]
    )

    # B jet pair quantities
    # Run 3 does not include b jet regression variables, so the producers for the b jet pair
    # quantities differ for both eras.
    bb_jet_pair_quantity_producers = get_for_era(
        {
            tuple(ERAS_RUN2): [
                pairquantities_bbpair.DiBjetPairQuantitiesRun2,
            ],
            tuple(ERAS_RUN3): [
                pairquantities_bbpair.DiBjetPairQuantitiesRun3,
            ]
        },
        era,
    )

    # Z boson pt reweighting
    # - TODO For Run 2, the corrections are provided in ROOT files and require a dedicated producer chain.
    # - For Run 3, the corrections are provided in correctionlib files.
    z_pt_reweighting_producers = get_for_era(
        {
            tuple(ERAS_RUN3): [
                boson_corrections.ZPtReweighting,
            ],
        },
        era,
        default=[],
    )

    # Recoil corrections
    # - TODO For Run 2, the corrections are provided in ROOT files and require a dedicated producer chain.
    # - For Run 3, the corrections are provided in correctionlib files.
    recoil_correction_producer = get_for_era(
        {
            tuple(ERAS_RUN2): None,
            tuple(ERAS_RUN3): boson_corrections.BosonRecoilCorrection,
        },
        era,
    )

    # Di-tau + jet trigger
    # - In Run 2, di-tau + jet triggers did not exist, so no producer is added.
    # - In Run 3, di-tau + jet triggers are available and the corresponding trigger flag producers
    #   are added to the tt scope.
    double_tau_jet_trigger_producers = get_for_era(
        {
            tuple(ERAS_RUN3): [
                triggers.DoubleTauTauJetTriggerFlags,
            ],
        },
        era,
        default=[],
    )

    # Tau ID scale factors in the mt channel
    # - In Run 2, the scale factors are provided from own measurements with the same methods as for
    #   embedding.
    # - In Run 3, the official measurements from the MUO POG are taken.
    mt_tau_sf_producers = get_for_era(
        {
            tuple(ERAS_RUN2): [
                scalefactors.Tau_2_VsJetTauID_lt_SF,
                scalefactors.Tau_2_VsEleTauID_SF_Run2,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
            tuple(ERAS_RUN3): [
                scalefactors.Tau_2_VsJetTauID_SF,
                scalefactors.Tau_2_VsEleTauID_SF_Run3,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
        },
        era,
    )

    # Tau ID scale factors in the et channel
    # - In Run 2, the scale factors are provided from own measurements with the same methods as for
    #   embedding.
    # - In Run 3, the official measurements from the TAU POG are taken.
    et_tau_sf_producers = get_for_era(
        {
            tuple(ERAS_RUN2): [
                scalefactors.Tau_2_VsJetTauID_lt_SF,
                scalefactors.Tau_2_VsEleTauID_SF_Run2,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
            tuple(ERAS_RUN3): [
                scalefactors.Tau_2_VsJetTauID_SF,
                scalefactors.Tau_2_VsEleTauID_SF_Run3,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
        },
        era,
    )

    # Tau ID scale factors in the tt channel 
    # - In Run 2, the scale factors are provided from own measurements with the same methods as for
    #   embedding.
    # - In Run 3, the official measurements from the TAU POG are taken.
    tt_tau_sf_producers = get_for_era(
        {
            tuple(ERAS_RUN2): [
                scalefactors.Tau_1_VsJetTauID_tt_SF,
                scalefactors.Tau_2_VsJetTauID_tt_SF,
                scalefactors.Tau_1_VsEleTauID_SF_Run2,
                scalefactors.Tau_2_VsEleTauID_SF_Run2,
                scalefactors.Tau_1_VsMuTauID_SF,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
            tuple(ERAS_RUN3): [
                scalefactors.Tau_1_VsJetTauID_SF,
                scalefactors.Tau_2_VsJetTauID_SF,
                scalefactors.Tau_1_VsEleTauID_SF_Run3,
                scalefactors.Tau_2_VsEleTauID_SF_Run3,
                scalefactors.Tau_1_VsMuTauID_SF,
                scalefactors.Tau_2_VsMuTauID_SF,
            ],
        },
        era,
    )

    #
    # PRODUCER DEFINITIONS
    #
    # Add producers to the configuration.
    #

    # global producers, to be executed before any channel selection
    configuration.add_producers(
        "global",
        [
            # event.RunLumiEventFilter,
            event.SampleFlags,
            event.Lumi,
            event.npartons,
            event.MetFilter,
            event.PUweights,
            event.LHE_Scale_weight,
            electrons.BaseElectrons,
            muons.BaseMuons,
            fatjets.GoodFatJets,
            event.DiLeptonVeto,
<<<<<<< HEAD
            met.MetBasics,
            boson_corrections.GenBosonQuantities,
=======
            puppimet.MetQuantitiesUncorrected,
>>>>>>> ba5715d (Update parameter values of Z boson pt and recoil corrections)
        ]
        + prefire_weight_producers
        + jet_selection_producers
        + jet_veto_map_producers
        + [
            electron_pt_correction_mc_producer,
            jet_energy_correction_producer,
            fat_jet_energy_correction_producer,
        ]
    )

    # Producers common to all scopes with at least one hadronic tau
    configuration.add_producers(
        SCOPES,
        [
            fatjets.FatJetCollection,
            fatjets.FatJetCollectionWithoutVeto,
            fatjets.BasicFatJetQuantities,
            jets.JetCollection,
            jets.JetCombinedCollection,
            jets.JetColumns,
            jets.BasicJetQuantities,
            jets.BJetCollection,
            jets.BasicBJetQuantities,
            pairselection.BBPairSelection,
            # pairselection.GoodBBPairFilter,
            pairselection.LVbjet1,
            pairselection.LVbjet2,
            genparticles.GenDiBjetPairQuantities,
            fatjets.FindFatjetMatchingBjet,
            fatjets.BasicMatchedFatJetQuantities,
            fatjets.FindXbbFatjet,
            fatjets.BasicXbbFatJetQuantities,
            fatjets.LeadingFatJetQuantities,
            scalefactors.btagging_SF,
            # TODO producers need to be refined for run 3, not considered at the moment
            #met.MetCorrections,
            #met.PFMetCorrections,
            puppimet.RenameMet,  # dummy producer for samples, on which MET is not corrected via recoil corrections
            puppimet.MetQuantities,
            pairquantities.DiTauPairMETQuantities,
            genparticles.GenMatching,
        ]
        + xbb_sf_producers
        + bb_jet_pair_quantity_producers,
    )

    # Producers for quantities in all scopes with hadronic taus
    configuration.add_producers(
        HAD_TAU_SCOPES,
        [
            tau_energy_correction_mc_producer,
        ]
    )

    # Producers for quantities in the et scope
    configuration.add_producers(
        ET_SCOPES,
        [
            electrons.GoodElectrons,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            electrons.NumberOfGoodElectrons,
            electrons.VetoElectrons,
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            pairselection.ETPairSelection,
            pairselection.GoodETPairFilter,
            pairselection.LVEl1,
            pairselection.LVTau2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.ETDiTauPairQuantities,
            genparticles.ETGenDiTauPairQuantities,
            scalefactors.EleID_SF,
            triggers.SingleEleTriggerFlags,
            triggers.DoubleEleTauTriggerFlags,
            scalefactors.SingleEleTriggerSF,
            scalefactors.DoubleEleTauTriggerSF,
            # TODO rework trigger setup before enabling this
            # triggers.ETGenerateCrossTriggerFlags,
            # triggers.GenerateSingleTrailingTauTriggerFlags,
        ]
        + et_tau_sf_producers
    )

    # Producers for quantities in the mt scope
    configuration.add_producers(
        MT_SCOPES,
        [
            muons.GoodMuons,
            muons.NumberOfGoodMuons,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            electrons.ExtraElectronsVeto,
            pairselection.MTPairSelection,
            pairselection.GoodMTPairFilter,
            pairselection.LVMu1,
            pairselection.LVTau2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.MTDiTauPairQuantities,
            genparticles.MTGenDiTauPairQuantities,
            triggers.SingleMuTriggerFlags,
            triggers.DoubleMuTauTriggerFlags,
            scalefactors.MuonIDIso_SF,
            scalefactors.SingleMuTriggerSF,
            scalefactors.DoubleMuTauTriggerSF,
            # TODO rework trigger setup before enabling this
            # triggers.GenerateSingleTrailingTauTriggerFlags,
        ]
        + mt_tau_sf_producers
    )

    # Producers for quantities in the tt scope
    configuration.add_producers(
        TT_SCOPES,
        [
            electrons.ExtraElectronsVeto,
            muons.ExtraMuonsVeto,
            taus.GoodTaus,
            taus.NumberOfGoodTaus,
            pairselection.TTPairSelection,
            pairselection.GoodTTPairFilter,
            pairselection.LVTau1,
            pairselection.LVTau2,
            pairselection.LVTau1Uncorrected,
            pairselection.LVTau2Uncorrected,
            pairquantities.TTDiTauPairQuantities,
            genparticles.TTGenDiTauPairQuantities,
            triggers.DoubleTauTauTriggerFlags,
            scalefactors.DoubleTauTauTriggerSF,
            # TODO rework trigger setup before enabling this
            # triggers.GenerateSingleTrailingTauTriggerFlags,
            # triggers.GenerateSingleLeadingTauTriggerFlags,
        ]
        + double_tau_jet_trigger_producers
        + tt_tau_sf_producers
    )

    # Producers for quantities in the et scope
    configuration.add_producers(
        EE_SCOPES,
        [
            electrons.GoodElectrons,
            electrons.NumberOfGoodElectrons,
            electrons.VetoElectrons,
            electrons.VetoSecondElectron,
            electrons.ExtraElectronsVeto,
            pairselection.ZElElPairSelection,
            pairselection.GoodElElPairFilter,
            pairselection.LVEl1,
            pairselection.LVEl2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVEl2Uncorrected,
            pairquantities.ElElPairQuantities,
            genparticles.ElElGenPairQuantities,
            scalefactors.EleID_SF,
            triggers.SingleEleTriggerFlags,
            scalefactors.SingleEleTriggerSF,
        ]
    )

    # Producers for quantities in the mm scope
    configuration.add_producers(
        MM_SCOPES,
        [
            muons.GoodMuons,
            muons.VetoMuons,
            muons.VetoSecondMuon,
            muons.ExtraMuonsVeto,
            muons.NumberOfGoodMuons,
            pairselection.ZMuMuPairSelection,
            pairselection.GoodMuMuPairFilter,
            pairselection.LVMu1,
            pairselection.LVMu2,
            pairselection.LVMu1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.MuMuPairQuantities,
            genparticles.MuMuGenPairQuantities,
            scalefactors.MuonIDIso_SF,
            triggers.SingleMuTriggerFlags,
            scalefactors.SingleMuTriggerSF,
        ],
    )

    # Producers for quantities in the em scope
    configuration.add_producers(
        EM_SCOPES,
        [
            electrons.GoodElectrons,
            muons.GoodMuons,
            electrons.VetoElectrons,
            electrons.ExtraElectronsVeto,
            muons.VetoMuons,
            muons.ExtraMuonsVeto,
            electrons.NumberOfGoodElectrons,
            muons.NumberOfGoodMuons,
            pairselection.EMPairSelection,
            pairselection.GoodEMPairFlag,
            pairselection.LVEl1,
            pairselection.LVMu2,
            pairselection.LVEl1Uncorrected,
            pairselection.LVMu2Uncorrected,
            pairquantities.EMDiTauPairQuantities,
            genparticles.EMGenDiTauPairQuantities,
            scalefactors.EleID_SF,
            scalefactors.MuonIDIso_SF,
            triggers.SingleEleTriggerFlags,
            triggers.SingleMuTriggerFlags,
            triggers.DoubleEleMuTriggerFlags,
            scalefactors.SingleEleTriggerSF,
            scalefactors.SingleMuTriggerSF,
        ],
    )


    #
    # PRODUCER MODIFICATIONS
    # 
    # Remove, append, or modify producers in specific cases.
    #


    # For DY samples, add producer for flag indicating the flavor of the decay products
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        AppendProducer(
            [
                event.LHEDrellYanDecayFlavor,
            ],
            samples=["dyjets", "dyjets_madgraph", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "dyjets_powheg"],
        )
    )

    # For DY and W samples, calculate the generator-level boson four-vector
    configuration.add_modification_rule(
        SCOPES,
        AppendProducer(
            [boson_corrections.GenBosonQuantities],
            samples=["dyjets_madgraph", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "dyjets_powheg", "wjets_madgraph", "wjets_amcatnlo"],
        ),
    )

    # For DY samples, apply Z pt reweighting
    configuration.add_modification_rule(
        SCOPES,
        AppendProducer(
            z_pt_reweighting_producers,
            samples=["dyjets_madgraph", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "dyjets_powheg"],
        )
    )

    # For DY and W samples, apply Z pt reweighting
    configuration.add_modification_rule(
        SCOPES,
        ReplaceProducer(
            [puppimet.RenameMet, recoil_correction_producer],
            samples=["dyjets_madgraph", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt", "dyjets_powheg", "wjets_madgraph", "wjets_amcatnlo"],
        )
    )

    # Remove tau ID scale factor producers from data samples in et scope
    configuration.add_modification_rule(
        ET_SCOPES,
        RemoveProducer(
            producers=et_tau_sf_producers,
            samples=["data"],
        ),
    )

    # Remove tau ID scale factor producers from data samples in mt scope
    configuration.add_modification_rule(
        MT_SCOPES,
        RemoveProducer(
            producers=mt_tau_sf_producers,
            samples=["data"],
        ),
    )

    # Remove tau ID scale factor producers from data samples in tt scope
    configuration.add_modification_rule(
        TT_SCOPES,
        RemoveProducer(
            producers=tt_tau_sf_producers,
            samples=["data"],
        ),
    )

    # Remove trigger scale factor producers from data and embedding samples in mt scope
    configuration.add_modification_rule(
        ELECTRON_SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.SingleEleTriggerSF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )
    configuration.add_modification_rule(
        ET_SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.DoubleEleTauTriggerSF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )


    # Remove trigger scale factor producers from data and embedding samples in mt scope
    configuration.add_modification_rule(
        MUON_SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.SingleMuTriggerSF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        )
    )
    configuration.add_modification_rule(
        MT_SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.DoubleMuTauTriggerSF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        )
    )

    # Remove trigger scale factor producers from data and embedding samples in tt scope
    configuration.add_modification_rule(
        TT_SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.DoubleTauTauTriggerSF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # TODO re-include
    #configuration.add_modification_rule(
    #    ["et", "mt", "tt"],
    #    AppendProducer(
    #        producers=[
    #            genparticles.GenBPairQuantities,
    #            genparticles.GenMatchingBPairFlag,
    #            genparticles.GenTauPairQuantities,
    #        ],
    #        samples=["nmssm_Ybb", "nmssm_Ytautau"],
    #    ),
    #)

    # Remove b tagging scale factor producers from data and embedding samples in all scopes 
    configuration.add_modification_rule(
        SCOPES,
        RemoveProducer(
            producers=[
                scalefactors.btagging_SF,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # Remove X -> bb fatjet producers from data and embedding samples in all scopes
    configuration.add_modification_rule(
        SCOPES,
        RemoveProducer(
            producers=[
                fatjets.fj_Xbb_hadflavor,
                fatjets.fj_Xbb_nBhad,
                fatjets.fj_Xbb_nChad,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # Remove X -> bb tagging scale factor producers from data and embedding samples in all scopes
    configuration.add_modification_rule(
        SCOPES,
        RemoveProducer(
            producers=xbb_sf_producers,
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # Remove the pileup weights from data and embedding samples
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        RemoveProducer(
            producers=[event.PUweights],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # Replace jet energy correction for data
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[jet_energy_correction_producer, jets.JetEnergyCorrection_data_Run2],
            samples=["data"],
        ),
    )

    # Replace fat jet energy correction for data
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[
                fat_jet_energy_correction_producer,
                fatjets.FatJetEnergyCorrection_data_Run2,
            ],
            samples=["data"],
        ),
    )

    # Replace jet energy correction for embedding with dummy rename operation
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[jet_energy_correction_producer, rename_jets_data_producer],
            samples=["embedding", "embedding_mc"],
        ),
    )

    # Replace fat jet energy correction for embedding with dummy rename operation
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[fat_jet_energy_correction_producer, rename_fatjets_data_producer],
            samples=["embedding", "embedding_mc"],
        ),
    )

    # Replace electron pt correction for data, as the correction is computed differently in data and
    # MC
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[
                electron_pt_correction_mc_producer,
                electron_pt_correction_data_producer,
            ],
            samples=["data"],
        ),
    )

    # Replace the tau energy correction producer for data samples
    configuration.add_modification_rule(
        HAD_TAU_SCOPES,
        ReplaceProducer(
            producers=[tau_energy_correction_mc_producer, taus.TauEnergyCorrection_data],
            samples=["data"],
        ),
    )

    # The number of partons is only defined for MC samples and only important to know for EW
    # process samples
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        RemoveProducer(
            producers=[event.npartons],
            exclude_samples=[
                "dyjets",
                "dyjets_madgraph",
                "dyjets_powheg",
                "dyjets_amcatnlo_ll",
                "dyjets_amcatnlo_tt",
                "wjets",
                "wjets_madgraph",
                "wjets_amcatnlo",
                "electroweak_boson",
            ],
        ),
    )

    # for whatever reason, the diboson samples do not have these weights in the ntuple....
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        RemoveProducer(
            producers=[event.LHE_Scale_weight],
            samples=["data", "embedding", "embedding_mc", "diboson", "hh2b2tau"],
        ),
    )

    # for whatever reason, the nmssm samples have one less entry of the weights and therefore need
    # special treatment
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        ReplaceProducer(
            producers=[event.LHE_Scale_weight, event.NMSSM_LHE_Scale_weight],
            samples=["nmssm_Ybb", "nmssm_Ytautau"],
        ),
    )

    # Remove the generator-level tau matching producers from data samples
    configuration.add_modification_rule(
        SCOPES,
        RemoveProducer(
            producers=[
                genparticles.GenMatching,
            ],
            samples=["data"],
        ),
    )

    # Remove the generator-level b jet pair quantities from data and embedding samples
    configuration.add_modification_rule(
        SCOPES,
        RemoveProducer(
            producers=[
                genparticles.GenDiBjetPairQuantities,
            ],
            samples=["data", "embedding", "embedding_mc"],
        ),
    )

    # For ttbar samples, top pt weights should be produced
    configuration.add_modification_rule(
        SCOPES,
        AppendProducer(
            producers=[event.TopPtReweighting],
            samples=["ttbar"],
        ),
    )

    # TODO needs to be refined for run 3, not considered at the moment
    #configuration.add_modification_rule(
    #    HAD_TAU_SCOPES,
    #    AppendProducer(
    #        producers=event.ZPtMassReweighting, samples=["dyjets", "electroweak_boson"]
    #    ),
    #)

    # Add Golden JSON filter for data and embedding samples
    configuration.add_modification_rule(
        GLOBAL_SCOPES,
        AppendProducer(
            producers=[event.JSONFilter],
            samples=["data", "embedding"],
        ),
    )

    # Remove generator-level tau quantities in et scope
    configuration.add_modification_rule(
        ET_SCOPES,
        RemoveProducer(
            producers=[genparticles.ETGenDiTauPairQuantities],
            samples=["data"],
        ),
    )

    # Remove generator-level tau quantities in mt scope
    configuration.add_modification_rule(
        MT_SCOPES,
        RemoveProducer(
            producers=[genparticles.MTGenDiTauPairQuantities],
            samples=["data"],
        ),
    )

    # Remove generator-level tau quantities in tt scope
    configuration.add_modification_rule(
        TT_SCOPES,
        RemoveProducer(
            producers=[genparticles.TTGenDiTauPairQuantities],
            samples=["data"],
        ),
    )

    # Remove generator-level dilepton quantities in ee scope
    configuration.add_modification_rule(
        EE_SCOPES,
        RemoveProducer(
            producers=[genparticles.ElElGenPairQuantities],
            samples=["data"],
        ),
    )

    # Remove generator-level dilepton quantities in mm scope
    configuration.add_modification_rule(
        MM_SCOPES,
        RemoveProducer(
            producers=[genparticles.MuMuGenPairQuantities],
            samples=["data"],
        ),
    )

    # Remove generator-level dilepton quantities in mm scope
    configuration.add_modification_rule(
        EM_SCOPES,
        RemoveProducer(
            producers=[genparticles.EMGenDiTauPairQuantities],
            samples=["data"],
        ),
    )

    # Append scale factor producers
    #configuration.add_modification_rule(
    #    MUON_SCOPES,
    #    AppendProducer(
    #        producers=[
    #            scalefactors.MuonIDIso_SF,
    #            scalefactors.SingleMuTriggerSF,
    #        ],
    #        exclude_samples=["data", "embedding", "embedding_mc"],
    #    ),
    #)

    # Output columns for all scopes
    configuration.add_outputs(
        SCOPES,
        [
            q.is_data,
            q.is_embedding,
            q.is_mc,
            nanoAOD.run,
            q.lumi,
            q.npartons,
            nanoAOD.event,
            q.puweight,
            q.lhe_scale_weight,
            q.pt_1,
            q.pt_2,
            q.eta_1,
            q.eta_2,
            q.phi_1,
            q.phi_2,
            q.nfatjets,
            # q.fj_pt_1,
            # q.fj_eta_1,
            # q.fj_phi_1,
            # q.fj_mass_1,
            # q.fj_msoftdrop_1,
            # q.fj_particleNet_XbbvsQCD_1,
            # q.fj_nsubjettiness_2over1_1,
            # q.fj_nsubjettiness_3over2_1,
            # q.fj_pt_2,
            # q.fj_eta_2,
            # q.fj_phi_2,
            # q.fj_mass_2,
            # q.fj_msoftdrop_2,
            # q.fj_particleNet_XbbvsQCD_2,
            # q.fj_nsubjettiness_2over1_2,
            # q.fj_nsubjettiness_3over2_2,
            # q.fj_matched_pt,
            # q.fj_matched_eta,
            # q.fj_matched_phi,
            # q.fj_matched_mass,
            # q.fj_matched_msoftdrop,
            # q.fj_matched_particleNet_XbbvsQCD,
            # q.fj_matched_nsubjettiness_2over1,
            # q.fj_matched_nsubjettiness_3over2,
            q.fj_Xbb_pt,
            q.fj_Xbb_eta,
            q.fj_Xbb_phi,
            q.fj_Xbb_mass,
            q.fj_Xbb_msoftdrop,
            q.fj_Xbb_particleNet_XbbvsQCD,
            q.fj_Xbb_nsubjettiness_2over1,
            q.fj_Xbb_nsubjettiness_3over2,
            q.fj_Xbb_hadflavor,
            q.fj_Xbb_nBhad,
            q.fj_Xbb_nChad,
            q.bpair_pt_1,
            q.bpair_pt_2,
            q.bpair_eta_1,
            q.bpair_eta_2,
            q.bpair_phi_1,
            q.bpair_phi_2,
            q.bpair_mass_1,
            q.bpair_mass_2,
            q.bpair_btag_value_1,
            q.bpair_btag_value_2,
            q.bpair_m_inv,
            q.bpair_deltaR,
            q.bpair_pt_dijet,
            q.genjet_pt_1,
            q.genjet_eta_1,
            q.genjet_phi_1,
            q.genjet_mass_1,
            q.genjet_hadFlavour_1,
            q.genjet_pt_2,
            q.genjet_eta_2,
            q.genjet_phi_2,
            q.genjet_mass_2,
            q.genjet_hadFlavour_2,
            q.genjet_m_inv,
            q.njets,
            q.jet_pt,
            q.jet_eta,
            q.jet_phi,
            q.jet_mass,
            q.jet_id,
            q.jet_deepjet_b_score,
            q.jet_deepjet_b_tagged_medium,
            q.jet_pt_pnet,
            q.jet_pt_pnet_with_neutrino,
            q.jet_pt_pnet_resolution,
            q.jet_pt_nanoaod,
            q.jet_pt_raw_factor,
            q.jpt_1,
            q.jpt_2,
            q.jeta_1,
            q.jeta_2,
            q.jphi_1,
            q.jphi_2,
            q.jtag_value_1,
            q.jtag_value_2,
            q.mjj,
            q.m_vis,
            q.deltaR_ditaupair,
            q.pt_vis,
            q.nbtag,
            # q.bpt_1,
            # q.bpt_2,
            # q.beta_1,
            # q.beta_2,
            # q.bphi_1,
            # q.bphi_2,
            # q.btag_value_1,
            # q.btag_value_2,
            q.btag_weight,
            q.mass_1,
            q.mass_2,
            q.dxy_1,
            q.dxy_2,
            q.dz_1,
            q.dz_2,
            q.q_1,
            q.q_2,
            q.iso_1,
            q.iso_2,
            q.gen_pt_1,
            q.gen_eta_1,
            q.gen_phi_1,
            q.gen_mass_1,
            q.gen_pdgid_1,
            q.gen_pt_2,
            q.gen_eta_2,
            q.gen_phi_2,
            q.gen_mass_2,
            q.gen_pdgid_2,
            q.gen_m_vis,
            q.met,
            q.metphi,
            #q.pfmet,
            #q.pfmetphi,
            q.met_uncorrected,
            q.metphi_uncorrected,
            #q.pfmet_uncorrected,
            #q.pfmetphi_uncorrected,
            q.metSumEt,
            q.metcov00,
            q.metcov01,
            q.metcov10,
            q.metcov11,
            q.pzetamissvis,
            q.mTdileptonMET,
            q.mt_1,
            q.mt_2,
            q.pt_tautau,
            # q.pt_ttjj,
            q.pt_tautaubb,
            q.mass_tautaubb,
            q.mt_tot,
            q.gen_match_1,
            q.gen_match_2,
            # TODO remove these variables as PF MET is not used anymore by us
            #q.pzetamissvis_pf,
            #q.mTdileptonMET_pf,
            #q.mt_1_pf,
            #q.mt_2_pf,
            #q.pt_tt_pf,
            # q.pt_ttjj_pf,
            #q.pt_ttbb_pf,
            #q.mt_tot_pf,
            q.pt_dijet,
            q.jet_hemisphere,
        ],
    )
    if era in ["2018"] and sample not in ["data", "embedding", "embedding_mc"]:
        # in 2018, we have the Xbb tagging scale factors
        configuration.add_outputs(
            SCOPES,
            [
                q.pNet_Xbb_weight,
            ],
        )

    if sample in ["dyjets", "dyjets_madgraph", "dyjets_powheg", "dyjets_amcatnlo_ll", "dyjets_amcatnlo_tt"]:
        configuration.add_outputs(
            SCOPES,
            [
                q.lhe_drell_yan_decay_flavor,
            ]
        )

    # add genWeight for everything but data
    if sample != "data":
        configuration.add_outputs(
            SCOPES,
            [
                nanoAOD.genWeight,
            ],
        )

    # jet vetomap selection only applies to Run 3 analyses
    if era in ERAS_RUN3:
        configuration.add_outputs(
            SCOPES,
            [
                q.jet_vetomap_veto,

            ],
        )

    configuration.add_outputs(
        "mt",
        [
            q.nmuons,
            q.ntaus,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            triggers.SingleMuTriggerFlags.output_group,
            triggers.DoubleMuTauTriggerFlags.output_group,
            # triggers.MTGenerateCrossTriggerFlags.output_group,
            # triggers.GenerateSingleTrailingTauTriggerFlags.output_group,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dimuon_veto,
            q.dilepton_veto,
            q.id_wgt_mu_1,
            q.iso_wgt_mu_1,
        ],
    )

    # add the old MVA ID scale factor producers only for Run 2 eras (not available for Run 3)
    if era in ERAS_RUN2:
        configuration.add_outputs(
            "mt",
            [
                scalefactors.Tau_2_VsJetTauID_lt_SF.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run2.output_group,
            ],
        )
    elif era in ERAS_RUN3:
        configuration.add_outputs(
            "mt",
            [
                p
                for p in scalefactors.DoubleMuTauTriggerSF.get_outputs("mt")
            ] + [
                p
                for p in scalefactors.MuonIDIso_SF.get_outputs("mt")

            ] + [
                scalefactors.SingleMuTriggerSF.output_group,
                scalefactors.Tau_2_VsJetTauID_SF.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run3.output_group,
            ],
        )

    configuration.add_outputs(
        "et",
        [
            p
            for p in scalefactors.DoubleEleTauTriggerSF.get_outputs("et")
        ]
        + [
            q.nelectrons,
            q.ntaus,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            triggers.SingleEleTriggerFlags.output_group,
            triggers.DoubleEleTauTriggerFlags.output_group,
            scalefactors.SingleEleTriggerSF.output_group,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dielectron_veto,
            q.dilepton_veto,
            # q.id_wgt_ele_wp90nonIso_1,
            # q.id_wgt_ele_wp80nonIso_1,
        ],
    )

    # add the old MVA ID scale factor producers only for Run 2 eras (not available for Run 3)
    if era in ERAS_RUN2:
        configuration.add_outputs(
            "et",
            [
                scalefactors.Tau_2_VsJetTauID_lt_SF.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run2.output_group,
            ],
        )
    elif era in ERAS_RUN3:
        configuration.add_outputs(
            "et",
            [
                p
                for p in scalefactors.EleID_SF.get_outputs("et")
            ]
            + [
                scalefactors.Tau_2_VsJetTauID_SF.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run3.output_group,
            ],
        )


    configuration.add_outputs(
        "tt",
        [
            q.ntaus,
            scalefactors.Tau_1_VsMuTauID_SF.output_group,
            scalefactors.Tau_2_VsMuTauID_SF.output_group,
            pairquantities.VsJetTauIDFlag_1.output_group,
            pairquantities.VsEleTauIDFlag_1.output_group,
            pairquantities.VsMuTauIDFlag_1.output_group,
            pairquantities.VsJetTauIDFlag_2.output_group,
            pairquantities.VsEleTauIDFlag_2.output_group,
            pairquantities.VsMuTauIDFlag_2.output_group,
            triggers.DoubleTauTauTriggerFlags.output_group,
        ] + [
                producer.output_group
                for producer in double_tau_jet_trigger_producers
        ] + [
            # q.taujet_pt_1,
            # q.taujet_pt_2,
            # q.gen_taujet_pt_2,
            q.tau_decaymode_1,
            q.tau_decaymode_2,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dimuon_veto,
            q.dilepton_veto,
            q.fj_leading_pt,
            q.fj_leading_msoftdrop,
        ],
    )

    # add the old MVA ID scale factor producers only for Run 2 eras (not available for Run 3)
    if era in ERAS_RUN2:
        configuration.add_outputs(
            "tt",
            [
                scalefactors.Tau_1_VsJetTauID_tt_SF.output_group,
                scalefactors.Tau_2_VsJetTauID_tt_SF.output_group,
                scalefactors.Tau_1_VsEleTauID_SF_Run2.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run2.output_group,
            ],
        )
    elif era in ERAS_RUN3:
        configuration.add_outputs(
            "tt",
            [
                p
                for p in scalefactors.DoubleTauTauTriggerSF.get_outputs("tt")
            ] + [
                scalefactors.Tau_1_VsJetTauID_SF.output_group,
                scalefactors.Tau_2_VsJetTauID_SF.output_group,
                scalefactors.Tau_1_VsEleTauID_SF_Run3.output_group,
                scalefactors.Tau_2_VsEleTauID_SF_Run3.output_group,
            ],
        )

    if "data" not in sample:
        configuration.add_outputs(
            "tt",
            [
                #q.trg_wgt_double_tau_1,
                #q.trg_wgt_double_tau_2,
                #q.trg_wgt_fatjet,  TODO rework trigger setup before enabling this
            ],
        )

    # Outputs for the mm scope
    configuration.add_outputs(
        "mm",
        [
            q.nmuons,
            triggers.SingleMuTriggerFlags.output_group,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dielectron_veto,
        ] + scalefactors.MuonIDIso_SF.get_outputs("mm")
        + scalefactors.SingleMuTriggerSF.get_outputs("mm"),
    )

    # Outputs for the ee scope
    configuration.add_outputs(
        "ee",
        [
            q.nelectrons,
            triggers.SingleEleTriggerFlags.output_group,
            q.muon_veto_flag,
            q.electron_veto_flag,
            q.dimuon_veto,
        ] + scalefactors.EleID_SF.get_outputs("ee")
        + scalefactors.SingleEleTriggerSF.get_outputs("ee"),
    )

    # Outputs for the em scope
    configuration.add_outputs(
        "em",
        [
            q.nelectrons,
            q.nmuons,
            triggers.SingleEleTriggerFlags.output_group,
            triggers.SingleMuTriggerFlags.output_group,
            triggers.DoubleEleMuTriggerFlags.output_group,
            q.electron_veto_flag,
            q.muon_veto_flag,
            q.dilepton_veto,
        ] + scalefactors.EleID_SF.get_outputs("em")
        + scalefactors.MuonIDIso_SF.get_outputs("em")
        + scalefactors.SingleEleTriggerSF.get_outputs("em")
        + scalefactors.SingleMuTriggerSF.get_outputs("em"),
    )

    # TODO re-include
    #if sample in ["nmssm_Ybb", "nmssm_Ytautau"]:
    #    configuration.add_outputs(
    #        HAD_TAU_SCOPES,
    #        [
    #            q.gen_b_pt_1,
    #            q.gen_b_eta_1,
    #            q.gen_b_phi_1,
    #            q.gen_b_mass_1,
    #            q.gen_b_pt_2,
    #            q.gen_b_eta_2,
    #            q.gen_b_phi_2,
    #            q.gen_b_mass_2,
    #            q.gen_b_m_inv,
    #            q.gen_b_deltaR,
    #            q.gen_bpair_match_flag,
    #            q.gen_tau_pt_1,
    #            q.gen_tau_eta_1,
    #            q.gen_tau_phi_1,
    #            q.gen_tau_mass_1,
    #            q.gen_tau_pt_2,
    #            q.gen_tau_eta_2,
    #            q.gen_tau_phi_2,
    #            q.gen_tau_mass_2,
    #            q.gen_tau_m_inv,
    #            q.gen_tau_deltaR,
    #        ],
    #    )

    #########################
    # LHE Scale Weight variations
    # up is muR=2.0, muF=2.0
    # down is muR=0.5, muF=0.5
    #########################
    if sample in ["ggh", "qqh"]:
        configuration.add_shift(
            SystematicShift(
                "muRWeightUp",
                shift_config={
                    "global": {
                        "muR": 2.0,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muRWeightDown",
                shift_config={
                    "global": {
                        "muR": 0.5,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightUp",
                shift_config={
                    "global": {
                        "muF": 2.0,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightDown",
                shift_config={
                    "global": {
                        "muF": 0.5,
                    }
                },
                producers={"global": [event.LHE_Scale_weight]},
            )
        )
    if sample in ["nmssm_Ybb", "nmssm_Ytautau"]:
        configuration.add_shift(
            SystematicShift(
                "muRWeightUp",
                shift_config={
                    "global": {
                        "muR": 2.0,
                    }
                },
                producers={"global": [event.NMSSM_LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muRWeightDown",
                shift_config={
                    "global": {
                        "muR": 0.5,
                    }
                },
                producers={"global": [event.NMSSM_LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightUp",
                shift_config={
                    "global": {
                        "muF": 2.0,
                    }
                },
                producers={"global": [event.NMSSM_LHE_Scale_weight]},
            )
        )
        configuration.add_shift(
            SystematicShift(
                "muFWeightDown",
                shift_config={
                    "global": {
                        "muF": 0.5,
                    }
                },
                producers={"global": [event.NMSSM_LHE_Scale_weight]},
            )
        )

    #########################
    # Lepton to tau fakes energy scalefactor shifts  #
    #########################
    if "dyjets" in sample or "electroweak_boson" in sample:
        configuration.add_shift(
            SystematicShift(
                name="tauMuFakeEsDown",
                shift_config={
                    "mt": {
                        "tau_mufake_es": "down",
                    }
                },
                producers={"mt": [taus.TauPtCorrection_muFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauMuFakeEsUp",
                shift_config={
                    "mt": {
                        "tau_mufake_es": "up",
                    }
                },
                producers={"mt": [taus.TauPtCorrection_muFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongBarrelDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_barrel": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongBarrelUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_barrel": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongEndcapDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_endcap": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prongEndcapUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM0_endcap": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroBarrelDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_barrel": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroBarrelUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_barrel": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroEndcapDown",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_endcap": "down",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="tauEleFakeEs1prong1pizeroEndcapUp",
                shift_config={
                    "et": {
                        "tau_elefake_es_DM1_endcap": "up",
                    }
                },
                producers={"et": [taus.TauPtCorrection_eleFake]},
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )

    #########################
    # Electron energy correction shifts
    #########################

    if era in ERAS_RUN2:
        configuration.add_shift(
            SystematicShift(
                name="eleEsResoUp",
                shift_config={
                    ("global"): {"ele_es_variation": "resolutionUp"},
                },
                producers={
                    ("global"): [
                        (
                            electrons.ElectronPtCorrectionMCRun2
                            if era in ERAS_RUN2
                            else electrons.ElectronPtCorrectionMCRun3
                        )
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="eleEsResoDown",
                shift_config={
                    ("global"): {"ele_es_variation": "resolutionDown"},
                },
                producers={
                    ("global"): [
                        (
                            electrons.ElectronPtCorrectionMCRun2
                            if era in ERAS_RUN2
                            else electrons.ElectronPtCorrectionMCRun3
                        )
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="eleEsScaleUp",
                shift_config={
                    ("global"): {"ele_es_variation": "scaleUp"},
                },
                producers={
                    ("global"): [
                        (
                            electrons.ElectronPtCorrectionMCRun2
                            if era in ERAS_RUN2
                            else electrons.ElectronPtCorrectionMCRun3
                        )
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="eleEsScaleDown",
                shift_config={
                    ("global"): {"ele_es_variation": "scaleDown"},
                },
                producers={
                    ("global"): [
                        (
                            electrons.ElectronPtCorrectionMCRun2
                            if era in ERAS_RUN2
                            else electrons.ElectronPtCorrectionMCRun3
                        )
                    ],
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )

    #########################
    # MET Shifts
    #########################
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnUp",
            quantity_change={
                nanoAOD.PuppiMET_pt: "PuppiMET_ptUnclusteredUp",
                nanoAOD.PuppiMET_phi: "PuppiMET_phiUnclusteredUp",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShiftByQuantity(
            name="metUnclusteredEnDown",
            quantity_change={
                nanoAOD.PuppiMET_pt: "PuppiMET_ptUnclusteredDown",
                nanoAOD.PuppiMET_phi: "PuppiMET_phiUnclusteredDown",
            },
            scopes=["global"],
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    #########################
    # Prefiring Shifts
    #########################
    if era != "2018":
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringDown",
                quantity_change={
                    nanoAOD_run2.L1PreFiringWeight_Nom: nanoAOD_run2.L1PreFiringWeight_Dn,
                },
                scopes=["global"],
            )
        )
        configuration.add_shift(
            SystematicShiftByQuantity(
                name="prefiringUp",
                quantity_change={
                    nanoAOD_run2.L1PreFiringWeight_Nom: nanoAOD_run2.L1PreFiringWeight_Up,
                },
                scopes=["global"],
            )
        )
    #########################
    # particleNet Xbb scale factor uncertainties
    #########################

    # add Xbb tagging scale factor shifts for 2018
    # TODO also provide these scale factors for other eras
    if era in ["2018"]:
        configuration.add_shift(
            SystematicShift(
                name="pNetXbbSFUp",
                shift_config={
                    ("mt", "et", "tt"): {"pNetXbb_sf_variation": "up"},
                },
                producers={
                    ("mt", "et", "tt"): {
                        scalefactors.Xbb_tagging_SF,
                    }
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )
        configuration.add_shift(
            SystematicShift(
                name="pNetXbbSFDown",
                shift_config={
                    ("mt", "et", "tt"): {"pNetXbb_sf_variation": "down"},
                },
                producers={
                    ("mt", "et", "tt"): {
                        scalefactors.Xbb_tagging_SF,
                    }
                },
            ),
            exclude_samples=["data", "embedding", "embedding_mc"],
        )

    #########################
    # MET Recoil Shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResponseUp",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": False,
                    "apply_recoil_response_systematic": True,
                    "recoil_systematic_shift_up": True,
                    "recoil_systematic_shift_down": False,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResponseDown",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": False,
                    "apply_recoil_response_systematic": True,
                    "recoil_systematic_shift_up": False,
                    "recoil_systematic_shift_down": True,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResolutionUp",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": True,
                    "apply_recoil_response_systematic": False,
                    "recoil_systematic_shift_up": True,
                    "recoil_systematic_shift_down": False,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )
    configuration.add_shift(
        SystematicShift(
            name="metRecoilResolutionDown",
            shift_config={
                ("et", "mt", "tt", "mm"): {
                    "apply_recoil_resolution_systematic": True,
                    "apply_recoil_response_systematic": False,
                    "recoil_systematic_shift_up": False,
                    "recoil_systematic_shift_down": True,
                },
            },
            producers={
                ("et", "mt", "tt", "mm"): [
                    met.ApplyRecoilCorrections,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc", "ttbar", "diboson", "singletop"],
    )

    #########################
    # Pileup Shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="PileUpUp",
            scopes=["global"],
            shift_config={
                ("global"): {"PU_reweighting_variation": "up"},
            },
            producers={
                "global": [
                    event.PUweights,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    configuration.add_shift(
        SystematicShift(
            name="PileUpDown",
            scopes=["global"],
            shift_config={
                ("global"): {"PU_reweighting_variation": "down"},
            },
            producers={
                "global": [
                    event.PUweights,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    #########################
    # Electron id/iso sf shifts
    #########################

    configuration.add_shift(
        SystematicShift(
            name="electronIdSFUp",
            scopes=["et"],
            shift_config={
                ("et"): {"ele_sf_variation": "sfup"},
            },
            producers={
                ("et"): [
                    scalefactors.EleID_SF,
                ],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="electronIdSFDown",
            scopes=["et"],
            shift_config={
                ("et"): {"ele_sf_variation": "sfdown"},
            },
            producers={
                ("et"): [
                    scalefactors.EleID_SF,
                ],
            },
        )
    )

    #########################
    # Muon id/iso sf shifts
    #########################

    configuration.add_shift(
        SystematicShift(
            name="muonIdSFUp",
            scopes=["mt"],
            shift_config={
                ("mt"): {"muon_id_sf_variation": "systup"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIdSFDown",
            scopes=["mt"],
            shift_config={
                ("mt"): {"muon_id_sf_variation": "systdown"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIsoSFUp",
            scopes=["mt"],
            shift_config={
                ("mt"): {"muon_iso_sf_variation": "syst_up"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )
    configuration.add_shift(
        SystematicShift(
            name="muonIsoSFDown",
            scopes=["mt"],
            shift_config={
                ("mt"): {"muon_iso_sf_variation": "syst_down"},
            },
            producers={
                ("mt"): [
                    scalefactors.MuonIDIso_SF,
                ],
            },
        ),
        exclude_samples=["data", "embedding", "embedding_mc"],
    )

    #########################
    # Trigger shifts
    #########################

    #
    # systematic shifts for single electron trigger corrections
    #

    if era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]:
        for _variation in ["up", "down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"singleEleTriggerSF{_variation.upper()}",
                    shift_config={
                        ("et"): {
                            "single_ele_trigger_sf": [
                                {
                                    "e_trigger_flagname": "trg_wgt_single_ele30",
                                    "e_trigger_sf_name": "HLT_SF_Ele30_MVAiso90ID",
                                    "e_trigger_variation": f"sf{_variation}",
                                },
                            ],
                        }
                    },
                    producers={("et"): scalefactors.SingleEleTriggerSF},
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )

    #
    # systematic shifts for double electron-tau trigger corrections
    #

    if era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]:
        for _variation in ["up", "down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"doubleEleTauTriggerSF{_variation.upper()}",
                    shift_config={
                        ("et"): {
                            "double_eletau_trigger_leg1_sf": [
                                {
                                    "et_trigger_leg1_flagname": "trg_wgt_double_ele24tau30_leg1",
                                    "et_trigger_leg1_sf_file": EraModifier(
                                        {
                                            **{
                                                _era: "DOES_NOT_EXIST"  # TODO does not exist for Run2 eras
                                                for _era in ERAS_RUN2
                                            },
                                            **{
                                                _era: f"data/hleprare/TriggerScaleFactors/{_era}/CrossEleTauHlt_EleLeg_v1.json"
                                                for _era in ERAS_RUN3
                                            },
                                        }
                                    ),
                                    "et_trigger_leg1_era": EraModifier(
                                        {
                                            **{
                                                _era: "DOES_NOT_EXIST"  # TODO does not exist for Run2 eras as correctionlib
                                                for _era in ERAS_RUN2
                                            },
                                            "2022preEE": "2022Re-recoBCD",
                                            "2022postEE": "2022Re-recoE+PromptFG ",
                                            "2023preBPix": "2023PromptC",
                                            "2023postBPix": "2023PromptD",
                                        }
                                    ),
                                    "et_trigger_leg1_sf_name": "Electron-HLT-SF",
                                    "et_trigger_leg1_path_id_name": "HLT_SF_Ele30_MVAiso90ID",
                                    "et_trigger_leg1_variation": f"sf{_variation}",
                                },
                            ],
                            "double_eletau_trigger_leg2_sf": [
                                {
                                    "et_trigger_leg2_flagname": "trg_wgt_double_ele24tau30_leg2",
                                    "et_trigger_leg2_sf_name": "etau",
                                    "et_trigger_leg2_variation": _variation,
                                },
                            ]
                        },
                    },
                    producers={
                        ("et"): [
                            scalefactors.DoubleEleTauTriggerSF,
                        ],
                    },
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )

    #
    # systematic shifts for single muon trigger corrections
    #

    # TODO check run 2 eras
    if era in ["2016preVFP", "2016postVFP", "2017", "2018", "2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]:
        for _variation in ["up", "down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"singleMuTriggerSF{_variation.upper()}",
                    shift_config={
                        ("mt"): {
                            "single_mu_trigger_sf": [
                                {
                                    "m_trigger_flagname": "trg_wgt_single_mu24",
                                    "m_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "m_trigger_variation": f"syst{_variation}",
                                },
                            ],
                        }
                    },
                    producers={("mt"): scalefactors.SingleMuTriggerSF},
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )

    #
    # systematic shifts for double muon-tau trigger corrections
    #

    if era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]:
        for _variation in ["up", "down"]:
            configuration.add_shift(
                SystematicShift(
                    name=f"doubleMuTauTriggerSF{_variation.upper()}",
                    shift_config={
                        ("mt"): {
                            "double_mutau_trigger_leg1_sf": [
                                {
                                    "mt_trigger_leg1_sf_file": EraModifier(
                                        {
                                            _era: f"data/hleprare/TriggerScaleFactors/{_era}/CrossMuTauHlt_MuLeg_v1.json"
                                            for _era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]
                                        }
                                    ),
                                    "mt_trigger_leg1_flagname": "trg_wgt_double_mu20tau27_leg1",
                                    "mt_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                                    "mt_trigger_leg1_variation": f"syst{_variation}",
                                },
                            ],
                            "double_mutau_trigger_leg2_sf": [
                                {
                                    "mt_trigger_leg2_flagname": "trg_wgt_double_mu20tau27_leg2",
                                    "mt_trigger_leg2_sf_name": "mutau",
                                    "mt_trigger_leg2_variation": _variation,
                                },
                            ],
                        },
                    },
                    producers={
                        ("mt"): [
                            scalefactors.DoubleMuTauTriggerSF,
                        ],
                    },
                ),
                exclude_samples=["data", "embedding", "embedding_mc"],
            )

    #configuration.add_shift(
    #    SystematicShift(
    #        name="ditauTriggerSFUp",
    #        shift_config={("tt"): {"ditau_trigger_syst": "up"}},
    #        producers={
    #            ("tt"): scalefactors.TTGenerateDoubleTauTriggerSF_MC,
    #        },
    #    ),
    #    exclude_samples=["data", "embedding", "embedding_mc"],
    #)
    #configuration.add_shift(
    #    SystematicShift(
    #        name="ditauTriggerSFDown",
    #        shift_config={("tt"): {"ditau_trigger_syst": "down"}},
    #        producers={
    #            ("tt"): scalefactors.TTGenerateDoubleTauTriggerSF_MC,
    #        },
    #    ),
    #    exclude_samples=["data", "embedding", "embedding_mc"],
    #)

    #########################
    # TauID scale factor shifts, channel dependent # Tau energy scale shifts, dm dependent
    #########################
    if era in ERAS_RUN2:
        add_tauVariations(
            configuration,
            scalefactors.Tau_1_VsEleTauID_SF_Run2,
            scalefactors.Tau_2_VsEleTauID_SF_Run2,
            sample,
        )
    elif era in ERAS_RUN3:
        add_tauVariations(
            configuration,
            scalefactors.Tau_1_VsEleTauID_SF_Run3,
            scalefactors.Tau_2_VsEleTauID_SF_Run3,
            sample,
        )

    #########################
    # Import triggersetup   #
    #########################
    add_diTauTriggerSetup(configuration)
    #########################
    # Add additional producers and SFs related to embedded samples
    #########################
    if sample == "embedding" or sample == "embedding_mc":
        setup_embedding(configuration, HAD_TAU_SCOPES)

    #########################
    # Jet energy resolution and jet energy scale
    #########################
    add_jetVariations(configuration, era)

    #########################
    # btagging scale factor shape variation
    #########################
    add_btagVariations(configuration)

    #########################
    # Jet energy correction for data
    #########################
    # add_jetCorrectionData(configuration, era)

    #########################
    # Finalize and validate the configuration
    #########################
    configuration.optimize()
    configuration.validate()
    configuration.report()
    return configuration.expanded_configuration()
