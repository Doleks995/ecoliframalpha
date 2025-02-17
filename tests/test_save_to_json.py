import os
import json
import pytest

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ecoliframalpha.utils import save_to_json

def test_save_to_json(tmp_path):
    """Test saving a dictionary to a JSON file."""
    data = {"name": "Alice", "age": 30}
    filename = "test_output.json"
    output_dir = tmp_path / "results"
    save_to_json(data, filename, str(output_dir))
    file_path = output_dir / filename
    assert file_path.exists()  # Ensure file was created
    # Verify content
    with open(file_path, "r") as json_file:
        loaded_data = json.load(json_file)
    assert loaded_data == data  # Ensure saved data matches

def test_save_to_json_custom_path(tmp_path):
    """Test saving JSON to a custom directory."""
    data = {"A": 1, "B": 2}
    custom_output = tmp_path / "custom_dir"
    filename = "custom_output.json"
    save_to_json(data, filename, str(custom_output))
    file_path = custom_output / filename
    assert file_path.exists()
    with open(file_path, "r") as json_file:
        loaded_data = json.load(json_file)
    assert loaded_data == data

def test_save_to_json_invalid_filename(tmp_path):
    """Test saving with an invalid filename."""
    data = {"key": "value"}
    with pytest.raises(OSError):  # Expect an error for bad filenames
        save_to_json(data, "invalid/\\:*?\"<>|.json", str(tmp_path))

def test_save_to_json_empty_dict(tmp_path):
    """Test saving an empty dictionary."""
    data = {}
    filename = "empty.json"
    save_to_json(data, filename, str(tmp_path))
    file_path = tmp_path / filename
    assert file_path.exists()
    with open(file_path, "r") as json_file:
        loaded_data = json.load(json_file)
    assert loaded_data == {}  # Ensure the saved file is an empty dictionary

def test_save_to_json_overwrite_existing(tmp_path):
    """Test overwriting an existing JSON file."""
    data1 = {"Col1": "First"}
    data2 = {"Col1": "Second"}  # Different data
    filename = "overwrite.json"
    save_to_json(data1, filename, str(tmp_path))
    file_path = tmp_path / filename
    assert file_path.exists()
    save_to_json(data2, filename, str(tmp_path))  # Overwrite
    with open(file_path, "r") as json_file:
        loaded_data = json.load(json_file)
    assert loaded_data == data2  # Ensure overwrite worked