#ifndef GUARDFAKEFACTORS_H
#define GUARDFAKEFACTORS_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "ROOT/RDataFrame.hxx"
#include "correction.h"

namespace fakefactors {

ROOT::RDF::RNode
BuildFloatVector(ROOT::RDF::RNode df, const std::string &output,
                 const std::vector<std::string> &input_columns);

namespace util {

std::vector<correction::Variable::Type>
to_clib_input(const std::vector<float> &vector);

void prepend(std::vector<correction::Variable::Type> &vector,
             const correction::Variable::Type &value);

void append(std::vector<correction::Variable::Type> &vector,
            const correction::Variable::Type &value);

const std::vector<correction::Variable::Type>
prepare_ff_input(const std::vector<float> &vector,
                 const std::string &variation);

const std::vector<correction::Variable::Type>
prepare_fractions_input(const std::vector<float> &vector,
                        const std::string &process,
                        const std::string &variation);

std::string join(const std::vector<correction::Variable::Type> &vector);

} // end namespace util

namespace xyh {

ROOT::RDF::RNode RawFakeFactorSemileptonic(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname, const std::string &qcd_inputs,
    const std::string &tt_inputs, const std::string &fraction_inputs,
    const std::string &ff_file, const std::string &ff_qcd_name,
    const std::string &ff_tt_name, const std::string &ff_fraction_name,
    const std::string &ff_qcd_variation, const std::string &ff_tt_variation,
    const std::string &ff_fraction_variation);

ROOT::RDF::RNode FakeFactorSemileptonic(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &outputname, const std::string &qcd_inputs,
    const std::string &tt_inputs, const std::string &fraction_inputs,
    const std::string &qcd_corr_dr_sr_inputs,
    const std::string &qcd_corr_closure_inputs,
    const std::string &tt_corr_closure_inputs, const std::string &ff_file,
    const std::string &ff_qcd_name, const std::string &ff_tt_name,
    const std::string &ff_fraction_name, const std::string &corr_file,
    const std::string &corr_qcd_dr_sr_name,
    const std::string &corr_qcd_closure_name,
    const std::string &corr_tt_closure_name,
    const std::string &ff_qcd_variation, const std::string &ff_tt_variation,
    const std::string &ff_fraction_variation,
    const std::string &qcd_corr_dr_sr_variation,
    const std::string &qcd_corr_closure_variation,
    const std::string &tt_corr_closure_variation);
} // end namespace xyh

ROOT::RDF::RNode raw_fakefactor_nmssm_lt(
    ROOT::RDF::RNode df, const std::string &outputname,
    const std::string &tau_pt, const std::string &njets,
    const std::string &lep_mt, const std::string &nbtags,
    const std::string &qcd_variation, const std::string &wjets_variation,
    const std::string &ttbar_variation, const std::string &fraction_variation,
    const std::string &ff_file);
ROOT::RDF::RNode raw_fakefactor_nmssm_tt(
    ROOT::RDF::RNode df, const std::string &outputname, const int &tau_idx,
    const std::string &tau_pt_1, const std::string &tau_pt_2,
    const std::string &njets, const std::string &m_vis,
    const std::string &nbtag, const std::string &qcd_variation,
    const std::string &ttbar_variation, const std::string &fraction_variation,
    const std::string &ff_file);
ROOT::RDF::RNode fakefactor_nmssm_lt(
    ROOT::RDF::RNode df, const std::string &outputname,
    const std::string &tau_pt, const std::string &njets,
    const std::string &lep_mt, const std::string &nbtags,
    const std::string &lep_pt, const std::string &m_vis,
    const std::string &tau_mass, const std::string &qcd_variation,
    const std::string &wjets_variation, const std::string &ttbar_variation,
    const std::string &fraction_variation,
    const std::string &qcd_corr_leppt_variation,
    const std::string &qcd_corr_taumass_variation,
    const std::string &qcd_corr_drsr_variation,
    const std::string &wjets_corr_leppt_variation,
    const std::string &wjets_corr_taumass_variation,
    const std::string &wjets_corr_drsr_variation,
    const std::string &ttbar_corr_leppt_variation,
    const std::string &ttbar_corr_taumass_variation, const std::string &ff_file,
    const std::string &ff_corr_file);
ROOT::RDF::RNode fakefactor_nmssm_boosted_lt(
    ROOT::RDF::RNode df, const std::string &outputname,
    const std::string &boosted_tau_pt, const std::string &njets,
    const std::string &boosted_lep_mt, const std::string &nbtags,
    const std::string &boosted_lep_pt, const std::string &boosted_m_vis,
    const std::string &boosted_dR_ditau, const std::string &qcd_variation,
    const std::string &wjets_variation, const std::string &ttbar_variation,
    const std::string &fraction_variation,
    const std::string &qcd_corr_leppt_variation,
    const std::string &qcd_corr_lepmt_variation,
    const std::string &qcd_corr_drsr_variation,
    const std::string &wjets_corr_leppt_variation,
    const std::string &wjets_corr_drsr_variation,
    const std::string &ttbar_corr_leppt_variation, const std::string &ff_file,
    const std::string &ff_corr_file);
ROOT::RDF::RNode fakefactor_nmssm_tt(
    ROOT::RDF::RNode df, const std::string &outputname, const int &tau_idx,
    const std::string &tau_pt_1, const std::string &tau_pt_2,
    const std::string &njets, const std::string &m_vis,
    const std::string &nbtag, const std::string &tau_mass_1,
    const std::string &tau_mass_2, const std::string &qcd_variation,
    const std::string &ttbar_variation, const std::string &fraction_variation,
    const std::string &qcd_corr_leppt_variation,
    const std::string &qcd_corr_taumass_variation,
    const std::string &qcd_corr_drsr_variation,
    const std::string &ttbar_corr_leppt_variation,
    const std::string &ttbar_corr_taumass_variation, const std::string &ff_file,
    const std::string &ff_corr_file);
} // namespace fakefactors
#endif /* GUARDFAKEFACTORS_H */
