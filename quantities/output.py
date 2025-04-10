from code_generation.quantity import Quantity

lumi = Quantity("lumi")
puweight = Quantity("puweight")
prefireweight = Quantity("prefiring_wgt")
lhe_scale_weight = Quantity("lhe_scale_weight")

# fake factors
raw_fake_factor = Quantity("raw_fake_factor")
raw_qcd_fake_factor = Quantity("raw_qcd_fake_factor")
raw_wjets_fake_factor = Quantity("raw_wjets_fake_factor")
raw_ttbar_fake_factor = Quantity("raw_ttbar_fake_factor")
qcd_fake_factor = Quantity("qcd_fake_factor")
wjets_fake_factor = Quantity("wjets_fake_factor")
ttbar_fake_factor = Quantity("ttbar_fake_factor")
fake_factor = Quantity("fake_factor")
raw_fake_factor_boosted = Quantity("raw_fake_factor_boosted")
fake_factor_boosted = Quantity("fake_factor_boosted")
raw_fake_factor_1 = Quantity("raw_fake_factor_1")
raw_fake_factor_2 = Quantity("raw_fake_factor_2")
fake_factor_1 = Quantity("fake_factor_1")
fake_factor_2 = Quantity("fake_factor_2")
raw_fake_factor_boosted_1 = Quantity("raw_fake_boosted_factor_1")
raw_fake_factor_boosted_2 = Quantity("raw_fake_boosted_factor_2")
fake_factor_boosted_1 = Quantity("fake_factor_boosted_1")
fake_factor_boosted_2 = Quantity("fake_factor_boosted_2")

# kinematic fit
kinfit_convergence_YToBB = Quantity("kinfit_convergence_YToBB")
kinfit_mX_YToBB = Quantity("kinfit_mX_YToBB")
kinfit_mY_YToBB = Quantity("kinfit_mY_YToBB")
kinfit_mh_YToBB = Quantity("kinfit_mh_YToBB")
kinfit_chi2_YToBB = Quantity("kinfit_chi2_YToBB")
kinfit_prob_YToBB = Quantity("kinfit_prob_YToBB")
kinfit_pull1_YToBB = Quantity("kinfit_pull1_YToBB")
kinfit_pull2_YToBB = Quantity("kinfit_pull2_YToBB")
kinfit_pullBalance_YToBB = Quantity("kinfit_pullBalance_YToBB")
kinfit_convergence_YToTauTau = Quantity("kinfit_convergence_YToTauTau")
kinfit_mX_YToTauTau = Quantity("kinfit_mX_YToTauTau")
kinfit_mY_YToTauTau = Quantity("kinfit_mY_YToTauTau")
kinfit_mh_YToTauTau = Quantity("kinfit_mh_YToTauTau")
kinfit_chi2_YToTauTau = Quantity("kinfit_chi2_YToTauTau")
kinfit_prob_YToTauTau = Quantity("kinfit_prob_YToTauTau")
kinfit_pull1_YToTauTau = Quantity("kinfit_pull1_YToTauTau")
kinfit_pull2_YToTauTau = Quantity("kinfit_pull2_YToTauTau")
kinfit_pullBalance_YToTauTau = Quantity("kinfit_pullBalance_YToTauTau")
kinfit_convergence = Quantity("kinfit_convergence")
kinfit_mX = Quantity("kinfit_mX")
kinfit_mY = Quantity("kinfit_mY")
kinfit_mh = Quantity("kinfit_mh")
kinfit_chi2 = Quantity("kinfit_chi2")
kinfit_prob = Quantity("kinfit_prob")
kinfit_pull1 = Quantity("kinfit_pull1")
kinfit_pull2 = Quantity("kinfit_pull2")
kinfit_pullBalance = Quantity("kinfit_pullBalance")
kinfit_convergence_YToBB_boosted = Quantity("kinfit_convergence_YToBB_boosted")
kinfit_mX_YToBB_boosted = Quantity("kinfit_mX_YToBB_boosted")
kinfit_mY_YToBB_boosted = Quantity("kinfit_mY_YToBB_boosted")
kinfit_mh_YToBB_boosted = Quantity("kinfit_mh_YToBB_boosted")
kinfit_chi2_YToBB_boosted = Quantity("kinfit_chi2_YToBB_boosted")
kinfit_prob_YToBB_boosted = Quantity("kinfit_prob_YToBB_boosted")
kinfit_pull1_YToBB_boosted = Quantity("kinfit_pull1_YToBB_boosted")
kinfit_pull2_YToBB_boosted = Quantity("kinfit_pull2_YToBB_boosted")
kinfit_pullBalance_YToBB_boosted = Quantity("kinfit_pullBalance_YToBB_boosted")
kinfit_convergence_YToTauTau_boosted = Quantity("kinfit_convergence_YToTauTau_boosted")
kinfit_mX_YToTauTau_boosted = Quantity("kinfit_mX_YToTauTau_boosted")
kinfit_mY_YToTauTau_boosted = Quantity("kinfit_mY_YToTauTau_boosted")
kinfit_mh_YToTauTau_boosted = Quantity("kinfit_mh_YToTauTau_boosted")
kinfit_chi2_YToTauTau_boosted = Quantity("kinfit_chi2_YToTauTau_boosted")
kinfit_prob_YToTauTau_boosted = Quantity("kinfit_prob_YToTauTau_boosted")
kinfit_pull1_YToTauTau_boosted = Quantity("kinfit_pull1_YToTauTau_boosted")
kinfit_pull2_YToTauTau_boosted = Quantity("kinfit_pull2_YToTauTau_boosted")
kinfit_pullBalance_YToTauTau_boosted = Quantity("kinfit_pullBalance_YToTauTau_boosted")
kinfit_convergence_boosted = Quantity("kinfit_convergence_boosted")
kinfit_mX_boosted = Quantity("kinfit_mX_boosted")
kinfit_mY_boosted = Quantity("kinfit_mY_boosted")
kinfit_mh_boosted = Quantity("kinfit_mh_boosted")
kinfit_chi2_boosted = Quantity("kinfit_chi2_boosted")
kinfit_prob_boosted = Quantity("kinfit_prob_boosted")
kinfit_pull1_boosted = Quantity("kinfit_pull1_boosted")
kinfit_pull2_boosted = Quantity("kinfit_pull2_boosted")
kinfit_pullBalance_boosted = Quantity("kinfit_pullBalance_boosted")

