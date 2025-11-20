#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/defaults.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace physicsobject {

namespace jet {

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
            // - 2 == pass tight & fail tightlepveto
            // - 6 == pass tight & pass tightlepveto
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


ROOT::RDF::RNode JetPtPNetRegression(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt_uncorrected,
    const std::string &jet_raw_factor,
    const std::string &jet_pnet_reg_pt_factor,
    const std::string &jet_collection_index
) {
    auto correction = [] (
        const ROOT::RVec<float> &jet_pt_uncorrected,
        const ROOT::RVec<float> &jet_raw_factor,
        const ROOT::RVec<float> &jet_pnet_reg_pt_factor,
        const ROOT::RVec<int> &jet_collection_index
    ) {
        // Jet_rawFactor is 1 - (raw pt)/(corrected pt) (from NANOAOD documentation)
        // Calculate raw pt before JEC
        auto jet_pt_raw = ROOT::VecOps::Take(
            jet_pt_uncorrected * (1 - jet_raw_factor),
            jet_collection_index
        );
        auto jet_pt_pnet = jet_pt_raw * ROOT::VecOps::Take(
            jet_pnet_reg_pt_factor,
            jet_collection_index
        );

        return jet_pt_pnet;
    };

    return df.Define(
        outputname,
        correction,
        {
            jet_pt_uncorrected,
            jet_raw_factor,
            jet_pnet_reg_pt_factor,
            jet_collection_index
        },
    );
}


ROOT::RDF::RNode JetPtPNetRegressionWithNeutrino(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt_uncorrected,
    const std::string &jet_raw_factor,
    const std::string &jet_pnet_reg_pt_factor,
    const std::string &jet_pnet_reg_pt_neutrino_factor,
    const std::string &jet_collection_index
) {
    auto correction = [] (
        const ROOT::RVec<float> &jet_pt_uncorrected,
        const ROOT::RVec<float> &jet_raw_factor,
        const ROOT::RVec<float> &jet_pnet_reg_pt_factor,
        const ROOT::RVec<float> &jet_pnet_reg_pt_neutrino_factor,
        const ROOT::RVec<int> &jet_collection_index
    ) {
        // Jet_rawFactor is 1 - (raw pt)/(corrected pt) (from NANOAOD documentation)
        // Calculate raw pt before JEC
        auto jet_pt_raw = ROOT::VecOps::Take(
            jet_pt_uncorrected * (1 - jet_raw_factor),
            jet_collection_index
        );
        auto jet_pt_pnet_neutrino = jet_pt_raw * ROOT::VecOps::Take(
            jet_pnet_reg_pt_factor * jet_pnet_reg_pt_neutrino_factor,
            jet_collection_index
        );

        return jet_pt_pnet_neutrino;
    };

    return df.Define(
        outputname,
        correction,
        {
            jet_pt_uncorrected,
            jet_raw_factor,
            jet_pnet_reg_pt_factor,
            jet_pnet_reg_pt_neutrino_factor,
            jet_collection_index
        },
    );
}


ROOT::RDF::RNode JetPtPNetRegressionResolution(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt_uncorrected,
    const std::string &jet_raw_factor,
    const std::string &jet_pnet_reg_pt_resolution_factor,
    const std::string &jet_collection_index
) {

    auto resolution = [] (
        const ROOT::RVec<float> &jet_pt_uncorrected,
        const ROOT::RVec<float> &jet_raw_factor,
        const ROOT::RVec<float> &jet_pnet_reg_pt_resolution_factor,
        const ROOT::RVec<int> &jet_collection_index
    ) {
        // Jet_rawFactor is 1 - (raw pt)/(corrected pt) (from NANOAOD documentation)
        // Calculate raw pt before JEC
        auto jet_pt_raw = ROOT::VecOps::Take(
            jet_pt_uncorrected * (1 - jet_raw_factor),
            jet_collection_index
        );
        auto jet_pt_pnet_res = jet_pt_raw * ROOT::VecOps::Take(
            jet_pnet_reg_pt_resolution_factor,
            jet_collection_index
        );

        return jet_pt_pnet_res;
    };

    // redefine the data type of the Jet ID mask
    return df.Define(
        outputname,
        resolution,
        {
            jet_pt_uncorrected,
            jet_raw_factor,
            jet_pnet_reg_pt_resolution_factor,
            jet_collection_index
        }
    );
}


} // end quantities


} // end jet

} // end physicsobject


#endif