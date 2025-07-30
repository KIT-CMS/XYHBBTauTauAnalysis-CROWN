#ifndef GUARDVETOES_HXX
#define GUARDVETOES_HXX

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


// namespace xyh
namespace xyh {

// namespace vetoes 
namespace vetoes {

/**
 * @brief Create flag for a dilepton veto.
 * 
 * This inline function is intended to be used in `ROOT::RDataFrame::Define` statements.
 * 
 * The vector `object_index` contains the indices of selected leptons.
 * The columns `eta`, `phi`, `charge` contain the values of the lepton observables for each lepton in the event.
 * The parameter `min_delta_r` is the minimum eta-phi separation of two leptons.
 * 
 * @param eta The lepton pseudorapidity.
 * @param phi The lepton azimuthal angle.
 * @param charge The lepton charge.
 * @param min_delta_r The minimum spatial distance between leptons to be considered for the veto.
 * @param logger_function_name name of the logger to be used.
 */
inline auto dilepton_veto(
    const ROOT::RVec<int> &object_index,
    const ROOT::RVec<float> &eta,
    const ROOT::RVec<float> &phi,
    const ROOT::RVec<int> &charge,
    const float &min_delta_r,
    const std::string &logger_function_name
) {
    // immediately return false if only one lepton has been found
    if (object_index.size() < 2) {
        return false;
    }

    // build combinations of leptons 
    auto combinations = ROOT::VecOps::Combinations(object_index, 2);

    // check if one of the combinations fulfills the dilepton veto requirements
    bool has_dilepton = false;
    for (int i = 0; i < combinations[0].size(); ++i) {
        // get the indices of the two leptons in the combination
        auto left = combinations[0][i];
        auto right = combinations[1][i];

        // check whether they have opposite charge and if they have a large enough separation
        auto delta_r = ROOT::VecOps::DeltaR(eta[left], eta[right], phi[left], phi[right]);
        auto is_os_and_resolved = (
            (charge[left] * charge[right] < 0)
            && (delta_r > min_delta_r)
        );

        // break if a valid combination of electrons has been found
        if (is_os_and_resolved) {
            Logger::get(logger_function_name)->debug("    Found combination ({}, {}) with opposite charge and deltaR = {} that passes criteria", left, right, delta_r);
            has_dilepton = true;
            break;
        }
    }

    return has_dilepton;
}

// function xyh::vetoes::dielectron
ROOT::RDF::RNode dielectron(
    ROOT::RDF::RNode df,
    const std::string &output_mask,
    const std::string &electron_pt,
    const std::string &electron_eta,
    const std::string &electron_phi,
    const std::string &electron_iso,
    const std::string &electron_dxy,
    const std::string &electron_dz,
    const std::string &electron_id,
    const std::string &electron_charge,
    const float &min_pt,
    const float &abs_max_eta,
    const float &max_iso,
    const float &max_dxy,
    const float &max_dz,
    const int &id_wp,
    const float &min_delta_r
);

// function xyh::vetoes::dimuon
ROOT::RDF::RNode dimuon(
    ROOT::RDF::RNode df,
    const std::string &output_mask,
    const std::string &muon_pt,
    const std::string &muon_eta,
    const std::string &muon_phi,
    const std::string &muon_iso,
    const std::string &muon_dxy,
    const std::string &muon_dz,
    const std::string &muon_is_pf_cand,
    const std::string &muon_is_tracker,
    const std::string &muon_is_global,
    const std::string &muon_charge,
    const float &min_pt,
    const float &abs_max_eta,
    const float &max_iso,
    const float &max_dxy,
    const float &max_dz,
    const float &min_delta_r
);

// function xyh::vetoes::jet_vetomap
ROOT::RDF::RNode jet_vetomap(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &output_mask,
    const std::string &jet_pt,
    const std::string &jet_id,
    const std::string &jet_ch_em_ef,
    const std::string &jet_n_em_ef,
    const std::string &muon_eta,
    const std::string &muon_phi,
    const std::string &muon_is_pfcand,
    const std::string &jet_vetomap_file,
    const std::string &jet_vetomap_name,
    const std::string &jet_vetomap_type,
    const float &min_pt,
    const int &id_wp,
    const float &max_em_frac,
    const float &min_delta_r_jet_muon
);

} // end namespace vetoes 

} // end namespace xyh


#endif  // end GUARDVETOES_HXX