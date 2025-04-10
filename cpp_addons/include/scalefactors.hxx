#ifndef GUARD_SCALEFACTORSEXT_H
#define GUARD_SCALEFACTORSEXT_H


namespace scalefactor {

namespace muon {

ROOT::RDF::RNode
trigger(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &eta, const std::string &year_id,
    const std::string &variation,
    const std::string &trigger_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

ROOT::RDF::RNode
id(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &eta,
    const std::string &year_id,
    const std::string &variation,
    const std::string &id_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

ROOT::RDF::RNode
iso(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &eta,
    const std::string &year_id,
    const std::string &variation,
    const std::string &iso_output,
    const std::string &sf_file,
    const std::string &idAlgorithm
);

} // end muon

namespace fatjet {

ROOT::RDF::RNode
pNetXbbSF(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &nBhad,
    const std::string &nChad, 
    const std::string &variation,
    const std::string &sf_output,
    const std::string &sf_file
);

ROOT::RDF::RNode
trigger(
    ROOT::RDF::RNode df,
    correctionManager::CorrectionManager &correctionManager,
    const std::string &pt,
    const std::string &msoftdrop,
    const std::string &sf_output, 
    const std::string &sf_file,
    const std::string &sf_name, 
    const std::string &variation
);

} // namespace fatjet

} // end scalefactor

#endif