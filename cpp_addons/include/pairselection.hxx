#ifndef GUARDPAIRSELECTIONEXT_H
#define GUARDPAIRSELECTIONEXT_H

#include "ROOT/RDataFrame.hxx"


namespace ditau_pairselection {

ROOT::RDF::RNode
findAdditionalTau(
    ROOT::RDF::RNode df,
    const std::string &outputname, 
    const std::string &tau_mask,
    const std::string &pairname
);

}


namespace boosted_ditau_pairselection {

auto
compareForPairs
(
    const ROOT::RVec<float> &lep1pt,
    const ROOT::RVec<float> &lep1eta,
    const ROOT::RVec<float> &lep1phi,
    const ROOT::RVec<float> &lep1mass,
    const ROOT::RVec<float> &lep2pt,
    const ROOT::RVec<float> &lep2eta,
    const ROOT::RVec<float> &lep2phi,
    const ROOT::RVec<float> &lep2mass
);

namespace semileptonic {

auto
PairSelectionAlgo(
    const float &mindeltaR,
    const float &maxdeltaR
);

} // end semileptonic

namespace fullhadronic {

auto PairSelectionAlgo(const float &mindeltaR, const float &maxdeltaR);
} // end namespace fullhadronic

namespace mutau {

ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR);
} // end mutau
namespace eltau {

ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR);
} // end mutau
namespace tautau {

ROOT::RDF::RNode PairSelection(ROOT::RDF::RNode df,
                               const std::vector<std::string> &input_vector,
                               const std::string &pairname,
                               const float &mindeltaR, const float &maxdeltaR);
} // end tautau
} // end boosted_ditau_pairselection


namespace bb_pairselection {

auto BBPairSelectionAlgo(const float &mindeltaR, const float &btag_WP_value);

ROOT::RDF::RNode
PairSelection(
    ROOT::RDF::RNode df,
    const std::vector<std::string> &input_vector,
    const std::string &pairname,
    const float &mindeltaR,
    const float &btag_WP_value
);

} // end bb_pairselection


#endif