base_taus_mask = Quantity("base_taus_mask")
good_taus_mask = Quantity("good_taus_mask")
base_muons_mask = Quantity("base_muons_mask")
good_muons_mask = Quantity("good_muons_mask")
veto_muons_boosted_mask = Quantity("veto_muons_boosted_mask")
veto_muons_mask = Quantity("veto_muons_mask")
veto_muons_mask_2 = Quantity("veto_muons_mask_2")
muon_veto_flag = Quantity("extramuon_veto")
boosted_muon_veto_flag = Quantity("boosted_extramuon_veto")
base_electrons_mask = Quantity("base_electrons_mask")
good_electrons_mask = Quantity("good_electrons_mask")
veto_electrons_boosted_mask = Quantity("veto_electrons_boosted_mask")
veto_electrons_mask = Quantity("veto_electrons_mask")
veto_electrons_mask_2 = Quantity("veto_electrons_mask_2")
electron_veto_flag = Quantity("extraelec_veto")
boosted_electron_veto_flag = Quantity("boosted_extraelec_veto")
jet_id_mask = Quantity("jet_id_mask")
jet_puid_mask = Quantity("jet_puid_mask")
jet_overlap_veto_mask = Quantity("jet_overlap_veto_mask")
jet_overlap_veto_mask_boosted = Quantity("jet_overlap_veto_mask_boosted")
good_jets_mask = Quantity("good_jets_mask")
good_bjets_mask = Quantity("good_bjets_mask")
base_photons_mask = Quantity("base_photons_mask")
Tau_pt_ele_corrected = Quantity("Tau_pt_ele_corrected")
Tau_pt_ele_mu_corrected = Quantity("Tau_pt_mu_corrected")
Tau_pt_corrected = Quantity("Tau_pt_corrected")
Tau_mass_corrected = Quantity("Tau_mass_corrected")
Jet_pt_corrected = Quantity("Jet_pt_corrected")
Jet_mass_corrected = Quantity("Jet_mass_corrected")
Jet_pt_corrected_bReg = Quantity("Jet_pt_corrected_bReg")
Jet_mass_corrected_bReg = Quantity("Jet_mass_corrected_bReg")
fatjet_id_mask = Quantity("fatjet_id_mask")
good_fatjets_mask = Quantity("good_fatjets_mask")
fatjet_overlap_veto_mask = Quantity("fatjet_overlap_veto_mask")
fatjet_overlap_veto_mask_boosted = Quantity("fatjet_overlap_veto_mask_boosted")
FatJet_pt_corrected = Quantity("FatJet_pt_corrected")
FatJet_mass_corrected = Quantity("FatJet_mass_corrected")
dibjetpair = Quantity("dibjetpair")
dibjetpair_boosted = Quantity("dibjetpair_boosted")
gen_dibjetpair = Quantity("gen_dibjetpair")
gen_truebpair = Quantity("gen_truebpair")
gen_truetaupair = Quantity("gen_truetaupair")
dileptonpair = Quantity("dileptonpair")
gen_dileptonpair = Quantity("gen_dileptonpair")
truegenpair = Quantity("truegenpair")
good_fatjet_collection = Quantity("good_fatjet_collection")
good_jet_collection = Quantity("good_jet_collection")
good_bjet_collection = Quantity("good_bjet_collection")
good_fatjet_collection_boosted = Quantity("good_fatjet_collection_boosted")
good_fatjet_collection_without_veto = Quantity("good_fatjet_collection_without_veto")
good_jet_collection_boosted = Quantity("good_jet_collection_boosted")
good_bjet_collection_boosted = Quantity("good_bjet_collection_boosted")
Electron_pt_corrected = Quantity("Electron_pt_corrected")

