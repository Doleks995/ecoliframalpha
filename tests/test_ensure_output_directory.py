import os
import pytest
from ecoliframalpha.utils import ensure_output_directory



def test_ensure_output_directory(tmp_path):
    """Test that the function creates a directory if it does not exist."""
    test_dir = tmp_path / "output"  # Create a temporary path (does not exist yet)
    # Call the function to create the directory
    ensure_output_directory(str(test_dir))
    # Verify that the directory now exists
    assert test_dir.exists() and test_dir.is_dir()


def test_ensure_output_directory_already_exists(tmp_path):
    """Test that the function does not modify an existing directory."""
    test_dir = tmp_path / "output"
    test_dir.mkdir()  # Manually create the directory
    # Capture the directory modification time before calling the function
    before_mtime = os.stat(test_dir).st_mtime
    # Call the function (should not modify the existing directory)
    ensure_output_directory(str(test_dir))
    # Ensure directory still exists
    assert test_dir.exists() and test_dir.is_dir()
    # Ensure modification time is unchanged
    after_mtime = os.stat(test_dir).st_mtime
    assert before_mtime == after_mtime


def test_ensure_output_directory_invalid_path():
    """Test that passing an invalid path raises an error."""
    with pytest.raises(OSError):  # Catch OS-level errors
        ensure_output_directory("/invalid_path/\\:*?\"<>|")  # Invalid characters

