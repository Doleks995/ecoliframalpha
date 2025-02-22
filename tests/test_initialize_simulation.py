import numpy as np
import pandas as pd
from ecoliframalpha.initialization import initialize_simulation 

def test_initialize_simulation_basic():
    """Test that the function correctly initializes simulation parameters."""
    num_cycles = 100
    nutrient_levels = [1.0, 0.75, 0.5]
    robust_codons = ["AAA", "GAT"]
    sensitive_codons = ["CGT", "CTG"]
    result = initialize_simulation(num_cycles, nutrient_levels, robust_codons, sensitive_codons)
    assert result["num_cycles"] == num_cycles
    assert result["nutrient_levels"] == nutrient_levels
    assert isinstance(result["codon_efficiency"], dict)
    assert isinstance(result["simulation_data"], pd.DataFrame)
    # Check DataFrame structure
    assert set(result["simulation_data"].columns) == {"cycle", "nutrient_level", "AAA_efficiency", "GAT_efficiency", "CGT_efficiency", "CTG_efficiency"}
    assert len(result["simulation_data"]) == num_cycles  # Correct number of cycles

def test_initialize_simulation_codon_efficiency():
    """Test that codon efficiencies are assigned correctly."""
    robust_codons = ["AAA", "GAT"]
    sensitive_codons = ["CGT", "CTG"]
    result = initialize_simulation(10, [1.0], robust_codons, sensitive_codons)
    codon_efficiency = result["codon_efficiency"]
    for codon in robust_codons:
        assert codon in codon_efficiency
        assert codon_efficiency[codon]["base_efficiency"] == 1.0
        assert codon_efficiency[codon]["type"] == "robust"
    for codon in sensitive_codons:
        assert codon in codon_efficiency
        assert codon_efficiency[codon]["base_efficiency"] == 0.5
        assert codon_efficiency[codon]["type"] == "sensitive"

def test_initialize_simulation_empty_codons():
    """Test the function when there are no codons provided."""
    result = initialize_simulation(10, [1.0], [], [])
    assert result["codon_efficiency"] == {}  # No codons should be in the efficiency dict
    assert "AAA_efficiency" in result["simulation_data"].columns  # Columns still exist
    assert "CTG_efficiency" in result["simulation_data"].columns

def test_initialize_simulation_different_nutrient_levels():
    """Test that nutrient levels are assigned correctly in the simulation."""
    nutrient_levels = [0.9, 0.8, 0.7, 0.6]
    result = initialize_simulation(50, nutrient_levels, ["AAA"], ["CGT"])
    assert set(result["simulation_data"]["nutrient_level"].unique()).issubset(nutrient_levels)

def test_initialize_simulation_large_num_cycles():
    """Test handling of a large number of simulation cycles."""
    num_cycles = 10000  # Large number
    result = initialize_simulation(num_cycles, [1.0], ["AAA"], ["CGT"])
    assert len(result["simulation_data"]) == num_cycles
