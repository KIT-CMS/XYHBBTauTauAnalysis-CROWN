#ifndef GUARD_TRIGGERSEXT_H
#define GUARD_TRIGGERSEXT_H


namespace trigger {

ROOT::RDF::RNode GenerateTriggerFlag(
    ROOT::RDF::RNode df, const std::string &triggerflag_name,
    const std::string &hltpath);

} // end trigger


#endif // end GUARD_TRIGGERSEXT_H