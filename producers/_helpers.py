from code_generation.quantity import Quantity
from code_generation.producer import Producer, ProducerGroup
from typing import Tuple


def type1_jet_collection_producer_factory(
    input: dict[str, Quantity],
    output: dict[str, Quantity],
    scopes: list[str],
    producer_prefix: str = "Type1Jet",
):
    # Get input variables
    jet_pt = input["jet_pt"]
    jet_eta = input["jet_eta"]
    jet_phi = input["jet_phi"]
    jet_id = input["jet_id"]
    jet_area = input["jet_area"]
    jet_raw_factor = input["jet_raw_factor"]
    jet_muon_subtr_factor = input["jet_muon_subtr_factor"]
    jet_ch_em_ef = input["jet_ch_em_ef"]
    jet_ne_em_ef = input["jet_ne_em_ef"]
    corrt1metjet_raw_pt = input["corrt1metjet_raw_pt"]
    corrt1metjet_eta = input["corrt1metjet_eta"]
    corrt1metjet_phi = input["corrt1metjet_phi"]
    corrt1metjet_area = input["corrt1metjet_area"]
    corrt1metjet_muon_subtr_factor = input["corrt1metjet_muon_subtr_factor"]
    corrt1metjet_em_ef = input["corrt1metjet_em_ef"]
    n_corrt1metjet = input["n_corrt1metjet"]

    # Get the output variables
    jet_raw_muon_subtr_pt = output["jet_raw_muon_subtr_pt"]
    jet_em_ef = output["jet_em_ef"]
    corrt1metjet_raw_muon_subtr_pt = output["corrt1metjet_raw_muon_subtr_pt"]
    corrt1metjet_id = output["corrt1metjet_id"]
    t1jet_raw_muon_subtr_pt = output["t1jet_raw_muon_subtr_pt"]
    t1jet_eta = output["t1jet_eta"]
    t1jet_phi = output["t1jet_phi"]
    t1jet_area = output["t1jet_area"]
    t1jet_em_ef = output["t1jet_em_ef"]
    t1jet_id = output["t1jet_id"]

    # Producers defined in this function, collected into a producer group at
    # the end of this function
    producers = []

    # Calculate raw and muon-subtracted jet pt
    producers.append(Producer(
        name=f"{producer_prefix}JetRawMuonSubtr",
        call="physicsobject::jet::jec::RawMuonSubtr({df}, {output}, {input})",
        input=[
            jet_pt,
            jet_raw_factor,
            jet_muon_subtr_factor,
        ],
        output=[jet_raw_muon_subtr_pt],
        scopes=scopes,
    ))

    # Calculate the muon-subtracted jet pt for the CorrT1METJet collection
    producers.append(Producer(
        name=f"{producer_prefix}CorrT1METJetRawMuonSubtr",
        call="physicsobject::jet::jec::RawMuonSubtr({df}, {output}, {input})",
        input=[
            corrt1metjet_raw_pt,
            corrt1metjet_muon_subtr_factor,
        ],
        output=[corrt1metjet_raw_muon_subtr_pt],
        scopes=scopes,
    ))

    # Dummy jet ID column for the CorrT1METJet collection, effectively not used
    # in the JEC (only for the HEMIssue variation in 2018)
    producers.append(Producer(
        name=f"{producer_prefix}CorrT1METJetIDDummy",
        call="event::quantity::Define<UChar_t>({df}, {output}, {input}, 2)",
        input=[n_corrt1metjet],
        output=[corrt1metjet_id],
        scopes=scopes,
    ))

    # For jets, charged and neutral em. energy fraction must be summed
    producers.append(Producer(
        name=f"{producer_prefix}JetEmEf",
        call="event::quantity::SumVectors<float>({df}, {output}, {input})",
        input=[jet_ch_em_ef, jet_ne_em_ef],
        output=[jet_em_ef],
        scopes=scopes,
    ))

    for (input_column_jet, input_column_corrjet), output_column, data_type in [
        ((jet_raw_muon_subtr_pt, corrt1metjet_raw_muon_subtr_pt), t1jet_raw_muon_subtr_pt, "float"),
        ((jet_eta, corrt1metjet_eta), t1jet_eta, "float"),
        ((jet_phi, corrt1metjet_phi), t1jet_phi, "float"),
        ((jet_area, corrt1metjet_area), t1jet_area, "float"),
        ((jet_id, corrt1metjet_id), t1jet_id, "int"),
        ((jet_em_ef, corrt1metjet_em_ef), t1jet_em_ef, "float"),
    ]:
        producers.append(Producer(
            name=f"{producer_prefix}Concatenate{output_column.name}",
            call=f"""
            event::quantity::Concatenate<{data_type}>(
                {{df}},
                {{output}},
                {{input}}
            )
            """,
            input=[input_column_jet, input_column_corrjet],
            output=[output_column],
            scopes=scopes,
        ))

    # Create a producer group for generating all columns needed to concatenate
    # the Jet and the CorrT1METJet collections
    concatenate_producer_group = ProducerGroup(
        name=f"{producer_prefix}Collection",
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=producers,
    )

    return concatenate_producer_group


