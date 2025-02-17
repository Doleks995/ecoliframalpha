import os
import pytest
import pandas as pd
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ecoliframalpha.utils import save_to_csv

def test_save_to_csv(tmp_path):
    """Test saving a DataFrame to a CSV file."""
    df = pd.DataFrame({"Name": ["Alice", "Bob"], "Age": [25, 30]})
    filename = "test_output.csv"
    output_dir = tmp_path / "results"
    save_to_csv(df, filename, str(output_dir))
    file_path = output_dir / filename
    assert file_path.exists()  # Ensure file was created
    # Verify content
    loaded_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df, loaded_df)  # Ensure saved data matches

def test_save_to_csv_custom_path(tmp_path):
    """Test saving to a custom directory."""
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    custom_output = tmp_path / "custom_dir"
    filename = "custom_output.csv"
    save_to_csv(df, filename, str(custom_output))
    file_path = custom_output / filename
    assert file_path.exists()
    loaded_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df, loaded_df)

def test_save_to_csv_invalid_filename(tmp_path):
    """Test saving with an invalid filename."""
    df = pd.DataFrame({"Data": [1, 2, 3]})
    with pytest.raises(OSError):  # Expect an error for bad filenames
        save_to_csv(df, "invalid/\\:*?\"<>|.csv", str(tmp_path))

def test_save_to_csv_empty_dataframe(tmp_path):
    """Test saving an empty DataFrame."""
    df = pd.DataFrame()
    filename = "empty.csv"
    save_to_csv(df, filename, str(tmp_path))
    file_path = tmp_path / filename
    assert file_path.exists()
    assert df.empty
    try:
        df = pd.read_csv(file_path)
        if not df.empty:
            sys.exit("The CSV file contains an empty DataFrame.")
    except pd.errors.EmptyDataError:
        pass
    #pd.testing.assert_frame_equal(df, loaded_df)

def test_save_to_csv_overwrite_existing(tmp_path):
    """Test overwriting an existing file."""
    df1 = pd.DataFrame({"Col1": [1, 2]})
    df2 = pd.DataFrame({"Col1": [3, 4]})  # Different data
    filename = "overwrite.csv"
    save_to_csv(df1, filename, str(tmp_path))
    file_path = tmp_path / filename
    assert file_path.exists()
    save_to_csv(df2, filename, str(tmp_path))  # Overwrite
    loaded_df = pd.read_csv(file_path)
    pd.testing.assert_frame_equal(df2, loaded_df)  # Ensure overwrite worked