# boosted Tau quantities
good_boostedtaus_mask = Quantity("good_boostedtaus_mask")
boostedTau_pt_corrected = Quantity("boostedTau_pt_corrected")
boostedTau_mass_corrected = Quantity("boostedTau_mass_corrected")
nboostedtaus = Quantity("nboostedtaus")
boosteddileptonpair = Quantity("boosteddileptonpair")
boosted_p4_1 = Quantity("boosted_p4_1")
boosted_p4_1_uncorrected = Quantity("boosted_p4_1_uncorrected")
boosted_pt_1 = Quantity("boosted_pt_1")
boosted_eta_1 = Quantity("boosted_eta_1")
boosted_phi_1 = Quantity("boosted_phi_1")
boosted_mass_1 = Quantity("boosted_mass_1")
boosted_p4_2 = Quantity("boosted_p4_2")
boosted_p4_2_uncorrected = Quantity("boosted_p4_2_uncorrected")
boosted_pt_2 = Quantity("boosted_pt_2")
boosted_eta_2 = Quantity("boosted_eta_2")
boosted_phi_2 = Quantity("boosted_phi_2")
boosted_mass_2 = Quantity("boosted_mass_2")
boosted_dxy_1 = Quantity("boosted_dxy_1")
boosted_dxy_2 = Quantity("boosted_dxy_2")
boosted_dz_1 = Quantity("boosted_dz_1")
boosted_dz_2 = Quantity("boosted_dz_2")
boosted_q_1 = Quantity("boosted_q_1")
boosted_q_2 = Quantity("boosted_q_2")
boosted_iso_1 = Quantity("boosted_iso_1")
boosted_iso_2 = Quantity("boosted_iso_2")
boosted_is_global_1 = Quantity("boosted_is_global_1")
boosted_tau_decaymode_1 = Quantity("boosted_tau_decaymode_1")
boosted_tau_decaymode_2 = Quantity("boosted_tau_decaymode_2")
boosted_tau_gen_match_1 = Quantity("boosted_tau_gen_match_1")
boosted_tau_gen_match_2 = Quantity("boosted_tau_gen_match_2")
boosted_taujet_pt_2 = Quantity("boosted_taujet_pt_2")
boosted_p4_vis = Quantity("boosted_p4_vis")
boosted_m_vis = Quantity("boosted_m_vis")
boosted_pt_vis = Quantity("boosted_pt_vis")
boosted_deltaR_ditaupair = Quantity("boosted_deltaR_ditaupair")
boosted_mt_1 = Quantity("boosted_mt_1")
boosted_mt_2 = Quantity("boosted_mt_2")
boosted_gen_match_1 = Quantity("boosted_gen_match_1")
boosted_gen_match_2 = Quantity("boosted_gen_match_2")
boosted_p4_tautaubb = Quantity("boosted_p4_tautaubb")
boosted_pt_tautaubb = Quantity("boosted_pt_tautaubb")
boosted_mass_tautaubb = Quantity("boosted_mass_tautaubb")
boosted_p4_fastmtt = Quantity("boosted_p4_fastmtt")
boosted_m_fastmtt = Quantity("boosted_m_fastmtt")
boosted_pt_fastmtt = Quantity("boosted_pt_fastmtt")
boosted_eta_fastmtt = Quantity("boosted_eta_fastmtt")
boosted_phi_fastmtt = Quantity("boosted_phi_fastmtt")
additional_boostedtau = Quantity("additional_boostedtau")
boosted_p4_add = Quantity("boosted_p4_add")
boosted_pt_add = Quantity("boosted_pt_add")
boosted_eta_add = Quantity("boosted_eta_add")
boosted_phi_add = Quantity("boosted_phi_add")
boosted_mass_add = Quantity("boosted_mass_add")

nelectrons = Quantity("nelectrons")
nmuons = Quantity("nmuons")
ntaus = Quantity("ntaus")
p4_1 = Quantity("p4_1")
p4_1_uncorrected = Quantity("p4_1_uncorrected")
pt_1 = Quantity("pt_1")
eta_1 = Quantity("eta_1")
phi_1 = Quantity("phi_1")
p4_2 = Quantity("p4_2")
p4_2_uncorrected = Quantity("p4_2_uncorrected")
pt_2 = Quantity("pt_2")
eta_2 = Quantity("eta_2")
phi_2 = Quantity("phi_2")
mass_1 = Quantity("mass_1")
mass_2 = Quantity("mass_2")
dxy_1 = Quantity("dxy_1")
dxy_2 = Quantity("dxy_2")
dz_1 = Quantity("dz_1")
dz_2 = Quantity("dz_2")
q_1 = Quantity("q_1")
q_2 = Quantity("q_2")
iso_1 = Quantity("iso_1")
iso_2 = Quantity("iso_2")
is_global_1 = Quantity("is_global_1")
is_global_2 = Quantity("is_global_2")
tau_decaymode_1 = Quantity("tau_decaymode_1")
tau_decaymode_2 = Quantity("tau_decaymode_2")
gen_match_1 = Quantity("gen_match_1")
gen_match_2 = Quantity("gen_match_2")
tau_gen_match_1 = Quantity("tau_gen_match_1")
tau_gen_match_2 = Quantity("tau_gen_match_2")
gen_tau_p4_1 = Quantity("gen_tau_p4_1")
gen_tau_p4_2 = Quantity("gen_tau_p4_2")
gen_tau_pt_1 = Quantity("gen_tau_pt_1")
gen_tau_pt_2 = Quantity("gen_tau_pt_2")
gen_tau_eta_1 = Quantity("gen_tau_eta_1")
gen_tau_eta_2 = Quantity("gen_tau_eta_2")
gen_tau_phi_1 = Quantity("gen_tau_phi_1")
gen_tau_phi_2 = Quantity("gen_tau_phi_2")
gen_tau_mass_1 = Quantity("gen_tau_mass_1")
gen_tau_mass_2 = Quantity("gen_tau_mass_2")
gen_tau_m_inv = Quantity("gen_tau_m_inv")
gen_tau_deltaR = Quantity("gen_tau_deltaR")
gen_boostedtaupair_match_flag = Quantity("gen_boostedtaupair_match_flag")
taujet_pt_1 = Quantity("taujet_pt_1")
taujet_pt_2 = Quantity("taujet_pt_2")
gen_taujet_pt_1 = Quantity("gen_taujet_pt_1")
gen_taujet_pt_2 = Quantity("gen_taujet_pt_2")
muon_nstations_1 = Quantity("muon_nstations_1")
muon_nstations_2 = Quantity("muon_nstations_2")
muon_ntrackerlayers_1 = Quantity("muon_ntrackerlayers_1")
muon_ntrackerlayers_2 = Quantity("muon_ntrackerlayers_2")
muon_pterr_1 = Quantity("muon_pterr_1")
muon_pterr_2 = Quantity("muon_pterr_2")

