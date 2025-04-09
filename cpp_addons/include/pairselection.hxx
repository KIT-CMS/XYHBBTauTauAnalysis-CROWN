#ifndef GUARDPAIRSELECTIONEXT_H
#define GUARDPAIRSELECTIONEXT_H

#include "ROOT/RDataFrame.hxx"


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