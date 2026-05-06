#include "../include/met.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <Math/Vector3D.h>
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>
#include <cmath>

namespace met {

ROOT::RDF::RNode
Type1Correction(ROOT::RDF::RNode df, const std::string &outputname,
                const std::string raw_met,
                const std::string &t1jet_pt_l1corrected,
                const std::string &t1jet_pt_corrected,
                const std::string &t1jet_eta, const std::string &t1jet_phi,
                const std::string &t1jet_em_ef, const float &t1jet_min_pt,
                const float &t1jet_max_abs_eta, const float &t1jet_max_em_ef) {

    auto type1_corr_func = [t1jet_min_pt, t1jet_max_abs_eta, t1jet_max_em_ef](
                               const ROOT::Math::PtEtaPhiMVector &raw_met,
                               const ROOT::RVec<float> &t1jet_pt_l1corrected,
                               const ROOT::RVec<float> &t1jet_pt_corrected,
                               const ROOT::RVec<float> &t1jet_eta,
                               const ROOT::RVec<float> &t1jet_phi,
                               const ROOT::RVec<float> &t1jet_em_ef) {
        // Select jets for the type-I correction
        auto mask = (t1jet_pt_corrected >= 15.0 && abs(t1jet_eta) <= 5.2 &&
                     t1jet_em_ef <= 0.9);

        // Calculate the difference vector between the fully corrected and the
        // L1-corrected transverse momentum vectors with all selected jets
        auto t1jet_p3_corrected =
            ROOT::VecOps::Construct<ROOT::Math::RhoEtaPhiVector>(
                t1jet_pt_corrected[mask], t1jet_eta[mask], t1jet_phi[mask]);
        auto t1jet_p3_l1corrected =
            ROOT::VecOps::Construct<ROOT::Math::RhoEtaPhiVector>(
                t1jet_pt_l1corrected[mask], t1jet_eta[mask], t1jet_phi[mask]);
        auto pt_vec_diff =
            ROOT::VecOps::Sum(t1jet_p3_corrected - t1jet_p3_l1corrected,
                              ROOT::Math::RhoEtaPhiVector(0.0, 0.0, 0.0));

        // Calculate the corrected MET vector
        auto met_corrected_3d =
            ROOT::Math::RhoEtaPhiVector(raw_met.Pt(), 0.0, raw_met.Phi()) +
            pt_vec_diff;

        return ROOT::Math::PtEtaPhiMVector(met_corrected_3d.Rho(), 0.0,
                                           met_corrected_3d.Phi(),
                                           met_corrected_3d.Rho());
    };

    return df.Define(outputname, type1_corr_func,
                     {raw_met, t1jet_pt_l1corrected, t1jet_pt_corrected,
                      t1jet_eta, t1jet_phi, t1jet_em_ef});
}

} // namespace met