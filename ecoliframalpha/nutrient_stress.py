import numpy as np
import pandas as pd

def apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=0.1, recovery_probability=0.05):
    """
    Simulates nutrient stress fluctuations and updates the translation results.

    Parameters:
        translation_results (pd.DataFrame): DataFrame containing translation efficiencies and nutrient levels.
        nutrient_levels (list): List of possible nutrient levels (e.g., [1.0, 0.75, 0.5, 0.25, 0.1]).
        stress_probability (float): Probability of a nutrient drop at each cycle.
        recovery_probability (float): Probability of nutrient recovery at each cycle.

    Returns:
        pd.DataFrame: Updated DataFrame with fluctuating nutrient levels.
    """
    # Initialize variables
    current_nutrient_level = nutrient_levels[0]  # Start with the highest nutrient level

    # Iterate over each cycle in the simulation
    for index in range(len(translation_results)):
        # Simulate stress or recovery events using random probabilities
        if np.random.rand() < stress_probability:
            # Drop to the next lower nutrient level if not already at the lowest level
            current_index = nutrient_levels.index(current_nutrient_level)
            if current_index < len(nutrient_levels) - 1:
                current_nutrient_level = nutrient_levels[current_index + 1]
        elif np.random.rand() < recovery_probability:
            # Recover to the next higher nutrient level if not already at the highest level
            current_index = nutrient_levels.index(current_nutrient_level)
            if current_index > 0:
                current_nutrient_level = nutrient_levels[current_index - 1]
        
        # Update nutrient level for the current cycle
        translation_results.at[index, "nutrient_level"] = current_nutrient_level

    return translation_results

if __name__ == "__main__":
    from initialization import initialize_simulation
    from translation_dynamics import simulate_translation

    # Example initialization
    initialization_results = initialize_simulation(
        num_cycles=1000,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        robust_codons=["AAA", "GAT"],
        sensitive_codons=["CGT", "CTG"],
    )

    # Simulate translation dynamics
    translation_results = simulate_translation(initialization_results)

    # Apply nutrient stress
    stressed_results = apply_nutrient_stress(
        translation_results,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        stress_probability=0.1,
        recovery_probability=0.05,
    )

    # Display updated results
    print(stressed_results.head())
