from ..quantities import output as q
from ..quantities import nanoAOD as nanoAOD
from code_generation.producer import Producer, ProducerGroup

####################
# Set of producers used for contruction of met related quantities
####################

BuildMetVector = Producer(
    name="BuildMetVector",
    call="lorentzvectors::buildMet({df}, {input}, {output})",
    input=[
        nanoAOD.MET_pt,
        nanoAOD.MET_phi,
    ],
    output=[q.met_p4],
    scopes=["global"],
)
BuildPFMetVector = Producer(
    name="BuildPFMetVector",
    call="lorentzvectors::buildMet({df}, {input}, {output})",
    input=[
        nanoAOD.PFMET_pt,
        nanoAOD.PFMET_phi,
    ],
    output=[q.pfmet_p4],
    scopes=["global"],
)
MetCov00 = Producer(
    name="MetCov00",
    call="event::quantity::Rename<float>({df}, {input}, {output})",
    input=[
        nanoAOD.MET_covXX,
    ],
    output=[q.metcov00],
    scopes=["global"],
)
MetCov01 = Producer(
    name="MetCov01",
    call="event::quantity::Rename<float>({df}, {input}, {output})",
    input=[
        nanoAOD.MET_covXY,
    ],
    output=[q.metcov01],
    scopes=["global"],
)
MetCov10 = Producer(
    name="MetCov10",
    call="event::quantity::Rename<float>({df}, {input}, {output})",
    input=[
        nanoAOD.MET_covXY,
    ],
    output=[q.metcov10],
    scopes=["global"],
)
MetCov11 = Producer(
    name="MetCov11",
    call="event::quantity::Rename<float>({df}, {input}, {output})",
    input=[
        nanoAOD.MET_covYY,
    ],
    output=[q.metcov11],
    scopes=["global"],
)
MetSumEt = Producer(
    name="MetSumEt",
    call="event::quantity::Rename<float>({df}, {input}, {output})",
    input=[
        nanoAOD.MET_sumEt,
    ],
    output=[q.metSumEt],
    scopes=["global"],
)
MetPt_uncorrected = Producer(
    name="MetPt_uncorrected",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.met_p4],
    output=[q.met_uncorrected],
    scopes=["global"],
)
MetPhi_uncorrected = Producer(
    name="MetPhi_uncorrected",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.met_p4],
    output=[q.metphi_uncorrected],
    scopes=["global"],
)
PFMetPt_uncorrected = Producer(
    name="PFMetPt_uncorrected",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.pfmet_p4],
    output=[q.pfmet_uncorrected],
    scopes=["global"],
)
PFMetPhi_uncorrected = Producer(
    name="PFMetPhi_uncorrected",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.pfmet_p4],
    output=[q.pfmetphi_uncorrected],
    scopes=["global"],
)
CalculateGenBosonVector = Producer(
    name="calculateGenBosonVector",
    call="met::calculateGenBosonVector({df}, {input}, {output}, {is_data})",
    input=[
        nanoAOD.GenParticle_pt,
        nanoAOD.GenParticle_eta,
        nanoAOD.GenParticle_phi,
        nanoAOD.GenParticle_mass,
        nanoAOD.GenParticle_pdgId,
        nanoAOD.GenParticle_status,
        nanoAOD.GenParticle_statusFlags,
    ],
    output=[q.recoil_genboson_p4_vec],
    scopes=["global"],
)
GenBosonMass = Producer(
    name="GenBosonMass",
    call="met::genBosonMass({df}, {output}, {input})",
    input=[q.recoil_genboson_p4_vec],
    output=[q.genbosonmass],
    scopes=["global"],
)
MetBasics = ProducerGroup(
    name="MetBasics",
    call=None,
    input=None,
    output=None,
    scopes=["global"],
    subproducers=[
        BuildPFMetVector,
        BuildMetVector,
        MetPt_uncorrected,
        MetPhi_uncorrected,
        PFMetPt_uncorrected,
        PFMetPhi_uncorrected,
        MetCov00,
        MetCov01,
        MetCov10,
        MetCov11,
        MetSumEt,
        CalculateGenBosonVector,
        GenBosonMass,
    ],
)


