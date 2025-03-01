import numpy as np
import pandas as pd
from ecoliframalpha.validation import validate_simulation

def test_validate_simulation_basic():
    """Test basic validation with simulated and experimental data."""
    variability_results = pd.DataFrame({
        "variance": [0.1, 0.2, 0.3],
        "Fano_factor": [1.2, 1.3, 1.4]
    })
    experimental_data = pd.DataFrame({
        "variance": [0.15, 0.25, 0.35],
        "Fano_factor": [1.1, 1.2, 1.3]
    })
    result = validate_simulation(variability_results, experimental_data)
    assert "variance" in result
    assert "Fano_factor" in result
    assert isinstance(result["variance"], dict)  # Should return a dictionary
    assert "correlation" in result["variance"]
    assert "mean_squared_error" in result["variance"]

def test_validate_simulation_missing_metric():
    """Test handling of missing metrics in one dataset."""
    variability_results = pd.DataFrame({"variance": [0.1, 0.2, 0.3]})
    experimental_data = pd.DataFrame({"Fano_factor": [1.1, 1.2, 1.3]})  # No "variance"
    result = validate_simulation(variability_results, experimental_data, metrics=["variance"])  # Explicitly test "variance" only
    assert result["variance"] == "Metric variance missing in variability results or experimental data."
    assert "Fano_factor" not in result  # Not requested

def test_validate_simulation_nan_values():
    """Test handling of NaN values in metrics."""
    variability_results = pd.DataFrame({"variance": [np.nan, np.nan, np.nan]})
    experimental_data = pd.DataFrame({"variance": [0.1, 0.2, 0.3]})
    result = validate_simulation(variability_results, experimental_data)
    assert result["variance"] == "Not enough data points for correlation."

def test_validate_simulation_constant_values():
    """Test handling of constant values in a dataset."""
    variability_results = pd.DataFrame({"variance": [0.5, 0.5, 0.5]})
    experimental_data = pd.DataFrame({"variance": [0.1, 0.2, 0.3]})

    result = validate_simulation(variability_results, experimental_data)

    assert result["variance"] == "Constant input detected."

def test_validate_simulation_single_data_point():
    """Test handling of a single data point in a dataset."""
    variability_results = pd.DataFrame({"variance": [0.2]})
    experimental_data = pd.DataFrame({"variance": [0.25]})

    result = validate_simulation(variability_results, experimental_data)

    assert result["variance"] == "Not enough data points for correlation."

def test_validate_simulation_partial_nan_values():
    """Test handling of partial NaN values (some valid data)."""
    variability_results = pd.DataFrame({"variance": [0.1, np.nan, 0.3, 0.4]})
    experimental_data = pd.DataFrame({"variance": [0.15, 0.25, np.nan, 0.25]})

    result = validate_simulation(variability_results, experimental_data)

    assert "variance" in result  # Ensure the key exists

    if isinstance(result["variance"], dict):
        assert "correlation" in result["variance"]
        assert "mean_squared_error" in result["variance"]
    else:
        assert result["variance"] == "NaN values detected in all entries."


def test_validate_simulation_all_metrics():
    """Test function when validating all available metrics."""
    variability_results = pd.DataFrame({
        "variance": [0.1, 0.2, 0.3],
        "Fano_factor": [1.2, 1.3, 1.4],
        "CV": [0.5, 0.6, 0.7],
        "CRI": [0.8, 0.9, 1.0]
    })
    experimental_data = pd.DataFrame({
        "variance": [0.15, 0.25, 0.35],
        "Fano_factor": [1.1, 1.2, 1.3],
        "CV": [0.4, 0.5, 0.6],
        "CRI": [0.7, 0.8, 0.9]
    })

    result = validate_simulation(variability_results, experimental_data)

    for metric in ["variance", "Fano_factor", "CV", "CRI"]:
        assert metric in result
        assert "correlation" in result[metric]
        assert "mean_squared_error" in result[metric]