# b-pair quantities bpair_reg_res_2_boosted
bpair_p4_1 = Quantity("bpair_p4_1")
bpair_p4_2 = Quantity("bpair_p4_2")
bpair_pt_1 = Quantity("bpair_pt_1")
bpair_eta_1 = Quantity("bpair_eta_1")
bpair_phi_1 = Quantity("bpair_phi_1")
bpair_mass_1 = Quantity("bpair_mass_1")
bpair_btag_value_1 = Quantity("bpair_btag_value_1")
bpair_reg_res_1 = Quantity("bpair_reg_res_1")
bpair_pt_2 = Quantity("bpair_pt_2")
bpair_eta_2 = Quantity("bpair_eta_2")
bpair_phi_2 = Quantity("bpair_phi_2")
bpair_mass_2 = Quantity("bpair_mass_2")
bpair_btag_value_2 = Quantity("bpair_btag_value_2")
bpair_reg_res_2 = Quantity("bpair_reg_res_2")
p4_bpair = Quantity("p4_bpair")
bpair_deltaR = Quantity("bpair_deltaR")
bpair_m_inv = Quantity("bpair_m_inv")
bpair_pt_dijet = Quantity("bpair_pt_dijet")
genjet_p4_1 = Quantity("genjet_p4_1")
genjet_p4_2 = Quantity("genjet_p4_2")
genjet_pt_1 = Quantity("genjet_pt_1")
genjet_eta_1 = Quantity("genjet_eta_1")
genjet_phi_1 = Quantity("genjet_phi_1")
genjet_mass_1 = Quantity("genjet_mass_1")
genjet_hadFlavour_1 = Quantity("genjet_hadFlavour_1")
genjet_pt_2 = Quantity("genjet_pt_2")
genjet_eta_2 = Quantity("genjet_eta_2")
genjet_phi_2 = Quantity("genjet_phi_2")
genjet_mass_2 = Quantity("genjet_mass_2")
genjet_hadFlavour_2 = Quantity("genjet_hadFlavour_2")
genjet_m_inv = Quantity("genjet_m_inv")
gen_b_p4_1 = Quantity("gen_b_p4_1")
gen_b_p4_2 = Quantity("gen_b_p4_2")
gen_b_pt_1 = Quantity("gen_b_pt_1")
gen_b_eta_1 = Quantity("gen_b_eta_1")
gen_b_phi_1 = Quantity("gen_b_phi_1")
gen_b_mass_1 = Quantity("gen_b_mass_1")
gen_b_pt_2 = Quantity("gen_b_pt_2")
gen_b_eta_2 = Quantity("gen_b_eta_2")
gen_b_phi_2 = Quantity("gen_b_phi_2")
gen_b_mass_2 = Quantity("gen_b_mass_2")
gen_b_m_inv = Quantity("gen_b_m_inv")
gen_b_deltaR = Quantity("gen_b_deltaR")
gen_bpair_match_flag = Quantity("gen_bpair_match_flag")
bpair_p4_1_boosted = Quantity("bpair_p4_1_boosted")
bpair_p4_2_boosted = Quantity("bpair_p4_2_boosted")
bpair_pt_1_boosted = Quantity("bpair_pt_1_boosted")
bpair_eta_1_boosted = Quantity("bpair_eta_1_boosted")
bpair_phi_1_boosted = Quantity("bpair_phi_1_boosted")
bpair_mass_1_boosted = Quantity("bpair_mass_1_boosted")
bpair_btag_value_1_boosted = Quantity("bpair_btag_value_1_boosted")
bpair_reg_res_1_boosted = Quantity("bpair_reg_res_1_boosted")
bpair_pt_2_boosted = Quantity("bpair_pt_2_boosted")
bpair_eta_2_boosted = Quantity("bpair_eta_2_boosted")
bpair_phi_2_boosted = Quantity("bpair_phi_2_boosted")
bpair_mass_2_boosted = Quantity("bpair_mass_2_boosted")
bpair_btag_value_2_boosted = Quantity("bpair_btag_value_2_boosted")
bpair_reg_res_2_boosted = Quantity("bpair_reg_res_2_boosted")
p4_bpair_boosted = Quantity("p4_bpair_boosted")
bpair_deltaR_boosted = Quantity("bpair_deltaR_boosted")
bpair_m_inv_boosted = Quantity("bpair_m_inv_boosted")
bpair_pt_dijet_boosted = Quantity("bpair_pt_dijet_boosted")

# Combined event quantities
p4_vis = Quantity("p4_vis")
m_vis = Quantity("m_vis")
p4_fastmtt = Quantity("p4_fastmtt")
m_fastmtt = Quantity("m_fastmtt")
pt_fastmtt = Quantity("pt_fastmtt")
eta_fastmtt = Quantity("eta_fastmtt")
phi_fastmtt = Quantity("phi_fastmtt")
pt_vis = Quantity("pt_vis")
pzetamissvis = Quantity("pzetamissvis")
mTdileptonMET = Quantity("mTdileptonMET")
mt_1 = Quantity("mt_1")
mt_2 = Quantity("mt_2")
p4_tautau = Quantity("p4_tautau")
pt_tautau = Quantity("pt_tautau")
pt_ttjj = Quantity("pt_ttjj")
p4_tautaubb = Quantity("p4_tautaubb")
pt_tautaubb = Quantity("pt_tautaubb")
mass_tautaubb = Quantity("mass_tautaubb")
mt_tot = Quantity("mt_tot")
deltaR_ditaupair = Quantity("deltaR_ditaupair")
pzetamissvis_pf = Quantity("pzetamissvis_pf")
mTdileptonMET_pf = Quantity("mTdileptonMET_pf")
mt_1_pf = Quantity("mt_1_pf")
mt_2_pf = Quantity("mt_2_pf")
pt_tt_pf = Quantity("pt_tt_pf")
pt_ttjj_pf = Quantity("pt_ttjj_pf")
pt_ttbb_pf = Quantity("pt_ttbb_pf")
mt_tot_pf = Quantity("mt_tot_pf")
pt_dijet = Quantity("pt_dijet")
jet_hemisphere = Quantity("jet_hemisphere")

