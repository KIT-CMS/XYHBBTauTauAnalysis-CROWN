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
                         try {
                             const int index = jetcollection.at(position);
                             reso = resolution.at(index);
                         } catch (const std::out_of_range &e) {
                         }
                         return reso;
                     },
                     {resolution_column, jetcollection});
}

} // end jet

} // end quantities

#endif