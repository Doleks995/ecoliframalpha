import sys
import json
import csv
from config.config import get_config

def get_user_inputs():
    """
    Fetches user-defined simulation parameters from:
    1. **Command-line arguments (`sys.argv`)**: Parses `--key value` pairs.
    2. **JSON input file (`--input_file path/to/config.json`)**: Reads parameters from a specified JSON file.
    3. **CSV input file (`--input_file path/to/config.csv`)**: Reads parameters from a CSV file.
    4. **Interactive user input**: If neither CLI arguments nor a file is provided, it prompts the user.

    Supported parameters:
    - `num_cycles` (int)
    - `nutrient_levels` (list of float)
    - `robust_codons` (list of str)
    - `sensitive_codons` (list of str)
    - `stress_probability` (float)
    - `recovery_probability` (float)

    Returns:
        dict: A dictionary containing all simulation parameters.
    """
    config = get_config()
    
    args = sys.argv[1:]  # Skip script name
    args_dict = {}

    # Convert CLI arguments into a dictionary (parsing "--key value" format)
    for i in range(len(args)):
        if args[i].startswith("--") and i + 1 < len(args) and not args[i + 1].startswith("--"):
            key = args[i][2:]  # Remove "--"
            value = args[i + 1]
            args_dict[key] = value

    # Check if an input file is provided
    file_inputs = {}
    if "input_file" in args_dict:
        input_file = args_dict["input_file"]
        if input_file.endswith(".json"):
            try:
                with open(input_file, "r") as file:
                    file_inputs = json.load(file)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Error reading JSON file: {e}", file=sys.stderr)
                sys.exit(1)
        elif input_file.endswith(".csv"):
            try:
                with open(input_file, "r") as file:
                    reader = csv.reader(file)
                    file_inputs = {row[0]: row[1] for row in reader if len(row) == 2}  # Convert CSV to dict
            except (FileNotFoundError, csv.Error) as e:
                print(f"Error reading CSV file: {e}", file=sys.stderr)
                sys.exit(1)

    # Fetch inputs: CLI > File > Interactive Prompt
    def get_value(key, prompt, default, convert_func=str):
        if key in args_dict:
            return convert_func(args_dict[key])  # Use CLI argument
        elif key in file_inputs:
            return file_inputs[key] if isinstance(file_inputs[key], list) else convert_func(file_inputs[key])
        else:
            user_input = input(f"{prompt} (default: {default}): ") or default
            return convert_func(user_input)

    # Process user inputs
    num_cycles = get_value("num_cycles", "Enter the number of simulation cycles", config["num_cycles"], int)
    nutrient_levels = get_value("nutrient_levels", "Enter nutrient levels (comma-separated)", config["nutrient_levels"],
                                lambda x: x if isinstance(x, list) else [float(i) for i in x.split(",")])
    robust_codons = get_value("robust_codons", "Enter robust codons (comma-separated)", config["robust_codons"],
                              lambda x: x if isinstance(x, list) else x.split(","))
    sensitive_codons = get_value("sensitive_codons", "Enter sensitive codons (comma-separated)", config["sensitive_codons"],
                                 lambda x: x if isinstance(x, list) else x.split(","))
    stress_probability = get_value("stress_probability", "Enter stress probability", config["stress_probability"], float)
    recovery_probability = get_value("recovery_probability", "Enter recovery probability",  config["recovery_probability"], float)


    return {
        "num_cycles": num_cycles,
        "nutrient_levels": nutrient_levels,
        "robust_codons": robust_codons,
        "sensitive_codons": sensitive_codons,
        "stress_probability": stress_probability,
        "recovery_probability": recovery_probability,
    }