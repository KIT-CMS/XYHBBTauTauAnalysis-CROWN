from code_generation.quantity import Quantity
from code_generation.producer import Producer, ProducerGroup
from typing import Tuple


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
        - `{config_parameter_prefix}_reapplyJES`: Flag whether to reapply the nominal JEC. The nominal JEC has already been performed in the `NanoAOD` production.
        - `{config_parameter_prefix}_jes_sources`: Uncertainty sources to be considered for a JEC/JER shift.
        - `{config_parameter_prefix}_jes_shift`: Name of the systematic shift that should be applied to the JEC.
        - `{config_parameter_prefix}_jer_shift`: Name of the systematic shift that should be applied to the JER.

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

    # get outputs
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
                f"{{{config_parameter_prefix}_jec_file}}, "
                f"{{{config_parameter_prefix}_jec_algo}}, "
                f"{{{config_parameter_prefix}_jes_tag_data}}"
            ")"
        ),
        input=[
            jet_pt,
            jet_eta,
            jet_area,
            jet_raw_factor,
            rho,
        ],
        output=[jet_pt_corrected],
        scopes=scopes,
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
                f"{{{config_parameter_prefix}_jec_file}}, "
                f"{{{config_parameter_prefix}_jec_algo}}, "
                f"{{{config_parameter_prefix}_jes_tag}}, "
                f"{{{config_parameter_prefix}_jes_sources}}, "
                f"{{{config_parameter_prefix}_jer_tag}}, "
                f"{{{config_parameter_prefix}_reapplyJES}}, "
                f"{{{config_parameter_prefix}_jes_shift}}, "
                f"{{{config_parameter_prefix}_jer_shift}}" 
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
                "{input}, "
                "{output}"
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
                "{input}, "
                "{output}"
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
        subproducers=[jet_pt_correction_mc, jet_mass_correction],
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
