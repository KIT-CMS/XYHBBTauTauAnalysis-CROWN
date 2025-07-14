#ifndef GUARDPAIRSELECTIONEXT_H
#define GUARDPAIRSELECTIONEXT_H

#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/utility/utility.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>


namespace ditau_pairselection {

/**
 * @brief Function to find the index of an additional hadronic tau besides the hadronic tau from 
 * the selected tau pair. This function is constructed for the semileptonic channels.
 *
 * @param df the Dataframe
 * @param outputname the column containing the name of the output column
 * @param tau_mask the column containing the mask of good taus
 * @param pairname the column containing the selected tau pair indices
 * 
 * @return the new Dataframe with the additional tau index column
 */
ROOT::RDF::RNode findAdditionalTau(ROOT::RDF::RNode df, const std::string &tau_mask, 
                                const std::string &pairname, const std::string &outputname) {
    return df.Define(
        outputname,
        [](const ROOT::RVec<int> &mask, const ROOT::RVec<int> &pair) {
            const int selected_index = pair.at(1);
            ROOT::RVec<int> selected_additional_tau = {-1};
            const auto original_tau_indices = ROOT::VecOps::Nonzero(mask);
            Logger::get("findAdditionalTau")
                ->debug("tau mask {}", original_tau_indices);
            Logger::get("findAdditionalTau")
                ->debug("Selected pair {}", pair);
            if (original_tau_indices.size() == 0 || selected_index < 0) {
                Logger::get("findAdditionalTau")
                    ->debug("no add. tau {}", selected_additional_tau);
                return selected_additional_tau;
            }
            for (auto &idx : original_tau_indices) {
                if (selected_index != idx) {
                    selected_additional_tau = {static_cast<int>(idx)};
                    break;
                }
            }
            Logger::get("findAdditionalTau")
                ->debug("add. tau {}", selected_additional_tau);
            return selected_additional_tau;
        },
        {tau_mask, pairname});
}

}


