import pandas as pd
import pytest
from ecoliframalpha.utils import normalize_data  

def test_normalize_data_basic():
    """Test normalizing a basic numeric series."""
    series = pd.Series([10, 20, 30, 40, 50])
    normalized = normalize_data(series)

    assert normalized.min() == 0  # Min should be 0
    assert normalized.max() == 1  # Max should be 1
    assert pytest.approx(normalized[2]) == 0.5  # Middle value should be ~0.5

def test_normalize_data_negative_values():
    """Test handling of negative numbers."""
    series = pd.Series([-10, 0, 10, 20])
    normalized = normalize_data(series)

    assert normalized.min() == 0
    assert normalized.max() == 1

def test_normalize_data_identical_values():
    """Test normalizing a series where all values are the same."""
    series = pd.Series([5, 5, 5, 5])
    normalized = normalize_data(series)

    assert (normalized == 0).all()  # Expect all values to be 0 instead of NaN

def test_normalize_data_empty_series():
    """Test normalizing an empty series."""
    series = pd.Series([], dtype=float)
    normalized = normalize_data(series)

    assert normalized.empty  # Should return an empty series

def test_normalize_data_nan_values():
    """Test handling of NaN values."""
    series = pd.Series([1, 2, float("nan"), 4, 5])
    normalized = normalize_data(series)

    assert not normalized.isna().all()  # Some values should be normalized
    assert normalized.dropna().min() == 0
    assert normalized.dropna().max() == 1

def test_normalize_data_large_numbers():
    """Test handling of very large numbers."""
    series = pd.Series([1e9, 2e9, 3e9])
    normalized = normalize_data(series)

    assert normalized.min() == 0
    assert normalized.max() == 1

def test_normalize_data_with_integers_and_floats():
    """Test normalizing a mix of integers and floats."""
    series = pd.Series([1, 2.5, 3.7, 4])
    normalized = normalize_data(series)

    assert normalized.min() == 0
    assert normalized.max() == 1
