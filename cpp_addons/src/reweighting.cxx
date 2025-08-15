#ifndef GUARDREWEIGHTINGEXT_CXX
#define GUARDREWEIGHTINGEXT_CXX

#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/utility/utility.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <Math/Vector4D.h>
#include <Math/VectorUtil.h>


namespace event {


    namespace reweighting {
        
        
        /**
         * @brief Function used to evaluate the lheScaleweight of an event from NMSSM signal samples. The weights
        are stored in the nanoAOD file an defined as w_var/w_nominal. Depending on the
        selected muR and muF value, a specific index has to be returned. The mapping
        between the index and the muR and muF values is:
        
        muF        | MuR   | index
        ------------|-------|-------
         0.5        | 0.5   | 0
         1.0        | 0.5   | 1
         2.0        | 0.5   | 2
         0.5        | 1.0   | 3
         2.0        | 1.0   | 4
         0.5        | 2.0   | 5
         1.0        | 2.0   | 6
         2.0        | 2.0   | 7
        
        In the NMSSM sample is now state for muF=1, muR=1 saved, which is different to other nanoAOD samples. 
        
         *
         * @param df The input dataframe
         * @param weightname the output name of the generated weight
         * @param lhe_scale_weights name of the column containing the lhe scale weights
         * @param muR the value of muR, possible values are 0.5, 1.0, 2.0
         * @param muF the value of muF, possible values are 0.5, 1.0, 2.0
         * @return ROOT::RDF::RNode
         */
        
        ROOT::RDF::RNode NMSSMLHEScaleWeights(ROOT::RDF::RNode df,
                                           const std::string &weightname,
                                           const std::string &lhe_scale_weights,
                                           const float muR, const float muF) {
            // find the index we have to use, first check if the muR and muF values are
            // valid, only 0.5, 1.0, 2.0 are allowed
            std::vector<float> allowed_values = {0.5, 1.0, 2.0};
            if (std::find(allowed_values.begin(), allowed_values.end(), muR) ==
                allowed_values.end()) {
                Logger::get("event::reweighting::NMSSMLHEScaleWeights")
                    ->error("Invalid value for muR: {}", muR);
                throw std::runtime_error("Invalid value for muR");
            }
            if (std::find(allowed_values.begin(), allowed_values.end(), muF) ==
                allowed_values.end()) {
                Logger::get("event::reweighting::NMSSMLHEScaleWeights")
                    ->error("Invalid value for muF: {}", muF);
                throw std::runtime_error("Invalid value for muF");
            }
            // now find the index
            std::map<std::pair<const float, const float>, int> index_map = {
                {{0.5, 0.5}, 0}, {{1.0, 0.5}, 1}, {{2.0, 0.5}, 2},
                {{0.5, 1.0}, 3}, {{2.0, 1.0}, 4},
                {{0.5, 2.0}, 5}, {{1.0, 2.0}, 6}, {{2.0, 2.0}, 7}, {{1.0, 1.0}, 8}};
            std::pair<const float, const float> variations = {muR, muF};
            int index = index_map[variations];
            auto lhe_scale_weights_lambda =
                [index](const ROOT::RVec<float> scale_weight) {
                    if (index==8) {
                        float default_weight = 1.;
                        return default_weight;
                    }
                    else {
                        return scale_weight.at(index);
                    }
                };
            auto df1 =
                df.Define(weightname, lhe_scale_weights_lambda, {lhe_scale_weights});
            return df1;
        }

    }

}


#endif