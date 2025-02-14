import numpy as np
import pandas as pd

def initialize_simulation(num_cycles, nutrient_levels, robust_codons, sensitive_codons):
    
    """
    Initializes the simulation environment and sets up parameters.
    
    Parameters:
        num_cycles (int): Number of translation cycles to simulate.
        nutrient_levels (list): List of nutrient availability scenarios.
        robust_codons (list): Codons with high stability under stress.
        sensitive_codons (list): Codons with low stability under stress.
    
    Returns:
        dict: A dictionary containing initialized simulation parameters and data structures.
    """
    # Initialize codon categories with their baseline efficiencies
    codon_efficiency = {
        codon: {"base_efficiency": 1.0, "type": "robust"} for codon in robust_codons
    }
    codon_efficiency.update({
        codon: {"base_efficiency": 0.5, "type": "sensitive"} for codon in sensitive_codons
    })
    
    # Create an initial dataframe to track translation efficiency over cycles
    simulation_data = pd.DataFrame({
        "cycle": np.arange(1, num_cycles + 1),
        "nutrient_level": np.random.choice(nutrient_levels, size=num_cycles),
        "AAA_efficiency": np.nan,  # Robust codon
        "GAT_efficiency": np.nan,  # Robust codon
        "CGT_efficiency": np.nan,  # Sensitive codon
        "CTG_efficiency": np.nan,  # Sensitive codon
    })
    
    # Return initialized parameters and data
    return {
        "num_cycles": num_cycles,
        "nutrient_levels": nutrient_levels,
        "codon_efficiency": codon_efficiency,
        "simulation_data": simulation_data,
    }

if __name__ == "__main__":
    # Example inputs
    num_cycles = 1000
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]
    robust_codons = ["AAA", "GAT"]
    sensitive_codons = ["CGT", "CTG"]

    # Initialize the simulation
    initialization_results = initialize_simulation(
        num_cycles, nutrient_levels, robust_codons, sensitive_codons
    )
    
    # Access initialized data
    print("Simulation Parameters:", initialization_results["codon_efficiency"])
    print("Sample Data:", initialization_results["simulation_data"].head())
