#ifndef GUARD_TRIGGERSEXT_H
#define GUARD_TRIGGERSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include <regex>


namespace trigger {


/**
 * @brief Function to generate a trigger flag based on an hlt path.
 *
 * @param df The input dataframe
 * @param triggerflag_name name of the output flag
 * @param hltpath name of the hlt path to be checked, this can be a valid regex.
 * If more than one matching HLT path is found, the function will throw an
 * exception, if no matching HLT path is found, the function will return a
 * dataframe with a flag of false for all entries
 * @return a new dataframe containing the trigger flag column
 */

ROOT::RDF::RNode GenerateTriggerFlag(
    ROOT::RDF::RNode df, const std::string &triggerflag_name,
    const std::string &hltpath) {

    auto triggermatch =
        [hltpath](bool hltpath_match) {
            Logger::get("GenerateTriggerFlag")->debug("Checking Trigger");
            Logger::get("CheckTriggerMatch")
                    ->debug("Selected trigger: {}", hltpath);
            bool result = false;
            result = hltpath_match;
            Logger::get("GenerateTriggerFlag")
                ->debug("---> HLT Match: {}", hltpath_match);
            Logger::get("GenerateTriggerFlag")
                ->debug("--->>>> result: {}", result);
            return result;
        };
    auto available_trigger = df.GetColumnNames();
    std::vector<std::string> matched_trigger_names;
    std::regex hltpath_regex = std::regex(hltpath);
    // loop over all available trigger names and check if the hltpath is
    // matching any of them
    for (auto &trigger : available_trigger) {
        if (std::regex_match(trigger, hltpath_regex)) {
            Logger::get("GenerateTriggerFlag")
                ->debug("Found matching trigger: {}", trigger);
            matched_trigger_names.push_back(trigger);
        }
    }
    // if no matching trigger was found return the initial dataframe
    if (matched_trigger_names.size() == 0) {
        Logger::get("GenerateTriggerFlag")
            ->info("No matching trigger for {} found, returning false for "
                   "trigger flag {}",
                   hltpath, triggerflag_name);
        auto df1 = df.Define(triggerflag_name, []() { return false; });
        return df1;
    } else if (matched_trigger_names.size() > 1) {
        Logger::get("GenerateTriggerFlag")
            ->debug(
                "More than one matching trigger found, not implemented yet");
        throw std::invalid_argument(
            "received too many matching trigger paths, not implemented yet");
    } else {
        Logger::get("GenerateTriggerFlag")
            ->debug("Found matching trigger: {}", matched_trigger_names[0]);
        auto df1 =
            df.Define(triggerflag_name, triggermatch,
                      {matched_trigger_names[0]});
        return df1;
    }
}

} // end trigger


#endif // end GUARD_TRIGGERSEXT_H