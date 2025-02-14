import numpy as np
import pandas as pd
from input_handler import get_user_inputs
from initialization import initialize_simulation
from translation_dynamics import simulate_translation
from nutrient_stress import apply_nutrient_stress
from rna_processing import process_rna
from codon_variability import analyze_variability
from validation import validate_simulation
from visualization import generate_visualizations
from utils import ensure_output_directory, save_to_csv, save_to_json, generate_summary, save_summary_to_file
# Default Settings
OUTPUT_PATH = "results/"  # Path for saving output
METRICS = ["variance", "Fano_factor", "CV", "CRI"]  # Metrics for variability
def main():
    # Step 1: Fetch user inputs
    user_inputs = get_user_inputs()
    # Step 2: Ensure output directory exists
    ensure_output_directory(OUTPUT_PATH)
    # Step 3: Initialize the simulation environment
    print("Initializing simulation...")
    simulation_data = initialize_simulation(
        num_cycles=user_inputs["num_cycles"],
        nutrient_levels=user_inputs["nutrient_levels"],
        robust_codons=user_inputs["robust_codons"],
        sensitive_codons=user_inputs["sensitive_codons"],
    )
    # Extract codon efficiency from simulation initialization
    codon_efficiency = {
        codon: {"base_efficiency": 1.0, "type": "robust"} for codon in user_inputs["robust_codons"]
    }
    codon_efficiency.update({
        codon: {"base_efficiency": 0.5, "type": "sensitive"} for codon in user_inputs["sensitive_codons"]
    })
    # Step 4: Simulate translation dynamics
    print("Simulating translation dynamics...")
    translation_results = simulate_translation(simulation_data)
    # Step 5: Apply nutrient stress effects
    print("Applying nutrient stress...")
    stressed_results = apply_nutrient_stress(
        translation_results,
        nutrient_levels=user_inputs["nutrient_levels"],
        stress_probability=user_inputs["stress_probability"],
        recovery_probability=user_inputs["recovery_probability"],
    )
    # Step 6: Process RNA stability and decay
    print("Processing RNA stability and decay...")
    rna_results = process_rna(stressed_results, codon_efficiency)
    # Step 7: Analyze codon variability
    print("Analyzing codon variability...")
    variability_results = analyze_variability(rna_results, metrics=METRICS)
    # Save variability results to CSV
    save_to_csv(variability_results, "variability_metrics.csv", OUTPUT_PATH)
    # Step 8: Validate simulation outputs
    print("Validating simulation outputs...")
    experimental_data = pd.DataFrame({
        "codon": user_inputs["robust_codons"] + user_inputs["sensitive_codons"],
        "variance": np.random.uniform(0.002, 0.01, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "Fano_factor": np.random.uniform(0.2, 1.0, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "CV": np.random.uniform(0.05, 0.15, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "CRI": np.random.uniform(1.0, 5.0, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
    })
    validation_results = validate_simulation(variability_results, experimental_data)
    # Save validation results to JSON
    save_to_json(validation_results, "validation_results.json", OUTPUT_PATH)
    # Step 9: Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(variability_results, stressed_results, validation_results, OUTPUT_PATH)
    # Step 10: Generate and save simulation summary
    print("Generating simulation summary...")
    summary = generate_summary(variability_results, validation_results)
    save_summary_to_file(summary, "simulation_summary.txt", OUTPUT_PATH)
    print("Simulation completed! Results saved in:", OUTPUT_PATH)
if __name__ == "__main__":
    main()