def stepwise_jerc_producer_factory(
    input: dict[str, Quantity],
    output: dict[str, Quantity],
    scopes: list[str],
    producer_prefix: str = "Jet",
    config_parameter_prefix: str = "jet",
) -> Tuple[ProducerGroup, ProducerGroup, ProducerGroup]:
    """
    Factory function to create producers needed for jet energy corrections.

    Parameters
    ----------

    input: Dict[str, Quantity]

        A dictionary with the input quantities.

        The `input` dictionary must have the following keys with the values being the corresponding :py:class:`~code_generation.quantity.Quantity` objects:

        -  `jet_pt`: The transverse momentum of the jets with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_eta`: The pseudorapidity of the jets.
        -  `jet_phi`: The azimuthal angle of the jets.
        -  `jet_mass`: The mass of the jets with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_area`: The effective jet area.
        -  `jet_raw_factor`: The factor to get the uncorrected jet energy from the jet energy with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_id`: The identification working point that the jets have passed.
        -  `gen_jet_pt`: The transverse momentum of particle-level jets.
        -  `gen_jet_eta`: The pseudorapidity of particle-level jets.
        -  `gen_jet_phi`: The azimuthal angle of particle-level jet.
        -  `rho`: The average energy density in the event.
        -  `luminosity_block`: The luminosity block number.
        -  `run`: The run number.
        -  `event`: The event number.

    output: Dict[str, Quantity]:

        A dictionary with the output quantities that will be produced by the producers.

        The `output` dictionary must have the following keys with the values being corresponding :py:class:`~code_generation.quantity.Quantity` objects:

        - `jet_pt_corrected`: The corrected transverse momentum of the jets.
        - `jet_mass_corrected`: The corrected mass of the jets.

    scopes: List[str]:

        List of analysis scopes, in which the JEC and JER are processed.

    producer_prefix: str, default: "Jet"

        Prefix used for the producer names.

    config_parameter_prefix: str

        Prefix used for the configuration parameter keys, to which producers in this function refer. The values of these parameters must be specified in the main configuration of the analysis.

        The following configuration parameters must be defined in order to use the producers in this function:

        - `{config_parameter_prefix}_jec_file`: The path to the file containing the JEC/JER corrections (in `data/` or `payloads/`).
        - `{config_parameter_prefix}_jes_tag`: The tag in the correction file that should be used for JEC of the simulation.
        - `{config_parameter_prefix}_jes_tag_data`: The tag in the correction file that should be used for JEC of the data.
        - `{config_parameter_prefix}_jer_tag`: The tag in the correction file that should be used for JER of the simulation.
        - `{config_parameter_prefix}_jec_algo`: The pileup mitigation algorithm that has been used for the jets (e.g. `AK4chs`, `AK8PFPuppi`).
        - `{config_parameter_prefix}_reapply_jes`: Flag whether to reapply the nominal JEC. The nominal JEC has already been performed in the `NanoAOD` production.
        - `{config_parameter_prefix}_jes_sources`: Uncertainty sources to be considered for a JEC/JER shift.
        - `{config_parameter_prefix}_jes_shift`: Name of the systematic shift that should be applied to the JEC.
        - `{config_parameter_prefix}_jer_shift`: Name of the systematic shift that should be applied to the JER.
        - `{config_parameter_prefix}_jer_master_seed`: Master seed for generating the seeds for JER smearing.

        LHC run number for which the JEC/JER corrections should be applied. Must be either `2` or `3`.

    Returns
    -------

    Tuple[ProducerGroup, ProducerGroup, ProducerGroup]:

        A tuple containing three :py:class:`~code_generation.producer.ProducerGroup` objects with the following names:

        - `{producer_prefix}EnergyCorrectionData`: The first element is the producer group for the jet energy corrections on data.
        - `{producer_prefix}EnergyCorrectionMC`: The second element is the producer group for the jet energy corrections on simulation.
        - `{producer_prefix}EnergyCorrectionEmb`: The third element is the producer group for the jet energy corrections on embedded events.
    """

    # Get output variables from dictionary
    jet_pt = input["jet_pt"]
    jet_eta = input["jet_eta"]
    jet_phi = input["jet_phi"]
    jet_area = input["jet_area"]
    jet_id = input["jet_id"]
    jet_seed = input["jet_seed"]
    genjet_pt = input["genjet_pt"]
    genjet_eta = input["genjet_eta"]
    genjet_phi = input["genjet_phi"]
    rho = input["rho"]

    # Get output variables from dictionary
    jet_jec_result = output["jet_jec_result"]
    jet_l1_pt = output["jet_l1_pt"]
    jet_l2rel_pt = output["jet_l2rel_pt"]
    jet_l2l3res_pt = output["jet_l2l3res_pt"]
    jet_corrected_pt = output["jet_corrected_pt"]

    # Jet pt correction for jets in data
    jet_pt_correction_data_producer = Producer(
        name=f"{producer_prefix}PtCorrectionData",
        call=f"""
        physicsobject::jet::jec::PtCorrectionData(
            {{df}},
            correctionManager,
            {{output}},
            {{input}},
            "{{{config_parameter_prefix}_jec_file}}",
            "{{{config_parameter_prefix}_jec_algo}}",
            "{{{config_parameter_prefix}_jes_tag}}",
            {{{config_parameter_prefix}_reapply_jes}},
            "{{era}}"
        )
        """,
        input=[
            jet_pt,
            jet_eta,
            jet_phi,
            jet_area,
            rho,
        ],
        output=[
            jet_jec_result,
            jet_l1_pt,
            jet_l2rel_pt,
            jet_l2l3res_pt,
            jet_corrected_pt,
        ],
        scopes=scopes,
    )

    # Jet pt correction for jets in MC
    jet_pt_correction_mc_producer = Producer(
        name=f"{producer_prefix}PtCorrectionMC",
        call=f"""
        physicsobject::jet::jec::PtCorrectionMC(
            {{df}},
            correctionManager,
            {{output}},
            {{input}},
            "{{{config_parameter_prefix}_jec_file}}",
            "{{{config_parameter_prefix}_jec_algo}}",
            "{{{config_parameter_prefix}_jes_tag}}",
            "{{{config_parameter_prefix}_jer_tag}}",
            {{{config_parameter_prefix}_jes_sources}},
            {{{config_parameter_prefix}_jes_shift_factor}},
            "{{{config_parameter_prefix}_jer_shift}}",
            {{{config_parameter_prefix}_reapply_jes}},
            "{{era}}"
        )
        """,
        input=[
            jet_pt,
            jet_eta,
            jet_phi,
            jet_area,
            jet_id,
            genjet_pt,
            genjet_eta,
            genjet_phi,
            rho,
            jet_seed,
        ],
        output=[
            jet_jec_result,
            jet_l1_pt,
            jet_l2rel_pt,
            jet_l2l3res_pt,
            jet_corrected_pt,
        ],
        scopes=scopes,
    )

    return jet_pt_correction_data_producer, jet_pt_correction_mc_producer


