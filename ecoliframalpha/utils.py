import os
import numpy as np
import pandas as pd
import json

def ensure_output_directory(path):
    """
    Ensures that the output directory exists. If it does not exist, it creates it.

    Parameters:
        path (str): Path to the output directory.

    Returns:
        bool: True if the directory was created, False if it already existed.

    Raises:
        OSError: If the directory cannot be created due to permission issues.
    """
    try:
        os.makedirs(path, exist_ok=True)  # Prevent race conditions
        return os.path.exists(path)  # True if created, False if already existed
    except OSError as e:
        print(f"Error: Unable to create directory '{path}': {e}")
        raise  # Re-raise the error for better debugging

def save_to_csv(dataframe, filename, output_path="results/"):
    """
    Saves a DataFrame to a CSV file.

    Parameters:
        dataframe (pd.DataFrame): DataFrame to save.
        filename (str): Name of the file.
        output_path (str): Path to save the file.

    Example:
        >>> df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
        >>> save_to_csv(df, "output.csv")
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)

    try:
        dataframe.to_csv(file_path, index=False)
        print(f"CSV saved to: {file_path}")
    except Exception as e:
        print(f"Failed to save CSV to {file_path}: {e}")
        raise

def save_to_json(data, filename, output_path="results/"):
    """
    Saves a dictionary to a JSON file.

    Parameters:
        data (dict): Dictionary to save.
        filename (str): Name of the file.
        output_path (str): Path to save the file.

    Example:
        >>> data = {"key": "value"}
        >>> save_to_json(data, "output.json")
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)

    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)
        print(f"JSON saved to: {file_path}")
    except Exception as e:
        print(f"Failed to save JSON to {file_path}: {e}")
        raise

def normalize_data(series):
    """
    Normalizes a pandas Series to a range of [0, 1].
    
    Parameters:
        series (pd.Series): Data series to normalize.

    Returns:
        pd.Series: Normalized data.

    Example:
        >>> s = pd.Series([10, 20, 30])
        >>> normalize_data(s)
    """
    if series.empty:
        print("Normalization attempted on an empty series.")
        return series

    min_val, max_val = series.min(), series.max()

    if min_val == max_val:
        return pd.Series(0, index=series.index)  # Return all zeros if no variation

    return (series - min_val) / (max_val - min_val)

def generate_summary(variability_results, validation_results):
    """
    Generates a textual summary of simulation results.

    Parameters:
        variability_results (pd.DataFrame): DataFrame containing variability metrics.
        validation_results (dict): Dictionary with validation metrics.

    Returns:
        str: Summary of the simulation results.

    Example:
        >>> df = pd.DataFrame({"variance": [0.1, 0.2]})
        >>> generate_summary(df, {"accuracy": 0.95})
    """
    summary = ["### Simulation Summary ###\n"]

    # Variability Results
    if not variability_results.empty:
        summary.append("Variability Metrics (Mean Values):")
        for metric in ["variance", "Fano_factor", "CV", "CRI"]:
            mean_value = variability_results[metric].mean() if metric in variability_results.columns else None
            summary.append(f"- {metric}: {mean_value:.4f}" if mean_value is not None else f"- {metric}: (Not available)")
    else:
        summary.append("No variability results available.")

    # Validation Results
    if validation_results:
        summary.append("\nValidation Metrics:")
        for key, value in validation_results.items():
            summary.append(f"- {key}: {value}")
    else:
        summary.append("\nNo validation results available.")

    return "\n".join(summary)

def save_summary_to_file(summary, filename="simulation_summary.txt", output_path="results/"):
    """
    Saves a simulation summary to a text file.

    Parameters:
        summary (str): Summary text to save.
        filename (str): Name of the file.
        output_path (str): Path to save the file.

    Example:
        >>> summary = "Simulation completed successfully."
        >>> save_summary_to_file(summary, "summary.txt")
    """
    ensure_output_directory(output_path)
    file_path = os.path.join(output_path, filename)

    try:
        with open(file_path, "w") as file:
            file.write(summary)
        print(f"Summary saved to: {file_path}")
        return file_path
    except Exception as e:
        print(f"Failed to save summary to {file_path}: {e}")
        raise
