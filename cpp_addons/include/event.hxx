#ifndef GUARDEVENTEXT_H
#define GUARDEVENTEXT_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include <Math/VectorUtil.h>


namespace event {

namespace quantity {

/**
 * @brief This function adds a new column to the dataframe, assigning it a
 * vector of constant value for all entries. The length of the vector is
 * determined by the column containing the number of objects in a collection,
 * e.g., `nJet` for the `Jet` collection.
 *
 * @tparam T type of the value to be assigned
 * @param df input dataframe
 * @param outputname name of the new column
 * @param number_column column containing the length of an object collection
 * for each event
 * @param value constant value to be assigned to the new column
 *
 * @return a dataframe with the new column
 */
template <typename T>
inline ROOT::RDF::RNode Define(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &number_column,
    T const &value
) {
    return df.Define(
        outputname,
        [value] (const int &number_column) {
            return ROOT::RVec<T>(number_column, value);
        },
        {number_column}
    );
}

template <typename T>
ROOT::RDF::RNode Concatenate(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &inputname_1,
    const std::string &inputname_2
) {
    auto cat_func = [] (
        ROOT::RVec<T> input_1,
        ROOT::RVec<T> input_2
    ) {
        return ROOT::VecOps::Concatenate(input_1, input_2);
    };

    return df.Define(
        outputname,
        cat_func,
        {inputname_1, inputname_2}

    );
}

/**
 * @brief This function sums two vectors. The output vector contains the
 * element-wise sum in each component.
 *
 * @tparam T type of the input column values
 * @param df input dataframe
 * @param outputname name of the new column containing the summed values
 * @param quantity_1 name of the first vector column in the sum
 * @param quantity_2 name of the second vector column in the sum
 *
 * @return a dataframe with the new column
 */
template <typename T>
inline ROOT::RDF::RNode SumVectors(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &quantity_1,
    const std::string &quantity_2,
    const T zero = T(0)
) {
    auto sum_func = [] (
        const ROOT::RVec<T> &quantity_1,
        const ROOT::RVec<T> &quantity_2
    ) {
        return quantity_1 + quantity_2;
    };
    return df.Define(outputname, sum_func, {quantity_1, quantity_2});
}

} // end namespace quantity

} // end namespace event


#endif