def jerc_producer_factory(
    input: dict[str, Quantity],
    output: dict[str, Quantity],
    scopes: list[str],
    producer_prefix: str = "Jet",
    config_parameter_prefix: str = "jet",
) -> Tuple[ProducerGroup, ProducerGroup, ProducerGroup]:
    """
    Factory function to create producers needed for jet energy corrections.

    Parameters
    ----------

    input: Dict[str, Quantity]

        A dictionary with the input quantities.

        The `input` dictionary must have the following keys with the values being the corresponding :py:class:`~code_generation.quantity.Quantity` objects:

        -  `jet_pt`: The transverse momentum of the jets with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_eta`: The pseudorapidity of the jets.
        -  `jet_phi`: The azimuthal angle of the jets.
        -  `jet_mass`: The mass of the jets with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_area`: The effective jet area.
        -  `jet_raw_factor`: The factor to get the uncorrected jet energy from the jet energy with the nominal JEC applied in the `NanoAOD` production.
        -  `jet_id`: The identification working point that the jets have passed.
        -  `gen_jet_pt`: The transverse momentum of particle-level jets.
        -  `gen_jet_eta`: The pseudorapidity of particle-level jets.
        -  `gen_jet_phi`: The azimuthal angle of particle-level jet.
        -  `rho`: The average energy density in the event.
        -  `luminosity_block`: The luminosity block number.
        -  `run`: The run number.
        -  `event`: The event number.

    output: Dict[str, Quantity]:

        A dictionary with the output quantities that will be produced by the producers.

        The `output` dictionary must have the following keys with the values being corresponding :py:class:`~code_generation.quantity.Quantity` objects:

        - `jet_pt_corrected`: The corrected transverse momentum of the jets.
        - `jet_mass_corrected`: The corrected mass of the jets.

    scopes: List[str]:

        List of analysis scopes, in which the JEC and JER are processed.

    producer_prefix: str, default: "Jet"

        Prefix used for the producer names.

    config_parameter_prefix: str

        Prefix used for the configuration parameter keys, to which producers in this function refer. The values of these parameters must be specified in the main configuration of the analysis.

        The following configuration parameters must be defined in order to use the producers in this function:

        - `{config_parameter_prefix}_jec_file`: The path to the file containing the JEC/JER corrections (in `data/` or `payloads/`).
        - `{config_parameter_prefix}_jes_tag`: The tag in the correction file that should be used for JEC of the simulation.
        - `{config_parameter_prefix}_jes_tag_data`: The tag in the correction file that should be used for JEC of the data.
        - `{config_parameter_prefix}_jer_tag`: The tag in the correction file that should be used for JER of the simulation.
        - `{config_parameter_prefix}_jec_algo`: The pileup mitigation algorithm that has been used for the jets (e.g. `AK4chs`, `AK8PFPuppi`).
        - `{config_parameter_prefix}_reapply_jes`: Flag whether to reapply the nominal JEC. The nominal JEC has already been performed in the `NanoAOD` production.
        - `{config_parameter_prefix}_jes_sources`: Uncertainty sources to be considered for a JEC/JER shift.
        - `{config_parameter_prefix}_jes_shift`: Name of the systematic shift that should be applied to the JEC.
        - `{config_parameter_prefix}_jer_shift`: Name of the systematic shift that should be applied to the JER.
        - `{config_parameter_prefix}_jer_master_seed`: Master seed for generating the seeds for JER smearing.

        LHC run number for which the JEC/JER corrections should be applied. Must be either `2` or `3`.

    Returns
    -------

    Tuple[ProducerGroup, ProducerGroup, ProducerGroup]:

        A tuple containing three :py:class:`~code_generation.producer.ProducerGroup` objects with the following names:

        - `{producer_prefix}EnergyCorrectionData`: The first element is the producer group for the jet energy corrections on data.
        - `{producer_prefix}EnergyCorrectionMC`: The second element is the producer group for the jet energy corrections on simulation.
        - `{producer_prefix}EnergyCorrectionEmb`: The third element is the producer group for the jet energy corrections on embedded events.
    """

    # get input quantities
    jet_pt = input["jet_pt"]
    jet_eta = input["jet_eta"]
    jet_phi = input["jet_phi"]
    jet_mass = input["jet_mass"]
    jet_area = input["jet_area"]
    jet_raw_factor = input["jet_raw_factor"]
    jet_id = input["jet_id"]
    gen_jet_pt = input["gen_jet_pt"]
    gen_jet_eta = input["gen_jet_eta"]
    gen_jet_phi = input["gen_jet_phi"]
    rho = input["rho"]
    luminosity_block = input["luminosity_block"]
    run = input["run"]
    event = input["event"]

    # get outputs
    jet_seed = output["jet_seed"]
    jet_pt_corrected = output["jet_pt_corrected"]
    jet_mass_corrected = output["jet_mass_corrected"]

    # jet pt correction for data jets
    jet_pt_correction_data = Producer(
        name=f"{producer_prefix}JetPtCorrectionData",
        call=(
            "physicsobject::jet::PtCorrectionData("
                "{df}, "
                "correctionManager, "
                "{output}, "
                "{input}, "
                f"\"{{{config_parameter_prefix}_jec_file}}\", "
                f"\"{{{config_parameter_prefix}_jec_algo}}\", "
                f"{{{config_parameter_prefix}_jes_tag_data}}, "
                "\"{era}\""
            ")"
        ),
        input=[
            jet_pt,
            jet_eta,
            jet_phi,
            jet_area,
            jet_raw_factor,
            rho,
            run,
        ],
        output=[jet_pt_corrected],
        scopes=scopes,
    )

    # initialize seed for jet energy resolution smearing
    jet_smearing_seed = Producer(
        name=f"{producer_prefix}SmearingSeed",
        call=f"event::quantity::GenerateSeed({{df}}, {{output}}, {{input}}, {{{config_parameter_prefix}_jer_master_seed}})",
        input=[
            luminosity_block,
            run,
            event,
        ],
        output=[jet_seed],
        scopes=["global"],
    )

    # jet pt correction for MC jets
    jet_pt_correction_mc = Producer(
        name=f"{producer_prefix}PtCorrectionMC",
        call=(
            "physicsobject::jet::PtCorrectionMC("
                "{df}, "
                "correctionManager, "
                "{output}, "
                "{input}, "
                f"\"{{{config_parameter_prefix}_jec_file}}\", "
                f"\"{{{config_parameter_prefix}_jec_algo}}\", "
                f"\"{{{config_parameter_prefix}_jes_tag}}\", "
                f"{{{config_parameter_prefix}_jes_sources}}, "
                f"\"{{{config_parameter_prefix}_jer_tag}}\", "
                f"{{{config_parameter_prefix}_reapply_jes}}, "
                f"{{{config_parameter_prefix}_jes_shift_factor}}, "
                f"\"{{{config_parameter_prefix}_jer_shift}}\", "
                "\"{era}\", "
                f"{{{config_parameter_prefix}_apply_jet_horn_veto}}"
            ")"
        ),
        input=[
            jet_pt,
            jet_eta,
            jet_phi,
            jet_area,
            jet_raw_factor,
            jet_id,
            gen_jet_pt,
            gen_jet_eta,
            gen_jet_phi,
            rho,
            jet_seed,
        ],
        output=[jet_pt_corrected],
        scopes=scopes,
    )

    # jet pt correction for jets in embedded events (just rename column)
    jet_pt_correction_emb = Producer(
        name=f"{producer_prefix}JetPtCorrectionEmb",
        call=(
            "event::quantity::Rename<ROOT::RVec<float>>("
                "{df}, "
                "{output}, "
                "{input}"
            ")"
        ),
        input=[jet_pt],
        output=[jet_pt_corrected],
        scopes=scopes,
    )

    # jet mass correction (data and MC)
    jet_mass_correction = Producer(
        name=f"{producer_prefix}MassCorrection",
        call=(
            "physicsobject::MassCorrectionWithPt("
                "{df}, "
                "{output}, "
                "{input}"
            ")"
        ),
        input=[
            jet_mass,
            jet_pt,
            jet_pt_corrected,
        ],
        output=[jet_mass_corrected],
        scopes=scopes,
    )

    # jet mass correction for jets in embedded events (just rename column)
    jet_mass_correction_emb = Producer(
        name=f"{producer_prefix}JetMassCorrectionEmb",
        call=(
            "event::quantity::Rename<ROOT::RVec<float>>("
                "{df}, "
                "{output}, "
                "{input}"
            ")"
        ),
        input=[jet_mass],
        output=[jet_mass_corrected],
        scopes=scopes,
    )

    # create jet energy correction group (data)
    jet_energy_correction_data = ProducerGroup(
        name=f"{producer_prefix}EnergyCorrectionData",
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=[jet_pt_correction_data, jet_mass_correction],
    )

    # create jet energy correction group (MC)
    jet_energy_correction_mc = ProducerGroup(
        name=f"{producer_prefix}EnergyCorrectionMC",
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=[jet_smearing_seed, jet_pt_correction_mc, jet_mass_correction],
    )

    # create jet energy correction group (embedding, just rename columns)
    jet_energy_correction_emb = ProducerGroup(
        name=f"{producer_prefix}EnergyCorrectionEmb",
        call=None,
        input=None,
        output=None,
        scopes=scopes,
        subproducers=[jet_pt_correction_emb, jet_mass_correction_emb],
    )

    return (
        jet_energy_correction_data,
        jet_energy_correction_mc,
        jet_energy_correction_emb,
    )
