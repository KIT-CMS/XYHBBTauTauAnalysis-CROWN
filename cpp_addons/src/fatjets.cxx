#ifndef GUARDFATJETSEXT_H
#define GUARDFATJETSEXT_H

#include "../include/basefunctions.hxx"
#include "../include/defaults.hxx"
#include "../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TRandom3.h"
#include "correction.h"
#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <cmath>
#include <typeinfo>


namespace fatjet {


namespace matching {


ROOT::RDF::RNode match_object(
    ROOT::RDF::RNode df,
    const std::string &output,
    const std::string &fatjet_eta,
    const std::string &fatjet_phi,
    const std::string &fatjet_index,
    const std::string &other_eta,
    const std::string &other_phi,
    const std::string &other_index,
    const float &max_delta_r
) {
    auto match = [max_delta_r] (
        const ROOT::RVec<float> &fatjet_etas,
        const ROOT::RVec<float> &fatjet_phis,
        const ROOT::RVec<float> &fatjet_indices,
        const ROOT::RVec<float> &other_etas,
        const ROOT::RVec<float> &other_phis,
        const ROOT::RVec<float> &other_indices,
        const ROOT::RVec<float> &
    ) {
        ROOT::RVec<ROOT::RVec<int>> other_indices_matched(fatjet_indices.size());
        for (const auto &fatjet_index : fatjet_indices) {
            ROOT::RVec<int> other_indices_matched_single(0);
            ROOT::RVec<int> delta_rs(0);
            for (const auto &other_index : other_indices) {
                auto delta_r = ROOT::VecOps::DeltaR(
                    fatjet_etas.at(fatjet_index),
                    fatjet_phis.at(fatjet_index),
                    other_etas.at(other_index),
                    other_phis.at(other_index)
                );
                if (delta_r < delta_r_max) {
                    other_indices_matched_single.push_back(other_index);
                    delta_rs.push_back(delta_r);
                }
                // sort with delta_r
                auto index = ROOT::VecOps::Argsort(delta_rs);
                auto other_indices_matched_single_sorted = ROOT::VecOps::Take(
                    other_indices_matched_single, index
                );
                other_indices_matched.push_back(other_indices_matched_single_sorted);
            }
        }
        return other_indices_matched;
    };

    return df.Define(
        output,
        match,
        {fatjet_eta, fatjet_phi, fatjet_index, other_eta, other_phi, other_index}
    )
}


ROOT::RDF::RNode count_matches(
    ROOT::RDF::RNode df,
    const std::string &output,
    const std::string &other_matches_index
) {
    auto match = (
        const ROOT::RVec<float> &other_matches_index,
    ) {
        ROOT::RVec<int> counts(0);
        for (int fatjet_index = 0; fatjet_index < other_matches_index.size(); ++fatjet_index) {
            counts.push_back(other_matches_index.at(fatjet_index).size());
        }
        return counts;
    };

    return df.Define(
        output,
        match,
        {other_matches_index}
    )
}

}

}


