import numpy as np
import pandas as pd
from scipy.stats import pearsonr
from sklearn.metrics import mean_squared_error

def validate_simulation(variability_results, experimental_data, metrics=["variance", "Fano_factor", "CV", "CRI"]):
    """
    Validates simulation results against experimental data.

    Parameters:
        variability_results (pd.DataFrame): DataFrame containing variability metrics for each codon.
        experimental_data (pd.DataFrame): DataFrame containing experimental benchmarks for the same codons.
        metrics (list): List of metrics to validate (options: "variance", "Fano_factor", "CV", "CRI").

    Returns:
        dict: A dictionary summarizing validation results, including correlation coefficients and errors.
    """
    validation_results = {}

    for metric in metrics:
        if metric in variability_results.columns and metric in experimental_data.columns:
            # Extract simulated and experimental values for the metric
            simulated = variability_results[metric].values
            experimental = experimental_data[metric].values

            # Check for NaN values
            if np.any(np.isnan(simulated)) or np.any(np.isnan(experimental)):
                print(f"Warning: Metric '{metric}' contains NaN values. Skipping validation for this metric.")
                validation_results[metric] = "NaN values detected."
                continue

            # Check for constant arrays
            if np.all(simulated == simulated[0]) or np.all(experimental == experimental[0]):
                print(f"Warning: Metric '{metric}' is constant in one or both datasets. Skipping correlation.")
                validation_results[metric] = "Constant input detected."
                continue

            # Calculate Pearson correlation coefficient
            correlation, _ = pearsonr(simulated, experimental)

            # Calculate mean squared error (MSE)
            mse = mean_squared_error(experimental, simulated)

            # Store validation results
            validation_results[metric] = {
                "correlation": correlation,
                "mean_squared_error": mse,
                "simulated_mean": np.mean(simulated),
                "experimental_mean": np.mean(experimental),
            }
        else:
            # Handle missing metrics
            validation_results[metric] = "Metric not found in both datasets."
            print(f"Warning: Metric '{metric}' missing in one of the datasets.")

    return validation_results

if __name__ == "__main__":
    from initialization import initialize_simulation
    from translation_dynamics import simulate_translation
    from nutrient_stress import apply_nutrient_stress
    from rna_processing import process_rna
    from codon_variability import analyze_variability

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
    rna_results = process_rna(
        stressed_results,
        codon_efficiency=initialization_results["codon_efficiency"],
        rnase_activity=0.05,
        decay_variability=0.1,
    )

    # Analyze codon variability
    variability_results = analyze_variability(rna_results, metrics=["variance", "Fano_factor", "CV", "CRI"])

    # Experimental benchmarks
    experimental_data = pd.DataFrame({
        "codon": ["AAA", "GAT", "CGT", "CTG"],
        "variance": [0.0026, 0.0031, 0.0079, 0.0098],
        "Fano_factor": [0.26, 0.31, 0.79, 0.98],
        "CV": [0.051, 0.061, 0.119, 0.141],
        "CRI": [4.1, 3.9, 1.6, 1.3],
    })

    # Validate simulation
    validation_results = validate_simulation(variability_results, experimental_data)

    # Display validation results
    for metric, result in validation_results.items():
        print(f"Validation for {metric}:")
        print(result)
        print()
