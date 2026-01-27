#ifndef GUARDJETSEXT_H
#define GUARDJETSEXT_H


namespace physicsobject {

namespace jet {

namespace quantities {

/**
 * @brief Get the value of a generator-level quantity of a jet.
 *
 * The reconstructed jet under consideration is chosen by providing its
 * position within a list of indices. Then, the `Jet_genJetIdx` or
 * `FatJet_genJetAK8Idx` of that jet is used to find the associated
 * generator-level jet, from which the requested quantity value is taken.
 *
 * @param df the input dataframe
 * @param output_name the name of the produced column
 * @param genjet_idx index column that holds the index of the associated generator-level jet
 * @param gen_quantity name of the quantity of the generator-level jet
 * @param index_vector name of the column containing index values
 * @param position position within the index vector used to retrieve the index 
 *
 * @return a dataframe with the new column
 */
template <typename T>
ROOT::RDF::RNode GetGenJetQuantity(
    ROOT::RDF::RNode df,
    const std::string &output_name,
    const std::string &genjet_idx,
    const std::string &gen_quantity,
    const std::string &index_vector,
    const int &position
) {

    auto get_gen_quantity = [position] (
        const ROOT::RVec<Short_t> &genjet_idx,
        const ROOT::RVec<T> &gen_quantity,
        const ROOT::RVec<int> &index_vector
    ) {
        // Define the result with the default value, which is returned when
        // accessing the entries in the vectors fails
        T result = default_value<T>();

        // Get the index to access in the fatjet list
        if (position >= 0 && position < index_vector.size()) {
            auto index = indices.at(position);
            if (index >= 0 && index < genjet_idx.size()) {
                auto gen_index = genjet_idx.at(index);
                result = gen_quantity.at(gen_index);
            }
        } else {
            Logger::get("event::quantity::Get")->debug(
                "Index not found, returning dummy value!"
            );
        }

        return result;
    };

    return df.Define(
        output_name,
        get_gen_quantity,
        {genjet_idx, gen_quantity, index_vector}
    );
}

}

}

}




ROOT::RDF::RNode
CorrectJetIDRun3NanoV12(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt,
    const std::string &jet_eta,
    const std::string &jet_id,
    const std::string &jet_ne_hef,
    const std::string &jet_ne_em_ef,
    const std::string &jet_mu_ef,
    const std::string &jet_ch_em_ef
);


ROOT::RDF::RNode
JetPtPNetRegression(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt_nanoaod,
    const std::string &jet_raw_factor,
    const std::string &jet_pnet_reg_pt_factor,
    const std::string &jet_collection_index
);


ROOT::RDF::RNode
JetPtPNetRegressionWithNeutrino(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &jet_pt_nanoaod,
    const std::string &jet_raw_factor,
    const std::string &jet_pnet_reg_pt_factor,
    const std::string &jet_pnet_reg_pt_neutrino_factor,
    const std::string &jet_collection_index
);


} // end quantities

} // end jet

} // end physicsobject


#endif
