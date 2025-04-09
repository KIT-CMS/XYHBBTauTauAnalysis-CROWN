#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H


namespace physicsobject {

namespace jet {

ROOT::RDF::RNode
BJetPtCorrection(
    ROOT::RDF::RNode df,
    const std::string &corrected_bjet_pt,
    const std::string &jet_pt,
    const std::string &good_bjet_mask,
    const std::string &corr_factor
);

} // end jet

} // end physicsobject

namespace quantities {

namespace jet {

ROOT::RDF::RNode
bRegRes(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &resolution_column,
    const std::string &jetcollection,
    const int &position
);

} // end jet

} // end quantities

#endif