import numpy as np
import pandas as pd
import pytest
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

    # Check dynamically created efficiency columns
    expected_columns = {"cycle", "nutrient_level"}
    expected_columns.update({f"{codon}_efficiency" for codon in robust_codons + sensitive_codons})

    assert set(result["simulation_data"].columns) == expected_columns
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

    assert result["codon_efficiency"] == {}  # No codons in the efficiency dictionary
    assert "cycle" in result["simulation_data"].columns
    assert "nutrient_level" in result["simulation_data"].columns

def test_initialize_simulation_different_nutrient_levels():
    """Test that nutrient levels are assigned correctly in the simulation."""
    nutrient_levels = [0.9, 0.8, 0.7, 0.6]
    result = initialize_simulation(50, nutrient_levels, ["AAA"], ["CGT"])

    assert set(result["simulation_data"]["nutrient_level"].unique()).issubset(nutrient_levels)

def test_initialize_simulation_large_num_cycles():
    """Test handling of a large number of simulation cycles."""
    num_cycles = 10000  # Large number
    result = initialize_simulation(num_cycles, [1.0], ["AAA"], ["CGT"])

    assert len(result["simulation_data"]) == num_cycles  # Should match input size

def test_initialize_simulation_invalid_num_cycles():
    """Test that the function raises an error when num_cycles is invalid."""
    with pytest.raises(ValueError, match="num_cycles must be a positive integer"):
        initialize_simulation(-5, [1.0], ["AAA"], ["CGT"])

    with pytest.raises(ValueError, match="num_cycles must be a positive integer"):
        initialize_simulation(0, [1.0], ["AAA"], ["CGT"])

def test_initialize_simulation_invalid_nutrient_levels():
    """Test that the function raises an error when nutrient_levels are invalid."""
    with pytest.raises(ValueError, match="nutrient_levels must be a list of numbers"):
        initialize_simulation(10, "invalid", ["AAA"], ["CGT"])

    with pytest.raises(ValueError, match="nutrient_levels must be a list of numbers"):
        initialize_simulation(10, [1.0, "string"], ["AAA"], ["CGT"])

def test_initialize_simulation_invalid_codons():
    """Test that the function raises an error when codons are invalid."""
    with pytest.raises(ValueError, match="robust_codons must be a list of strings"):
        initialize_simulation(10, [1.0], "AAA,GAT", ["CGT"])

    with pytest.raises(ValueError, match="sensitive_codons must be a list of strings"):
        initialize_simulation(10, [1.0], ["AAA"], "CGT,CTG")

def test_initialize_simulation_no_cycles():
    """Test what happens when num_cycles is 1 (minimum case)."""
    result = initialize_simulation(1, [0.5], ["AAA"], ["CGT"])
    
    assert len(result["simulation_data"]) == 1
    assert result["simulation_data"]["cycle"].iloc[0] == 1  # Cycle should start at 1
