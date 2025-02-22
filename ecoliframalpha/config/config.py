

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

    config["metrics"] = ["variance", "Fano_factor", "CV", "CRI"]  # Metrics for variability

    config["num_cycles"]= 1000

    return config