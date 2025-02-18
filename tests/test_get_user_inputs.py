import os
import pytest
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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

