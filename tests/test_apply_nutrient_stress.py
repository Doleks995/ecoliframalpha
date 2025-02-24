import numpy as np
import pandas as pd
import pytest
from ecoliframalpha.nutrient_stress import apply_nutrient_stress  

def test_apply_nutrient_stress_basic():
    """Test nutrient stress application with standard values."""
    np.random.seed(42)  # Fix seed for reproducibility

    translation_results = pd.DataFrame({"cycle": range(10), 
                                        "nutrient_levels": [1.0] * 10}) 
    nutrient_levels = [1.0, 0.75, 0.5, 0.25, 0.1]

    result = apply_nutrient_stress(translation_results, nutrient_levels)

    assert "nutrient_levels" in result.columns  
    assert len(result) == len(translation_results)  # Same number of rows
    assert result["nutrient_levels"].isin(nutrient_levels).all()  # Valid levels only

def test_apply_nutrient_stress_empty_dataframe():
    """Test handling of an empty translation_results DataFrame."""
    translation_results = pd.DataFrame(columns=["cycle", "nutrient_levels"])  #Ensure correct columns
    nutrient_levels = [1.0, 0.75, 0.5]

    result = apply_nutrient_stress(translation_results, nutrient_levels)

    assert result.empty  # Should return an empty DataFrame

def test_apply_nutrient_stress_invalid_probability():
    """Test invalid stress and recovery probability values."""
    translation_results = pd.DataFrame({"cycle": range(5), "nutrient_levels": [1.0] * 5})
    nutrient_levels = [1.0, 0.75, 0.5, 0.25]

    with pytest.raises(ValueError, match="stress_probability must be between 0 and 1"):
        apply_nutrient_stress(translation_results, nutrient_levels, stress_probability=-0.1)

    with pytest.raises(ValueError, match="recovery_probability must be between 0 and 1"):
        apply_nutrient_stress(translation_results, nutrient_levels, recovery_probability=1.5)

def test_apply_nutrient_stress_does_not_modify_original():
    """Ensure function does not modify the input DataFrame."""
    translation_results = pd.DataFrame({"cycle": range(5), "nutrient_levels": [1.0] * 5})
    nutrient_levels = [1.0, 0.75, 0.5]

    original_copy = translation_results.copy()
    apply_nutrient_stress(translation_results, nutrient_levels)

    pd.testing.assert_frame_equal(translation_results, original_copy)  # Ensure original is unchanged
