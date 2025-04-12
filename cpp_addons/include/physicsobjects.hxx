#ifndef GUARD_PHYSICSOBJECTSEXT_H
#define GUARD_PHYSICSOBJECTSEXT_H


namespace v12 {

namespace physicsobject {

namespace electron {


ROOT::RDF::RNode CutCBID(ROOT::RDF::RNode df, const std::string &maskname,
                         const std::string &nameID, const int &IDvalue);

}

}

}


#endif