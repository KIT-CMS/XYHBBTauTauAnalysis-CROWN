#ifndef GUARD_BASEFUNCTIONSEXT_H
#define GUARD_BASEFUNCTIONSEXT_H

#include "../../../../include/utility/Logger.hxx"
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDFHelpers.hxx"
#include "ROOT/RVec.hxx"


namespace basefunctions {


/**
 * @brief Take elements with given elements from an input vector.
 * 
 * The lambda function takes an `RVec` object from the column `input`
 * and a list of indices from the column `collection_index` . It
 * returns a new `RVec` object, saved in the new column `output`, that
 * contains the elements of the input vector with the specified indices.
 * 
 * Internally, this function makes use of the `ROOT::VecOps::Take`
 * function.
 * 
 * @param df The RDataFrame, to which the new column is added.
 * @param output The name of the new column.
 * @param input The name of the input column.
 * @param collection_index The name of the column with an index list.
 * 
 * @returns An RDataFrame with a new column.
 */
template <typename T>
ROOT::RDF::RNode take(
    ROOT::RDF::RNode df,
    const std::string &output,
    const std::string &input,
    const std::string &collection_index
) {

    auto select = (
        const ROOT::RVec<T> &input,
        const ROOT::RVec<int> &collection_index
    ) {
        Logger::get("take")->debug("input vector: {}", input);
        Logger::get("take")->debug("collection index: {}", collection_index);
        auto output = ROOT::VecOps::Take(input, collection_index);
        Logger::get("take")->debug("output vector: {}", output);
        return output;
    };

    return df.Define(
        output,
        select,
        {input, collection_index}
    );
}


} // end basefunctions

#endif