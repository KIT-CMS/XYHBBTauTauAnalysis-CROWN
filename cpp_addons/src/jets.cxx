#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/defaults.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace physicsobject {

namespace jet {

/// Function to apply b jet energy regression. The correction is applied to b jets
/// identified via the discriminant of e.g. the DeepJet tagger from nanoAOD
///
/// \param[in] df the input dataframe
/// \param[out] corrected_bjet_pt the name of the corrected jet pts
/// \param[in] jet_pt name of the input jet pts
/// \param[in] good_bjet_mask name of the mask with information about good b jets
/// \param[in] corr_factor name of the column with the correction factors for the jet pts
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode BJetPtCorrection(ROOT::RDF::RNode df, const std::string &corrected_bjet_pt,
                           const std::string &jet_pt, const std::string &good_bjet_mask,
                           const std::string &corr_factor) {
    return df.Define(corrected_bjet_pt,
                     [](const ROOT::RVec<float> &jet_pt, const ROOT::RVec<int> &good_bjet_mask, 
                        const ROOT::RVec<float> &corr_factor) {
                        ROOT::RVec<float> pt_values_corrected;
                        for (int i = 0; i < jet_pt.size(); i++) {
                            float corr_pt = jet_pt.at(i);
                            if (good_bjet_mask.at(i)) {
                                // applying b jet energy correction
                                corr_pt = jet_pt.at(i) * corr_factor.at(i);
                                
                                Logger::get("BJetEnergyCorrection")
                                    ->debug("applying b jet energy correction: orig. jet "
                                            "pt {} to corrected "
                                            "jet pt {} with correction factor {}",
                                            jet_pt.at(i), corr_pt, corr_factor.at(i));
                            }
                            pt_values_corrected.push_back(corr_pt);
                        }
                        return pt_values_corrected;
                     },
                     {jet_pt, good_bjet_mask, corr_factor});
}

namespace quantities {

/**
 * @brief Patch for wrong Jet ID values in Run3 NanoAOD v12 samples.
 * 
 * The implementation follows the recipe by the [JME POG](https://twiki.cern.ch/twiki/bin/view/CMS/JetID13p6TeV#nanoAOD_Flags).
 * 
 * @param df the input dataframe
 * @param outputname the name of the produced column
 * @param jet_pt name of the column with jet pt values
 * @param jet_eta name of the column with jet eta values
 * @param jet_id name of the column with (broken) jet ID values 
 * @param jet_ne_hef name of the column with neutral hadron energy fraction
 * @param jet_ne_em_ef name of the column with neutral EM energy fraction
 * @param jet_mu_ef name of the column with muon energy fraction
 * @param jet_ch_em_ef name of the column with charged EM energy fraction
 * 
 * @return a dataframe with the new column
 */
ROOT::RDF::RNode CorrectJetIDRun3NanoV12(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_id,
    const std::string &jet_ne_hef,
    const std::string &jet_ne_em_ef,
    const std::string &jet_mu_ef,
    const std::string &jet_ch_em_ef
) {

    // we do not need to ensure the correct casting for NanoAOD v9 samples here as this fix applies to NanoAOD v12 samples only

    auto correction = [] (
        const ROOT::RVec<float> &jet_pt,
        const ROOT::RVec<float> &jet_eta,
        const ROOT::RVec<UChar_t> &jet_id_v12,
        const ROOT::RVec<float> &jet_ne_hef,
        const ROOT::RVec<float> &jet_ne_em_ef,
        const ROOT::RVec<float> &jet_mu_ef,
        const ROOT::RVec<float> &jet_ch_em_ef
    ) {
        // cast jet_id to integer
        auto jet_id = static_cast<ROOT::RVec<int>>(jet_id_v12);

        // apply the JME POG recipe
        auto jet_id_corrected = ROOT::RVec<int>(jet_id.size(), 0);
        for (int i = 0; i < jet_pt.size(); ++i) {
            // evaluate if the jet passes the tight WP
            bool pass_tight = false;
            if (abs(jet_eta.at(i)) <= 2.7) {
                pass_tight = jet_id.at(i) & (1 << 1);
            } else if (abs(jet_eta.at(i)) > 2.7 && abs(jet_eta.at(i)) <= 3.0) {
                pass_tight = (jet_id.at(i) & (1 << 1)) && (jet_ne_hef.at(i) < 0.99);
            } else if (abs(jet_eta.at(i)) > 3.0) {
                pass_tight = (jet_id.at(i) & (1 << 1)) && (jet_ne_em_ef.at(i) < 0.4);
            }

            // evaluate if the jet passes the tight WP and fulfills the lepton veto
            bool pass_tight_lep_veto = false;
            if (abs(jet_eta.at(i)) <= 2.7) {
                pass_tight_lep_veto = pass_tight && (jet_mu_ef.at(i) < 0.8) && (jet_ch_em_ef.at(i) < 0.8);
            } else {
                pass_tight_lep_veto = pass_tight;
            }

            // return value of the working point that is passed
            // - 0 == fail
            // - 2 == pass tight & fail tightLepVeto
            // - 6 == pass tight & pass tightLepVeto
            if (pass_tight && !pass_tight_lep_veto) {
                jet_id_corrected[i] = 2;
            } else if (pass_tight && pass_tight_lep_veto) {
                jet_id_corrected[i] = 6;
            } else {
                jet_id_corrected[i] = 0;
            }
        }

        // convert the data type to default in NanoAOD v12 (UChar_t)
        auto jet_id_corrected_v12 = static_cast<ROOT::RVec<UChar_t>>(jet_id_corrected);

        return jet_id_corrected_v12;
    };

    // redefine the data type of the Jet ID mask
    return df.Define(
        outputname,
        correction,
        {
            jet_pt,
            jet_eta,
            jet_id,
            jet_ne_hef,
            jet_ne_em_ef,
            jet_mu_ef,
            jet_ch_em_ef
        }
    );
}

} // end quantities

} // end jet

} // end physicsobject

namespace quantities {

namespace jet {

/** @brief Function to writeout the value of the resolution of a b-jet. The resolution was estimated as a part of a DNN based energy regresion task.
 *
 * @param df the input dataframe
 * @param outputname the name of the produced quantity
 * @param resolution_column name of the column that contains resolution values of
 * the jets
 * @param jetcollection name of the vector that contains jet indices of the
 * jets belonging to the collection, its length constitutes the output quantity
 * @param position The position in the jet collection vector, which is used to
 * store the index of the particle in the particle quantity vectors.
 *
 * @return a dataframe with the new column
 */
ROOT::RDF::RNode
bRegRes(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &resolution_column,
    const std::string &jetcollection,
    const int &position
) {
    return df.Define(outputname,
                     [position](const ROOT::RVec<float> &resolution,
                                const ROOT::RVec<int> &jetcollection) {
                         float reso = default_float;
                         if (position >= 0) {
                             const int index = jetcollection.at(position);
                             if (index >= 0) {
                                reso = resolution.at(index);
                             }
                         }
                         return reso;
                     },
                     {resolution_column, jetcollection});
}

} // end jet

} // end quantities


#endif