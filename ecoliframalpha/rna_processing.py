import numpy as np
import pandas as pd

def process_rna(stressed_results, codon_efficiency, rnase_activity=0.05, decay_variability=0.1):
    """
    Processes RNA stability and decay based on codon efficiency.

    Parameters:
        stressed_results (pd.DataFrame): Dataframe with codon efficiencies and nutrient levels.
        codon_efficiency (dict): Codon efficiency data from initialization.
        rnase_activity (float): Baseline RNA degradation rate (0 ≤ rnase_activity ≤ 1).
        decay_variability (float): Variability in RNA degradation.

    Returns:
        pd.DataFrame: Updated dataframe with RNA stability accounted for.
    """
    if stressed_results.empty:
        raise ValueError("Empty dataset provided to process_rna().")
    #Ensure required column exists
    if "nutrient_levels" not in stressed_results.columns:
        raise ValueError("Missing required column: 'nutrient_levels'")

    # Validate parameters
    if not (0 <= rnase_activity <= 1):
        raise ValueError("rnase_activity must be between 0 and 1.")

    if not (0 <= decay_variability <= 1):
        raise ValueError("decay_variability must be between 0 and 1.")

    # Copy the DataFrame to avoid modifying the original
    updated_results = stressed_results.copy()

    # Calculate decay rates based on codon efficiency
    for codon, properties in codon_efficiency.items():
        if "base_efficiency" not in properties:
            raise ValueError(f"Missing 'base_efficiency' for codon: {codon}")

        codon_column = f"{codon}_efficiency"

        # Ensure the codon efficiency column exists
        if codon_column not in updated_results.columns:
            raise KeyError(f"Column '{codon_column}' missing in stressed_results.")

        # Compute RNA degradation using an exponential decay model
        base_decay_rate = rnase_activity * (1 + decay_variability * (1 - properties["base_efficiency"]))
        decay_factor = np.exp(-base_decay_rate * (1 + updated_results["nutrient_levels"] * decay_variability))

        # Apply decay but prevent values from becoming negative
        updated_results[codon_column] *= decay_factor
        updated_results[codon_column] = updated_results[codon_column].clip(lower=0)

    return updated_results




if __name__ == "__main__":
    from initialization import initialize_simulation
    from translation_dynamics import simulate_translation
    from nutrient_stress import apply_nutrient_stress

    # Example initialization
    num_cycles = 1000
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]
    robust_codons = ["AAA", "GAT"]
    sensitive_codons = ["CGT", "CTG"]

    # Initialize simulation
    initialization_results = initialize_simulation(
        num_cycles=num_cycles,
        nutrient_levels=nutrient_levels,
        robust_codons=robust_codons,
        sensitive_codons=sensitive_codons,
    )
    codon_efficiency = {
        codon: {"base_efficiency": 1.0, "type": "robust"} for codon in robust_codons
    }
    codon_efficiency.update({
        codon: {"base_efficiency": 0.5, "type": "sensitive"} for codon in sensitive_codons
    })

    # Simulate translation dynamics
    translation_results = simulate_translation(initialization_results)

    # Apply nutrient stress
    stressed_results = apply_nutrient_stress(
        translation_results,
        nutrient_levels=nutrient_levels,
        stress_probability=0.1,
        recovery_probability=0.05,
    )

    # Process RNA stability and degradation
    rna_results = process_rna(stressed_results, codon_efficiency, rnase_activity=0.05, decay_variability=0.1)

    # Display updated results
    print(rna_results.head())
