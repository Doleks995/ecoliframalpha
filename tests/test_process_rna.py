import pandas as pd
import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ecoliframalpha.rna_processing import process_rna  

def test_process_rna_basic():
    """Test RNA decay processing under normal conditions."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6]
    })
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    result = process_rna(stressed_results, codon_efficiency)

    assert "AAA_efficiency" in result.columns
    assert len(result) == len(stressed_results)
    assert (result["AAA_efficiency"] <= 1.0).all()  # Efficiency should not increase

def test_process_rna_empty_dataframe():
    """Test handling of an empty DataFrame."""
    stressed_results = pd.DataFrame()
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    with pytest.raises(ValueError, match="Empty dataset"):
        result = process_rna(stressed_results, codon_efficiency)


def test_process_rna_missing_nutrient_column():
    """Test handling when 'nutrient_level' column is missing."""
    stressed_results = pd.DataFrame({"AAA_efficiency": [1.0, 0.8, 0.6]})
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    with pytest.raises(ValueError, match="Missing required column: 'nutrient_level'"):
        process_rna(stressed_results, codon_efficiency)

def test_process_rna_missing_codon_efficiency():
    """Test handling when a codon is missing 'base_efficiency'."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6]
    })
    codon_efficiency = {"AAA": {}}  # Missing 'base_efficiency'

    with pytest.raises(ValueError, match="Missing 'base_efficiency' for codon: AAA"):
        process_rna(stressed_results, codon_efficiency)

def test_process_rna_rnase_activity_effect():
    """Test that increasing RNase activity leads to faster efficiency decay."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6]
    })
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    result_low_rnase = process_rna(stressed_results, codon_efficiency, rnase_activity=0.01)
    result_high_rnase = process_rna(stressed_results, codon_efficiency, rnase_activity=0.1)

    assert (result_low_rnase["AAA_efficiency"] > result_high_rnase["AAA_efficiency"]).all()
    
def test_process_rna_decay_variability_effect():
    """Test that increasing decay variability leads to greater efficiency reduction."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6]
    })
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    result_low_variability = process_rna(stressed_results, codon_efficiency, decay_variability=0.01)
    result_high_variability = process_rna(stressed_results, codon_efficiency, decay_variability=0.2)

    assert (result_low_variability["AAA_efficiency"] > result_high_variability["AAA_efficiency"]).all()

def test_process_rna_multiple_codons():
    """Test RNA processing for multiple codons."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6],
        "GGG_efficiency": [0.9, 0.7, 0.5]
    })
    codon_efficiency = {
        "AAA": {"base_efficiency": 0.9},
        "GGG": {"base_efficiency": 0.8}
    }

    result = process_rna(stressed_results, codon_efficiency)

    assert "AAA_efficiency" in result.columns
    assert "GGG_efficiency" in result.columns
    assert (result["AAA_efficiency"] >= result["GGG_efficiency"]).all()

def test_process_rna_does_not_modify_original():
    """Ensure function does not modify the input DataFrame."""
    stressed_results = pd.DataFrame({
        "nutrient_level": [1.0, 0.5, 0.2],
        "AAA_efficiency": [1.0, 0.8, 0.6]
    })
    codon_efficiency = {"AAA": {"base_efficiency": 0.9}}

    original_copy = stressed_results.copy()
    process_rna(stressed_results, codon_efficiency)

    pd.testing.assert_frame_equal(stressed_results, original_copy)  # Ensure original is unchanged
