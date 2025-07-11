from constants import M_SCOPES
from code_generation.modifiers import EraModifier
from code_generation.configuration import Configuration


def add_mt_trigger_setup(configuration: Configuration):

    # single-muon trigger
    # https://twiki.cern.ch/twiki/bin/viewauth/CMS/MuonHLT2022
    configuration.add_config_parameters(
        M_SCOPES,
        {
            "singlemuon_trigger": EraModifier(
                {
                    "2022preEE": [
                        {
                            "flagname": "trg_single_mu24",
                            "hlt_path": "HLT_IsoMu24",
                            "ptcut": 25,
                            "etacut": 2.1,
                            "filterbit": -1,
                            "trigger_particle_id": 13,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ]
                }
            )
        }
    )

    # muon-tau cross trigger
    # https://twiki.cern.ch/twiki/bin/view/CMS/TauTrigger#Trigger_Table_for_2022
    configuration.add_config_parameters(
        M_SCOPES,
        {
            "mutau_cross_trigger": EraModifier(
                {
                    "2022preEE": [
                        {
                            "flagname": "trg_mu20tau27",
                            "hlt_path": "HLT_IsoMu20_eta2p1_LooseDeepTauPFTauHPS27_eta2p1_CrossL1",
                            "p1_ptcut": 21,
                            "p2_ptcut": 29,
                            "p1_etacut": 2.1,
                            "p2_etacut": 2.1,
                            "p1_filterbit": -1,
                            "p2_filterbit": -1,
                            "p1_trigger_particle_id": 11,
                            "p2_trigger_particle_id": 15,
                            "max_deltaR_triggermatch": 0.4,
                        }
                    ]
                }
            ),
        }
    )

    return configuration
