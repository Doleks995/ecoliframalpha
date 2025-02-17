import os
import numpy as np
import pandas as pd
import json

def ensure_output_directory(path):
    """
    Ensures that the output directory exists. If not, creates it.
    Parameters:
        path (str): Path to the output directory.
    """
    if not os.path.exists(path):
        os.makedirs(path)
def save_to_csv(dataframe, filename, output_path="results/"):
    """
    Saves a DataFrame to a CSV file.
    Parameters:
        dataframe (pd.DataFrame): DataFrame to save.
        filename (str): Name of the file to save.
        output_path (str): Path to the directory where the file will be saved.
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)
    dataframe.to_csv(file_path, index=False)
    print(f"Data saved to: {file_path}")
def save_to_json(data, filename, output_path="results/"):
    """
    Saves a dictionary to a JSON file.
    Parameters:
        data (dict): Dictionary to save.
        filename (str): Name of the file to save.
        output_path (str): Path to the directory where the file will be saved.
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"JSON results saved to: {file_path}")
    
def normalize_data(series):
    """
    Normalizes a pandas Series to a range of [0, 1].
    Parameters:
        series (pd.Series): The data series to normalize.
    Returns:
        pd.Series: Normalized data.
    """
    return (series - series.min()) / (series.max() - series.min())

def generate_summary(variability_results, validation_results):
    """
    Generates a textual summary of simulation results.
    Parameters:
        variability_results (pd.DataFrame): DataFrame containing variability metrics.
        validation_results (dict): Dictionary with validation metrics.
    Returns:
        str: Summary of the simulation results.
    """
    summary = []
    summary.append("### Simulation Summary ###\n")
    summary.append("Variability Metrics (Mean Values):\n")
    for metric in ["variance", "Fano_factor", "CV", "CRI"]:
        if metric in variability_results.columns:
            mean_value = variability_results[metric].mean()
            summary.append(f"- {metric}: {mean_value:.4f}")
    summary.append("\nValidation Results:\n")
    for metric, results in validation_results.items():
        if isinstance(results, dict):
            summary.append(f"- {metric}: Correlation = {results['correlation']:.4f}, MSE = {results['mean_squared_error']:.6f}")
    return "\n".join(summary)
def save_summary_to_file(summary, filename="simulation_summary.txt", output_path="results/"):
    """
    Saves a simulation summary to a text file.
    Parameters:
        summary (str): Summary text to save.
        filename (str): Name of the file.
        output_path (str): Path to the directory where the file will be saved.
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)
    with open(file_path, "w") as file:
        file.write(summary)
    print(f"Summary saved to: {file_path}")
if __name__ == "__main__":
    from utils import (
        save_to_csv,
        save_to_json,
        normalize_data,
        generate_summary,
        save_summary_to_file,
    )
    import pandas as pd
    # Example Data
    variability_results = pd.DataFrame({
        "codon": ["AAA", "GAT", "CGT", "CTG"],
        "variance": [0.0026, 0.0031, 0.0079, 0.0098],
        "Fano_factor": [0.26, 0.31, 0.79, 0.98],
        "CV": [0.051, 0.061, 0.119, 0.141],
        "CRI": [4.1, 3.9, 1.6, 1.3],
    })
    validation_results = {
        "variance": {
            "correlation": 0.98,
            "mean_squared_error": 0.00001,
            "simulated_mean": 0.00275,
            "experimental_mean": 0.00285,
        },
        "Fano_factor": {
            "correlation": 0.95,
            "mean_squared_error": 0.00002,
            "simulated_mean": 0.35,
            "experimental_mean": 0.36,
        },
    }
    # Save results
    save_to_csv(variability_results, "variability_metrics.csv")
    save_to_json(validation_results, "validation_results.json")
    # Normalize data and generate summary
    normalized_variance = normalize_data(variability_results["variance"])
    variability_results["normalized_variance"] = normalized_variance
    summary = generate_summary(variability_results, validation_results)
    print(summary)
    # Save summary to file
    save_summary_to_file(summary)
