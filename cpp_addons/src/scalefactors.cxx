#ifndef GUARD_SCALEFACTORSEXT_H
#define GUARD_SCALEFACTORSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"


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
                         const std::string &eta, const std::string &year_id,
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
                  [evaluator, year_id, variation,
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
                              {year_id, std::abs(eta), pt, variation});
                      }
                      return sf;
                  },
                  {pt, eta});
    return df1;
}

/**
 * @brief Function used to evaluate id scale factors from muons with
 * correctionlib. Configuration:
 * - [UL2018 Muon
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2018_UL.html)
 * - [UL2017 Muon
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2017_UL.html)
 * - [UL2016preVFP Muon
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2016preVFP_UL.html)
 * - [UL2016postVFP Muon
 * ID](https://cms-nanoaod-integration.web.cern.ch/commonJSONSFs/MUO_muon_Z_Run2_UL/MUO_muon_Z_2016postVFP_UL.html)
 *
 * @param df The input dataframe
 * @param correctionManager The CorrectionManager object
 * @param pt muon pt
 * @param eta muon eta
 * @param year_id id for the year of data taking and mc compaign
 * @param variation id for the variation of the scale factor "sf" for nominal
 * and "systup"/"systdown" for up/down variation
 * @param id_output name of the id scale factor column
 * @param sf_file path to the file with the muon scale factors
 * @param idAlgorithm name of the muon id scale factor
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode id(ROOT::RDF::RNode df,
                    correctionManager::CorrectionManager &correctionManager,
                    const std::string &pt, const std::string &eta,
                    const std::string &year_id, const std::string &variation,
                    const std::string &id_output, const std::string &sf_file,
                    const std::string &idAlgorithm) {

    Logger::get("muonIdSF")->debug("Setting up functions for muon id sf");
    Logger::get("muonIdSF")->debug("ID - Name {}", idAlgorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, idAlgorithm);
    auto df1 = df.Define(
        id_output,
        [evaluator, year_id, variation](const float &pt, const float &eta) {
            Logger::get("muonIdSF")->debug("ID - pt {}, eta {}", pt, eta);
            double sf = 1.;
            // preventing muons with default values due to tau energy correction
            // shifts below good tau pt selection
            if (pt >= 0.0 && std::abs(eta) >= 0.0) {
                sf = evaluator->evaluate(
                    {year_id, std::abs(eta), pt, variation});
            }
            return sf;
        },
        {pt, eta});
    return df1;
}

/**
 * @brief Function used to evaluate iso scale factors from muons with
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
 * @param iso_output name of the iso scale factor column
 * @param sf_file path to the file with the muon scale factors
 * @param idAlgorithm name of the muon iso scale factor
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode iso(ROOT::RDF::RNode df,
                     correctionManager::CorrectionManager &correctionManager,
                     const std::string &pt, const std::string &eta,
                     const std::string &year_id, const std::string &variation,
                     const std::string &iso_output, const std::string &sf_file,
                     const std::string &idAlgorithm) {

    Logger::get("muonIsoSF")->debug("Setting up functions for muon iso sf");
    Logger::get("muonIsoSF")->debug("ISO - Name {}", idAlgorithm);
    auto evaluator = correctionManager.loadCorrection(sf_file, idAlgorithm);
    auto df1 = df.Define(
        iso_output,
        [evaluator, year_id, variation](const float &pt, const float &eta) {
            Logger::get("muonIsoSF")->debug("ISO - pt {}, eta {}", pt, eta);
            double sf = 1.;
            // preventing muons with default values due to tau energy correction
            // shifts below good tau pt selection
            if (pt >= 0.0 && std::abs(eta) >= 0.0) {
                sf = evaluator->evaluate(
                    {year_id, std::abs(eta), pt, variation});
            }
            return sf;
        },
        {pt, eta});
    return df1;
}

} // end muon


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