# Jet and b Jet quantities
njets = Quantity("njets")
nbtag = Quantity("nbtag")
njets_boosted = Quantity("njets_boosted")
nbtag_boosted = Quantity("nbtag_boosted")
jet_p4_1 = Quantity("jet_p4_1")
jpt_1 = Quantity("jpt_1")
jeta_1 = Quantity("jeta_1")
jphi_1 = Quantity("jphi_1")
jtag_value_1 = Quantity("jtag_value_1")
jet_p4_2 = Quantity("jet_p4_2")
jpt_2 = Quantity("jpt_2")
jeta_2 = Quantity("jeta_2")
jphi_2 = Quantity("jphi_2")
jtag_value_2 = Quantity("jtag_value_2")
mjj = Quantity("mjj")
bjet_p4_1 = Quantity("bjet_p4_1")
bpt_1 = Quantity("bpt_1")
beta_1 = Quantity("beta_1")
bphi_1 = Quantity("bphi_1")
btag_value_1 = Quantity("btag_value_1")
bjet_p4_2 = Quantity("bjet_p4_2")
bpt_2 = Quantity("bpt_2")
beta_2 = Quantity("beta_2")
bphi_2 = Quantity("bphi_2")
btag_value_2 = Quantity("btag_value_2")

# FatJet quantities
nfatjets = Quantity("nfatjets")
fatjet_p4_1 = Quantity("fatjet_p4_1")
fj_pt_1 = Quantity("fj_pt_1")
fj_eta_1 = Quantity("fj_eta_1")
fj_phi_1 = Quantity("fj_phi_1")
fj_mass_1 = Quantity("fj_mass_1")
fj_msoftdrop_1 = Quantity("fj_msoftdrop_1")
fj_particleNet_XbbvsQCD_1 = Quantity("fj_particleNet_XbbvsQCD_1")
fj_nsubjettiness_2over1_1 = Quantity("fj_nsubjettiness_2over1_1")
fj_nsubjettiness_3over2_1 = Quantity("fj_nsubjettiness_3over2_1")
fatjet_p4_2 = Quantity("fatjet_p4_2")
fj_pt_2 = Quantity("fj_pt_2")
fj_eta_2 = Quantity("fj_eta_2")
fj_phi_2 = Quantity("fj_phi_2")
fj_mass_2 = Quantity("fj_mass_2")
fj_msoftdrop_2 = Quantity("fj_msoftdrop_2")
fj_particleNet_XbbvsQCD_2 = Quantity("fj_particleNet_XbbvsQCD_2")
fj_nsubjettiness_2over1_2 = Quantity("fj_nsubjettiness_2over1_2")
fj_nsubjettiness_3over2_2 = Quantity("fj_nsubjettiness_3over2_2")
bpair_fatjet = Quantity("bpair_fatjet")
matched_fatjet_p4 = Quantity("matched_fatjet_p4")
fj_matched_pt = Quantity("fj_matched_pt")
fj_matched_eta = Quantity("fj_matched_eta")
fj_matched_phi = Quantity("fj_matched_phi")
fj_matched_mass = Quantity("fj_matched_mass")
fj_matched_msoftdrop = Quantity("fj_matched_msoftdrop")
fj_matched_particleNet_XbbvsQCD = Quantity("fj_matched_particleNet_XbbvsQCD")
fj_matched_nsubjettiness_2over1 = Quantity("fj_matched_nsubjettiness_2over1")
fj_matched_nsubjettiness_3over2 = Quantity("fj_matched_nsubjettiness_3over2")
Xbb_fatjet = Quantity("Xbb_fatjet")
Xbb_fatjet_p4 = Quantity("Xbb_fatjet_p4")
fj_Xbb_pt = Quantity("fj_Xbb_pt")
fj_Xbb_eta = Quantity("fj_Xbb_eta")
fj_Xbb_phi = Quantity("fj_Xbb_phi")
fj_Xbb_mass = Quantity("fj_Xbb_mass")
fj_Xbb_msoftdrop = Quantity("fj_Xbb_msoftdrop")
fj_Xbb_particleNet_XbbvsQCD = Quantity("fj_Xbb_particleNet_XbbvsQCD")
fj_Xbb_nsubjettiness_2over1 = Quantity("fj_Xbb_nsubjettiness_2over1")
fj_Xbb_nsubjettiness_3over2 = Quantity("fj_Xbb_nsubjettiness_3over2")
fj_Xbb_hadflavor = Quantity("fj_Xbb_hadflavor")
fj_Xbb_nBhad = Quantity("fj_Xbb_nBhad")
fj_Xbb_nChad = Quantity("fj_Xbb_nChad")
nfatjets_boosted = Quantity("nfatjets_boosted")
Xbb_fatjet_boosted = Quantity("Xbb_fatjet_boosted")
Xbb_fatjet_p4_boosted = Quantity("Xbb_fatjet_p4_boosted")
fj_Xbb_pt_boosted = Quantity("fj_Xbb_pt_boosted")
fj_Xbb_eta_boosted = Quantity("fj_Xbb_eta_boosted")
fj_Xbb_phi_boosted = Quantity("fj_Xbb_phi_boosted")
fj_Xbb_mass_boosted = Quantity("fj_Xbb_mass_boosted")
fj_Xbb_msoftdrop_boosted = Quantity("fj_Xbb_msoftdrop_boosted")
fj_Xbb_particleNet_XbbvsQCD_boosted = Quantity("fj_Xbb_particleNet_XbbvsQCD_boosted")
fj_Xbb_nsubjettiness_2over1_boosted = Quantity("fj_Xbb_nsubjettiness_2over1_boosted")
fj_Xbb_nsubjettiness_3over2_boosted = Quantity("fj_Xbb_nsubjettiness_3over2_boosted")
fj_Xbb_hadflavor_boosted = Quantity("fj_Xbb_hadflavor_boosted")
fj_Xbb_nBhad_boosted = Quantity("fj_Xbb_nBhad_boosted")
fj_Xbb_nChad_boosted = Quantity("fj_Xbb_nChad_boosted")
pNet_Xbb_weight = Quantity("pNet_Xbb_weight")
# pNet_Xbb_weight_flv = Quantity("pNet_Xbb_weight_flv")
pNet_Xbb_weight_boosted = Quantity("pNet_Xbb_weight_boosted")
leading_fatjet_p4 = Quantity("leading_fatjet_p4")
fj_leading_pt = Quantity("fj_leading_pt")
fj_leading_msoftdrop = Quantity("fj_leading_msoftdrop")

