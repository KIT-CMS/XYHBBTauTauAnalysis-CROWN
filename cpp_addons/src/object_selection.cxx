namespace xyh {

    namespace object_selection {

        /**
         * @brief Create a selection mask for tight electrons, based on various criteria.
         *
         * @param df The input data frame.
         * @param output_mask The output mask column.
         * @param electron_pt The electrons' tranverse momenta.
         * @param electron_eta The electrons' pseudorapidities.
         * @param electron_iso The electrons' isolation values.
         * @param electron_dxy The electrons' impact parameter values (xy plane).
         * @param electron_dz The electrons' impact parameter values (z direction).
         * @param electron_id The electrons' identification flags.
         * @param min_pt Minimum transverse momentum for the electrons.
         * @param abs_max_eta Maximum absolute pseudorapidity for the electrons.
         * @param max_iso Maximum isolation value for the electrons.
         * @param max_dxy Maximum impact parameter value (xy plane) for the electrons.
         * @param max_dz Maximum impact parameter value (z direction) for the electrons.
         * @param id_wp The working point for the electron identification.
         */
         
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
            const float &max_dz,
            const int &id_wp
        ) {
            auto select = [
                min_pt, abs_max_eta, max_iso, max_dxy, max_dz, id_wp
            ] (
                const ROOT::RVec<float> &pt,
                const ROOT::RVec<float> &eta,
                const ROOT::RVec<float> &iso,
                const ROOT::RVec<float> &dxy,
                const ROOT::RVec<float> &dz,
                const ROOT::RVec<int> &ids
            ) {
                return (
                    (pt > min_pt)
                    && (abs(eta) < abs_max_eta)
                    && (iso < max_iso)
                    && (abs(dxy) < max_dxy)
                    && (abs(dz) < max_dz)
                    && (ids >= id_wp)
                )
            };

            return df.Define(
                outputname,
                select,
                {
                    electron_pt,
                    electron_eta,
                    electron_iso,
                    electron_dxy,
                    electron_dz,
                    electron_ids
                }
            );
        }

        /**
         * @brief Create a selection mask for tight muons, based on various criteria.
         *
         * @param df The input data frame.
         * @param output_mask The output mask column.
         * @param muon_pt The muons' tranverse momenta.
         * @param muon_eta The muons' pseudorapidities.
         * @param muon_iso The muons' isolation values.
         * @param muon_dxy The muons' impact parameter values (xy plane).
         * @param muon_dz The muons' impact parameter values (z direction).
         * @param muon_id The muons' identification flags.
         * @param min_pt Minimum transverse momentum for the muons.
         * @param abs_max_eta Maximum absolute pseudorapidity for the muons.
         * @param max_iso Maximum isolation value for the muons.
         * @param max_dxy Maximum impact parameter value (xy plane) for the muons.
         * @param max_dz Maximum impact parameter value (z direction) for the muons.
         * @param id_wp The working point for the muon identification.
         */
        ROOT::RDF::RNode muon(
            ROOT::RDF::RNode df,
            const std::string &output_mask,
            const std::string &muon_pt,
            const std::string &muon_eta,
            const std::string &muon_iso,
            const std::string &muon_dxy,
            const std::string &muon_dz,
            const std::string &muon_ids,
            const float &min_pt,
            const float &abs_max_eta,
            const float &max_iso,
            const float &max_dxy,
            const float &max_dz,
            const int &id_wp
        ) {
            auto select = [
                min_pt, abs_max_eta, max_iso, max_dxy, max_dz, id_wp
            ] (
                const ROOT::RVec<float> &pt,
                const ROOT::RVec<float> &eta,
                const ROOT::RVec<float> &iso,
                const ROOT::RVec<float> &dxy,
                const ROOT::RVec<float> &dz,
                const ROOT::RVec<bool> &ids
            ) {
                return (
                    (pt > min_pt)
                    && (abs(eta) < abs_max_eta)
                    && (iso < max_iso)
                    && (abs(dxy) < max_dxy)
                    && (abs(dz) < max_dz)
                    && (ids >= id_wp)
                )
            };

            return df.Define(
                outputname,
                select,
                {
                    muon_pt,
                    muon_eta,
                    muon_iso,
                    muon_dxy,
                    muon_dz,
                    muon_ids
                }
            );
        }

        /**
         * @brief Create a selection mask for tight taus, based on various criteria.
         *
         * @param df The input data frame.
         * @param output_mask The output mask column.
         * @param tau_pt The taus' tranverse momenta.
         * @param tau_eta The taus' pseudorapidities.
         * @param tau_decay_mode The taus' decay mode flags.
         * @param tau_dz The taus' impact parameter values (z direction).
         * @param tau_id_vs_electron The tau vs electrons discriminators' flags.
         * @param tau_id_vs_muon The tau vs muons discriminators' flags.
         * @param tau_id_vs_jet The tau vs jets discriminators' flags.
         * @param min_pt Minimum transverse momentum for the muons.
         * @param abs_max_eta Maximum absolute pseudorapidity for the muons.
         * @param decay_modes Tau decay mode flags.
         * @param max_dz Maximum impact parameter value (z direction) for the muons.
         * @param id_vs_electron_wp The working point for the tau vs electrons identification.
         * @param id_vs_muon_wp The working point for the tau vs muons identification.
         * @param id_vs_jet_wp The working point for the tau vs jets identification.
         */
        ROOT::RDF::RNode tau(
            ROOT::RDF::RNode df,
            const std::string &output_mask,
            const std::string &tau_pt,
            const std::string &tau_eta,
            const std::string &tau_decay_mode,
            const std::string &tau_dz,
            const std::string &tau_id_vs_electron,
            const std::string &tau_id_vs_muon,
            const std::string &tau_id_vs_jet,
            const float &min_pt,
            const float &abs_max_eta,
            const std::vector<int> &decay_modes,
            const float &max_dz,
            const int &id_vs_electron_wp,
            const int &id_vs_muon_wp,
            const int &id_vs_jet_wp
        ) {
            auto select = [
                min_pt, abs_max_eta, decay_modes, max_dz, id_vs_electron_wp, id_vs_muon_wp, id_vs_jet_wp
            ] (
                const ROOT::RVec<float> &pt,
                const ROOT::RVec<float> &eta,
                const ROOT::RVec<int> &decay_mode,
                const ROOT::RVec<float> &dz,
                const ROOT::RVec<int> &id_vs_electron,
                const ROOT::RVec<int> &id_vs_muon,
                const ROOT::RVec<int> &id_vs_jet
            ) {
                // construct a decay mode mask
                auto decay_mode_mask = ROOT::VecOps::RVec<bool>(decay_mode.size(), false);
                for (const auto &mode : decay_modes) {
                    decay_mode_mask |= (decay_mode == mode);
                }

                return (
                    (pt > min_pt)
                    && (abs(eta) < abs_max_eta)
                    && decay_mode_mask
                    && (abs(dz) < max_dz)
                    && (id_vs_electron >= id_vs_electron_wp)
                    && (id_vs_muon >= id_vs_muon_wp)
                    && (id_vs_jet >= id_vs_jet_wp)
                )
            };

            return df.Define(
                outputname,
                select,
                {
                    tau_pt,
                    tau_eta,
                    tau_decay_mode,
                    tau_dz,
                    tau_id_vs_electron,
                    tau_id_vs_muon,
                    tau_id_vs_jet
                }
            );
        }

    }

}