namespace boosted_ditau_pairselection {

/**
 * @brief Function used to sort two particles based on the
 * pt of the two particles.
 * 
 * The function is used as the ordering function for the
 * [ROOT::VecOps::Sort()](https://root.cern.ch/doc/master/group__vecops.html#ga882439c2ff958157d2990b52dd76f599)
 * algorithm. If two quantities are the same within a given epsilon of
 * 1e-5, the next criterion is applied. The sorting is done using the
 * following criterion odering:
 * -# Isolation of the first particle
 * -# pt of the first particle
 * -# Isolation of the second particle
 * -# pt of the second particle
 *
 * @param lep1pt `ROOT::RVec<float>` containing pts of the first
 * particle
 * @param lep2pt `ROOT::RVec<float>` containing pts
 * of the second particle
 *
 * @return true or false based on the particle ordering.
 */
auto compareForPairs(const ROOT::RVec<float> &lep1pt, const ROOT::RVec<float> &lep2pt) {
    return [lep1pt, lep2pt](auto value_next, auto value_previous) {
        Logger::get("PairSelectionCompare")->debug("lep1 Pt: {}", lep1pt);
        Logger::get("PairSelectionCompare")->debug("lep2 Pt: {}", lep2pt);
        bool result = false;
        Logger::get("PairSelectionCompare")
            ->debug("Next pair: {}, {}", std::to_string(value_next.first),
                    std::to_string(value_next.second));
        Logger::get("PairSelectionCompare")
            ->debug("Previous pair: {}, {}",
                    std::to_string(value_previous.first),
                    std::to_string(value_previous.second));
        const auto i1_next = value_next.first;
        const auto i1_previous = value_previous.first;
        const auto i2_next = value_next.second;
        const auto i2_previous = value_previous.second;
        Logger::get("PairSelectionCompare")
            ->debug("i1_next: {}, i1_previous : {}", i1_next, i1_previous);
        // start with lep1 isolation
        const auto pt1_next = lep1pt.at(i1_next);
        const auto pt1_previous = lep1pt.at(i1_previous);

        if (not utility::ApproxEqual(pt1_next, pt1_previous)) {
            result = pt1_next > pt1_previous;
        } else {
            // if too similar, compare lep2 pt
            Logger::get("PairSelectionCompare")
                ->debug("pt lep 1 too similar, taking pt 2");
            const auto pt2_next = lep2pt.at(i2_next);
            const auto pt2_previous = lep2pt.at(i2_previous);
            result = pt2_next > pt2_previous;
        }
        Logger::get("PairSelectionCompare")
            ->debug("Returning result {}", result);
        return result;
    };
}

namespace semileptonic {

/// Implementation of the pair selection algorithm. First, only events
/// that contain at least one goodlepton and one goodboostedTau are considered.
/// Events contain at least one good lepton and one good boostedtau, if the
/// boostedtau_mask and the mounmask both have nonzero elements. These masks are
/// constructed using the functions from the physicsobject namespace
/// (e.g. physicsobject::CutMin<float>).
///
/// \returns an `ROOT::RVec<int>` with two values, the first one beeing
/// the lepton index and the second one beeing the tau index.
auto PairSelectionAlgo(const float &mindeltaR, const float &maxdeltaR) {
    Logger::get("semileptonic::PairSelectionAlgo")
        ->debug("Setting up algorithm");
    return [mindeltaR, maxdeltaR](const ROOT::RVec<float> &tau_pt,
                       const ROOT::RVec<float> &tau_eta,
                       const ROOT::RVec<float> &tau_phi,
                       const ROOT::RVec<float> &tau_mass,
                       const ROOT::RVec<float> &lepton_pt,
                       const ROOT::RVec<float> &lepton_eta,
                       const ROOT::RVec<float> &lepton_phi,
                       const ROOT::RVec<float> &lepton_mass,
                       const ROOT::RVec<int> &lepton_mask,
                       const ROOT::RVec<int> &boostedtau_mask) {
        // first entry is the lepton index,
        // second entry is the tau index
        ROOT::RVec<int> selected_pair = {-1, -1};
        const auto original_tau_indices = ROOT::VecOps::Nonzero(boostedtau_mask);
        const auto original_lepton_indices = ROOT::VecOps::Nonzero(lepton_mask);

        if (original_tau_indices.size() == 0 or
            original_lepton_indices.size() == 0) {
            return selected_pair;
        }
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Running algorithm on good taus and leptons");

        const auto selected_tau_pt =
            ROOT::VecOps::Take(tau_pt, original_tau_indices);
        const auto selected_lepton_pt =
            ROOT::VecOps::Take(lepton_pt, original_lepton_indices);

        const auto pair_indices = ROOT::VecOps::Combinations(
            selected_lepton_pt,
            selected_tau_pt); // Gives indices of mu-tau pair
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Pairs: {} {}", pair_indices[0], pair_indices[1]);

        const auto pairs = ROOT::VecOps::Construct<std::pair<UInt_t, UInt_t>>(
            pair_indices[0], pair_indices[1]);
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Pairs size: {}", pairs.size());
        int counter = 0;
        for (auto &pair : pairs) {
            counter++;
            Logger::get("semileptonic::PairSelectionAlgo")
                ->debug("Constituents pair {}. : {} {}", counter, pair.first,
                        pair.second);
        }

        const auto sorted_pairs = ROOT::VecOps::Sort(
            pairs,
            boosted_ditau_pairselection::compareForPairs(selected_lepton_pt,
                            selected_tau_pt));

        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Original TauPt: {}", tau_pt);
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Original leptonPt: {}", lepton_pt);

        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Selected TauPt: {}", selected_tau_pt);
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Selected leptonPt: {}", selected_lepton_pt);

        // construct the four vectors of the selected leptons and taus to check
        // deltaR and reject a pair if the candidates are too close

        for (auto &candidate : sorted_pairs) {
            auto leptonindex = original_lepton_indices[candidate.first];
            ROOT::Math::PtEtaPhiMVector lepton = ROOT::Math::PtEtaPhiMVector(
                lepton_pt.at(leptonindex), lepton_eta.at(leptonindex),
                lepton_phi.at(leptonindex), lepton_mass.at(leptonindex));
            Logger::get("semileptonic::PairSelectionAlgo")
                ->debug("{} lepton vector: {}", leptonindex, lepton);
            auto tauindex = original_tau_indices[candidate.second];
            ROOT::Math::PtEtaPhiMVector tau = ROOT::Math::PtEtaPhiMVector(
                tau_pt.at(tauindex), tau_eta.at(tauindex), tau_phi.at(tauindex),
                tau_mass.at(tauindex));
            Logger::get("semileptonic::PairSelectionAlgo")
                ->debug("{} tau vector: {}", tauindex, tau);
            Logger::get("semileptonic::PairSelectionAlgo")
                ->debug("DeltaR: {}",
                        ROOT::Math::VectorUtil::DeltaR(lepton, tau));
            if ((ROOT::Math::VectorUtil::DeltaR(lepton, tau) > mindeltaR) && (ROOT::Math::VectorUtil::DeltaR(lepton, tau) < maxdeltaR)) {
                Logger::get("semileptonic::PairSelectionAlgo")
                    ->debug(
                        "Selected original pair indices: mu = {} , tau = {}",
                        leptonindex, tauindex);
                Logger::get("semileptonic::PairSelectionAlgo")
                    ->debug("leptonPt = {} , TauPt = {} ", lepton.Pt(),
                            tau.Pt());
                Logger::get("semileptonic::PairSelectionAlgo")
                    ->debug("leptonPt = {} , TauPt = {} ",
                            lepton_pt[leptonindex], tau_pt[tauindex]);
                selected_pair = {static_cast<int>(leptonindex),
                                 static_cast<int>(tauindex)};
                break;
            }
        }
        Logger::get("semileptonic::PairSelectionAlgo")
            ->debug("Final pair {} {}", selected_pair[0], selected_pair[1]);

        return selected_pair;
    };
}
} // end semileptonic

namespace fullhadronic {

/// Implementation of the ditau pair selection algorithm for the fullhadronic
/// channel. First, only events that contain two goodboostedTaus are considered. Events
/// contain at two good boostedtau, if the boostedtau_mask has at least two nonzero elements.
/// These mask is contructed constructed using the functions from the
/// physicsobject namespace (e.g. physicsobject::CutMin<float>).
///
/// \returns an `ROOT::RVec<int>` with two values, the first one beeing
/// the leading tau index and the second one beeing trailing tau index.
auto PairSelectionAlgo(const float &mindeltaR, const float &maxdeltaR) {
    Logger::get("fullhadronic::PairSelectionAlgo")
        ->debug("Setting up algorithm");
    return [mindeltaR, maxdeltaR](const ROOT::RVec<float> &tau_pt,
                       const ROOT::RVec<float> &tau_eta,
                       const ROOT::RVec<float> &tau_phi,
                       const ROOT::RVec<float> &tau_mass,
                       const ROOT::RVec<int> &boostedtau_mask) {
        // first entry is the leading tau index,
        // second entry is the trailing tau index
        ROOT::RVec<int> selected_pair = {-1, -1};
        const auto original_tau_indices = ROOT::VecOps::Nonzero(boostedtau_mask);

        if (original_tau_indices.size() < 2) {
            return selected_pair;
        }
        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Running algorithm on good taus");

        const auto selected_tau_pt =
            ROOT::VecOps::Take(tau_pt, original_tau_indices);

        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Original TauPt: {}", tau_pt);

        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Selected TauPt: {}", selected_tau_pt);

        const auto pair_indices = ROOT::VecOps::Combinations(
            selected_tau_pt, 2); // Gives indices of tau-tau pairs
        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Pairs: {} {}", pair_indices[0], pair_indices[1]);

        const auto pairs = ROOT::VecOps::Construct<std::pair<UInt_t, UInt_t>>(
            pair_indices[0], pair_indices[1]);
        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Pairs size: {}", pairs.size());
        int counter = 0;
        for (auto &pair : pairs) {
            counter++;
            Logger::get("fullhadronic::PairSelectionAlgo")
                ->debug("Constituents pair {}. : {} {}", counter, pair.first,
                        pair.second);
        }

        const auto sorted_pairs = ROOT::VecOps::Sort(
            pairs, boosted_ditau_pairselection::compareForPairs(selected_tau_pt,
                                   selected_tau_pt));

        // construct the four vectors of the selected taus to check
        // deltaR and reject a pair if the candidates are too close
        bool found = false;
        for (auto &candidate : sorted_pairs) {
            auto tau_index_1 = original_tau_indices[candidate.first];
            ROOT::Math::PtEtaPhiMVector tau_1 = ROOT::Math::PtEtaPhiMVector(
                tau_pt.at(tau_index_1), tau_eta.at(tau_index_1),
                tau_phi.at(tau_index_1), tau_mass.at(tau_index_1));
            Logger::get("fullhadronic::PairSelectionAlgo")
                ->debug("{} leadint tau vector: {}", tau_index_1, tau_1);
            auto tau_index_2 = original_tau_indices[candidate.second];
            ROOT::Math::PtEtaPhiMVector tau_2 = ROOT::Math::PtEtaPhiMVector(
                tau_pt.at(tau_index_2), tau_eta.at(tau_index_2),
                tau_phi.at(tau_index_2), tau_mass.at(tau_index_2));
            Logger::get("fullhadronic::PairSelectionAlgo")
                ->debug("{} tau vector: {}", tau_index_2, tau_2);
            Logger::get("fullhadronic::PairSelectionAlgo")
                ->debug("DeltaR: {}",
                        ROOT::Math::VectorUtil::DeltaR(tau_1, tau_2));
            if ((ROOT::Math::VectorUtil::DeltaR(tau_1, tau_2) > mindeltaR) && (ROOT::Math::VectorUtil::DeltaR(tau_1, tau_2) < maxdeltaR)) {
                Logger::get("fullhadronic::PairSelectionAlgo")
                    ->debug("Selected original pair indices: tau_1 = {} , "
                            "tau_2 = {}",
                            tau_index_1, tau_index_2);
                Logger::get("fullhadronic::PairSelectionAlgo")
                    ->debug("Tau_1 Pt = {} , Tau_2 Pt = {} ", tau_1.Pt(),
                            tau_2.Pt());
                selected_pair = {static_cast<int>(tau_index_1),
                                 static_cast<int>(tau_index_2)};
                found = true;
                break;
            }
        }
        // sort it that the leading tau in pt is first
        if (found) {
            if (tau_pt.at(selected_pair[0]) < tau_pt.at(selected_pair[1])) {
                std::swap(selected_pair[0], selected_pair[1]);
            }
        }
        Logger::get("fullhadronic::PairSelectionAlgo")
            ->debug("Final pair {} {}", selected_pair[0], selected_pair[1]);

        return selected_pair;
    };
}

} // end fullhadronic

namespace mutau {

/**
 * @brief Function used to select the pair of boosted tau leptons based on the standard
 * pair selection algorithm
 *
 * @param df the input dataframe
 * @param input_vector vector of strings containing the columns needed for the
 * alogrithm. For the muTau pair selection these values are:
    - boostedtau_pt
    - boostedtau_eta
    - boostedtau_phi
    - boostedtau_mass
    - muon_pt
    - muon_eta
    - muon_phi
    - muon_mass
    - boostedtau_mask containing the flags whether the tau is a good tau or not
    - muon_mask containing the flags whether the muon is a good muon or not
 * @param pairname name of the new column containing the pair index
 * @param mindeltaR the seperation between the muon at the tau has to be larger
 * than this value
 * @param maxdeltaR the seperation between the muon at the tau has to be smaller
 * than this value
 * @return a new dataframe with the pair index column added
 */
ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR) {
    Logger::get("mutau::PairSelection")
        ->debug("Setting up boosted MuTau pair building");
    auto df1 = df.Define(
        pairname,
        boosted_ditau_pairselection::semileptonic::PairSelectionAlgo(mindeltaR, maxdeltaR),
        input_vector);
    return df1;
}
} // end mutau

