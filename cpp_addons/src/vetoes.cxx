#ifndef GUARDVETOES_CXX
#define GUARDVETOES_CXX


#include "../../../../include/utility/Logger.hxx"
#include "../include/vetoes.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <vector>


// namespace xyh
namespace xyh {

    // namespace vetoes 
    namespace vetoes {

        /**
         * @brief Create a veto flag mask for a di-electron system in the event.
         * 
         * The selection criteria for considered electrons include kinematic, impact parameter, isolation, and identification requirements.
         * An event is vetoed if at least one pair of selected electrons has a larger eta-phi separation than `min_delta_r` and if the electrons have opposite charge.
         * For events that are vetoed, a value of `true` is stored in the new column, otherwise `false`.
         * The electron identification value is a integer indicating the loosest working point that the electron passes (works with cut-based ID).
         *
         * @param df The input data frame.
         * @param output_mask The output mask column.
         * @param electron_pt The tranverse momentum column.
         * @param electron_eta The pseudorapidity column.
         * @param electron_phi The azimuthal angle column.
         * @param electron_iso The relative isolation column.
         * @param electron_dxy The impact parameter (xy plane) column.
         * @param electron_dz The impact parameter (z direction) column.
         * @param electron_id The identification column. The column should contain interger values indicating the loosest working point that the electron passes.
         * @param electron_charge The charge column.
         * @param min_pt The minimum transverse momentum for selected electrons.
         * @param abs_max_eta Maximum absolute pseudorapidity for selected electrons.
         * @param max_iso Maximum isolation value for selected electrons.
         * @param max_dxy Maximum impact parameter value (xy plane) for selected electrons.
         * @param max_dz Maximum impact parameter value (z direction) for selected electrons.
         * @param id_wp The working point for the electron identification.
         * @param min_delta_r The minimum eta-phi separation of two electrons.
         * @return A new data frame with the veto column.
         */
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
        ) {
            auto select = [
                min_pt, abs_max_eta, max_iso, max_dxy, max_dz, id_wp, min_delta_r, electron_id
            ] (
                const ROOT::RVec<float> &pt,
                const ROOT::RVec<float> &eta,
                const ROOT::RVec<float> &phi,
                const ROOT::RVec<float> &iso,
                const ROOT::RVec<float> &dxy,
                const ROOT::RVec<float> &dz,
                const ROOT::RVec<bool> &id,
                const ROOT::RVec<int> &charge
            ) {
                // debug output for selection criteria and electron observables
                Logger::get("xyh::vetoes::dielectron")->debug("Create selection masks for electrons");
                Logger::get("xyh::vetoes::dielectron")->debug("    min_pt {}, abs_max_eta {}, max_iso {}, max_dxy {}, max_dz {}, id_wp {}, min_delta_r {}", min_pt, abs_max_eta, max_iso, max_dxy, max_dz, id_wp, min_delta_r);
                Logger::get("xyh::vetoes::dielectron")->debug("    electron_id {}", electron_id);
                Logger::get("xyh::vetoes::dielectron")->debug("    pt {}", pt);
                Logger::get("xyh::vetoes::dielectron")->debug("    eta {}", eta);
                Logger::get("xyh::vetoes::dielectron")->debug("    phi {}", phi);
                Logger::get("xyh::vetoes::dielectron")->debug("    iso {}", iso);
                Logger::get("xyh::vetoes::dielectron")->debug("    dxy {}", dxy);
                Logger::get("xyh::vetoes::dielectron")->debug("    dz {}", dz);
                Logger::get("xyh::vetoes::dielectron")->debug("    id {}", id);
                Logger::get("xyh::vetoes::dielectron")->debug("    charge {}", charge);

                // create the index list of selected electron candidates
                auto object_index = ROOT::VecOps::Nonzero(
                    (pt > min_pt)
                    && (abs(eta) < abs_max_eta)
                    && (iso < max_iso)
                    && (abs(dxy) < max_dxy)
                    && (abs(dz) < max_dz)
                    && (id >= id_wp)
                );

                // evaluate conditions for di-electron veto
                auto has_dielectron = xyh::vetoes::dilepton_veto(object_index, eta, phi, charge, min_delta_r, "xyh::vetoes::dielectron");

                // debug output for the final selection mask
                Logger::get("xyh::object_selection::electron")->debug("    veto value is {}", has_dielectron);

                return has_dielectron;
            };

            return df.Define(
                output_mask,
                select,
                {
                    electron_pt,
                    electron_eta,
                    electron_phi,
                    electron_iso,
                    electron_dxy,
                    electron_dz,
                    electron_id,
                    electron_charge
                }
            );
        }

