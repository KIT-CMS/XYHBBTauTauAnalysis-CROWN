#ifndef GUARD_SCALEFACTORSEXT_H
#define GUARD_SCALEFACTORSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"


namespace v12 {

namespace scalefactor {

namespace jet {

/**
 * @brief Function used to evaluate b-tagging scale factors of jets with
 * correctionlib, configurations:
 * - [UL2018 b-tagging
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/BTV_btagging_Run2_UL/BTV_btagging_2018_UL.html)
 * - [UL2017 b-tagging
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/BTV_btagging_Run2_UL/BTV_btagging_2017_UL.html)
 * - [UL2016preVFP b-tagging
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/BTV_btagging_Run2_UL/BTV_btagging_2016preVFP_UL.html)
 * - [UL2016postVFP b-tagging
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/BTV_btagging_Run2_UL/BTV_btagging_2016postVFP_UL.html)
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt jet pt
 * @param eta jet eta
 * @param btag_discr btag value of a jet based on a b-jet tagger (e.g. DeepJet)
 * @param flavor flavor of the jet
 * @param jet_mask mask for good/selected jets
 * @param bjet_mask mask for good/selected b jets
 * @param jet_veto_mask veto mask for overlapping jets
 * @param variation id for the variation of the scale factor. Available Values:
 * central, down_*, up_* (* name of variation)
 * @param sf_output name of the scale factor column
 * @param sf_file path to the file with the btagging scale factors
 * @param corr_algorithm name of the btagging correction algorithm
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode
btagSF(ROOT::RDF::RNode df,
       correctionManager::CorrectionManager &correctionManager,
       const std::string &pt, const std::string &eta,
       const std::string &btag_discr, const std::string &flavor,
       const std::string &jet_mask, const std::string &bjet_mask,
       const std::string &jet_veto_mask, const std::string &variation,
       const std::string &sf_output, const std::string &sf_file,
       const std::string &corr_algorithm) {
    Logger::get("btagSF")->debug(
        "Setting up functions for b-tag sf with correctionlib");
    Logger::get("btagSF")->debug("Correction algorithm - Name {}",
                                 corr_algorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, corr_algorithm);
    auto btagSF_lambda = [evaluator,
                          variation](const ROOT::RVec<float> &pt_values,
                                     const ROOT::RVec<float> &eta_values,
                                     const ROOT::RVec<float> &btag_values,
                                     const ROOT::RVec<UChar_t> &flavors,
                                     const ROOT::RVec<int> &jet_mask,
                                     const ROOT::RVec<int> &bjet_mask,
                                     const ROOT::RVec<int> &jet_veto_mask) {
        Logger::get("btagSF")->debug("Vatiation - Name {}", variation);
        float sf = 1.;
        for (int i = 0; i < pt_values.size(); i++) {
            Logger::get("btagSF")->debug(
                "jet masks - jet {}, bjet {}, jet veto {}", jet_mask.at(i),
                bjet_mask.at(i), jet_veto_mask.at(i));
            // considering only good jets/bjets, this is needed since jets and
            // bjets might have different cuts depending on the analysis
            if ((jet_mask.at(i) || bjet_mask.at(i)) && jet_veto_mask.at(i)) {
                Logger::get("btagSF")->debug(
                    "SF - pt {}, eta {}, btag value {}, flavor {}",
                    pt_values.at(i), eta_values.at(i), btag_values.at(i),
                    flavors.at(i));
                float jet_sf = 1.;
                // considering only phase space where the scale factors are
                // defined
                if (pt_values.at(i) >= 20.0 && pt_values.at(i) < 10000.0 &&
                    std::abs(eta_values.at(i)) < 2.5) {
                    // for c jet related uncertainties only scale factors of
                    // c-jets are varied, the rest is nominal/central
                    if (variation.find("cferr") != std::string::npos) {
                        // flavor=4 means c-flavor
                        if (flavors.at(i) == 4) {
                            jet_sf = evaluator->evaluate(
                                {variation, flavors.at(i),
                                 std::abs(eta_values.at(i)), pt_values.at(i),
                                 btag_values.at(i)});
                        } else {
                            jet_sf = evaluator->evaluate(
                                {"central", flavors.at(i),
                                 std::abs(eta_values.at(i)), pt_values.at(i),
                                 btag_values.at(i)});
                        }
                    }
                    // for nominal/central and all other uncertainties c-jets
                    // have a scale factor of 1 (only for central defined in
                    // json file from BTV)
                    else {
                        if (flavors.at(i) != 4) {
                            jet_sf = evaluator->evaluate(
                                {variation, flavors.at(i),
                                 std::abs(eta_values.at(i)), pt_values.at(i),
                                 btag_values.at(i)});
                        } else {
                            jet_sf = evaluator->evaluate(
                                {"central", flavors.at(i),
                                 std::abs(eta_values.at(i)), pt_values.at(i),
                                 btag_values.at(i)});
                        }
                    }
                }
                Logger::get("btagSF")->debug("Jet Scale Factor {}", jet_sf);
                sf *= jet_sf;
            }
        };
        Logger::get("btagSF")->debug("Event Scale Factor {}", sf);
        return sf;
    };
    auto df1 = df.Define(
        sf_output, btagSF_lambda,
        {pt, eta, btag_discr, flavor, jet_mask, bjet_mask, jet_veto_mask});
    return df1;
}

} // namespace jet

} // namespace scalefactor

} // namespace v12


namespace scalefactor {

namespace muon {

/**
 * @brief Function used to evaluate trigger scale factors from muons with
 * correctionlib. Configurations:
 * - [UL2018 Muon
 * Iso](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2018_UL.html)
 * - [UL2017 Muon
 * Iso](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2017_UL.html)
 * - [UL2016preVFP Muon
 * Iso](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2016preVFP_UL.html)
 * - [UL2016postVFP Muon
 * Iso](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2016postVFP_UL.html)
 *
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt muon pt
 * @param eta muon eta
 * @param year_id id for the year of data taking and mc compaign
 * @param variation id for the variation of the scale factor "sf" for nominal
 * and "systup"/"systdown" the up/down variation
 * @param trigger_output name of the trigger scale factor column
 * @param sf_file path to the file with the muon scale factors
 * @param idAlgorithm name of the muon trigger scale factor
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode trigger(ROOT::RDF::RNode df, correctionManager::CorrectionManager &correctionManager, 
                         const std::string &pt,
                         const std::string &eta,
                         const std::string &variation,
                         const std::string &trigger_output,
                         const std::string &sf_file,
                         const std::string &idAlgorithm) {

    Logger::get("muonTriggerSF")
        ->debug("Setting up functions for muon trigger sf");
    Logger::get("muonTriggerSF")->debug("Trigger - Name {}", idAlgorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, idAlgorithm);
    auto df1 =
        df.Define(trigger_output,
                  [evaluator, variation,
                   idAlgorithm](const float &pt, const float &eta) {
                      Logger::get("muonTriggerSF")
                          ->debug("Trigger - pt {}, eta {}", pt, eta);
                      double sf = 1.;
                      float low_pt_threshold = 26.0; // for IsoMu24 trigger
                      if (idAlgorithm.find("Mu50") != std::string::npos) {
                          low_pt_threshold = 52.0;
                      }
                      // preventing muons for which scale factor is not defined
                      // for
                      if (pt > low_pt_threshold && std::abs(eta) >= 0.0 &&
                          std::abs(eta) < 2.4) {
                          sf = evaluator->evaluate(
                              {std::abs(eta), pt, variation});
                      }
                      return sf;
                  },
                  {pt, eta});
    return df1;
}

} // end muon

namespace tau {
/**
 * @brief Function used to evaluate vsJets tau id scale factors in the lt
channel with
 * correctionlib

Description of the bit map used to define the tau id working points of the
DeepTau2017v2p1 tagger.
vsJets                              | Value | Bit (value used in the config)
------------------------------------|-------|-------
no ID selection (takes every tau)   |  0    | -
VVVLoose                            |  1    | 1
VVLoose                             |  2    | 2
VLoose                              |  4    | 3
Loose                               |  8    | 4
Medium                              |  16   | 5
Tight                               |  32   | 6
VTight                              |  64   | 7
VVTight                             |  128  | 8
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt tau pt
 * @param decayMode decay mode of the tau
 * @param genMatch column with genmatch values (from prompt e, prompt mu,
 * tau->e, tau->mu, had. tau)
 * @param selectedDMs list of allowed decay modes for which a scale factor
 * should be calculated
 * @param wp working point of the ID cut
 * @param sf_vsjet_tau30to35 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tau35to40 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tau40to500 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tau500to1000 id for the variation of the scale factor "sf"
for nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tau1000toinf id for the variation of the scale factor "sf"
for nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_dependence "pt", "dm" or "eta" based scale factors
 * @param vsele_wp working point of the vsEle cut
 * @param id_output name of the id scale factor column
 * @param sf_file path to the file with the tau scale factors
 * @param idAlgorithm name of the tau id scale factor
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode
id_mva_vsJet_lt(ROOT::RDF::RNode df,
            correctionManager::CorrectionManager &correctionManager,
            const std::string &pt, const std::string &decayMode,
            const std::string &genMatch, const std::vector<int> &selectedDMs,
            const std::string &wp, const std::string &sf_vsjet_tau30to35,
            const std::string &sf_vsjet_tau35to40,
            const std::string &sf_vsjet_tau40to500,
            const std::string &sf_vsjet_tau500to1000,
            const std::string &sf_vsjet_tau1000toinf,
            const std::string &sf_dependence, const std::string &vsele_wp,
            const std::string &id_output, const std::string &sf_file,
            const std::string &idAlgorithm) {

    Logger::get("TauIDMVAvsJet_lt_SF")
        ->debug("Setting up function for tau id vsJet sf");
    Logger::get("TauIDMVAvsJet_lt_SF")->debug("ID - Name {}", idAlgorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, idAlgorithm);
    auto idSF_calculator = [evaluator, wp, vsele_wp, sf_vsjet_tau30to35,
                            sf_vsjet_tau35to40, sf_vsjet_tau40to500,
                            sf_vsjet_tau500to1000, sf_vsjet_tau1000toinf,
                            sf_dependence, selectedDMs,
                            idAlgorithm](const float &pt, const int &decayMode,
                                         const int &genMatch) {
        Logger::get("TauIDMVAvsJet_lt_SF")->debug("ID - decayMode {}", decayMode);
        // only calculate SFs for allowed tau decay modes (also excludes default
        // values due to tau energy correction shifts below good tau pt
        // selection)
        double sf = 1.;
        if (std::find(selectedDMs.begin(), selectedDMs.end(), decayMode) !=
            selectedDMs.end()) {
            Logger::get("TauIDMVAvsJet_lt_SF")
                ->debug("ID {} - pt {}, decayMode {}, genMatch {}, wp {}, "
                        "sf_vsjet_tau30to35 {}, sf_vsjet_tau35to40 {}, "
                        "sf_vsjet_tau40to500{}, sf_vsjet_tau500to1000 {}, "
                        "sf_vsjet_tau1000toinf {}, sf_dependence {}",
                        idAlgorithm, pt, decayMode, genMatch, wp,
                        sf_vsjet_tau30to35, sf_vsjet_tau35to40,
                        sf_vsjet_tau40to500, sf_vsjet_tau500to1000,
                        sf_vsjet_tau1000toinf, sf_dependence);
            if (pt >= 30.0 && pt < 35.0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tau30to35, sf_dependence});
            } else if (pt >= 35.0 && pt < 40.0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tau35to40, sf_dependence});
            } else if (pt >= 40.0 && pt < 500.0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tau40to500, sf_dependence});
            } else if (pt >= 500.0 && pt < 1000.0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tau500to1000, sf_dependence});
            } else if (pt >= 1000.0 && pt < 2000.0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tau1000toinf, sf_dependence});
            } else {
                sf = 1.;
            }
        }
        Logger::get("TauIDvsJet_lt_SF")->debug("Scale Factor {}", sf);
        return sf;
    };
    auto df1 = df.Define(id_output, idSF_calculator, {pt, decayMode, genMatch});
    return df1;
}

/**
 * @brief Function used to evaluate vsJets tau id scale factors in the tt
channel with
 * correctionlib

Description of the bit map used to define the tau id working points of the
DeepTau2017v2p1 tagger.
vsJets                              | Value | Bit (value used in the config)
------------------------------------|-------|-------
no ID selection (takes every tau)   |  0    | -
VVVLoose                            |  1    | 1
VVLoose                             |  2    | 2
VLoose                              |  4    | 3
Loose                               |  8    | 4
Medium                              |  16   | 5
Tight                               |  32   | 6
VTight                              |  64   | 7
VVTight                             |  128  | 8
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt tau pt
 * @param decayMode decay mode of the tau
 * @param genMatch column with genmatch values (from prompt e, prompt mu,
 * tau->e, tau->mu, had. tau)
 * @param selectedDMs list of allowed decay modes for which a scale factor
 * should be calculated
 * @param wp working point of the ID cut
 * @param sf_vsjet_tauDM0 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tauDM1 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tauDM10 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_vsjet_tauDM11 id for the variation of the scale factor "sf" for
nominal
 * and "systup"/"systdown" the up/down variation
 * @param sf_dependence "pt", "dm" or "eta" based scale factors
 * @param vsele_wp working point of the vsEle cut
 * @param id_output name of the id scale factor column
 * @param sf_file path to the file with the tau scale factors
 * @param idAlgorithm name of the tau id scale factor
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode id_mva_vsJet_tt(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt, const std::string &decayMode,
    const std::string &genMatch, const std::vector<int> &selectedDMs,
    const std::string &wp, const std::string &sf_vsjet_tauDM0,
    const std::string &sf_vsjet_tauDM1, const std::string &sf_vsjet_tauDM10,
    const std::string &sf_vsjet_tauDM11, const std::string &sf_dependence,
    const std::string &vsele_wp, const std::string &id_output,
    const std::string &sf_file, const std::string &idAlgorithm) {

    Logger::get("TauIDMVAvsJet_tt_SF")
        ->debug("Setting up function for tau id vsJet sf");
    Logger::get("TauIDMVAvsJet_tt_SF")->debug("ID - Name {}", idAlgorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, idAlgorithm);
    auto idSF_calculator = [evaluator, wp, vsele_wp, sf_vsjet_tauDM0,
                            sf_vsjet_tauDM1, sf_vsjet_tauDM10, sf_vsjet_tauDM11,
                            sf_dependence, selectedDMs,
                            idAlgorithm](const float &pt, const int &decayMode,
                                         const int &genMatch) {
        Logger::get("TauIDMVAvsJet_tt_SF")->debug("ID - decayMode {}", decayMode);
        // only calculate SFs for allowed tau decay modes (also excludes default
        // values due to tau energy correction shifts below good tau pt
        // selection)
        double sf = 1.;
        if (std::find(selectedDMs.begin(), selectedDMs.end(), decayMode) !=
            selectedDMs.end()) {
            Logger::get("TauIDMVAvsJet_tt_SF")
                ->debug("ID {} - pt {}, decayMode {}, genMatch {}, wp {}, "
                        "sf_vsjet_tauDM0 {}, sf_vsjet_tauDM1 {}, "
                        "sf_vsjet_tauDM10{}, "
                        "sf_vsjet_tauDM11 {}, sf_dependence {}",
                        idAlgorithm, pt, decayMode, genMatch, wp,
                        sf_vsjet_tauDM0, sf_vsjet_tauDM1, sf_vsjet_tauDM10,
                        sf_vsjet_tauDM11, sf_dependence);
            if (decayMode == 0) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tauDM0, sf_dependence});
            } else if (decayMode == 1) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tauDM1, sf_dependence});
            } else if (decayMode == 10) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tauDM10, sf_dependence});
            } else if (decayMode == 11) {
                sf = evaluator->evaluate(
                    {pt, decayMode, static_cast<int>(genMatch), wp,
                     sf_vsjet_tauDM11, sf_dependence});
            } else {
                sf = 1.;
            }
        }
        Logger::get("TauIDMVAvsJet_tt_SF")->debug("Scale Factor {}", sf);
        return sf;
    };
    auto df1 = df.Define(id_output, idSF_calculator, {pt, decayMode, genMatch});
    return df1;
}

} // namespace tau


namespace fatjet {
/**
 * @brief Function used to evaluate particleNet
 * correctionlib
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt fatjet pt
 * @param nBhadrons number of B hadrons in a fatjet
 * @param nChadrons number of C hadrons in a fatjet
 * @param variation name of the variation of the scale factor. Available Values:
 * nominal, down, up
 * @param sf_output name of the scale factor column
 * @param sf_file path to the file with the particleNet Xbb scale factors
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode
pNetXbbSF(ROOT::RDF::RNode df, correctionManager::CorrectionManager &correctionManager,
        const std::string &pt, const std::string &nBhad, const std::string &nChad, 
        const std::string &variation, const std::string &sf_output, const std::string &sf_file) {
    Logger::get("pNetXbbSF")->debug(
        "Setting up functions for particleNet X(bb) sf with correctionlib");

    auto evaluator = correctionManager.loadCorrection(sf_file, "particleNet_Xbb_tagger_SF");

    auto pNetXbbSF_lambda = [evaluator, variation](const float &pt_value, const int &nBhad, const int &nChad) {
        Logger::get("pNetXbbSF")->debug("Variation - Name {}", variation);
        float sf = 1.;

        if (pt_value >= 200.0) {
            if (nBhad>0) {
                sf = evaluator->evaluate({pt_value, "B", variation});
            }
            else if (nBhad==0 && nChad>0) {
                sf = evaluator->evaluate({pt_value, "C", variation});
            }
            else if (nBhad==0 && nChad==0) {
                sf = evaluator->evaluate({pt_value, "L", variation});
            }
            else {
                sf = 1.;
            }
        }

        Logger::get("pNetXbbSF")->debug("Fatjet Scale Factor {} for pt {}, nBhadrons {}, nChadrons {}", sf, pt_value, nBhad, nChad);
        return sf;
    };
    auto df1 = df.Define(sf_output, pNetXbbSF_lambda, {pt, nBhad, nChad});
    return df1;
}


/**
 * @brief Function used to evaluate trigger scale factors of fatjets with
 * correctionlib
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt fatjet pt
 * @param msoftdrop fatjet softdrop mass
 * @param sf_output name of the scale factor column
 * @param sf_file path to the file with the trigger scale factors
 * @param sf_name name of the trigger scale factors
 * @param variation name of the variation of the scale factor. Available Values:
 * nominal, down, up
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode
trigger(ROOT::RDF::RNode df, correctionManager::CorrectionManager &correctionManager,
       const std::string &pt, const std::string &msoftdrop, 
       const std::string &sf_output, const std::string &sf_file, const std::string &sf_name, 
       const std::string &variation) {
    Logger::get("FatjetTriggerSF")->debug(
        "Setting up functions for fatjet trigger sf with correctionlib");

    auto evaluator = correctionManager.loadCorrection(sf_file, sf_name);

    auto FatjetTriggerSF_lambda = [evaluator, variation](const float &pt, const float &msoftdrop) {
        Logger::get("FatjetTriggerSF")->debug("Variation - Name {}", variation);
        float sf = 1.;

        if (pt >= 0.0) {
            sf = evaluator->evaluate({pt, msoftdrop, variation});
        }

        Logger::get("FatjetTriggerSF")->debug("Fatjet Scale Factor {} for pt {} and msoftdrop {}", sf, pt, msoftdrop);
        return sf;
    };
    auto df1 = df.Define(sf_output, FatjetTriggerSF_lambda, {pt, msoftdrop});
    return df1;
}
} // end fatjet

} // end scalefactor

#endif