import os
import pandas as pd
import pytest
from ecoliframalpha.visualization import generate_visualizations

def test_generate_visualizations_creates_files(tmp_path):
    """Test that the function creates expected visualization files."""
    variability_results = pd.DataFrame({
        "codon": ["AAA", "GGG"],
        "variance": [0.1, 0.2],
        "Fano_factor": [1.5, 2.0]
    })
    
    stressed_results = pd.DataFrame({
        "nutrient_levels": [0.2, 0.4, 0.6, 0.8, 1.0],
        "AAA_efficiency": [0.8, 0.85, 0.9, 0.95, 1.0],
        "GGG_efficiency": [0.7, 0.75, 0.8, 0.85, 0.9]
    })

    validation_results = {
        "accuracy": {"experimental_mean": [0.8, 0.85, 0.9], "simulated_mean": [0.78, 0.83, 0.88]}
    }

    output_dir = str(tmp_path)
    generate_visualizations(variability_results, stressed_results, validation_results, output_dir)

    assert os.path.exists(os.path.join(output_dir, "codon_efficiencies_smoothed.png"))
    assert os.path.exists(os.path.join(output_dir, "nutrient_levels.png"))
    assert os.path.exists(os.path.join(output_dir, "variability_metrics.png"))
    assert os.path.exists(os.path.join(output_dir, "validation_accuracy.png"))

def test_generate_visualizations_empty_dataframes(tmp_path):
    """Test that the function handles empty DataFrames without errors."""
    variability_results = pd.DataFrame()
    stressed_results = pd.DataFrame()
    validation_results = {}

    output_dir = str(tmp_path)
    with pytest.raises(ValueError, match="One or more input DataFrames are empty."):
        generate_visualizations(variability_results, stressed_results, validation_results, output_dir)

    assert not os.listdir(output_dir)  # No files should be created

def test_generate_visualizations_missing_columns():
    """Test that the function raises an error if required columns are missing."""
    variability_results = pd.DataFrame({"wrong_column": [1, 2, 3]})
    stressed_results = pd.DataFrame({"wrong_column": [0.1, 0.2, 0.3]})
    validation_results = {
        "accuracy": {"experimental_mean": [0.8, 0.85, 0.9], "simulated_mean": [0.78, 0.83, 0.88]}
    }

    with pytest.raises(ValueError, match="Missing 'nutrient_levels' column in stressed_results DataFrame."):
        generate_visualizations(pd.DataFrame({"codon": ["AAA", "GGG"]}), 
                                stressed_results, 
                                validation_results)

    with pytest.raises(ValueError, match="Missing 'codon' column in variability_results DataFrame."):
        generate_visualizations(variability_results, 
                                pd.DataFrame({"nutrient_levels": [0.1, 0.2, 0.3]}), 
                                validation_results)
