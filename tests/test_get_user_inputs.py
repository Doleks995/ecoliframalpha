import pytest
import json
from unittest.mock import patch
import sys
from ecoliframalpha.input_handler import get_user_inputs


def test_get_user_inputs_defaults(monkeypatch):
    """Test get_user_inputs() using all default values."""
    inputs = iter(["", "", "", "", "", "", ""])  # Simulate pressing Enter for all inputs
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result["num_cycles"] == 1000
    assert result["nutrient_levels"] == [1.0, 0.75, 0.5, 0.25, 0.1]
    assert result["robust_codons"] == ["AAA", "GAT"]
    assert result["sensitive_codons"] == ["CGT", "CTG"]
    assert result["stress_probability"] == 0.1
    assert result["recovery_probability"] == 0.05

def test_get_user_inputs_custom(monkeypatch):
    """Test get_user_inputs() with user-provided values."""
    inputs = iter([
        "500",  # num_cycles
        "0.9,0.8,0.7",  # nutrient_levels
        "GGC,TTT",  # robust_codons
        "AAT,TGA",  # sensitive_codons
        "0.2",  # stress_probability
        "0.1"  # recovery_probability
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result["num_cycles"] == 500
    assert result["nutrient_levels"] == [0.9, 0.8, 0.7]
    assert result["robust_codons"] == ["GGC", "TTT"]
    assert result["sensitive_codons"] == ["AAT", "TGA"]
    assert result["stress_probability"] == 0.2
    assert result["recovery_probability"] == 0.1

def test_get_user_inputs_invalid_numeric(monkeypatch):
    """Test handling of invalid numeric input (should raise ValueError)."""
    inputs = iter([
        "not_a_number",  # num_cycles (invalid)
        "", "", "", "", "", ""  # Other inputs (default)
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(ValueError):
        get_user_inputs()

def test_get_user_inputs_invalid_float(monkeypatch):
    """Test handling of invalid float input (should raise ValueError)."""
    inputs = iter([
        "", "", "", "",  # Valid entries
        "not_a_float",  # stress_probability (invalid)
        ""  # recovery_probability (default)
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    with pytest.raises(ValueError):
        get_user_inputs()

def test_get_user_inputs_empty_lists(monkeypatch):
    """Test handling when users enter empty lists (should use defaults)."""
    inputs = iter([
        "",  # num_cycles (default)
        "",  # nutrient_levels (default)
        "",  # robust_codons (default)
        "",  # sensitive_codons (default)
        "",  # stress_probability (default)
        ""   # recovery_probability (default)
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    result = get_user_inputs()

    assert result["nutrient_levels"] == [1.0, 0.75, 0.5, 0.25, 0.1]
    assert result["robust_codons"] == ["AAA", "GAT"]
    assert result["sensitive_codons"] == ["CGT", "CTG"]



def test_get_user_inputs_cli_arguments(monkeypatch):
    """Test that command-line arguments override defaults correctly."""
    test_args = [
        "script.py", "--num_cycles", "500",
        "--nutrient_levels", "1.0,0.5",
        "--robust_codons", "AAA,GGG",
        "--sensitive_codons", "TTC,ATC",
        "--stress_probability", "0.2",
        "--recovery_probability", "0.1"
    ]
    monkeypatch.setattr(sys, "argv", test_args)

    inputs = get_user_inputs()
    assert inputs["num_cycles"] == 500
    assert inputs["nutrient_levels"] == [1.0, 0.5]
    assert inputs["robust_codons"] == ["AAA", "GGG"]
    assert inputs["sensitive_codons"] == ["TTC", "ATC"]
    assert inputs["stress_probability"] == 0.2
    assert inputs["recovery_probability"] == 0.1

def test_get_user_inputs_file_input(tmp_path, monkeypatch):
    """Test that a JSON input file is correctly read."""
    config = {
        "num_cycles": 800,
        "nutrient_levels": [0.9, 0.7],
        "robust_codons": ["CCC"],
        "sensitive_codons": ["GGG"],
        "stress_probability": 0.3,
        "recovery_probability": 0.15
    }
    config_path = tmp_path / "config.json"
    with open(config_path, "w") as file:
        json.dump(config, file)

    test_args = ["script.py", "--input_file", str(config_path)]
    monkeypatch.setattr(sys, "argv", test_args)

    inputs = get_user_inputs()
    assert inputs == config  # Entire config should match

def test_get_user_inputs_interactive(monkeypatch):
    """Test that interactive mode prompts the user correctly."""
    mock_inputs = iter(["700", "1.0,0.8", "AAA,GAT", "CGT,CTG", "0.25", "0.15"])
    monkeypatch.setattr("builtins.input", lambda _: next(mock_inputs))
    monkeypatch.setattr(sys, "argv", ["script.py"])  # No CLI arguments

    inputs = get_user_inputs()
    assert inputs["num_cycles"] == 700
    assert inputs["nutrient_levels"] == [1.0, 0.8]
    assert inputs["robust_codons"] == ["AAA", "GAT"]
    assert inputs["sensitive_codons"] == ["CGT", "CTG"]
    assert inputs["stress_probability"] == 0.25
    assert inputs["recovery_probability"] == 0.15

def test_get_user_inputs_invalid_file(monkeypatch):
    """Test handling of missing JSON file."""
    test_args = ["script.py", "--input_file", "non_existent.json"]
    monkeypatch.setattr(sys, "argv", test_args)

    with pytest.raises(SystemExit):
        get_user_inputs()  # Should exit due to FileNotFoundError
