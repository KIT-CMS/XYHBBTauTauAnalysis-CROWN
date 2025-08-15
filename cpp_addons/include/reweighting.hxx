#ifndef GUARDREWEIGHTINGEXT_HXX
#define GUARDREWEIGHTINGEXT_HXX

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace event {


    namespace reweighting {
        
        ROOT::RDF::RNode NMSSMLHEScaleWeights(ROOT::RDF::RNode df,
                                           const std::string &weightname,
                                           const std::string &lhe_scale_weights,
                                           const float muR, const float muF);

    }

}

#endif