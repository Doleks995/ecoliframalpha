import numpy as np
import pandas as pd

def apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=0.1, recovery_probability=0.05):
    """
    Simulates nutrient stress fluctuations and updates the translation results.

    Parameters:
        translation_results (pd.DataFrame): DataFrame containing translation efficiencies and nutrient levels.
        nutrient_levels (list): List of possible nutrient levels (e.g., [1.0, 0.75, 0.5, 0.25, 0.1]).
        stress_probability (float): Probability of a nutrient drop at each cycle (0 ≤ p ≤ 1).
        recovery_probability (float): Probability of nutrient recovery at each cycle (0 ≤ p ≤ 1).

    Returns:
        pd.DataFrame: Updated DataFrame with fluctuating nutrient levels.
    """
    # Validate inputs
    if not isinstance(nutrient_levels, list) or len(nutrient_levels) == 0:
        raise ValueError("nutrient_levels must be a non-empty list of numeric values.")

    if not (0 <= stress_probability <= 1):
        raise ValueError("stress_probability must be between 0 and 1.")

    if not (0 <= recovery_probability <= 1):
        raise ValueError("recovery_probability must be between 0 and 1.")

    if translation_results.empty:
        return translation_results  # Return unchanged if DataFrame is empty

    # Copy to prevent modifying input DataFrame
    updated_results = translation_results.copy()

    # Iterate over each cycle in the simulation
    for index, val in enumerate(updated_results["nutrient_levels"]):  # Ensure correct column name
        val = float(val)  # Ensure `val` is a float to avoid lookup issues
        current_index = nutrient_levels.index(val)

        if np.random.rand() < stress_probability:
            if current_index < len(nutrient_levels)-1:
                updated_results.loc[index, "nutrient_levels"] = nutrient_levels[current_index + 1]
        elif np.random.rand() < recovery_probability:
            if current_index > 0:
                updated_results.loc[index, "nutrient_levels"] = nutrient_levels[current_index - 1]


    return updated_results


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
