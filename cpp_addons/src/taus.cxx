#ifndef GUARD_TAUSEXT_CXX
#define GUARD_TAUSEXT_CXX

#include "../include/utility/CorrectionManager.hxx"
#include "../include/utility/Logger.hxx"
#include "../include/utility/utility.hxx"
#include "../include/defaults.hxx"
#include "ROOT/RDataFrame.hxx"
#include "correction.h"
#include <stdexcept>
#include <unordered_map>



namespace physicsobject {


namespace tau {


namespace scalefactor {

/**
 * @brief This function calculates scale factors (SFs) for tau identification (ID) 
 * against jets (`vsJet`). The scale factors are loaded from a correctionlib file 
 * using a specified scale factor name and variation.
 *
 * @note It is advisable to use the `sf_dependence` mode `"dm"` for Run 3 analyses. This is also
 * recommended by the TAU POG.  For each decay mode, the scale factor is parametereized as a
 * separate function of the tau \f$p_T\f$. The `sf_dependence` mode `"pt"` should be used with care.
 * The use of this set of scale factors has not been tested thoroughly in this framework.
 * 
 * The parameter `variation` can take strings consistent with the following expressions:
 * 
 * - `nom`: The nominal scale factor.
 * - `stat$i_dm$DM_$updown`: Statistical uncertainties on fit parameters, uncorrelated across DMs
 *    and eras.
 * - `syst_allears_$updown`: Systematic uncertainty component correlated across all DMs and eras.
 * - `syst_$era_$updown`: Systematic uncertainty component correlated across DMs and uncorrelated
 *    across eras.
 * - `syst_TES_$era_dm$DM_$updown`: Systematic uncertainty due to uncertainty in TES, uncorrelated
 *    across eras and decay modes.
 * 
 * For the `$` expressions, substitute, `$i = 1, 2`, `$DM = 0, 1, 10, 11`,
 * `$era = 2022_preEE, 2022_postEE, 2023_preBPix, 2023_postBPix`, `$updown = up, down`.
 * 
 * @param df input dataframe
 * @param correction_manager correction manager responsible for loading the
 * tau scale factor file
 * @param outputname name of the output column containing the vsJets ID scale factor
 * @param pt name of the column containing the transverse momentum of a tau
 * @param decay_mode name of the column containing the decay mode of the tau
 * @param gen_match name of the column with the matching information of the
 * hadronic tau to generator-level particles (matches are: 1=prompt e, 2=prompt mu,
 * 3=tau->e, 4=tau->mu, 5=had. tau, 0=unmatched)
 * @param sf_file path to the file with the tau scale factors
 * @param sf_name name of the tau scale factor for the vsJet ID correction
 * @param wp working point of the vsJet ID
 * @param vsele_wp working point of the vsEle ID
 * @param sf_dependence variable dependence of the scale factor, opions are "pt" or "dm"
 * @param variation name of the scale factor variation. The different possibilities to use  for this
 * this parameter are listed above.
 *
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode Id_vsJet(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correction_manager,
    const std::string &outputname, 
    const std::string &pt, const std::string &decay_mode,
    const std::string &gen_match, 
    const std::string &sf_file, const std::string &sf_name,
    const std::string &wp, const std::string &vsele_wp,
    const std::string &sf_dependence,
    const std::string &variation
) {
    Logger::get("physicsobject::tau::scalefactor::Id_vsJet")
        ->debug("Setting up function for tau ID vsJet scale factor");
    Logger::get("physicsobject::tau::scalefactor::Id_vsJet")->debug("ID - Name {}", sf_name);
    auto evaluator = correction_manager.loadCorrection(sf_file, sf_name);

    auto sf_calculator = [
        evaluator,
        wp,
        vsele_wp,
        variation,
        sf_dependence,
        sf_name
    ](
        const float &pt,
        const int &decay_mode,
        const int &gen_match
    ) {
        Logger::get("physicsobject::tau::scalefactor::Id_vsJet")
            ->debug("Evaluate tau ID vsJet scale factor for algorithm {}", sf_name);

        // set default value of scale factor of 1 in the case that the correction is not provided
        double sf = 1.;

        // only calculate SFs for allowed tau decay modes (also excludes default
        // values due to tau energy correction shifts below good tau pt
        // selection)
        const std::unordered_set<int> valid_modes = {0, 1, 10, 11};
        if (valid_modes.count(decay_mode)) {
            Logger::get("physicsobject::tau::scalefactor::Id_vsJet")
                ->debug(
                    "    pt {}, decay mode {}, gen_match {}, wp {}, vsele_wp {}, variation {}, "
                    "sf_dependence {}",
                    pt,
                    decay_mode,
                    gen_match,
                    wp,
                    vsele_wp,
                    variation,
                    sf_dependence
                );
        } else {
            Logger::get("physicsobject::tau::scalefactor::Id_vsJet")
                ->debug(
                    "    Skip scale factor evaluation (invalid decay mode {})", decay_mode
                );
        }

        Logger::get("physicsobject::tau::scalefactor::Id_vsJet")
            ->debug("    Scale factor {}", sf);
 
        return sf;
    };

    return df.Define(outputname, sf_calculator, {pt, decay_mode, gen_match});
}

}

}

}

#endif