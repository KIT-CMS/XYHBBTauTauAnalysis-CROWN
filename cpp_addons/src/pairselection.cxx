#ifndef GUARDPAIRSELECTIONEXT_H
#define GUARDPAIRSELECTIONEXT_H

#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>

namespace bb_pairselection {

/**
 * @brief Implementation of the bb pair selection algorithm.
 *
 * @param mindeltaR minimum delta R between the jets of the bb pair
 * @param btag_WP_value minimal value of the b tagging score
 * 
 * @return vector with two indices, representing the selected jets
 * of the bb pair
 */
auto BBPairSelectionAlgo(
    const float &mindeltaR,
    const float &btag_WP_value
) {
    Logger::get("bb::PairSelectionAlgo")->debug("Setting up algorithm");
    return [mindeltaR,
            btag_WP_value](const ROOT::RVec<float> &jet_pt,
                           const ROOT::RVec<float> &jet_eta,
                           const ROOT::RVec<float> &jet_phi,
                           const ROOT::RVec<float> &jet_mass,
                           const ROOT::RVec<float> &jet_btag_discr,
                           const ROOT::RVec<int> &good_bjet_collection,
                           const ROOT::RVec<int> &good_jet_collection) {
        // first entry is index of the leading bjet,
        // second entry is the index of the subleading bjet or non b-tagged jet
        // with the highest btag value
        ROOT::RVec<int> selected_pair = {-1, -1};

        if (good_bjet_collection.size() == 1) {
            Logger::get("bb::PairSelectionAlgo")
                ->debug("Running algorithm on one good bjet");

            int highest_non_tag_jet_index = -1;
            float highest_non_tag_value = -1.;
            const auto selected_jet_btag_values =
                ROOT::VecOps::Take(jet_btag_discr, good_jet_collection);

            auto leading_bjet_index = good_bjet_collection[0];
            ROOT::Math::PtEtaPhiMVector leading_bjet =
                ROOT::Math::PtEtaPhiMVector(jet_pt.at(leading_bjet_index),
                                            jet_eta.at(leading_bjet_index),
                                            jet_phi.at(leading_bjet_index),
                                            jet_mass.at(leading_bjet_index));
            Logger::get("bb::PairSelectionAlgo")
                ->debug("{} leading bjet vector: {}", leading_bjet_index,
                        leading_bjet);

            for (auto &index : good_jet_collection) {
                ROOT::Math::PtEtaPhiMVector subleading_candidate =
                    ROOT::Math::PtEtaPhiMVector(
                        jet_pt.at(index), jet_eta.at(index), jet_phi.at(index),
                        jet_mass.at(index));
                Logger::get("bb::PairSelectionAlgo")
                    ->debug("{} subleading non bjet candidate vector: {}",
                            index, subleading_candidate);

                if ((selected_jet_btag_values[index] < btag_WP_value) &&
                    (selected_jet_btag_values[index] > highest_non_tag_value) &&
                    (index != good_bjet_collection[0]) &&
                    (ROOT::Math::VectorUtil::DeltaR(
                         leading_bjet, subleading_candidate) > mindeltaR)) {
                    highest_non_tag_jet_index = index;
                    highest_non_tag_value = selected_jet_btag_values[index];
                }
            }

            selected_pair = {static_cast<int>(leading_bjet_index),
                                static_cast<int>(highest_non_tag_jet_index)};
            Logger::get("bb::PairSelectionAlgo")
                ->debug("Final pair {} {}", selected_pair[0],
                        selected_pair[1]);

            return selected_pair;
           
        } else if (good_bjet_collection.size() >= 2) {
            Logger::get("bb::PairSelectionAlgo")
                ->debug("Running algorithm on at least two good bjets");

            auto leading_bjet_index = good_bjet_collection[0];
            ROOT::Math::PtEtaPhiMVector leading_bjet =
                ROOT::Math::PtEtaPhiMVector(jet_pt.at(leading_bjet_index),
                                            jet_eta.at(leading_bjet_index),
                                            jet_phi.at(leading_bjet_index),
                                            jet_mass.at(leading_bjet_index));
            Logger::get("bb::PairSelectionAlgo")
                ->debug("{} leading bjet vector: {}", leading_bjet_index,
                        leading_bjet);

            for (auto &index : good_bjet_collection) {
                ROOT::Math::PtEtaPhiMVector subleading_candidate =
                    ROOT::Math::PtEtaPhiMVector(
                        jet_pt.at(index), jet_eta.at(index), jet_phi.at(index),
                        jet_mass.at(index));
                Logger::get("bb::PairSelectionAlgo")
                    ->debug("{} subleading bjet candidate vector: {}", index,
                            subleading_candidate);
                if ((index != leading_bjet_index) &&
                    (ROOT::Math::VectorUtil::DeltaR(
                         leading_bjet, subleading_candidate) > mindeltaR)) {
                    selected_pair = {static_cast<int>(leading_bjet_index),
                                     static_cast<int>(index)};
                    Logger::get("bb::PairSelectionAlgo")
                        ->debug("Final pair {} {}", selected_pair[0],
                                selected_pair[1]);
                    break;
                }
            }
            return selected_pair;
        } else {
            return selected_pair;
        }
    };
}
/**
 * @brief Function used to select a pair of b-jets
 *
 * @param df the input dataframe
 * @param input_vector vector of strings containing the columns needed for the
 * alogrithm. For the bb pair selection these values are:
    - jet_pt
    - jet_eta
    - jet_phi
    - jet_mass
    - jet_btag_discr
    - good_bjet_collection containing the list of all good bjets (pt sorted)
    - good_jet_collection containing the list of all good jets (pt sorted)
 * @param pairname name of the new column containing the pair index
 * @param mindeltaR the seperation between a b-tagged jet and a fatjet has to be
 smaller than
 * @param btag_WP_value the working point value for a jet to be b-tagged
 * this value
 * 
 * @return a new dataframe with the pair index column added
 */
ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR,
                               const float &btag_WP_value) {
    Logger::get("bb::PairSelection")->debug("Setting up bb pair building");
    auto df1 = df.Define(
        pairname,
        bb_pairselection::BBPairSelectionAlgo(mindeltaR, btag_WP_value),
        input_vector);
    return df1;
}

} // end bb_pairselection

#endif