dielectron_veto = Quantity("dielectron_veto")
dimuon_veto = Quantity("dimuon_veto")
dilepton_veto = Quantity("dilepton_veto")

## Gen Quantities
gen_p4_1 = Quantity("gen_p4_1")
gen_pt_1 = Quantity("gen_pt_1")
gen_eta_1 = Quantity("gen_eta_1")
gen_phi_1 = Quantity("gen_phi_1")
gen_mass_1 = Quantity("gen_mass_1")
gen_pdgid_1 = Quantity("gen_pdgid_1")

gen_p4_2 = Quantity("gen_p4_2")
gen_pt_2 = Quantity("gen_pt_2")
gen_eta_2 = Quantity("gen_eta_2")
gen_phi_2 = Quantity("gen_phi_2")
gen_mass_2 = Quantity("gen_mass_2")
gen_pdgid_2 = Quantity("gen_pdgid_2")
gen_m_vis = Quantity("gen_m_vis")

hadronic_gen_taus = Quantity("hadronic_gen_taus")

topPtReweightWeight = Quantity("topPtReweightWeight")
ZPtMassReweightWeight = Quantity("ZPtMassReweightWeight")

## HTXS quantities
ggh_NNLO_weight = Quantity("ggh_NNLO_weight")
THU_ggH_Mu = Quantity("THU_ggH_Mu")
THU_ggH_Res = Quantity("THU_ggH_Res")
THU_ggH_Mig01 = Quantity("THU_ggH_Mig01")
THU_ggH_Mig12 = Quantity("THU_ggH_Mig12")
THU_ggH_VBF2j = Quantity("THU_ggH_VBF2j")
THU_ggH_VBF3j = Quantity("THU_ggH_VBF3j")
THU_ggH_PT60 = Quantity("THU_ggH_PT60")
THU_ggH_PT120 = Quantity("THU_ggH_PT120")
THU_ggH_qmtop = Quantity("THU_ggH_qmtop")
THU_qqH_TOT = Quantity("THU_qqH_TOT")
THU_qqH_PTH200 = Quantity("THU_qqH_PTH200")
THU_qqH_Mjj60 = Quantity("THU_qqH_Mjj60")
THU_qqH_Mjj120 = Quantity("THU_qqH_Mjj120")
THU_qqH_Mjj350 = Quantity("THU_qqH_Mjj350")
THU_qqH_Mjj700 = Quantity("THU_qqH_Mjj700")
THU_qqH_Mjj1000 = Quantity("THU_qqH_Mjj1000")
THU_qqH_Mjj1500 = Quantity("THU_qqH_Mjj1500")
THU_qqH_25 = Quantity("THU_qqH_25")
THU_qqH_JET01 = Quantity("THU_qqH_JET01")

## MET quantities
met_p4 = Quantity("met_p4")
recoil_genboson_p4_vec = Quantity("recoil_genboson_p4_vec")
genbosonmass = Quantity("genbosonmass")
npartons = Quantity("npartons")
met_p4_leptoncorrected = Quantity("met_p4_leptoncorrected")
met_p4_jetcorrected = Quantity("met_p4_jetcorrected")
met_p4_recoilcorrected = Quantity("met_p4_recoilcorrected")
met = Quantity("met")
metphi = Quantity("metphi")
metSumEt = Quantity("metSumEt")
metcov00 = Quantity("metcov00")
metcov01 = Quantity("metcov01")
metcov10 = Quantity("metcov10")
metcov11 = Quantity("metcov11")
met_uncorrected = Quantity("met_uncorrected")
metphi_uncorrected = Quantity("metphi_uncorrected")
met_p4_boosted_leptoncorrected = Quantity("met_p4_boosted_leptoncorrected")
met_p4_boosted_jetcorrected = Quantity("met_p4_boosted_jetcorrected")
met_p4_boosted_recoilcorrected = Quantity("met_p4_boosted_recoilcorrected")
met_boosted = Quantity("met_boosted")
metphi_boosted = Quantity("metphi_boosted")

## PFMET quantities
pfmet = Quantity("pfmet")
pfmet_p4 = Quantity("pfmet_p4")
pfmetphi = Quantity("pfmetphi")
pfmet_uncorrected = Quantity("pfmet_uncorrected")
pfmetphi_uncorrected = Quantity("pfmetphi_uncorrected")
pfmet_p4_leptoncorrected = Quantity("pfmet_p4_leptoncorrected")
pfmet_p4_jetcorrected = Quantity("pfmet_p4_jetcorrected")
pfmet_p4_recoilcorrected = Quantity("pfmet_p4_recoilcorrected")
pfmet_boosted = Quantity("pfmet_boosted")
pfmetphi_boosted = Quantity("pfmetphi_boosted")
pfmet_p4_boosted_leptoncorrected = Quantity("pfmet_p4_boosted_leptoncorrected")
pfmet_p4_boosted_jetcorrected = Quantity("pfmet_p4_boosted_jetcorrected")
pfmet_p4_boosted_recoilcorrected = Quantity("pfmet_p4_boosted_recoilcorrected")

