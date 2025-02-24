import numpy as np
import pandas as pd
from scipy.special import expit  # For modeling Hill functions
from config.config import get_config

def simulate_translation(initialization_results):
    """
    Simulates the translation dynamics across cycles using a Hill function.

    Parameters:
        initialization_results (dict): Output from the initialization module containing:
            - "simulation_data" (pd.DataFrame): Tracks translation efficiency over cycles.
            - "codon_efficiency" (dict): Dictionary with baseline efficiency values.
            - "nutrient_levels" (list of float): Available nutrient levels.

    Returns:
        pd.DataFrame: Updated DataFrame with simulated codon translation efficiencies.

    Raises:
        ValueError: If required keys are missing from `initialization_results`.
    """
    config = get_config()

    # Validate required keys
    required_keys = ["simulation_data", "codon_efficiency", "nutrient_levels"]
    missing_keys = [key for key in required_keys if key not in initialization_results]
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")

    # Extract simulation data
    simulation_data = initialization_results["simulation_data"]
    codon_efficiency = initialization_results["codon_efficiency"]
    nutrient_levels = initialization_results["nutrient_levels"]

    # Constants for translation dynamics
    max_efficiency = config["max_efficiency"]  # Maximum codon efficiency under optimal conditions
    min_efficiency = config["min_efficiency"]  # Minimum codon efficiency under severe stress
    hill_coefficient = config["hill_coefficient"]   # Hill function steepness
    nutrient_threshold = config["nutrient_threshold"]  # Nutrient level threshold for half-maximal efficiency

    # Iterate over each cycle in the simulation
    for index, val in enumerate(nutrient_levels):
        nutrient_level = val  # Extract current cycle's nutrient level

        # Update codon efficiencies
        for codon, properties in codon_efficiency.items():
            base_efficiency = properties["base_efficiency"]  # Reset to base value every row
            
            # Compute new efficiency from scratch
            efficiency = max_efficiency
            efficiency = max_efficiency * expit(hill_coefficient * (nutrient_level - nutrient_threshold))

            if properties["type"] == "robust":
                efficiency = efficiency * base_efficiency  
            elif properties["type"] == "sensitive":
                efficiency = efficiency * base_efficiency * nutrient_level  # Sensitive codons degrade with stress

            # Ensure efficiency doesn't drop below min_efficiency
            efficiency = max(efficiency, min_efficiency)

            # update only the current row
            simulation_data.loc[index, f"{codon}_efficiency"] = efficiency

    print("Translation simulation completed successfully.")
    return simulation_data


if __name__ == "__main__":
    from initialization import initialize_simulation
    
    # Example initialization
    initialization_results = initialize_simulation(
        num_cycles=5,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        robust_codons=["AAA", "GAT"],
        sensitive_codons=["CGT", "CTG"],
    )
    
    # Simulate translation dynamics
    translation_results = simulate_translation(initialization_results)
    
    # Display results
    print(translation_results)

