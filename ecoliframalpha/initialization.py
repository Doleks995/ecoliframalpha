import numpy as np
import pandas as pd
from .config.config import get_config

def initialize_simulation(num_cycles, nutrient_levels, robust_codons=["AAA", "GAT"], sensitive_codons=["CGT", "CTG"] ):
    
    """
    Initializes the simulation environment and sets up parameters.

    Parameters:
        num_cycles (int): Number of translation cycles to simulate.
        nutrient_levels (list of float): List of possible nutrient availability levels.
        robust_codons (list of str): List of codons with high stability under stress.
        sensitive_codons (list of str): List of codons with low stability under stress.

    Returns:
        dict: A dictionary containing:
            - "num_cycles" (int): Number of cycles.
            - "nutrient_levels" (list of float): Nutrient level options.
            - "codon_efficiency" (dict): Dictionary mapping codons to efficiency data.
            - "simulation_data" (pd.DataFrame): DataFrame tracking cycle-based efficiencies.

    Raises:
        ValueError: If input parameters are invalid.
    """
    config = get_config()
    # Validate inputs
    if not isinstance(num_cycles, int) or num_cycles <= 0:
        raise ValueError("num_cycles must be a positive integer.")
    if not isinstance(nutrient_levels, list) or not all(isinstance(n, (int, float)) for n in nutrient_levels):
        raise ValueError("nutrient_levels must be a list of numbers.")
    if not isinstance(robust_codons, list) or not all(isinstance(c, str) for c in robust_codons):
        raise ValueError("robust_codons must be a list of strings.")
    if not isinstance(sensitive_codons, list) or not all(isinstance(c, str) for c in sensitive_codons):
        raise ValueError("sensitive_codons must be a list of strings.")


    # Initialize codon efficiency data
    codon_efficiency = {codon: {"base_efficiency": config["base_efficiency_robust"], "type": "robust"} for codon in robust_codons}
    codon_efficiency.update({codon: {"base_efficiency": config["base_efficiency_sensitive"], "type": "sensitive"} for codon in sensitive_codons})

    # Generate efficiency column names dynamically
    efficiency_columns = {f"{codon}_efficiency": np.nan for codon in robust_codons + sensitive_codons}

    # Create an initial dataframe to track translation efficiency over cycles
    simulation_data = pd.DataFrame({
        "cycle": np.arange(1, num_cycles + 1),
        "nutrient_level": np.random.choice(nutrient_levels, size=num_cycles),
        **efficiency_columns,  # Dynamically add efficiency columns
    })

    return {
        "num_cycles": num_cycles,
        "nutrient_levels": nutrient_levels,
        "codon_efficiency": codon_efficiency,
        "simulation_data": simulation_data,
    }