namespace fatjet {
/// Function to find a fatjet which matches to the leading b-jet from a b-jet
/// pair. The match is done with a deltaR criterium.
///
/// \param[in] df the input dataframe
/// \param[out] output_name the name of the selected fatjet (index)
/// \param[in] good_fatjet_collection name of the collection with the indices of
/// good fatjets \param[in] fatjet_pt name of the fatjet pts \param[in]
/// fatjet_eta name of the fatjet etas \param[in] fatjet_phi name of the fatjet
/// phis \param[in] fatjet_mass name of the fatjet masses \param[in] bpair_p4_1
/// four vector of the leading b-jet from the selected b-jet pair \param[in]
/// deltaRmax maximum required distance in dR between b-jet and a fatjet
/// candidate
///
/// \return a dataframe containing the new mask
auto FindFatjetMatchingBjet(ROOT::RDF::RNode df, const std::string &output_name,
                            const std::string &good_fatjet_collection,
                            const std::string &fatjet_pt,
                            const std::string &fatjet_eta,
                            const std::string &fatjet_phi,
                            const std::string &fatjet_mass,
                            const std::string &bpair_p4_1,
                            const float &deltaRmax) {
    Logger::get("fatjet::FatjetMatchingToBjet")->debug("Setting up algorithm");
    auto df1 = df.Define(
        output_name,
        [deltaRmax](const ROOT::RVec<int> &good_fatjet_collection,
                    const ROOT::RVec<float> &fatjet_pt,
                    const ROOT::RVec<float> &fatjet_eta,
                    const ROOT::RVec<float> &fatjet_phi,
                    const ROOT::RVec<float> &fatjet_mass,
                    const ROOT::Math::PtEtaPhiMVector &bpair_p4_1) {
            ROOT::RVec<int> selected_fatjet = {-1};
            if ((good_fatjet_collection.size() > 0) && (bpair_p4_1.pt() > 0)) {
                Logger::get("fatjet::FatjetMatchingToBjet")
                    ->debug("Running algorithm on at least one good fatjet");
                for (auto &index : good_fatjet_collection) {
                    ROOT::Math::PtEtaPhiMVector fatjet_candidate =
                        ROOT::Math::PtEtaPhiMVector(
                            fatjet_pt.at(index), fatjet_eta.at(index),
                            fatjet_phi.at(index), fatjet_mass.at(index));
                    Logger::get("fatjet::FatjetMatchingToBjet")
                        ->debug("{} fatjet candidate vector: {}", index,
                                fatjet_candidate);
                    if ((ROOT::Math::VectorUtil::DeltaR(
                             bpair_p4_1, fatjet_candidate) < deltaRmax)) {
                        selected_fatjet = {static_cast<int>(index)};
                        Logger::get("fatjet::FatjetMatchingToBjet")
                            ->debug("Final fatjet {}", selected_fatjet[0]);
                        break;
                    }
                }
            }
            return selected_fatjet;
        },
        {good_fatjet_collection, fatjet_pt, fatjet_eta, fatjet_phi, fatjet_mass,
         bpair_p4_1});
    return df1;
}
/// Function to find a fatjet with the highest particleNet X(bb) vs QCD score 
///
/// \param[in] df the input dataframe
/// \param[out] output_name the name of the selected fatjet (index)
/// \param[in] good_fatjet_collection name of the collection with the indices of
/// good fatjets \param[in] fatjet_pNet_Xbb name of the variable with the Xbb particleNet scores 
/// \param[in] fatjet_pNet_QCD name of the variable with the QCD particleNet scores 
///
/// \return a dataframe containing the new mask
auto FindXbbFatjet(ROOT::RDF::RNode df, const std::string &output_name,
                            const std::string &good_fatjet_collection,
                            const std::string &fatjet_pNet_Xbb, const std::string &fatjet_pNet_QCD) {
    Logger::get("fatjet::FindXbbFatjet")->debug("Setting up algorithm");
    auto df1 = df.Define(
        output_name,
        [](const ROOT::RVec<int> &good_fatjet_collection,
           const ROOT::RVec<float> &Xbb_tagger, const ROOT::RVec<float> &QCD_tagger) {
            ROOT::RVec<int> selected_fatjet = {-1};
            float highest_pNet_value = default_float;
            if ((good_fatjet_collection.size() > 0)) {
                Logger::get("fatjet::FindXbbFatjet")
                    ->debug("Running algorithm on at least one good fatjet");
                float Xbb = default_float;
                float QCD = default_float;
                float Xbb_vs_QCD = default_float;
                for (auto &index : good_fatjet_collection) {
                    Xbb = Xbb_tagger.at(index);
                    QCD = QCD_tagger.at(index);
                    Xbb_vs_QCD = Xbb / (Xbb + QCD);
                    if (Xbb_vs_QCD > highest_pNet_value) {
                        highest_pNet_value = Xbb_vs_QCD;
                        selected_fatjet = {static_cast<int>(index)};
                    }
                }
                Logger::get("fatjet::FindXbbFatjet")
                            ->debug("Final fatjet {}", selected_fatjet[0]);
            }
            return selected_fatjet;
        },
        {good_fatjet_collection, fatjet_pNet_Xbb, fatjet_pNet_QCD});
    return df1;
}
} // end namespace fatjet

