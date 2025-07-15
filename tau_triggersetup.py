from code_generation.configuration import Configuration
from code_generation.modifiers import EraModifier

from .constants import M_SCOPES, MT_SCOPES, ERAS_RUN2, ERAS_RUN3


def add_diTauTriggerSetup(configuration: Configuration):
    ## MT, MM scope trigger setup
    configuration.add_config_parameters(
        M_SCOPES,
        {
            "single_mu_trigger": EraModifier(
                {
                    **{
                        _era: [
                            # trigger:            HLT_IsoMu24
                            # final filter:       hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 OR hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p08 OR hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered
                            # filter bit:         2
                            # documentation:      https://twiki.cern.ch/twiki/bin/view/CMS/MuonHLT2022
                            {
                                "flagname": "trg_single_mu24",
                                "hlt_path": "HLT_IsoMu24",
                                "min_pt": 26,
                                "max_abs_eta": 2.4,
                                "filter_bit": 2,
                                "particle_id": 13,
                                "match_max_delta_r": 0.4,
                            },
                        ]
                        for _era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]
                    },
                    "2018": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "min_pt": 26,
                            "max_abs_eta": 2.1,
                            "filter_bit": -1,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "min_pt": 28,
                            "max_abs_eta": 2.1,
                            "filter_bit": -1,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_mu50",
                        #     "hlt_path": "HLT_Mu50",
                        #     "ptcut": 55,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 13,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "min_pt": 25,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu27",
                            "hlt_path": "HLT_IsoMu27",
                            "min_pt": 28,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "min_pt": 25,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_mu22",
                            "hlt_path": "HLT_IsoMu22",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk",
                            "hlt_path": "HLT_IsoTkMu22",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_eta2p1",
                            "hlt_path": "HLT_IsoMu22_eta2p1",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu22_tk_eta2p1",
                            "hlt_path": "HLT_IsoTkMu22_eta2p1",
                            "min_pt": 23,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "min_pt": 25,
                            "max_abs_eta": 2.5,
                            "filter_bit": 3,
                            "particle_id": 13,
                            "match_max_delta_r": 0.4,
                        },
                    ],
                }
            ),
            "boosted_singlemuon_trigger": EraModifier(
                {
                    # TODO placeholder for Run3 and 2016-2017 eras, add these triggers also there
                    **{
                        _era: []
                        for _era in ERAS_RUN3 + ["2016preVFP", "2016postVFP", "2017"]
                    },
                    "2018": [
                        {
                            "flagname": "trg_single_mu24_boosted",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_mu27_boosted",
                        #     "hlt_path": "HLT_IsoMu27",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 13,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_mu50_boosted",
                            "hlt_path": "HLT_Mu50",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_oldmu100_boosted",
                            "hlt_path": "HLT_OldMu100",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_tkmu100_boosted",
                            "hlt_path": "HLT_TkMu100",
                            "ptcut": 50,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )
    configuration.add_config_parameters(
        MT_SCOPES,
        {
            "double_mutau_trigger": EraModifier(
                {
                    **{
                        _era: [
                            # trigger:            HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1
                            # final filter muon:  hltL3crIsoBigORMu18erTauXXer2p1L1f0L2f10QL3f20QL3trkIsoFiltered
                            # filter bit muon:    3
                            # final filter tau:   hltHpsOverlapFilterIsoMu20LooseMuTauWPDeepTauPFTau27L1Seeded
                            # filter bit tau:     9
                            # documentation:      https://twiki.cern.ch/twiki/bin/view/CMS/TauTrigger#Trigger_Table_for_2022
                            #                     https://twiki.cern.ch/twiki/bin/view/CMS/TauTrigger#Trigger_Table_for_2023
                            {
                                "flagname": "trg_mu20tau27",
                                "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                                "p1_min_pt": 20,
                                "p1_max_abs_eta": 2.1,
                                "p1_particle_id": 13,
                                "p1_filter_bit": 3,
                                "p2_min_pt": 27,
                                "p2_max_abs_eta": 2.1,
                                "p2_particle_id": 15,
                                "p2_filter_bit": 9,
                                "match_max_delta_r": 0.4,
                            }
                        ]
                        for _era in ["2022preEE", "2022postEE", "2023preBPix", "2023postBPix"]
                    },
                    "2018": [
                        {
                            "flagname": "trg_cross_mu20tau27_hps",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1",
                            "p1_min_pt": 21,
                            "p1_max_abs_eta": 2.1,
                            "p1_filter_bit": 3,
                            "p1_particle_id": 13,
                            "p2_min_pt": 32,
                            "p2_max_abs_eta": 2.1,
                            "p2_filter_bit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_particle_id": 15,
                            "match_max_delta_r": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_min_pt": 21,
                            "p1_max_abs_eta": 2.1,
                            "p1_filter_bit": 3,
                            "p1_particle_id": 13,
                            "p2_min_pt": 32,
                            "p2_max_abs_eta": 2.1,
                            "p2_filter_bit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_particle_id": 15,
                            "match_max_delta_r": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_cross_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseChargedIsoPFTau27_eta2p1_CrossL1",
                            "p1_min_pt": 21,
                            "p1_max_abs_eta": 2.1,
                            "p1_filter_bit": 3,
                            "p1_particle_id": 13,
                            "p2_min_pt": 32,
                            "p2_max_abs_eta": 2.1,
                            "p2_filter_bit": 4,
                            "p2_particle_id": 15,
                            "match_max_delta_r": 0.4,
                        }
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_min_pt": 20,
                            "p1_max_abs_eta": 2.1,
                            "p1_filter_bit": 3,
                            "p1_particle_id": 13,
                            "p2_min_pt": 22,
                            "p2_max_abs_eta": 2.1,
                            "p2_filter_bit": 4,
                            "p2_particle_id": 15,
                            "match_max_delta_r": 0.4,
                        }
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_mu19tau20",
                            "hlt_path": "HLT_IsoMu19_eta2p1_LooseIsoPFTau20_SingleL1",
                            "p1_min_pt": 20,
                            "p1_max_abs_eta": 2.1,
                            "p1_filter_bit": 3,
                            "p1_particle_id": 13,
                            "p2_min_pt": 22,
                            "p2_max_abs_eta": 2.1,
                            "p2_filter_bit": 4,
                            "p2_particle_id": 15,
                            "match_max_delta_r": 0.4,
                        }
                    ],
                }
            ),
        },
    )
    ## ET, EE scope trigger setup
    configuration.add_config_parameters(
        ["et"],
        {
            "singleelectron_trigger": EraModifier(
                {
                    # TODO placeholder for Run3 eras, add these triggers also there
                    **{
                        _era: []
                        for _era in ERAS_RUN3
                    },
                    "2018": [
                        # {
                        #     "flagname": "trg_single_ele27",
                        #     "hlt_path": "HLT_Ele27_WPTight_Gsf",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_single_ele27",
                            "hlt_path": "HLT_Ele27_WPTight_Gsf",
                            "ptcut": 28,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele32",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_ele35",
                            "hlt_path": "HLT_Ele35_WPTight_Gsf",
                            "ptcut": 36,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_single_ele25",
                            "hlt_path": "HLT_Ele25_eta2p1_WPTight_Gsf",
                            "ptcut": 26,
                            "etacut": 2.1,
                            "filterbit": 1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            "boosted_singleelectron_trigger": EraModifier(
                {
                    # TODO placeholders, add triggers for 2018
                    **{
                        _era: []
                        for _era in ERAS_RUN3
                    },
                    "2018": [
                        # {
                        #     "flagname": "trg_single_ele27_boosted",
                        #     "hlt_path": "HLT_Ele27_WPTight_Gsf",
                        #     "ptcut": 28,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele32_boosted",
                            "hlt_path": "HLT_Ele32_WPTight_Gsf",
                            "ptcut": 33,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # {
                        #     "flagname": "trg_single_ele35_boosted",
                        #     "hlt_path": "HLT_Ele35_WPTight_Gsf",
                        #     "ptcut": 36,
                        #     "etacut": 2.1,
                        #     "filterbit": -1,
                        #     "trigger_particle_id": 11,
                        #     "max_deltaR_triggermatch": 0.4,
                        # },
                        {
                            "flagname": "trg_single_ele115_boosted",
                            "hlt_path": "HLT_Ele115_CaloIdVT_GsfTrkIdT",
                            "ptcut": 115,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_single_photon200_boosted",
                            "hlt_path": "HLT_Photon200",
                            "ptcut": 115,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 11,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )
    # ET scope crosstrigger
    configuration.add_config_parameters(
        ["et"],
        {
            "eltau_cross_trigger": EraModifier(
                {
                    # TODO placeholder for Run3 eras, add these triggers also there
                    **{
                        _era: []
                        for _era in ERAS_RUN3
                    },
                    "2018": [
                        {
                            "flagname": "trg_cross_ele24tau30_hps",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 4, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTau30_eta2p1_CrossL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_cross_ele24tau20",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_cross_ele24tau20",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20_SingleL1",
                            "p1_ptcut": 25,
                            "p2_ptcut": 32,
                            "p1_etacut": 2.5,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau20_crossL1",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau20",
                            "p1_ptcut": 25,
                            "p2_ptcut": 25,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_cross_ele24tau30",
                            "hlt_path": "HLT_Ele24_eta2p1_WPLoose_Gsf_LooseIsoPFTau30",
                            "p1_ptcut": 25,
                            "p2_ptcut": 35,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 1,
                            "p1_trigger_particle_id": 11,
                            "p2_filterbit": 4,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
        },
    )

    ## TT scope trigger setup
    configuration.add_config_parameters(
        ["tt"],
        {
            "doubletau_trigger": EraModifier(
                {
                    # TODO placeholder for Run3 eras, add these triggers also there
                    **{
                        _era: []
                        for _era in ERAS_RUN3
                    },
                    "2018": [
                        {
                            "flagname": "trg_double_tau35_mediumiso_hps",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        # the non HPS version exists for data only, but add it anyway to have the flag in the ntuple
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p2_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": -1,  # TODO switch to "p1_filterbit": 6, if the bits are correct
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2017": [
                        {
                            "flagname": "trg_double_tau40_tightiso",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau40_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau40_mediumiso_tightid",
                            "hlt_path": "HLT_DoubleMediumChargedIsoPFTau40_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_tightiso_tightid",
                            "hlt_path": "HLT_DoubleTightChargedIsoPFTau35_Trk1_TightID_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016preVFP": [
                        {
                            "flagname": "trg_double_tau35_mediumiso",
                            "hlt_path": "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                    "2016postVFP": [
                        {
                            "flagname": "trg_double_tau35_mediumiso",
                            "hlt_path": "HLT_DoubleMediumIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                        {
                            "flagname": "trg_double_tau35_mediumcombiso",
                            "hlt_path": "HLT_DoubleMediumCombinedIsoPFTau35_Trk1_eta2p1_Reg",
                            "p1_ptcut": 40,
                            "p2_ptcut": 40,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": 6,
                            "p1_trigger_particle_id": 15,
                            "p2_filterbit": 6,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        },
                    ],
                }
            ),
            "boosted_ditau_trigger": EraModifier(
                {
                    # TODO placeholder for Run3 eras, add these triggers also there
                    **{
                        _era: []
                        for _era in ERAS_RUN3
                    },
                    "2018": [
                        # {
                        #     "flagname": "trg_ak8pfht750_trimmass50",
                        #     "hlt_path": "HLT_AK8PFHT750_TrimMass50",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfht800_trimmass50",
                        #     "hlt_path": "HLT_AK8PFHT800_TrimMass50",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet60",
                        #     "hlt_path": "HLT_AK8PFJet60",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet80",
                        #     "hlt_path": "HLT_AK8PFJet80",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet140",
                        #     "hlt_path": "HLT_AK8PFJet140",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet200",
                        #     "hlt_path": "HLT_AK8PFJet200",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet260",
                        #     "hlt_path": "HLT_AK8PFJet260",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet320",
                        #     "hlt_path": "HLT_AK8PFJet320",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet400",
                        #     "hlt_path": "HLT_AK8PFJet400",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet40",
                        #     "hlt_path": "HLT_AK8PFJet40",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet450",
                        #     "hlt_path": "HLT_AK8PFJet450",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet500",
                        #     "hlt_path": "HLT_AK8PFJet500",
                        # },
                        # {
                        #     "flagname": "trg_ak8pfjet360_trimmass30",
                        #     "hlt_path": "HLT_AK8PFJet360_TrimMass30",
                        # },
                        {
                            "flagname": "trg_ak8pfjet400_trimmass30",
                            "hlt_path": "HLT_AK8PFJet400_TrimMass30",
                        },
                        # {
                        #     "flagname": "trg_pfht250",
                        #     "hlt_path": "HLT_PFHT250",
                        # },
                        # {
                        #     "flagname": "trg_pfht350",
                        #     "hlt_path": "HLT_PFHT350",
                        # },
                        # {
                        #     "flagname": "trg_pfjet40",
                        #     "hlt_path": "HLT_PFJet40",
                        # },
                        # {
                        #     "flagname": "trg_pfjet60",
                        #     "hlt_path": "HLT_PFJet60",
                        # },
                        # {
                        #     "flagname": "trg_pfjet80",
                        #     "hlt_path": "HLT_PFJet80",
                        # },
                        # {
                        #     "flagname": "trg_pfjet140",
                        #     "hlt_path": "HLT_PFJet140",
                        # },
                        # {
                        #     "flagname": "trg_pfjet200",
                        #     "hlt_path": "HLT_PFJet200",
                        # },
                        # {
                        #     "flagname": "trg_pfjet260",
                        #     "hlt_path": "HLT_PFJet260",
                        # },
                        # {
                        #     "flagname": "trg_pfjet320",
                        #     "hlt_path": "HLT_PFJet320",
                        # },
                        # {
                        #     "flagname": "trg_pfjet400",
                        #     "hlt_path": "HLT_PFJet400",
                        # },
                        # {
                        #     "flagname": "trg_pfjet450",
                        #     "hlt_path": "HLT_PFJet450",
                        # },
                        # {
                        #     "flagname": "trg_pfjet500",
                        #     "hlt_path": "HLT_PFJet500",
                        # },
                        # {
                        #     "flagname": "trg_pfjet550",
                        #     "hlt_path": "HLT_PFJet550",
                        # },
                        {
                            "flagname": "trg_pfht500_pfmet100_pfmht100_idtight",
                            "hlt_path": "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
                        },
                        # {
                        #     "flagname": "trg_pfht500_pfmet110_pfmht110_idtight",
                        #     "hlt_path": "HLT_PFHT500_PFMET110_PFMHT110_IDTight",
                        # },
                        # {
                        #     "flagname": "trg_pfmet110_pfmht110_idtight",
                        #     "hlt_path": "HLT_PFMET110_PFMHT110_IDTight",
                        # },
                        {
                            "flagname": "trg_pfmet120_pfmht120_idtight",
                            "hlt_path": "HLT_PFMET120_PFMHT120_IDTight",
                        },
                        # {
                        #     "flagname": "trg_pfmetnomu110_pfmhtnomu110_idtight",
                        #     "hlt_path": "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight",
                        # },
                        {
                            "flagname": "trg_pfmetnomu120_pfmhtnomu120_idtight",
                            "hlt_path": "HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
                        },
                    ]
                }
            ),
        },
    )

    # single muon trigger scale factors
    configuration.add_config_parameters(
        M_SCOPES,
        {
            "single_mu_trigger_sf": [
                {
                    "m_trigger_flagname": "trg_wgt_single_mu24",
                    "m_trigger_sf_name": "NUM_IsoMu24_DEN_CutBasedIdTight_and_PFIsoTight",
                    "m_trigger_variation": "nominal",
                },
            ],
        },
    )

    # double muon-tau trigger scale factors
    configuration.add_config_parameters(
        MT_SCOPES,
        {
            "double_mutau_trigger_leg1_sf": [
                {
                    "mt_trigger_leg1_sf_file": EraModifier(
                        {
                            **{
                                _era: "DOES_NOT_EXIST"  # TODO does not exist for Run2 eras
                                for _era in ERAS_RUN2
                            },
                            **{
                                _era: f"data/hleprare/TriggerScaleFactors/{_era}/CrossMuTauHlt_MuLeg_v1.json"
                                for _era in ERAS_RUN3
                            },
                        }
                    ),
                    "mt_trigger_leg1_flagname": "trg_wgt_double_mu20tau27_leg1",
                    "mt_trigger_leg1_sf_name": "NUM_IsoMu20_DEN_CutBasedIdTight_and_PFIsoTight",
                    "mt_trigger_leg1_variation": "nominal",
                },
            ],
            "double_mutau_trigger_leg2_sf": [
                {
                    "mt_trigger_leg2_flagname": "trg_wgt_double_mu20tau27_leg2",
                    "mt_trigger_leg2_sf_name": "mutau",
                    "mt_trigger_leg2_variation": "nom",
                },
            ],
        },
    )

    ## TT singletau trigger
    # configuration.add_config_parameters(
    #     ["tt"],
    #     {
    #         "singletau_trigger_leading": EraModifier(
    #             {
    #                 "2018": [
    #                     {
    #                         "flagname": "trg_single_tau180_1",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2017": [
    #                     {
    #                         "flagname": "trg_single_tau180_1",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2016postVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #                 "2016preVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_1",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #             }
    #         )
    #     },
    # )

    ## trailing singletau trigger
    # configuration.add_config_parameters(
    #     ["et", "mt", "tt"],
    #     {
    #         "singletau_trigger_trailing": EraModifier(
    #             {
    #                 "2018": [
    #                     {
    #                         "flagname": "trg_single_tau180_2",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2017": [
    #                     {
    #                         "flagname": "trg_single_tau180_2",
    #                         "hlt_path": "HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1",
    #                         "ptcut": 180,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     }
    #                 ],
    #                 "2016postVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #                 "2016preVFP": [
    #                     {
    #                         "flagname": "trg_single_tau120_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau120_Trk50_eta2p1_v",
    #                         "ptcut": 120,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                     {
    #                         "flagname": "trg_single_tau140_2",
    #                         "hlt_path": "HLT_VLooseIsoPFTau140_Trk50_eta2p1_v",
    #                         "ptcut": 140,
    #                         "etacut": 2.1,
    #                         "filterbit": 5,
    #                         "trigger_particle_id": 15,
    #                         "max_deltaR_triggermatch": 0.4,
    #                     },
    #                 ],
    #             }
    #         )
    #     },
    # )

    return configuration
