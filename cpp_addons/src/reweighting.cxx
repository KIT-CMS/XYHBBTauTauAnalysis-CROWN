#ifndef GUARDREWEIGHTINGEXT_H
#define GUARDREWEIGHTINGEXT_H

#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace v12 {

namespace reweighting {

/**
 * @brief Function used to calculate top pt reweighting
 *
 * @param df The input dataframe
 * @param weightname name of the derived weight
 * @param gen_pdgids name of the column containing the PDG-IDs of the generator
 * particles
 * @param gen_status name of the column containing the status flags of the
 * generator particles, where bit 13 contains the isLastCopy flag
 * @param gen_pt name of the column containing the pt of the generator particles
 * @return a new dataframe containing the new column
 */
ROOT::RDF::RNode topptreweighting(ROOT::RDF::RNode df,
                                  const std::string &weightname,
                                  const std::string &gen_pdgids,
                                  const std::string &gen_status,
                                  const std::string &gen_pt) {

    auto ttbarreweightlambda = [](const ROOT::RVec<int> pdgid,
                                  const ROOT::RVec<int> status,
                                  const ROOT::RVec<float> pt) {
        std::vector<float> top_pts;
        for (size_t i = 0; i < pdgid.size(); i++) {
            if (std::abs(pdgid[i]) == 6 && ((status[i] >> 13) & 1) == 1)
                top_pts.push_back(pt[i]);
        }
        if (top_pts.size() != 2) {
            std::cout << top_pts.size();
            Logger::get("topptreweighting")
                ->error("TTbar reweighting applied to event with not exactly "
                        "two top quarks. Probably due to wrong sample type. "
                        "n_top: {}",
                        top_pts.size());
            throw std::runtime_error("Bad number of top quarks.");
        }

        if (top_pts[0] > 500.0)
            top_pts[0] = 500.0;
        if (top_pts[1] > 500.0)
            top_pts[1] = 500.0;
        const float parameter_a = 0.0615;
        const float parameter_b = -0.0005;
        return sqrt(exp(parameter_a + parameter_b * top_pts[0]) *
                    exp(parameter_a + parameter_b * top_pts[1]));
    };
    auto df1 = df.Define(weightname, ttbarreweightlambda,
                         {gen_pdgids, gen_status, gen_pt});
    return df1;
}

} // namespace reweighing


} // namespace v12


#endif