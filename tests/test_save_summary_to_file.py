import pytest
from ecoliframalpha.utils import save_summary_to_file

def test_save_summary_to_file(tmp_path):
    """Test saving a summary to a text file."""
    summary_text = "This is a test summary."
    filename = "test_summary.txt"
    output_dir = tmp_path / "results"
    save_summary_to_file(summary_text, filename, str(output_dir))
    file_path = output_dir / filename
    assert file_path.exists()  # Ensure file was created
    with open(file_path, "r") as file:
        saved_content = file.read()
    assert saved_content == summary_text  # Check file content

def test_save_summary_to_file_custom_path(tmp_path):
    """Test saving a summary to a custom directory."""
    summary_text = "Custom directory test."
    custom_output = tmp_path / "custom_dir"
    filename = "custom_summary.txt"
    save_summary_to_file(summary_text, filename, str(custom_output))
    file_path = custom_output / filename
    assert file_path.exists()
    with open(file_path, "r") as file:
        saved_content = file.read()
    assert saved_content == summary_text

def test_save_summary_to_file_invalid_filename(tmp_path):
    """Test saving with an invalid filename."""
    summary_text = "Invalid filename test."
    with pytest.raises(OSError):  # Expect an error for bad filenames
        save_summary_to_file(summary_text, "invalid/\\:*?\"<>|.txt", str(tmp_path))

def test_save_summary_to_file_empty_summary(tmp_path):
    """Test saving an empty summary."""
    summary_text = ""
    filename = "empty_summary.txt"
    save_summary_to_file(summary_text, filename, str(tmp_path))
    file_path = tmp_path / filename
    assert file_path.exists()
    with open(file_path, "r") as file:
        saved_content = file.read()
    assert saved_content == ""  # Ensure file is empty
