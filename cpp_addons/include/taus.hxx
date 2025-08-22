#ifndef GUARD_TAUSEXT_HXX
#define GUARD_TAUSEXT_HXX

#include "../include/utility/CorrectionManager.hxx"
#include "ROOT/RDataFrame.hxx"


namespace physicsobject {
namespace tau {
namespace scalefactor {

ROOT::RDF::RNode Id_vsJet(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correction_manager,
    const std::string &outputname, 
    const std::string &pt, const std::string &decay_mode,
    const std::string &gen_match, 
    const std::string &sf_file, const std::string &sf_name,
    const std::string &wp, const std::string &vsele_wp,
    const std::string &sf_dependence,
    const std::string &variation);


}
}
}

#endif