import numpy as np
import pandas as pd
from ecoliframalpha.codon_variability import analyze_variability

def test_analyze_variability_basic():
    """Test basic variability analysis with valid data."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [0.8, 0.9, 1.0],
        "GGG_efficiency": [0.6, 0.7, 0.8]
    })

    result = analyze_variability(rna_results)

    assert "codon" in result.columns
    assert "variance" in result.columns
    assert len(result) == 2  # Two codons analyzed
    assert set(result["codon"]) == {"AAA", "GGG"}

def test_analyze_variability_empty_dataframe():
    """Test function with an empty DataFrame."""
    rna_results = pd.DataFrame()

    result = analyze_variability(rna_results)

    assert result.empty  # Should return an empty DataFrame
    assert all(item in list(result.columns) for item in ["codon", "variance", "Fano_factor", "CV", "CRI"])

def test_analyze_variability_no_efficiency_columns():
    """Test function when there are no '_efficiency' columns."""
    rna_results = pd.DataFrame({
        "random_column": [1, 2, 3]
    })

    result = analyze_variability(rna_results)

    assert result.empty  # No valid codons, should return empty DataFrame

def test_analyze_variability_nan_values():
    """Test function when codon efficiencies contain NaNs."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [np.nan, np.nan, np.nan],  # All NaN
        "GGG_efficiency": [0.6, 0.7, np.nan]  # Some NaN
    })

    result = analyze_variability(rna_results)

    assert result[result["codon"] == "AAA"]["variance"].isna().all()  # Should be NaN
    assert not result[result["codon"] == "GGG"]["variance"].isna().all()  # Should compute normally

def test_analyze_variability_single_codon():
    """Test function with a single codon."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [0.5, 0.7, 0.9, 1.0]
    })

    result = analyze_variability(rna_results)

    assert len(result) == 1  # Only one codon
    assert result["codon"].iloc[0] == "AAA"

def test_analyze_variability_requested_metrics():
    """Test function when specific metrics are requested."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [0.8, 0.9, 1.0]
    })

    result = analyze_variability(rna_results, metrics=["variance", "CV"])  # Request only two metrics

    assert "variance" in result.columns
    assert "CV" in result.columns
    assert "Fano_factor" not in result.columns
    assert "CRI" not in result.columns

def test_analyze_variability_all_zero_values():
    """Test function when codon efficiencies are all zero."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [0, 0, 0, 0]
    })

    result = analyze_variability(rna_results)

    assert result["Fano_factor"].isna().all()  # Should be NaN (mean is 0)
    assert result["CV"].isna().all()  # Should be NaN (mean is 0)
    assert result["CRI"].isna().all()  # Should be NaN (no variability)

def test_analyze_variability_high_variability():
    """Test function with high variability data."""
    rna_results = pd.DataFrame({
        "AAA_efficiency": [0.1, 0.9, 0.2, 0.8]
    })

    result = analyze_variability(rna_results)

    assert result["variance"].iloc[0] > 0  # Variance should be positive
    assert result["CV"].iloc[0] > 0  # CV should be positive
