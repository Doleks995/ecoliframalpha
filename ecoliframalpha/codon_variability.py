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
    # Define valid metrics
    valid_metrics = {"variance", "Fano_factor", "CV", "CRI"}
    
    # Validate `metrics` input
    metrics = set(metrics) & valid_metrics  # Remove any invalid metrics
    if not metrics:
        raise ValueError(f"Metrics must be chosen from {valid_metrics}")

    # Return empty DataFrame if input is empty
    if rna_results.empty:
        return pd.DataFrame(columns=["codon"] + list(metrics))  

    # Extract codons from DataFrame columns
    codons = [col.replace("_efficiency", "") for col in rna_results.columns if col.endswith("_efficiency")]
    if not codons:
        return pd.DataFrame(columns=["codon"] + list(metrics))  # Return early if no efficiency columns

    # Use a list of dictionaries for efficiency
    results = []

    # Loop through each codon and calculate metrics
    for codon in codons:
        efficiencies = rna_results[f"{codon}_efficiency"].dropna()  # Remove NaNs for calculations

        # Store results for this codon
        codon_data = {"codon": codon}

        if efficiencies.empty:
            # Store NaN if all values are missing
            for metric in metrics:
                codon_data[metric] = np.nan
        else:
            # Compute required values
            mean_efficiency = efficiencies.mean()
            variance = efficiencies.var(ddof=1)  # Sample variance
            std_dev = efficiencies.std(ddof=1)  # Sample standard deviation
            max_val = efficiencies.max()
            min_val = efficiencies.min()
            range_val = max_val - min_val if max_val > min_val else np.nan

            # Store only requested metrics
            if "variance" in metrics:
                codon_data["variance"] = variance
            if "Fano_factor" in metrics:
                codon_data["Fano_factor"] = variance / mean_efficiency if mean_efficiency > 0 else np.nan
            if "CV" in metrics:
                codon_data["CV"] = std_dev / mean_efficiency if mean_efficiency > 0 else np.nan
            if "CRI" in metrics:
                codon_data["CRI"] = mean_efficiency / range_val if range_val > 0 else np.nan

        results.append(codon_data)

    # Convert list of dictionaries to DataFrame
    return pd.DataFrame(results, columns=["codon"] + list(metrics))

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
    rna_results = process_rna(stressed_results, initialization_results["codon_efficiency"], rnase_activity=0.05, decay_variability=0.1)

    # Analyze codon variability
    variability_results = analyze_variability(rna_results, metrics=["variance", "Fano_factor", "CV", "CRI"])

    # Display results
    print(variability_results)