## embedding quantities
emb_genweight = Quantity("emb_genweight")
emb_initialMETEt = Quantity("emb_initialMETEt")
emb_initialMETphi = Quantity("emb_initialMETphi")
emb_initialPuppiMETEt = Quantity("emb_initialPuppiMETEt")
emb_initialPuppiMETphi = Quantity("emb_initialPuppiMETphi")
emb_isMediumLeadingMuon = Quantity("emb_isMediumLeadingMuon")
emb_isMediumTrailingMuon = Quantity("emb_isMediumTrailingMuon")
emb_isTightLeadingMuon = Quantity("emb_isTightLeadingMuon")
emb_isTightTrailingMuon = Quantity("emb_isTightTrailingMuon")
emb_InitialPairCandidates = Quantity("emb_InitialPairCandidates")
emb_SelectionOldMass = Quantity("emb_SelectionOldMass")
emb_SelectionNewMass = Quantity("emb_SelectionNewMass")
emb_triggersel_wgt = Quantity("emb_triggersel_wgt")
emb_idsel_wgt_1 = Quantity("emb_idsel_wgt_1")
emb_idsel_wgt_2 = Quantity("emb_idsel_wgt_2")

# sample flags
is_data = Quantity("is_data")
is_embedding = Quantity("is_embedding")
is_ttbar = Quantity("is_ttbar")
is_dyjets = Quantity("is_dyjets")
is_wjets = Quantity("is_wjets")
is_ggh_htautau = Quantity("is_ggh_htautau")
is_vbf_htautau = Quantity("is_vbf_htautau")
is_diboson = Quantity("is_diboson")
is_vbf_hbb = Quantity("is_vbf_hbb")
is_ggh_hbb = Quantity("is_ggh_hbb")
is_rem_hbb = Quantity("is_rem_hbb")
is_embedding_mc = Quantity("is_embedding_mc")
is_singletop = Quantity("is_singletop")
is_rem_htautau = Quantity("is_rem_htautau")
is_electroweak_boson = Quantity("is_electroweak_boson")


# Electron Weights
reco_wgt_ele_1 = Quantity("reco_wgt_ele_1")
reco_wgt_ele_2 = Quantity("reco_wgt_ele_2")
id_wgt_ele_wp90nonIso_1 = Quantity("id_wgt_ele_wp90nonIso_1")
id_wgt_ele_wp90nonIso_2 = Quantity("id_wgt_ele_wp90nonIso_2")
id_wgt_ele_wp80nonIso_1 = Quantity("id_wgt_ele_wp80nonIso_1")
id_wgt_ele_wp80nonIso_2 = Quantity("id_wgt_ele_wp80nonIso_2")
id_wgt_ele_1 = Quantity("id_wgt_ele_1")
id_wgt_ele_2 = Quantity("id_wgt_ele_2")
iso_wgt_ele_1 = Quantity("iso_wgt_ele_1")
iso_wgt_ele_2 = Quantity("iso_wgt_ele_2")
reco_wgt_ele_boosted_1 = Quantity("reco_wgt_ele_boosted_1")
id_wgt_ele_boosted_wp90nonIso_1 = Quantity("id_wgt_ele_boosted_wp90nonIso_1")
id_wgt_ele_boosted_wp80nonIso_1 = Quantity("id_wgt_ele_boosted_wp80nonIso_1")
id_wgt_ele_boosted_1 = Quantity("id_wgt_ele_boosted_1")
iso_wgt_ele_boosted_1 = Quantity("iso_wgt_ele_boosted_1")
# Muon weights
id_wgt_mu_1 = Quantity("id_wgt_mu_1")
id_wgt_mu_2 = Quantity("id_wgt_mu_2")
iso_wgt_mu_1 = Quantity("iso_wgt_mu_1")
iso_wgt_mu_2 = Quantity("iso_wgt_mu_2")
reco_wgt_mu_boosted_1 = Quantity("reco_wgt_mu_boosted_1")
id_wgt_mu_boosted_1 = Quantity("id_wgt_mu_boosted_1")
iso_wgt_mu_boosted_1 = Quantity("iso_wgt_mu_boosted_1")
# trg_wgt_single_mu50_boosted = Quantity("trg_wgt_single_mu50_boosted")
emb_id_wgt_mu_boosted_1 = Quantity("emb_id_wgt_mu_boosted_1")
emb_iso_wgt_mu_boosted_1 = Quantity("emb_iso_wgt_mu_boosted_1")
# btag weight
btag_weight = Quantity("btag_weight")
btag_weight_boosted = Quantity("btag_weight_boosted")
# ditau trigger weights
trg_wgt_double_tau_1 = Quantity("trg_wgt_double_tau_1")
trg_wgt_double_tau_2 = Quantity("trg_wgt_double_tau_2")
trg_wgt_fatjet = Quantity("trg_wgt_fatjet")

