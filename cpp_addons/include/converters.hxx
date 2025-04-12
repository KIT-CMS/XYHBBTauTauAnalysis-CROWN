#ifndef GUARD_CONVERTERSEXT_H
#define GUARD_CONVERTERSEXT_H

#include "../../../../include/utility/CorrectionManager.hxx"
#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"


namespace converters {

template<typename T, typename U>
ROOT::RDF::RNode
cast(ROOT::RDF::RNode df,
       const std::string &input,
       const std::string &output
) {
    auto df1 = df.Define(
        output,
        [] (const T& input) {
            return static_cast<U>(input);
        },
        {input});

    return df1;
}

} // end converters

#endif