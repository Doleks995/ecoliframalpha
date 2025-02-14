import numpy as np
import pandas as pd

def process_rna(stressed_results, codon_efficiency, rnase_activity=0.05, decay_variability=0.1):
    """
    Processes RNA stability and decay based on codon efficiency.

    Parameters:
        stressed_results (pd.DataFrame): Dataframe with codon efficiencies and nutrient levels.
        codon_efficiency (dict): Codon efficiency data from initialization.
        rnase_activity (float): Baseline RNA degradation rate.
        decay_variability (float): Variability in RNA degradation.

    Returns:
        pd.DataFrame: Updated dataframe with RNA stability accounted for.
    """
    # Calculate decay rates based on codon efficiency
    for codon, properties in codon_efficiency.items():
        base_decay_rate = rnase_activity * (1 + decay_variability * (1 - properties["base_efficiency"]))
        
        # Apply RNA processing effects directly to the DataFrame
        stressed_results[f"{codon}_efficiency"] *= (
            1 - base_decay_rate - stressed_results["nutrient_level"] * decay_variability
        )
        
        # Clip efficiencies to ensure non-negative values
        stressed_results[f"{codon}_efficiency"] = stressed_results[f"{codon}_efficiency"].clip(lower=0)

    return stressed_results


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
