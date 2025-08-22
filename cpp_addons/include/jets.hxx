#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H


namespace physicsobject {

namespace jet {

namespace quantities {

ROOT::RDF::RNode
CorrectJetIDRun3NanoV12(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_id,
    const std::string &jet_ne_hef,
    const std::string &jet_ne_em_ef,
    const std::string &jet_mu_ef,
    const std::string &jet_ch_em_ef
); 

} // end quantities

} // end jet

} // end physicsobject


#endif