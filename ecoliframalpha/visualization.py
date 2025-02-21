import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_visualizations(variability_results, stressed_results, validation_results, output_path="results/"):
    """
    Generates visualizations for codon variability, nutrient stress, and validation results.

    Parameters:
        variability_results (pd.DataFrame): DataFrame containing variability metrics for each codon.
        stressed_results (pd.DataFrame): DataFrame containing translation efficiencies and nutrient levels.
        validation_results (dict): Dictionary containing validation metrics.
        output_path (str): Path to save the generated visualizations.
    """
    # Ensure output directory exists
    os.makedirs(output_path, exist_ok=True)

    if stressed_results.empty or variability_results.empty:
        raise ValueError("One or more input DataFrames are empty.")

    # Ensure necessary columns exist in stressed_results
    if "nutrient_levels" not in stressed_results.columns:
        raise ValueError("Missing 'nutrient_levels' column in stressed_results DataFrame.")

    # Ensure variability_results has at least 'codon' column
    if "codon" not in variability_results.columns:
        raise ValueError("Missing 'codon' column in variability_results DataFrame.")

    # Skip visualization if DataFrames are empty
    if stressed_results.empty or variability_results.empty:
        print("Skipping visualization: Input DataFrames are empty.")
        return

    # Smooth data (handle NaN values)
    for codon in [col.replace("_efficiency", "") for col in stressed_results.columns if "_efficiency" in col]:
        stressed_results[f"{codon}_efficiency_smooth"] = (
            stressed_results[f"{codon}_efficiency"].rolling(window=10).mean().bfill()
        )

    # Subset data for visualization
    subset = stressed_results.head(min(200, len(stressed_results)))

    # 1. Plot smoothed codon efficiencies
    plt.figure(figsize=(12, 6))
    for codon in ["AAA", "GAT", "CGT", "CTG"]:
        if f"{codon}_efficiency_smooth" in subset.columns:
            plt.plot(subset.index, subset[f"{codon}_efficiency_smooth"], label=codon, alpha=0.8)
    plt.title("Codon Translation Efficiencies Across Cycles")
    plt.xlabel("Cycle")
    plt.ylabel("Translation Efficiency")
    plt.legend(title="Codons")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "codon_efficiencies_smoothed.png"))
    plt.close()

    # 2. Plot Nutrient Levels Across Cycles
    plt.figure(figsize=(12, 6))
    plt.plot(stressed_results.index, stressed_results["nutrient_levels"], color="green", alpha=0.8)
    plt.title("Nutrient Levels Across Cycles")
    plt.xlabel("Cycle")
    plt.ylabel("Nutrient Level")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "nutrient_levels.png"))
    plt.close()

    # 3. Bar Plot for Variability Metrics
    plt.figure(figsize=(12, 6))
    variability_long = variability_results.melt(id_vars=["codon"], var_name="Metric", value_name="Value")
    sns.barplot(x="codon", y="Value", hue="Metric", data=variability_long)
    plt.title("Codon Variability Metrics")
    plt.xlabel("Codon")
    plt.ylabel("Metric Value")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "variability_metrics.png"))
    plt.close()

    # 4. Scatter Plot for Validation (Simulated vs. Experimental)
    for metric, results in validation_results.items():
        if isinstance(results, dict) and "experimental_mean" in results and "simulated_mean" in results:
            plt.figure(figsize=(8, 6))
            experimental = results["experimental_mean"]
            simulated = results["simulated_mean"]
            plt.scatter(experimental, simulated, label=f"Metric: {metric}")
            plt.plot([min(experimental), max(experimental)], [min(experimental), max(experimental)], 
                     linestyle="--", color="red", label="Perfect Agreement")
            plt.title(f"Validation of {metric}")
            plt.xlabel("Experimental Data")
            plt.ylabel("Simulated Data")
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_path, f"validation_{metric}.png"))
            plt.close()

    print("All visualizations generated and saved in:", output_path)


if __name__ == "__main__":
    from initialization import initialize_simulation
    from translation_dynamics import simulate_translation
    from nutrient_stress import apply_nutrient_stress
    from rna_processing import process_rna
    from codon_variability import analyze_variability
    from validation import validate_simulation

    # Initialize and simulate
    initialization_results = initialize_simulation(
        num_cycles=1000,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        robust_codons=["AAA", "GAT"],
        sensitive_codons=["CGT", "CTG"],
    )
    translation_results = simulate_translation(initialization_results)
    stressed_results = apply_nutrient_stress(
        translation_results,
        nutrient_levels=[1.0, 0.75, 0.5, 0.25, 0.1],
        stress_probability=0.1,
        recovery_probability=0.05,
    )
    rna_results = process_rna(stressed_results, rnase_activity=0.05, decay_variability=0.1)
    variability_results = analyze_variability(rna_results)
    experimental_data = pd.DataFrame({
        "codon": ["AAA", "GAT", "CGT", "CTG"],
        "variance": [0.0026, 0.0031, 0.0079, 0.0098],
        "Fano_factor": [0.26, 0.31, 0.79, 0.98],
        "CV": [0.051, 0.061, 0.119, 0.141],
        "CRI": [4.1, 3.9, 1.6, 1.3],
    })
    validation_results = validate_simulation(variability_results, experimental_data)

    # Generate visualizations
    generate_visualizations(variability_results, stressed_results, validation_results)