# ML variables
transformed_njets = Quantity("transformed_njets")
transformed_nbtag = Quantity("transformed_nbtag")
transformed_nfatjets = Quantity("transformed_nfatjets")
transformed_pt_1 = Quantity("transformed_pt_1")
transformed_pt_2 = Quantity("transformed_pt_2")
transformed_eta_1 = Quantity("transformed_eta_1")
transformed_eta_2 = Quantity("transformed_eta_2")
transformed_phi_1 = Quantity("transformed_phi_1")
transformed_phi_2 = Quantity("transformed_phi_2")
transformed_deltaR_ditaupair = Quantity("transformed_deltaR_ditaupair")
transformed_m_vis = Quantity("transformed_m_vis")
transformed_m_fastmtt = Quantity("transformed_m_fastmtt")
transformed_pt_fastmtt = Quantity("transformed_pt_fastmtt")
transformed_eta_fastmtt = Quantity("transformed_eta_fastmtt")
transformed_phi_fastmtt = Quantity("transformed_phi_fastmtt")
transformed_bpair_pt_1 = Quantity("transformed_bpair_pt_1")
transformed_bpair_eta_1 = Quantity("transformed_bpair_eta_1")
transformed_bpair_phi_1 = Quantity("transformed_bpair_phi_1")
transformed_bpair_btag_value_1 = Quantity("transformed_bpair_btag_value_1")
transformed_bpair_pt_2 = Quantity("transformed_bpair_pt_2")
transformed_bpair_eta_2 = Quantity("transformed_bpair_eta_2")
transformed_bpair_phi_2 = Quantity("transformed_bpair_phi_2")
transformed_bpair_btag_value_2 = Quantity("transformed_bpair_btag_value_2")
transformed_bpair_m_inv = Quantity("transformed_bpair_m_inv")
transformed_bpair_deltaR = Quantity("transformed_bpair_deltaR")
transformed_bpair_pt_dijet = Quantity("transformed_bpair_pt_dijet")
transformed_fj_Xbb_pt = Quantity("transformed_fj_Xbb_pt")
transformed_fj_Xbb_eta = Quantity("transformed_fj_Xbb_eta")
transformed_fj_Xbb_phi = Quantity("transformed_fj_Xbb_phi")
transformed_fj_Xbb_msoftdrop = Quantity("transformed_fj_Xbb_msoftdrop")
transformed_fj_Xbb_nsubjettiness_2over1 = Quantity("transformed_fj_Xbb_nsubjettiness_2over1")
transformed_fj_Xbb_nsubjettiness_3over2 = Quantity("transformed_fj_Xbb_nsubjettiness_3over2")
transformed_met = Quantity("transformed_met")
transformed_metphi = Quantity("transformed_metphi")
transformed_mass_tautaubb = Quantity("transformed_mass_tautaubb")
transformed_pt_tautaubb = Quantity("transformed_pt_tautaubb")
transformed_kinfit_mX = Quantity("transformed_kinfit_mX")
transformed_kinfit_mY = Quantity("transformed_kinfit_mY")
transformed_kinfit_chi2 = Quantity("transformed_kinfit_chi2")
transformed_mt_1 = Quantity("transformed_mt_1")

transformed_njets_boosted = Quantity("transformed_njets_boosted")
transformed_nbtag_boosted = Quantity("transformed_nbtag_boosted")
transformed_nfatjets_boosted = Quantity("transformed_nfatjets_boosted")
transformed_boosted_pt_1 = Quantity("transformed_boosted_pt_1")
transformed_boosted_pt_2 = Quantity("transformed_boosted_pt_2")
transformed_boosted_eta_1 = Quantity("transformed_boosted_eta_1")
transformed_boosted_eta_2 = Quantity("transformed_boosted_eta_2")
transformed_boosted_phi_1 = Quantity("transformed_boosted_phi_1")
transformed_boosted_phi_2 = Quantity("transformed_boosted_phi_2")
transformed_boosted_deltaR_ditaupair = Quantity("transformed_boosted_deltaR_ditaupair")
transformed_boosted_m_vis = Quantity("transformed_boosted_m_vis")
transformed_boosted_m_fastmtt = Quantity("transformed_boosted_m_fastmtt")
transformed_boosted_pt_fastmtt = Quantity("transformed_boosted_pt_fastmtt")
transformed_boosted_eta_fastmtt = Quantity("transformed_boosted_eta_fastmtt")
transformed_boosted_phi_fastmtt = Quantity("transformed_boosted_phi_fastmtt")
transformed_bpair_pt_1_boosted = Quantity("transformed_bpair_pt_1_boosted")
transformed_bpair_eta_1_boosted = Quantity("transformed_bpair_eta_1_boosted")
transformed_bpair_phi_1_boosted = Quantity("transformed_bpair_phi_1_boosted")
transformed_bpair_btag_value_1_boosted = Quantity("transformed_bpair_btag_value_1_boosted")
transformed_bpair_pt_2_boosted = Quantity("transformed_bpair_pt_2_boosted")
transformed_bpair_eta_2_boosted = Quantity("transformed_bpair_eta_2_boosted")
transformed_bpair_phi_2_boosted = Quantity("transformed_bpair_phi_2_boosted")
transformed_bpair_btag_value_2_boosted = Quantity("transformed_bpair_btag_value_2_boosted")
transformed_bpair_m_inv_boosted = Quantity("transformed_bpair_m_inv_boosted")
transformed_bpair_deltaR_boosted = Quantity("transformed_bpair_deltaR_boosted")
transformed_bpair_pt_dijet_boosted = Quantity("transformed_bpair_pt_dijet_boosted")
transformed_fj_Xbb_pt_boosted = Quantity("transformed_fj_Xbb_pt_boosted")
transformed_fj_Xbb_eta_boosted = Quantity("transformed_fj_Xbb_eta_boosted")
transformed_fj_Xbb_phi_boosted = Quantity("transformed_fj_Xbb_phi_boosted")
transformed_fj_Xbb_msoftdrop_boosted = Quantity("transformed_fj_Xbb_msoftdrop_boosted")
transformed_fj_Xbb_nsubjettiness_2over1_boosted = Quantity("transformed_fj_Xbb_nsubjettiness_2over1_boosted")
transformed_fj_Xbb_nsubjettiness_3over2_boosted = Quantity("transformed_fj_Xbb_nsubjettiness_3over2_boosted")
transformed_met_boosted = Quantity("transformed_met_boosted")
transformed_metphi_boosted = Quantity("transformed_metphi_boosted")
transformed_boosted_mass_tautaubb = Quantity("transformed_boosted_mass_tautaubb")
transformed_boosted_pt_tautaubb = Quantity("transformed_boosted_pt_tautaubb")
transformed_kinfit_mX_boosted = Quantity("transformed_kinfit_mX_boosted")
transformed_kinfit_mY_boosted = Quantity("transformed_kinfit_mY_boosted")
transformed_kinfit_chi2_boosted = Quantity("transformed_kinfit_chi2_boosted")
transformed_boosted_mt_1 = Quantity("transformed_boosted_mt_1")