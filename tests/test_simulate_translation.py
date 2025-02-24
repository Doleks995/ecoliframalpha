import pandas as pd
import pytest
from ecoliframalpha.translation_dynamics import simulate_translation

def test_simulate_translation_basic():
    """Test basic translation simulation with valid data."""
    simulation_data = pd.DataFrame({"nutrient_level": [0.2, 0.5, 0.8]})
    codon_efficiency = {
        "AAA": {"base_efficiency": 1.0, "type": "robust"},
        "GGG": {"base_efficiency": 0.8, "type": "sensitive"},
    }
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    initialization_results = {"simulation_data": simulation_data, 
                              "codon_efficiency": codon_efficiency, 
                              "nutrient_levels": nutrient_levels
                              }

    result = simulate_translation(initialization_results)

    assert "AAA_efficiency" in result.columns
    assert "GGG_efficiency" in result.columns
    assert len(result) == len(simulation_data)  # Same number of rows

def test_simulate_translation_missing_keys():
    """Test error handling when required keys are missing."""
    with pytest.raises(ValueError, match="Missing required key"):
        simulate_translation({"simulation_data": pd.DataFrame()})  # Missing 'codon_efficiency'
        simulate_translation({"simulation_data": pd.DataFrame(), "codon_efficiency": {}})#'simulation_data' is empty
        simulate_translation({"simulation_data": pd.DataFrame({"random_column": [0.1, 0.2, 0.3]}), 
                              "codon_efficiency": {"AAA": {"base_efficiency": 1.0, "type": "robust"}}})#Missing 'nutrient_levels'
        simulate_translation({"simulation_data": pd.DataFrame({"nutrient_level": [0.2, 0.5, 0.8]}), 
                              "codon_efficiency": {"AAA": {"base_efficiency": 1.0}}})#Missing codon type
