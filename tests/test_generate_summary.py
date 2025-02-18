import pandas as pd
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ecoliframalpha.utils import generate_summary

def test_generate_summary_basic():
    """Test basic summary generation with valid data."""
    variability_results = pd.DataFrame({
        "variance": [1.2, 1.8, 2.5],
        "Fano_factor": [0.3, 0.4, 0.5],
        "CV": [0.2, 0.3, 0.4],
        "CRI": [0.9, 1.1, 1.3]
    })
    validation_results = {"accuracy": 0.95, "precision": 0.88}
    summary = generate_summary(variability_results, validation_results)
    assert "### Simulation Summary ###" in summary
    assert "- variance: 1.8333" in summary  # Mean of [1.2, 1.8, 2.5]
    assert "- accuracy: 0.95" in summary
    assert "- precision: 0.88" in summary

def test_generate_summary_missing_metrics():
    """Test when some metrics are missing from variability_results."""
    variability_results = pd.DataFrame({"variance": [1.5, 2.0]})
    validation_results = {}
    summary = generate_summary(variability_results, validation_results)
    assert "- variance: 1.7500" in summary
    assert "- Fano_factor: (Not available)" in summary
    assert "No validation results available." in summary

def test_generate_summary_empty_variability():
    """Test summary when variability_results is empty."""
    variability_results = pd.DataFrame()
    validation_results = {"recall": 0.82}
    summary = generate_summary(variability_results, validation_results)
    assert "No variability results available." in summary
    assert "- recall: 0.82" in summary

def test_generate_summary_empty_inputs():
    """Test summary when both inputs are empty."""
    variability_results = pd.DataFrame()
    validation_results = {}
    summary = generate_summary(variability_results, validation_results)
    assert "No variability results available." in summary
    assert "No validation results available." in summary
