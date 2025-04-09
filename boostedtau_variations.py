from code_generation.configuration import Configuration
from code_generation.systematics import SystematicShift
from .producers import scalefactors as scalefactors
from .producers import muons as muons
from .producers import electrons as electrons
from .producers import boostedtaus as boostedtaus


def add_boostedtauVariations(configuration: Configuration, sample: str):
    if sample == "embedding" or sample == "embedding_mc" or sample == "data":
        return configuration
    #########################
    # MVA2017v2 scale factor shifts
    #########################
    # old MVA shifts et/mt, tau pt dependent
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau30to35Down",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau30to35": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau30to35Up",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau30to35": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau35to40Down",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau35to40": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau35to40Up",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau35to40": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau40to500Down",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau40to500": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau40to500Up",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau40to500": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau500to1000Down",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau500to1000": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau500to1000Up",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau500to1000": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau1000toInfDown",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau1000toinf": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTau1000toInfUp",
            shift_config={("et", "mt"): {"boostedtau_sf_iso_tau1000toinf": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_oldIsoTauID_lt_SF},
        )
    )
    # old MVA shifts tt, tau dm dependent
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM0Down",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM0": "down"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM0Up",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM0": "up"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM1Down",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM1": "down"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM1Up",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM1": "up"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM10Down",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM10": "down"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="oldIsoTauDM10Up",
            shift_config={"tt": {"boostedtau_sf_iso_tauDM10": "up"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_oldIsoTauID_tt_SF,
                    scalefactors.Tau_2_oldIsoTauID_tt_SF,
                ]
            },
        )
    )
    #########################
    # AntiEleID scale factor shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="antiEleBarrelDown",
            shift_config={("et", "mt"): {"boostedtau_sf_antiele_barrel": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiEleTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleBarrelUp",
            shift_config={("et", "mt"): {"boostedtau_sf_antiele_barrel": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiEleTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleEndcapDown",
            shift_config={("et", "mt"): {"boostedtau_sf_antiele_endcap": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiEleTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleEndcapUp",
            shift_config={("et", "mt"): {"boostedtau_sf_antiele_endcap": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiEleTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleBarrelDown",
            shift_config={"tt": {"boostedtau_sf_antiele_barrel": "down"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_antiEleTauID_SF,
                    scalefactors.Tau_2_antiEleTauID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleBarrelUp",
            shift_config={"tt": {"boostedtau_sf_antiele_barrel": "up"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_antiEleTauID_SF,
                    scalefactors.Tau_2_antiEleTauID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleEndcapDown",
            shift_config={"tt": {"boostedtau_sf_antiele_endcap": "down"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_antiEleTauID_SF,
                    scalefactors.Tau_2_antiEleTauID_SF,
                ]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiEleEndcapUp",
            shift_config={"tt": {"boostedtau_sf_antiele_endcap": "up"}},
            producers={
                "tt": [
                    scalefactors.Tau_1_antiEleTauID_SF,
                    scalefactors.Tau_2_antiEleTauID_SF,
                ]
            },
        )
    )
    #########################
    # AntiMuID scale factor shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel1Down",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel1": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel1Up",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel1": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel2Down",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel2": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel2Up",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel2": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel3Down",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel3": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel3Up",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel3": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel4Down",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel4": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel4Up",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel4": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel5Down",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel5": "down"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel5Up",
            shift_config={("et", "mt"): {"boostedtau_sf_antimu_wheel5": "up"}},
            producers={("et", "mt"): scalefactors.Tau_2_antiMuTauID_SF},
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel1Down",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel1": "down"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel1Up",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel1": "up"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel2Down",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel2": "down"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel2Up",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel2": "up"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel3Down",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel3": "down"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel3Up",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel3": "up"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel4Down",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel4": "down"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel4Up",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel4": "up"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel5Down",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel5": "down"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="antiMuWheel5Up",
            shift_config={"tt": {"boostedtau_sf_antimu_wheel5": "up"}},
            producers={
                "tt": [scalefactors.Tau_1_antiMuTauID_SF, scalefactors.Tau_2_antiMuTauID_SF]
            },
        )
    )
    #########################
    # TES Shifts
    #########################
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs1prong0pizeroDown",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM0": "down"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs1prong0pizeroUp",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM0": "up"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs1prong1pizeroDown",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM1": "down"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs1prong1pizeroUp",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM1": "up"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs3prong0pizeroDown",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM10": "down"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )
    configuration.add_shift(
        SystematicShift(
            name="boostedtauEs3prong0pizeroUp",
            shift_config={("et", "mt", "tt"): {"boostedtau_ES_shift_DM10": "up"}},
            producers={("et", "mt", "tt"): boostedtaus.boostedTauPtCorrection},
            ignore_producers={
                "et": [boostedtaus.boostedLVEl1, electrons.VetoElectrons_boosted],
                "mt": [boostedtaus.boostedLVMu1, muons.VetoMuons_boosted],
                "tt": [],
            },
        )
    )

    return configuration