        /**
         * @brief Create a veto flag mask for a di-muon system in the event.
         * 
         * The selection criteria for considered muons include kinematic, impact parameter, isolation, and identification requirements.
         * An event is vetoed if at least one pair of selected muons has a larger eta-phi separation than `min_delta_r` and if the muons have opposite charge.
         * For events that are vetoed, a value of `true` is stored in the new column, otherwise `false`.
         * For the muon identification, the flags for particle-flow candidate, global, and tracker identification are combined.
         *
         * @param df The input data frame.
         * @param output_mask The output mask column.
         * @param muon_pt The tranverse momentum column.
         * @param muon_eta The pseudorapidity column.
         * @param muon_phi The azimuthal angle column.
         * @param muon_iso The relative isolation column.
         * @param muon_dxy The impact parameter (xy plane) column.
         * @param muon_dz The impact parameter (z direction) column.
         * @param muon_is_pf_cand Column with flag whether the muon is a particle-flow candidate.
         * @param muon_is_tracker Column with flag whether the muon is tracker.
         * @param muon_is_global Column with flag whether the muon is global.
         * @param muon_charge The charge column.
         * @param min_pt The minimum transverse momentum for selected muons.
         * @param abs_max_eta Maximum absolute pseudorapidity for selected muons.
         * @param max_iso Maximum isolation value for selected muons.
         * @param max_dxy Maximum impact parameter value (xy plane) for selected muons.
         * @param max_dz Maximum impact parameter value (z direction) for selected muons.
         * @param min_delta_r The minimum eta-phi separation of two muons.
         * @return A new data frame with the veto column.
         */
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
        ) {
            auto select = [
                min_pt, abs_max_eta, max_iso, max_dxy, max_dz, min_delta_r, muon_is_pf_cand, muon_is_tracker, muon_is_global
            ] (
                const ROOT::RVec<float> &pt,
                const ROOT::RVec<float> &eta,
                const ROOT::RVec<float> &phi,
                const ROOT::RVec<float> &iso,
                const ROOT::RVec<float> &dxy,
                const ROOT::RVec<float> &dz,
                const ROOT::RVec<bool> &is_pf_cand,
                const ROOT::RVec<bool> &is_tracker,
                const ROOT::RVec<bool> &is_global,
                const ROOT::RVec<int> &charge
            ) {
                // debug output for selection criteria and electron observables
                Logger::get("xyh::vetoes::dimuon")->debug("Create selection masks for muons");
                Logger::get("xyh::vetoes::dimuon")->debug("    min_pt {}, abs_max_eta {}, max_iso {}, max_dxy {}, max_dz {}, min_delta_r {}", min_pt, abs_max_eta, max_iso, max_dxy, max_dz, min_delta_r);
                Logger::get("xyh::vetoes::dimuon")->debug("    muon_id {} && {} && {}", muon_is_pf_cand, muon_is_tracker, muon_is_global);
                Logger::get("xyh::vetoes::dimuon")->debug("    pt {}", pt);
                Logger::get("xyh::vetoes::dimuon")->debug("    eta {}", eta);
                Logger::get("xyh::vetoes::dimuon")->debug("    phi {}", phi);
                Logger::get("xyh::vetoes::dimuon")->debug("    iso {}", iso);
                Logger::get("xyh::vetoes::dimuon")->debug("    dxy {}", dxy);
                Logger::get("xyh::vetoes::dimuon")->debug("    dz {}", dz);
                Logger::get("xyh::vetoes::dimuon")->debug("    is_pf_cand {}", is_pf_cand);
                Logger::get("xyh::vetoes::dimuon")->debug("    is_tracker {}", is_tracker);
                Logger::get("xyh::vetoes::dimuon")->debug("    is_global {}", is_global);
                Logger::get("xyh::vetoes::dimuon")->debug("    charge {}", charge);

                // create the index list of selected muon candidates
                auto object_index = ROOT::VecOps::Nonzero(
                    (pt > min_pt)
                    && (abs(eta) < abs_max_eta)
                    && (iso < max_iso)
                    && (abs(dxy) < max_dxy)
                    && (abs(dz) < max_dz)
                    && (is_pf_cand && is_tracker && is_global)
                );

                // evaluate conditions for di-muon veto
                auto has_dimuon = xyh::vetoes::dilepton_veto(object_index, eta, phi, charge, min_delta_r, "xyh::vetoes::dimuon");

                // debug output for the final selection mask
                Logger::get("xyh::object_selection::dimuon")->debug("    veto value is {}", has_dimuon);

                return has_dimuon;
            };

            return df.Define(
                output_mask,
                select,
                {
                    muon_pt,
                    muon_eta,
                    muon_phi,
                    muon_iso,
                    muon_dxy,
                    muon_dz,
                    muon_is_pf_cand,
                    muon_is_tracker,
                    muon_is_global,
                    muon_charge
                }
            );
        }

    } // end namespace vetoes 

} // end namespace xyh


#endif  // end GUARDVETOES_CXX