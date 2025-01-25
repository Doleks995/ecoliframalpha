import json

def get_user_inputs():
    """
    Fetch user-defined inputs for the simulation.

    Returns:
        dict: A dictionary containing simulation parameters.
    """
    print("Welcome to the Codon Simulation Tool!")

    # Ask for input or provide defaults
    num_cycles = int(input("Enter the number of simulation cycles (default: 1000): ") or 1000)
    nutrient_levels = input("Enter nutrient levels as a comma-separated list (default: 1.0,0.75,0.5,0.25,0.1): ")
    nutrient_levels = [float(x) for x in (nutrient_levels or "1.0,0.75,0.5,0.25,0.1").split(",")]

    robust_codons = input("Enter robust codons as a comma-separated list (default: AAA,GAT): ")
    robust_codons = robust_codons.split(",") or ["AAA", "GAT"]

    sensitive_codons = input("Enter sensitive codons as a comma-separated list (default: CGT,CTG): ")
    sensitive_codons = sensitive_codons.split(",") or ["CGT", "CTG"]

    stress_probability = float(input("Enter stress probability (default: 0.1): ") or 0.1)
    recovery_probability = float(input("Enter recovery probability (default: 0.05): ") or 0.05)

    return {
        "num_cycles": num_cycles,
        "nutrient_levels": nutrient_levels,
        "robust_codons": robust_codons,
        "sensitive_codons": sensitive_codons,
        "stress_probability": stress_probability,
        "recovery_probability": recovery_probability,
    }