namespace quantities {
namespace fatjet {
/// Function to writeout the value of the softdrop mass for a fatjet.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] m_softdrop name of the column that contains the softdrop mass of
/// the fatjets
/// \param[in] fatjetcollection name of the vector that contains fatjet indices
/// of the fatjets belonging to the collection, its length constitutes the
/// output quantity \param position The position in the fatjet collection
/// vector, which is used to store the index of the particle in the particle
/// quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode msoftdrop(ROOT::RDF::RNode df, const std::string &outputname,
                           const std::string &m_softdrop,
                           const std::string &fatjetcollection,
                           const int &position) {
    return df.Define(outputname,
                    [position](const ROOT::RVec<float> &softdrop_masses,
                                const ROOT::RVec<int> &fatjetcollection) {
                        float mass = default_float;
                        if (position >= 0) {
                           const int index = fatjetcollection.at(position);
                           if (index >= 0) {
                               mass = softdrop_masses.at(index);
                           }
                        }
                        return mass;
                    },
                    {m_softdrop, fatjetcollection});
}


ROOT::RDF::RNode mass_particlenet(
    ROOT::RDF::RNode df, const std::string &outputname,
    const std::string &mass,
    const std::string &masscorr_pnet,
    const std::string &fatjetcollection
) {
    return df.Define(outputname,
                    [] (const ROOT::RVec<float> &masses,
                        const ROOT::RVec<float> &masscorr_pnet,
                        const ROOT::RVec<int> &fatjetcollection) {
                        auto masses_selected = ROOT::VecOps::Take(masses, fatjetcollection);
                        auto masscorr_selected = ROOT::VecOps::Take(masscorr_pnet, fatjetcollection);
                        return masses_selected * masscorr_selected;
                    },
                    {mass, masscorr_pnet, fatjetcollection});
}


ROOT::RDF::RNode mass_particlenet(
    ROOT::RDF::RNode df, const std::string &outputname,
    const std::string &mass,
    const std::string &masscorr_pnet,
    const std::string &fatjetcollection,
    const int &position) {
    return df.Define(outputname,
                    [position](const ROOT::RVec<float> &masses,
                               const ROOT::RVec<float> &masscorr_pnet,
                               const ROOT::RVec<int> &fatjetcollection) {
                        float mass = default_float;
                        float corr = 1.0;
                        if (position >= 0) {
                           const int index = fatjetcollection.at(position);
                           if (index >= 0) {
                               mass = masses.at(index);
                               corr = masscorr_pnet.at(index);
                           }
                        }
                        return corr * mass;
                    },
                    {mass, masscorr_pnet, fatjetcollection});
}



/// Function to writeout the value of the particleNet Xbb vs QCD tagger for a
/// fatjet.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] pNet_Xbb name of the column that contains the particleNet raw
/// value for X->bb of the fatjets \param[in] pNet_QCD name of the column that
/// contains the particleNet raw value for QCD of the fatjets \param[in]
/// fatjetcollection name of the vector that contains fatjet indices of the
/// fatjets belonging to the collection, its length constitutes the output
/// quantity \param position The position in the fatjet collection vector, which
/// is used to store the index of the particle in the particle quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode
particleNet_XbbvsQCD(ROOT::RDF::RNode df, const std::string &outputname,
                     const std::string &pNet_Xbb, const std::string &pNet_QCD,
                     const std::string &fatjetcollection, const int &position) {
    return df.Define(outputname,
                     [position](const ROOT::RVec<float> &Xbb_tagger,
                                const ROOT::RVec<float> &QCD_tagger,
                                const ROOT::RVec<int> &fatjetcollection) {
                        float Xbb = default_float;
                        float QCD = default_float;
                        float Xbb_vs_QCD = default_float;
                        if (position >= 0) {
                            const int index = fatjetcollection.at(position);
                            if (index >= 0) {
                                Xbb = Xbb_tagger.at(index);
                                QCD = QCD_tagger.at(index);
                                Xbb_vs_QCD = Xbb / (Xbb + QCD);
                            }
                        }
                        return Xbb_vs_QCD;
                     },
                     {pNet_Xbb, pNet_QCD, fatjetcollection});
}
/// Function to writeout the N- over N-1-prong n-subjettiness ratio for a
/// fatjet. This variable is should discriminate between fatjets with N subjets
/// and fatjets with N-1 subjets. Lower values mean the fatjet is more N-prong
/// like, higher values more N-1-prong like.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] tauN name of the column that contains the n-subjettiness for
/// N-prong of the fatjets \param[in] tauNm1 name of the column that contains
/// the n-subjettiness for N-1-prong of the fatjets \param[in] fatjetcollection
/// name of the vector that contains fatjet indices of the fatjets belonging to
/// the collection, its length constitutes the output quantity \param position
/// The position in the fatjet collection vector, which is used to store the
/// index of the particle in the particle quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode
nsubjettiness_ratio(ROOT::RDF::RNode df, const std::string &outputname,
                    const std::string &tauN, const std::string &tauNm1,
                    const std::string &fatjetcollection, const int &position) {
    return df.Define(outputname,
                    [position](const ROOT::RVec<float> &nsubjettiness_N,
                               const ROOT::RVec<float> &nsubjettiness_Nm1,
                               const ROOT::RVec<int> &fatjetcollection) {
                        float nsubjet_N = default_float;
                        float nsubjet_Nm1 = default_float;
                        float ratio = default_float;
                        if (position >= 0) { 
                            const int index = fatjetcollection.at(position);
                            if (index >= 0) {
                                nsubjet_N = nsubjettiness_N.at(index);
                                nsubjet_Nm1 = nsubjettiness_Nm1.at(index);
                                ratio = nsubjet_N / nsubjet_Nm1;
                            }
                        }
                        return ratio;
                    },
                    {tauN, tauNm1, fatjetcollection});
}
/// Function to writeout the value of the hadron flavor for a fatjet.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] fatjet_hadflavor name of the column that contains the hadron flavor of
/// the fatjets
/// \param[in] fatjetcollection name of the vector that contains fatjet indices
/// of the fatjets belonging to the collection, its length constitutes the
/// output quantity \param position The position in the fatjet collection
/// vector, which is used to store the index of the particle in the particle
/// quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode hadflavor(ROOT::RDF::RNode df, const std::string &outputname,
                           const std::string &fatjet_hadflavor,
                           const std::string &fatjetcollection,
                           const int &position) {
    return df.Define(outputname,
                    [position](const ROOT::RVec<int> &fatjet_hadflavor,
                               const ROOT::RVec<int> &fatjetcollection) {
                        int flavor = default_int;
                        if (position >= 0) { 
                            const int index = fatjetcollection.at(position);
                            if (index >= 0) {
                                flavor = fatjet_hadflavor.at(index);
                            }
                        }
                        return flavor;
                    },
                    {fatjet_hadflavor, fatjetcollection});
}

