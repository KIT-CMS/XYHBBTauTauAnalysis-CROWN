#ifndef GUARD_SCALEFACTORSEXT_H
#define GUARD_SCALEFACTORSEXT_H


namespace v12 {

namespace scalefactor {

namespace jet {

ROOT::RDF::RNode
btagSF(ROOT::RDF::RNode df,
       correctionManager::CorrectionManager &correctionManager,
       const std::string &pt, const std::string &eta,
       const std::string &btag_discr, const std::string &flavor,
       const std::string &jet_mask, const std::string &bjet_mask,
       const std::string &jet_veto_mask, const std::string &variation,
       const std::string &sf_output, const std::string &sf_file,
       const std::string &corr_algorithm);

} // namespace jet

} // scalefactor

} // namespace v12


namespace scalefactor {

namespace muon {

ROOT::RDF::RNode
trigger(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &eta, const std::string &year_id,
    const std::string &variation,
    const std::string &trigger_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

namespace tau {

ROOT::RDF::RNode
id_mva_vsJet_lt(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &decayMode,
    const std::string &genMatch,
    const std::vector<int> &selectedDMs,
    const std::string &wp,
    const std::string &sf_vsjet_tau30to35,
    const std::string &sf_vsjet_tau35to40,
    const std::string &sf_vsjet_tau40to500,
    const std::string &sf_vsjet_tau500to1000,
    const std::string &sf_vsjet_tau1000toinf,
    const std::string &sf_dependence,
    const std::string &vsele_wp,
    const std::string &id_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

ROOT::RDF::RNode
id_mva_vsJet_tt(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &decayMode,
    const std::string &genMatch,
    const std::vector<int> &selectedDMs,
    const std::string &wp,
    const std::string &sf_vsjet_tauDM0,
    const std::string &sf_vsjet_tauDM1,
    const std::string &sf_vsjet_tauDM10,
    const std::string &sf_vsjet_tauDM11,
    const std::string &sf_dependence,
    const std::string &vsele_wp,
    const std::string &id_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

} // namespace tau


namespace fatjet {

ROOT::RDF::RNode
pNetXbbSF(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &nBhad,
    const std::string &nChad, 
    const std::string &variation,
    const std::string &sf_output,
    const std::string &sf_file
);

ROOT::RDF::RNode
trigger(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &msoftdrop,
    const std::string &sf_output, 
    const std::string &sf_file,
    const std::string &sf_name, 
    const std::string &variation
);

} // namespace fatjet

} // end scalefactor

#endif