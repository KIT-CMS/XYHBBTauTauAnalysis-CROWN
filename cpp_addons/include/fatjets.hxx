#ifndef GUARDFATJETSEXT_H
#define GUARDFATJETSEXT_H

#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


namespace fatjet {


namespace matching {


template <typename T>
ROOT::RDF::RNode matched_object_quantity(
    ROOT::RDF::RNode df,
    const std::string &output,
    const std::string &input,
    const std::string &other_matches_index,
    const int &position
) {
    auto get_quantity = [position] (
        const ROOT::RVec<T> &input,
        const ROOT::RVec<float> &other_matches_index
    ) {
        T output = default_value<T>();
        auto default_output = default_value<T>();
        for (int fatjet_index = 0; fatjet_index < other_matches_index.size(); ++fatjet_index) {
            auto other_matches_index_single = other_matches_index.at(fatjet_index);
            if (position >= 0 && position < other_matches_index_single.size()) {
                const int index = other_matches_index_single.at(position);
                output = input.at(index);
            }
        }
        return output;
    };

    return df.Define(
        output,
        get_quantity,
        {input, other_matches_index}
    )
}

}

}


namespace fatjet {

namespace matching {

ROOT::RDF::RNode match_object(
    ROOT::RDF::RNode df,
    const std::string &output,
    const std::string &fatjet_eta,
    const std::string &fatjet_phi,
    const std::string &fatjet_index,
    const std::string &other_eta,
    const std::string &other_phi,
    const std::string &other_index,
    const float &max_delta_r
);

}

}


namespace fatjet {

ROOT::RDF::RNode
FindFatjetMatchingBjet(
    ROOT::RDF::RNode df,
    const std::string &output_name,
    const std::string &good_fatjet_collection,
    const std::string &fatjet_pt,
    const std::string &fatjet_eta,
    const std::string &fatjet_phi,
    const std::string &fatjet_mass,
    const std::string &bpair_p4_1,
    const float &deltaRmax
);

ROOT::RDF::RNode
FindXbbFatjet(
    ROOT::RDF::RNode df,
    const std::string &output_name,
    const std::string &good_fatjet_collection,
    const std::string &fatjet_pNet_Xbb,
    const std::string &fatjet_pNet_QCD
);

} // end fatjet


namespace quantities {

namespace fatjet {

ROOT::RDF::RNode
msoftdrop(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &m_softdrop,
    const std::string &fatjetcollection,
    const int &position
);

ROOT::RDF::RNode
particleNet_XbbvsQCD(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &pNet_Xbb,
    const std::string &pNet_QCD,
    const std::string &fatjetcollection,
    const int &position
);

ROOT::RDF::RNode
nsubjettiness_ratio(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &tauN,
    const std::string &tauNm1,
    const std::string &fatjetcollection,
    const int &position
);

ROOT::RDF::RNode
hadflavor(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &fatjet_hadflavor,
    const std::string &fatjetcollection,
    const int &position
);

ROOT::RDF::RNode
nHadrons(
    ROOT::RDF::RNode df,
    const std::string &outputname,
    const std::string &fatjet_nHadrons,
    const std::string &fatjetcollection,
    const int &position
);

} // end fatjet

} // end quantities


#endif /* GUARDFATJETS_H */