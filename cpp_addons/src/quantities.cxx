#ifndef GUARDQUANTITIESEXT_H
#define GUARDQUANTITIESEXT_H

#include "../../../../include/utility/Logger.hxx"
#include "../../../../include/defaults.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace v12 {

namespace quantities {

namespace tau {

/// Function to writeout a flag if a tau passes a specific tau id cut. The
/// particle is identified via the index stored in the pair vector
///
/// \param df the dataframe to add the quantity to
/// \param outputname name of the new column containing the flag
/// \param position index of the position in the pair vector
/// \param pairname name of the column containing the pair vector
/// \param nameID name of the ID column in the NanoAOD
/// \param idxID bitvalue of the WP the has to be passed
///
/// \returns a dataframe with the new column

ROOT::RDF::RNode TauIDFlag(ROOT::RDF::RNode df, const std::string &outputname,
                           const int &position, const std::string &pairname,
                           const std::string &nameID, const int &idxID) {
    return df.Define(
        outputname,
        [position, idxID](const ROOT::RVec<int> &pair,
                          const ROOT::RVec<UChar_t> &IDs) {
            Logger::get("tauIDFlag")
                ->debug(
                    "position tau in pair {}, pair {}, id bit {}, vsjet ids {}",
                    position, pair, idxID, IDs);
            const int index = pair.at(position);
            const int ID = static_cast<int>(IDs.at(index, default_int));
            if (ID != default_int) {
                return int(ID >= idxID);
            } else {
                return 0;
            }
        },
        {pairname, nameID});
}

}

}

}

#endif