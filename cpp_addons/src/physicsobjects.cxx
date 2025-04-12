#ifndef GUARD_PHYSICSOBJECTSEXT_H
#define GUARD_PHYSICSOBJECTSEXT_H

#include "ROOT/RDFHelpers.hxx"
#include "ROOT/RDataFrame.hxx"
#include <Math/VectorUtil.h>


namespace v12 {

namespace physicsobject {

namespace electron {

/// Function to cut electrons based on the cut based electron ID
///
/// \param[in] df the input dataframe
/// \param[out] maskname the name of the new mask to be added as column to
/// the dataframe
/// \param[in] nameID name of the ID column in the NanoAOD
/// \param[in] IDvalue value of the WP the has to be passed
///
/// \return a dataframe containing the new mask
ROOT::RDF::RNode CutCBID(ROOT::RDF::RNode df, const std::string &maskname,
                         const std::string &nameID, const int &IDvalue) {
    auto df1 =
        df.Define(
            maskname,
            [IDvalue] (const ROOT::VecOps::RVec<UChar_t> &cutbased_id) {
                ROOT::RVec<int> cutbased_id_int = static_cast<ROOT::RVec<int>>(cutbased_id);
                std::cout << cutbased_id_int << std::endl;
                auto mask = cutbased_id_int >= IDvalue;
                std::cout << mask << std::endl;
                return (ROOT::RVec<int>) mask;
            },
            {nameID}
        );
    return df1;
}

}

}

}


#endif