#ifndef GUARDREWEIGHTINGEXT_H


namespace v12 {

namespace reweighting {

ROOT::RDF::RNode topptreweighting(
    ROOT::RDF::RNode df,
    const std::string &weightname,
    const std::string &gen_pdgids,
    const std::string &gen_status,
    const std::string &gen_pt
);

} // namespace reweighing

} // namespace v12


#endif