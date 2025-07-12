#ifndef GUARDOBJECTSELECTION_H
#define GUARDOBJECTSELECTION_H


#include "ROOT/RDataFrame.hxx"
#include <vector>


// namespace xyh
namespace xyh {

// namespace xyh::object_selection
namespace object_selection {

// function xyh::object_selection::electron
ROOT::RDF::RNode electron(
    ROOT::RDF::RNode df,
    const std::string &output_mask,
    const std::string &electron_pt,
    const std::string &electron_eta,
    const std::string &electron_iso,
    const std::string &electron_dxy,
    const std::string &electron_dz,
    const std::string &electron_id,
    const float &min_pt,
    const float &abs_max_eta,
    const float &max_iso,
    const float &max_dxy,
    const float &max_dz
);

// function xyh::object_selection::muon
ROOT::RDF::RNode muon(
    ROOT::RDF::RNode df,
    const std::string &output_mask,
    const std::string &muon_pt,
    const std::string &muon_eta,
    const std::string &muon_iso,
    const std::string &muon_dxy,
    const std::string &muon_dz,
    const std::string &muon_id,
    const float &min_pt,
    const float &abs_max_eta,
    const float &max_iso,
    const float &max_dxy,
    const float &max_dz
);

// function xyh::object_selection::tau
ROOT::RDF::RNode tau(
    ROOT::RDF::RNode df,
    const std::string &output_mask,
    const std::string &tau_pt,
    const std::string &tau_eta,
    const std::string &tau_dz,
    const std::string &tau_decay_mode,
    const std::string &tau_id_vs_jet,
    const std::string &tau_id_vs_electron,
    const std::string &tau_id_vs_muon,
    const float &min_pt,
    const float &abs_max_eta,
    const float &max_dz,
    const std::vector<int> &decay_modes,
    const int &id_vs_jet_wp,
    const int &id_vs_electron_wp,
    const int &id_vs_muon_wp
);

} // end namespace xyh::object_selection

} // end namespace xyh


#endif  // end GUARDOBJECTSELECTION_H