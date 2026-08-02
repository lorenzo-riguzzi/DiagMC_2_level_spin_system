import sys
from typing import Optional
import yaml
import argparse
import scripts.simulation 

def run_simulation(config_file: str = "config.yaml", mode_override: Optional[str] = None) -> None:
    """ Simulation function to execute the diagrammatic Monte Carlo simulation
        Reads the parameters from the config.yaml file and calls the required simulation
    """
    
    try:
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file}' not found.")
        sys.exit(1)
    
    mode = mode_override if mode_override is not None else config.get("mode")
    
    if mode is None:
        print("Error: No mode specified. Provide a subcommand (e.g. 'diagmc single_run') or set 'mode' in your config file.")
        sys.exit(1)
    
    if mode == "single_run":
        scripts.simulation.single_run(config)
    elif mode == "convergence_test":
        scripts.simulation.convergence_test(config)
    elif mode == "sweep":
        scripts.simulation.sweep(config)
    else:
        print(f"Error: Unknown simulation execution mode '{mode}' specified.")
        sys.exit(1)


def main() -> None:
    """Main function to execute the code and implement the command line interface for the simulation."""
    
    parser = argparse.ArgumentParser(
        description="Diagrammatic Monte Carlo simulation of a 2-level spin system."
    )
    
    parser.add_argument(
        "-c", "--config",
        default = "config.yaml",
        help = "Path to the .yaml configuration file (default: config.yaml)"
    )
    
    subparsers = parser.add_subparsers(dest = "subcommand", help = "Simulation mode to run")
        
    subparsers.add_parser("single_run", help = "Run a single simulation with the specified parameters.")
    subparsers.add_parser("convergence_test", help = "Run a convergence test with the specified parameters.")
    subparsers.add_parser("sweep", help = "Run a parameter sweep with the specified parameters.")
    
    args = parser.parse_args()
    
    run_simulation(config_file = args.config, mode_override = args.subcommand)

if __name__ == "__main__":
    main()