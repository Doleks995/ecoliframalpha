

def get_config():
    """
    Produces a config dictionary contaning all of the relevant parameters to use as input of the package.

    Returns:
        dict: config
    """
    config={}


    #Establish paths
    config["input_path"] = "" #Path for input data
    config["output_path"] = "results/" # Path for saving output

    #Establish metrics
    config["metrics"] = ["variance", "Fano_factor", "CV", "CRI"]  # Metrics for variability

    #Establish simulation parameters
    config["num_cycles"]= 1000
    config["nutrient_levels"] = [1.0, 0.75, 0.5, 0.25, 0.1]
    config["robust_codons"] = ["AAA", "GAT"]
    config["sensitive_codons"] = ["CGT", "CTG"]
    config["stress_probability"] = 0.1
    config["recovery_probability"] = 0.05

    config["possible_codons"] = [
    "UUU", "UUC",  # Phenylalanine (Phe)
    "UUA", "UUG",  # Leucine (Leu)
    "CUU", "CUC", "CUA", "CUG",  # Leucine (Leu)
    "AUU", "AUC", "AUA",  # Isoleucine (Ile)
    "AUG",  # Methionine (Met) - Start Codon
    "GUU", "GUC", "GUA", "GUG",  # Valine (Val)
    
    "UCU", "UCC", "UCA", "UCG",  # Serine (Ser)
    "CCU", "CCC", "CCA", "CCG",  # Proline (Pro)
    "ACU", "ACC", "ACA", "ACG",  # Threonine (Thr)
    "GCU", "GCC", "GCA", "GCG",  # Alanine (Ala)
    
    "UAU", "UAC",  # Tyrosine (Tyr)
    "UAA", "UAG",  # STOP Codons
    "CAU", "CAC",  # Histidine (His)
    "CAA", "CAG",  # Glutamine (Gln)
    "AAU", "AAC",  # Asparagine (Asn)
    "AAA", "AAG",  # Lysine (Lys)
    "GAU", "GAC",  # Aspartic Acid (Asp)
    "GAA", "GAG",  # Glutamic Acid (Glu)
    
    "UGU", "UGC",  # Cysteine (Cys)
    "UGA",  # STOP Codon
    "UGG",  # Tryptophan (Trp)
    "CGU", "CGC", "CGA", "CGG",  # Arginine (Arg)
    "AGU", "AGC",  # Serine (Ser)
    "AGA", "AGG",  # Arginine (Arg)
    "GGU", "GGC", "GGA", "GGG"   # Glycine (Gly)
]

    #Codon efficiency data
    config["base_efficiency_robust"] = 1.0
    config["base_efficiency_sensitive"] = 0.5

    #RNA processing data
    config["rnase_activity"] = 0.05
    config["decay_variability"] = 0.1

    #Constants for translation dynamics
    config["max_efficiency"] = 1.5
    config["min_efficiency"] = 0.1
    config["hill_coefficient"] = 2
    config["nutrient_threshold"] = 0.5


    return config