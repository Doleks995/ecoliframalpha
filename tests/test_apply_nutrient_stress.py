import numpy as np
import pandas as pd
import pytest
from ecoliframalpha.nutrient_stress import apply_nutrient_stress  

def test_apply_nutrient_stress_basic():
    """Test nutrient stress application with standard values."""
    np.random.seed(42)  # Fix seed for reproducibility

    translation_results = pd.DataFrame({"cycle": range(10)})
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    result = apply_nutrient_stress(translation_results, nutrient_levels)

    assert "nutrient_level" in result.columns
    assert len(result) == len(translation_results)  # Same number of rows
    assert result["nutrient_level"].isin(nutrient_levels).all()  # Valid levels only

def test_apply_nutrient_stress_empty_dataframe():
    """Test handling of an empty translation_results DataFrame."""
    translation_results = pd.DataFrame()
    nutrient_levels = [1.0, 0.75, 0.5]

    result = apply_nutrient_stress(translation_results, nutrient_levels)

    assert result.empty  # Should return an empty DataFrame

def test_apply_nutrient_stress_single_cycle():
    """Test behavior when there is only one cycle."""
    translation_results = pd.DataFrame({"cycle": [0]})
    nutrient_levels = [1.0, 0.5]

    result = apply_nutrient_stress(translation_results, nutrient_levels)

    assert len(result) == 1
    assert result["nutrient_level"].isin(nutrient_levels).all()

def test_apply_nutrient_stress_stress_dominates():
    """Test behavior when stress probability is 1 (always decreases)."""
    np.random.seed(42)
    
    translation_results = pd.DataFrame({"cycle": range(5)})
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    result = apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=1.0, recovery_probability=0.0)

    assert result["nutrient_level"].iloc[-1] == 0.1  # Should reach the lowest level

def test_apply_nutrient_stress_recovery_dominates():
    """Test behavior when recovery probability is 1 (always increases)."""
    np.random.seed(42)

    translation_results = pd.DataFrame({"cycle": range(5)})
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    result = apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=0.0, recovery_probability=1.0)

    assert result["nutrient_level"].iloc[-1] == 1.0  # Should stay at highest level

def test_apply_nutrient_stress_random_behavior():
    """Test that nutrient fluctuations follow the expected trend."""
    np.random.seed(42)

    translation_results = pd.DataFrame({"cycle": range(20)})
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    result = apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=0.3, recovery_probability=0.3)

    assert result["nutrient_level"].min() >= 0.1  # Should not go below min level
    assert result["nutrient_level"].max() <= 1.0  # Should not exceed max level

def test_apply_nutrient_stress_invalid_nutrient_levels():
    """Test function raises an error when nutrient_levels is invalid."""
    translation_results = pd.DataFrame({"cycle": range(5)})

    with pytest.raises(ValueError, match="nutrient_levels must be a non-empty list"):
        apply_nutrient_stress(translation_results, [])

    with pytest.raises(ValueError, match="nutrient_levels must be a non-empty list"):
        apply_nutrient_stress(translation_results, None)

def test_apply_nutrient_stress_does_not_modify_original():
    """Ensure function does not modify the input DataFrame."""
    translation_results = pd.DataFrame({"cycle": range(5)})
    nutrient_levels = [1.0, 0.75, 0.5]

    original_copy = translation_results.copy()
    apply_nutrient_stress(translation_results, nutrient_levels)

    pd.testing.assert_frame_equal(translation_results, original_copy)  # Ensure original is unchanged