/// Function to writeout  the number of hadrons for a fatjet.
///
/// \param[in] df the input dataframe
/// \param[out] outputname the name of the produced quantity
/// \param[in] fatjet_nHadrons name of the column that contains the number of 
/// hadrons of the fatjets
/// \param[in] fatjetcollection name of the vector that contains fatjet indices
/// of the fatjets belonging to the collection, its length constitutes the
/// output quantity \param position The position in the fatjet collection
/// vector, which is used to store the index of the particle in the particle
/// quantity vectors.
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode nHadrons(ROOT::RDF::RNode df, const std::string &outputname,
                           const std::string &fatjet_nHadrons,
                           const std::string &fatjetcollection,
                           const int &position) {
    return df.Define(outputname,
                     [position](const ROOT::RVec<UChar_t> &fatjet_nHadrons,
                                const ROOT::RVec<int> &fatjetcollection) {
                        int nHad = default_int;
                        if (position >= 0) { 
                            const int index = fatjetcollection.at(position);
                            if (index >= 0) {
                                nHad = static_cast<int>(fatjet_nHadrons.at(index));
                            }
                        }
                        return nHad;
                    },
                    {fatjet_nHadrons, fatjetcollection});
}
} // end namespace fatjet
} // end namespace quantities
#endif /* GUARDFATJETS_H */