from code_generation.configuration import Configuration
from code_generation.producer import Producer
from code_generation.systematics import get_adjusted_add_shift_SystematicShift
from code_generation.helpers import defaults
from .producers import scalefactors as scalefactors
from .producers import pairselection as pairselection
from .producers import muons as muons
from .producers import electrons as electrons
from .producers import taus as taus


def add_tauVariations(configuration: Configuration, sample: str, era: str) -> Configuration:

    add_shift = get_adjusted_add_shift_SystematicShift(configuration)

    with defaults(
        shift_map={"Up": "up", "Down": "down"}
        ):
        
        #########################
        # Lepton to tau fakes energy scalefactor shifts  #
        #########################
        if int(era[:4]) < 2022:
            if ("dyjets" in sample or "electroweak_boson" in sample):
                add_shift(
                    name="tauMuFakeEs",
                    shift_key="tau_mufake_es",
                    scopes="mt",
                    producers=[taus.TauPtCorrectionMC],
                )
                with defaults(
                    scopes="et",
                    producers=[taus.TauPtCorrectionMC],
                ):
                    add_shift(name="tauEleFakeEsDM0Barrel", shift_key="tau_elefake_es_DM0_barrel")
                    add_shift(name="tauEleFakeEsDM0Endcap", shift_key="tau_elefake_es_DM0_endcap")
                    add_shift(name="tauEleFakeEsDM1Barrel", shift_key="tau_elefake_es_DM1_barrel")
                    add_shift(name="tauEleFakeEsDM1Endcap", shift_key="tau_elefake_es_DM1_endcap")
            with defaults(scopes=("et", "mt", "tt")):
                with defaults(producers=[taus.TauEnergyCorrectionMC],
                              exclude_samples=["data", "embedding", "embedding_mc"]): 
                    for dm in ["DM0", "DM1", "DM10", "DM11"]:
                        for pt in [""]:
                            add_shift(name=f"tauEs{dm}{pt}", shift_key=f"tau_ES_shift_{dm}{pt}")

        elif int(era[:4]) >= 2022:
            with defaults(scopes=("et", "mt", "tt")): # This is not doing anything ... ?
                with defaults(producers=[taus.TauEnergyCorrectionMC]): # propagate to mass too
                    for dm in ["0", "1", "10", "11"]:
                        # genuine tau
                        add_shift(name=f"tauEsDM{dm}", shift_key=f"tau_ES_shift_DM{dm}")
                        # ele fake
                        add_shift(name=f"tauEleFakeEsDM{dm}", shift_key=f"tau_elefake_es_DM{dm}")
                    # muon fake
                    add_shift(name="tauMuFakeEs", shift_key="tau_mufake_es")

        #########################
        # TauID scale factor shifts
        #########################
        with defaults(
            exclude_samples=["data", "embedding", "embedding_mc"]
            ):

            if int(era[:4]) < 2022:
                with defaults(scopes=("et", "mt")):
                    with defaults(producers=[scalefactors.TauIDVsJetSF2]):
                        for dm in ["DM0", "DM1", "DM10", "DM11"]:
                            for pt in [""]:
                                add_shift(name=f"vsJetTau{dm}{pt}", shift_key=f"tau_id_sf_vsjet_{dm}{pt}")
                    with defaults(producers=[scalefactors.TauIDVsEleSF2]):
                        add_shift(name="vsEleBarrel", shift_key="tau_id_sf_vsele_barrel")
                        add_shift(name="vsEleEndcap", shift_key="tau_id_sf_vsele_endcap")
                    with defaults(producers=[scalefactors.TauIDVsMuSF2]):
                        for wheel in range(1, 6):
                            add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_id_sf_vsmu_wheel{wheel}")
                with defaults(scopes="tt"):
                    with defaults(producers=[scalefactors.TauIDVsJetSF1, scalefactors.TauIDVsJetSF2]):
                        for dm in ["DM0", "DM1", "DM10", "DM11"]:
                            for pt in [""]:
                                add_shift(name=f"vsJetTau{dm}{pt}", shift_key=f"tau_id_sf_vsjet_{dm}{pt}")
                    with defaults(producers=[scalefactors.TauIDVsEleSF1, scalefactors.TauIDVsEleSF2]):
                        add_shift(name="vsEleBarrel", shift_key="tau_id_sf_vsele_barrel")
                        add_shift(name="vsEleEndcap", shift_key="tau_id_sf_vsele_endcap")
                    with defaults(producers=[scalefactors.TauIDVsMuSF1, scalefactors.TauIDVsMuSF2]):
                        for wheel in range(1, 6):
                            add_shift(name=f"vsMuWheel{wheel}", shift_key=f"tau_id_sf_vsmu_wheel{wheel}")
                
            else: # TODO: Check before usage!!!
                # vs Ele
                with defaults(name="vsEleBarrel", shift_key="tau_sf_vsele_barrel"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.TauIDVsEleSF2])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                with defaults(name="vsEleEndcap", shift_key="tau_sf_vsele_endcap"):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.TauIDVsEleSF2])
                    add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsEleTauID_SF])
                # vs Muon
                for wheel in range(1, 6):
                    with defaults(name=f"vsMuWheel{wheel}", shift_key=f"tau_sf_vsmu_wheel{wheel}"):
                        add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.TauIDVsMuSF2])
                        add_shift(scopes=("tt"),producers=[scalefactors.Tau_1_VsMuTauID_SF])
                # vs Jet
                with defaults(
                    name="tau_vsjet_variation",
                    shift_key="tau_sf_vsjet_variation",
                ):
                    add_shift(scopes=("et", "mt", "tt"),producers=[scalefactors.TauIDVsJetSF2])
                    add_shift(scopes=("tt"),producers=[scalefactors.TauIDVsJetSF1])
