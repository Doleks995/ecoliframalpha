import numpy as np
import pandas as pd
from scipy.special import expit  # For modeling Hill functions

def simulate_translation(initialization_results):
    """
    Simulates the translation dynamics across cycles.

    Parameters:
        initialization_results (dict): Output from the initialization module containing simulation parameters
                                       and initial data structures.

    Returns:
        pd.DataFrame: Updated DataFrame with simulated translation efficiencies for each codon.
    """
    # Extract data from initialization results
    simulation_data = initialization_results["simulation_data"]
    codon_efficiency = initialization_results["codon_efficiency"]
    nutrient_levels = initialization_results["nutrient_levels"]
    
    # Constants for translation dynamics
    max_efficiency = 1.5  # Maximum codon efficiency under optimal conditions
    min_efficiency = 0.1  # Minimum codon efficiency under severe stress
    hill_coefficient = 2  # Hill function steepness
    nutrient_threshold = 0.5  # Nutrient level threshold for half-maximal efficiency

    # Iterate over each cycle in the simulation
    for index, row in simulation_data.iterrows():
        nutrient_level = row["nutrient_level"]

        # Update codon efficiencies using a Hill function
        for codon, properties in codon_efficiency.items():
            base_efficiency = properties["base_efficiency"]
            efficiency = max_efficiency * expit(hill_coefficient * (nutrient_level - nutrient_threshold))
            
            # Scale efficiency based on codon type
            if properties["type"] == "robust":
                efficiency *= base_efficiency
            elif properties["type"] == "sensitive":
                efficiency *= base_efficiency * nutrient_level

            simulation_data.at[index, f"{codon}_efficiency"] = efficiency
                    
            # Scale efficiency for robust and sensitive codons
            if properties["type"] == "robust":
                efficiency *= base_efficiency  # Robust codons maintain higher efficiency
            elif properties["type"] == "sensitive":
                efficiency *= base_efficiency * nutrient_level  # Sensitive codons degrade with stress
            
            # Update the simulation data
            simulation_data.at[index, f"{codon}_efficiency"] = efficiency

    return simulation_data

if __name__ == "__main__":
    from initialization import initialize_simulation
    
    # Example initialization
    initialization_results = initialize_simulation(
        num_cycles=1000,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        robust_codons=["AAA", "GAT"],
        sensitive_codons=["CGT", "CTG"],
    )
    
    # Simulate translation dynamics
    translation_results = simulate_translation(initialization_results)
    
    # Display results
    print(translation_results.head())

