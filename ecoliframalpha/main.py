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
from config.config import get_config


#Set default configuration



def main():

    config = get_config()

    # Step 1: Fetch user inputs
    user_inputs = get_user_inputs()

    # Step 2: Ensure output path exists
    ensure_output_directory(config["output_path"])
    if config["input_path"]: ensure_output_directory(config["input_path"]) 

    # Step 3: Initialize the simulation environment
    print("Initializing simulation...")
    simulation_data = initialize_simulation(
        num_cycles=user_inputs["num_cycles"],
        nutrient_levels=user_inputs["nutrient_levels"],
        robust_codons=user_inputs["robust_codons"],
        sensitive_codons=user_inputs["sensitive_codons"],
    )

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
    rna_results = process_rna(stressed_results, simulation_data["codon_efficiency"], config["rnase_activity"], config["decay_variability"])
    
    # Step 7: Analyze codon variability
    print("Analyzing codon variability...")
    variability_results = analyze_variability(rna_results, metrics=config["metrics"])
    # Save variability results to CSV
    save_to_csv(variability_results, "variability_metrics.csv", config["output_path"])

    # Step 8: Validate simulation outputs
    print("Validating simulation outputs...")
    experimental_data = pd.DataFrame({
        "codon": user_inputs["robust_codons"] + user_inputs["sensitive_codons"],
        "variance": np.random.uniform(0.002, 0.01, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "Fano_factor": np.random.uniform(0.2, 1.0, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "CV": np.random.uniform(0.05, 0.15, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
        "CRI": np.random.uniform(1.0, 5.0, len(user_inputs["robust_codons"] + user_inputs["sensitive_codons"])),
    })
    validation_results = validate_simulation(variability_results, experimental_data, config["metrics"])
    # Save validation results to JSON
    save_to_json(validation_results, "validation_results.json", config["output_path"])

    # Step 9: Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(variability_results, stressed_results, validation_results, config["output_path"])
    
    # Step 10: Generate and save simulation summary
    print("Generating simulation summary...")
    summary = generate_summary(variability_results, validation_results)
    save_summary_to_file(summary, "simulation_summary.txt", config["output_path"])
    print("Simulation completed! Results saved in:", config["output_path"])
if __name__ == "__main__":
    main()