namespace eltau {

/**
 * @brief Function used to select the pair of boosted tau leptons based on the standard
 * pair selection algorithm
 *
 * @param df the input dataframe
 * @param input_vector vector of strings containing the columns needed for the
 * alogrithm. For the ElTau pair selection these values are:
    - boostedtau_pt
    - boostedtau_eta
    - boostedtau_phi
    - boostedtau_mass
    - electron_pt
    - electron_eta
    - electron_phi
    - electron_mass
    - boostedtau_mask containing the flags whether the tau is a good tau or not
    - electron_mask containing the flags whether the electron is a good electron
 or not
 * @param pairname name of the new column containing the pair index
 * @param mindeltaR the seperation between the electron at the tau has to be larger than
 * this value
 * @param maxdeltaR the seperation between the electron at the tau has to be smaller
 * than this value
 * @return a new dataframe with the pair index column added
 */
ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR) {
    Logger::get("eltau::PairSelection")
        ->debug("Setting up boosted ElTau pair building");
    auto df1 = df.Define(
        pairname,
        boosted_ditau_pairselection::semileptonic::PairSelectionAlgo(mindeltaR, maxdeltaR),
        input_vector);
    return df1;
}
} // end eltau

namespace tautau {

/**
 * @brief Function used to select the pair of boosted tau leptons based on the standard
 * pair selection algorithm
 *
 * @param df the input dataframe
 * @param input_vector vector of strings containing the columns needed for the
 * alogrithm. For the TauTau pair selection these values are:
    - boostedtau_pt
    - boostedtau_eta
    - boostedtau_phi
    - boostedtau_mass
    - boostedtau_mask containing the flags whether the tau is a good tau or not
 * @param pairname name of the new column containing the pair index
 * @param mindeltaR the seperation between the two tau candidates has to be
 larger than
 * this value
 * @return a new dataframe with the pair index column added
 */
ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR) {
    Logger::get("tautau::PairSelection")
        ->debug("Setting up boosted TauTau pair building");
    auto df1 = df.Define(
        pairname,
        boosted_ditau_pairselection::fullhadronic::PairSelectionAlgo(mindeltaR, maxdeltaR),
        input_vector);
    return df1;
}

} // end tautau

} // end boosted_ditau_pairselection



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