PropagateLeptonsToMet = Producer(
    name="PropagateLeptonsToMet",
    call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
    input=[q.met_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
    output=[q.met_p4_leptoncorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PropagateLeptonsToPFMet = Producer(
    name="PropagateLeptonsToPFMet",
    call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
    input=[q.pfmet_p4, q.p4_1_uncorrected, q.p4_2_uncorrected, q.p4_1, q.p4_2],
    output=[q.pfmet_p4_leptoncorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PropagateLeptonsToMet_boosted = Producer(
    name="PropagateLeptonsToMet_boosted",
    call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
    input=[q.met_p4, q.boosted_p4_1_uncorrected, q.boosted_p4_2_uncorrected, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.met_p4_boosted_leptoncorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PropagateLeptonsToPFMet_boosted = Producer(
    name="PropagateLeptonsToPFMet_boosted",
    call="met::propagateLeptonsToMet({df}, {input}, {output}, {propagateLeptons})",
    input=[q.pfmet_p4, q.boosted_p4_1_uncorrected, q.boosted_p4_2_uncorrected, q.boosted_p4_1, q.boosted_p4_2],
    output=[q.pfmet_p4_boosted_leptoncorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

PropagateJetsToMet = Producer(
    name="PropagateJetsToMet",
    call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
    input=[
        q.met_p4_leptoncorrected,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_mass,
    ],
    output=[q.met_p4_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PropagateJetsToPFMet = Producer(
    name="PropagateJetsToPFMet",
    call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
    input=[
        q.pfmet_p4_leptoncorrected,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_mass,
    ],
    output=[q.pfmet_p4_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

PropagateJetsToMet_boosted = Producer(
    name="PropagateJetsToMet_boosted",
    call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
    input=[
        q.met_p4_boosted_leptoncorrected,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_mass,
    ],
    output=[q.met_p4_boosted_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PropagateJetsToPFMet_boosted = Producer(
    name="PropagateJetsToPFMet_boosted",
    call="met::propagateJetsToMet({df}, {input}, {output}, {propagateJets}, {min_jetpt_met_propagation})",
    input=[
        q.pfmet_p4_boosted_leptoncorrected,
        q.Jet_pt_corrected_bReg,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        q.Jet_mass_corrected,
        nanoAOD.Jet_pt,
        nanoAOD.Jet_eta,
        nanoAOD.Jet_phi,
        nanoAOD.Jet_mass,
    ],
    output=[q.pfmet_p4_boosted_jetcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

ApplyRecoilCorrections = Producer(
    name="ApplyRecoilCorrections",
    call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
    input=[
        q.met_p4_jetcorrected,
        q.recoil_genboson_p4_vec,
        q.Jet_pt_corrected_bReg,
    ],
    output=[q.met_p4_recoilcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
ApplyRecoilCorrectionsPFMet = Producer(
    name="ApplyRecoilCorrectionsPFMet",
    call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
    input=[
        q.pfmet_p4_jetcorrected,
        q.recoil_genboson_p4_vec,
        q.Jet_pt_corrected_bReg,
    ],
    output=[q.pfmet_p4_recoilcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

ApplyRecoilCorrections_boosted = Producer(
    name="ApplyRecoilCorrections_boosted",
    call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
    input=[
        q.met_p4_boosted_jetcorrected,
        q.recoil_genboson_p4_vec,
        q.Jet_pt_corrected_bReg,
    ],
    output=[q.met_p4_boosted_recoilcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
ApplyRecoilCorrectionsPFMet_boosted = Producer(
    name="ApplyRecoilCorrectionsPFMet_boosted",
    call='met::applyRecoilCorrections({df}, {input}, {output}, "{recoil_corrections_file}", "{recoil_systematics_file}", {applyRecoilCorrections}, {apply_recoil_resolution_systematic}, {apply_recoil_response_systematic}, {recoil_systematic_shift_up}, {recoil_systematic_shift_down}, {is_wjets})',
    input=[
        q.pfmet_p4_boosted_jetcorrected,
        q.recoil_genboson_p4_vec,
        q.Jet_pt_corrected_bReg,
    ],
    output=[q.pfmet_p4_boosted_recoilcorrected],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)

MetPt = Producer(
    name="MetPt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.met_p4_recoilcorrected],
    output=[q.met],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PFMetPt = Producer(
    name="PFMetPt",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.pfmet_p4_recoilcorrected],
    output=[q.pfmet],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
MetPhi = Producer(
    name="MetPhi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.met_p4_recoilcorrected],
    output=[q.metphi],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PFMetPhi = Producer(
    name="PFMetPhi",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.pfmet_p4_recoilcorrected],
    output=[q.pfmetphi],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
MetCorrections = ProducerGroup(
    name="MetCorrections",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    subproducers=[
        PropagateLeptonsToMet,
        PropagateJetsToMet,
        ApplyRecoilCorrections,
        MetPt,
        MetPhi,
    ],
)
PFMetCorrections = ProducerGroup(
    name="PFMetCorrections",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    subproducers=[
        PropagateLeptonsToPFMet,
        PropagateJetsToPFMet,
        ApplyRecoilCorrectionsPFMet,
        PFMetPt,
        PFMetPhi,
    ],
)

MetPt_boosted = Producer(
    name="MetPt_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.met_p4_boosted_recoilcorrected],
    output=[q.met_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PFMetPt_boosted = Producer(
    name="PFMetPt_boosted",
    call="quantities::pt({df}, {output}, {input})",
    input=[q.pfmet_p4_boosted_recoilcorrected],
    output=[q.pfmet_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
MetPhi_boosted = Producer(
    name="MetPhi_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.met_p4_boosted_recoilcorrected],
    output=[q.metphi_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
PFMetPhi_boosted = Producer(
    name="PFMetPhi_boosted",
    call="quantities::phi({df}, {output}, {input})",
    input=[q.pfmet_p4_boosted_recoilcorrected],
    output=[q.pfmetphi_boosted],
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
)
MetCorrections_boosted = ProducerGroup(
    name="MetCorrections_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    subproducers=[
        PropagateLeptonsToMet_boosted,
        PropagateJetsToMet_boosted,
        ApplyRecoilCorrections_boosted,
        MetPt_boosted,
        MetPhi_boosted,
    ],
)
PFMetCorrections_boosted = ProducerGroup(
    name="PFMetCorrections_boosted",
    call=None,
    input=None,
    output=None,
    scopes=["et", "mt", "tt", "em", "mm", "ee"],
    subproducers=[
        PropagateLeptonsToPFMet_boosted,
        PropagateJetsToPFMet_boosted,
        ApplyRecoilCorrectionsPFMet_boosted,
        PFMetPt_boosted,
        PFMetPhi_boosted,
    ],
)