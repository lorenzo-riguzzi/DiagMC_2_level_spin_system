import sys
import yaml
import scripts.simulation 

def main():
    """ Main function to execute the diagrammatic Monte Carlo simulation
        Reads the parameters from the config.yaml file and calls the required simulation
    """
    
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.yaml"
    
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    
    mode = config.get("mode")
    
    if mode == "single_run":
        scripts.simulation.single_run(config)
    elif mode == "convergence_test":
        scripts.simulation.convergence_test(config)
    elif mode == "sweep":
        print("To be implemented yet")
    else:
        print(f"Error: Unknown simulation execution mode '{mode}' specified.")
        sys.exit(1)


if __name__ == "__main__":
    main()  