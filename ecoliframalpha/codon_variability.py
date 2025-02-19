import numpy as np
import pandas as pd

def analyze_variability(rna_results, metrics=["variance", "Fano_factor", "CV", "CRI"]):
    """
    Analyzes codon-specific variability in translation efficiency.

    Parameters:
        rna_results (pd.DataFrame): DataFrame containing translation efficiencies for each codon across cycles.
        metrics (list): List of metrics to calculate (options: "variance", "Fano_factor", "CV", "CRI").

    Returns:
        pd.DataFrame: A summary DataFrame with variability metrics for each codon.
    """
    # Validate input
    if rna_results.empty:
        return pd.DataFrame(columns=["codon"] + metrics)  # Return empty DataFrame with correct columns

    # Extract codons from the DataFrame columns
    codons = [col.replace("_efficiency", "") for col in rna_results.columns if "_efficiency" in col]

    if not codons:  # No efficiency columns found
        return pd.DataFrame(columns=["codon"] + metrics)

    # Initialize results dictionary
    variability_results = {metric: [] for metric in metrics}
    variability_results["codon"] = []

    # Loop through each codon and calculate metrics
    for codon in codons:
        efficiencies = rna_results[f"{codon}_efficiency"].dropna()  # Remove NaNs for calculations

        if efficiencies.empty:
            # If all values are NaN, store NaN for each requested metric
            variability_results["codon"].append(codon)
            for metric in metrics:
                variability_results[metric].append(np.nan)
            continue  # Skip to the next codon

        mean_efficiency = np.mean(efficiencies)
        variance = np.var(efficiencies, ddof=1)  # Use sample variance
        fano_factor = variance / mean_efficiency if mean_efficiency > 0 else np.nan
        cv = np.std(efficiencies, ddof=1) / mean_efficiency if mean_efficiency > 0 else np.nan
        cri = mean_efficiency / (np.max(efficiencies) - np.min(efficiencies)) if np.max(efficiencies) > np.min(efficiencies) else np.nan

        # Append results for the current codon
        variability_results["codon"].append(codon)
        if "variance" in metrics:
            variability_results["variance"].append(variance)
        if "Fano_factor" in metrics:
            variability_results["Fano_factor"].append(fano_factor)
        if "CV" in metrics:
            variability_results["CV"].append(cv)
        if "CRI" in metrics:
            variability_results["CRI"].append(cri)

    # Convert results dictionary to DataFrame
    return pd.DataFrame(variability_results)


if __name__ == "__main__":
    from initialization import initialize_simulation
    from translation_dynamics import simulate_translation
    from nutrient_stress import apply_nutrient_stress
    from rna_processing import process_rna

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

    # Process RNA stability and degradation
    rna_results = process_rna(stressed_results, rnase_activity=0.05, decay_variability=0.1)

    # Analyze codon variability
    variability_results = analyze_variability(rna_results, metrics=["variance", "Fano_factor", "CV", "CRI"])

    # Display results
    print(variability_results)

