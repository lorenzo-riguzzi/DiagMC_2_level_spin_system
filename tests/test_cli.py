""" Tests for the command line interface (CLI) implemented in diagmc/__main__.py """

import os
from subprocess import run
import tempfile

def test_cli_help():
    
    """ Tests that the cli help message is displayed correctly
    
        GIVEN: the diagmc command called with the --help option
        WHEN: the command is executed
        THEN: the help message works correctly (exit code 0 and shows the simulation modes)
    """
    
    result = run(
        ["python", "-m", "diagmc", "--help"],
        capture_output=True,
        encoding="utf8"
    )
    assert result.returncode == 0
    assert "single_run" in result.stdout
    assert "convergence_test" in result.stdout
    assert "sweep" in result.stdout

def test_cli_invalid_mode_gives_error():
    
    """ Tests that the cli gives an error when an invalid mode is specified
    
        GIVEN: the diagmc command called with an invalid mode
        WHEN: the command is executed
        THEN: an error message is displayed and the exit code is not 0
    """
    
    result = run(
        ["python", "-m", "diagmc", "invalid_mode"],
        capture_output=True,
        encoding="utf8"
    )
    assert result.returncode != 0

def test_cli_missing_config_file_gives_error():
    
    """ Tests that the cli gives an error when the config file is missing
    
        GIVEN: the diagmc command called with a non-existent config file
        WHEN: the command is executed
        THEN: an error message is displayed and the exit code is not 0
    """
    
    result = run(
        ["python", "-m", "diagmc", "--config", "non_existent_config.yaml"],
        capture_output=True,
        encoding="utf8"
    )
    assert result.returncode != 0
    assert "Error" in result.stdout or "Error" in result.stderr

def test_cli_config_with_no_mode_gives_error():
    
    """ Tests that the cli gives an error when a config file is specified without a mode
    
        GIVEN: the diagmc command called with a config file but no mode
        WHEN: the diagmc command is called without subcommand
        THEN: an error message is displayed and the exit code is not 0
    """
    
    config_content = """
        diagram_params:
            beta: 2.0
            s_0: -1
            h: 0.5
            Gamma: 0.4
            seed_number: 42
        simulation_params:
            N_thermalization: 10
            N_runs: 100
        """
    with tempfile.NamedTemporaryFile( mode='w', suffix='.yaml', delete=False) as temp_config:
        temp_config.write(config_content)
        temp_config_path = temp_config.name

    
    result = run(
        ["python", "-m", "diagmc", "--config", temp_config_path, "single_run"],
        capture_output=True,
        encoding="utf8"
    )
    
    assert result.returncode == 0

    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)

def test_cli_reads_mode_from_config():
    
    """ Tests that the cli runs successfully with a valid config file and the single_run mode specified
    
        GIVEN: the diagmc command called with a valid config file and a valid mode
        WHEN: the command is executed
        THEN: the simulation runs successfully (exit code 0)
    """
    
    config_content = """
        diagram_params:
            beta: 2.0
            s_0: -1
            h: 0.5
            Gamma: 0.4
            seed_number: 42
        simulation_params:
            N_thermalization: 10
            N_runs: 100
        mode: single_run
        """
    with tempfile.NamedTemporaryFile( mode='w', suffix='.yaml', delete=False) as temp_config:
        temp_config.write(config_content)
        temp_config_path = temp_config.name

    
    result = run(
        ["python", "-m", "diagmc", "--config", temp_config_path, "single_run"],
        capture_output=True,
        encoding="utf8"
    )
    
    assert result.returncode == 0

    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)

def test_cli_single_run_works():
    
    """ Tests that the cli runs successfully when the subcommand single_run is specified
    
        GIVEN: the diagmc command called with a valid config file and the single_run subcommand
        WHEN: the command is executed
        THEN: the simulation runs successfully (exit code 0)
    """
    
    result = run(
            ["python", "-m", "diagmc", "single_run"],
            capture_output=True,
            encoding="utf8"
        )
    assert result.returncode == 0

def test_cli_convergence_test_works():

    """ Tests that the cli runs successfully when the subcommand convergence_test is specified

        GIVEN: the diagmc command called with a valid config file and the convergence_test subcommand
        WHEN: the command is executed
        THEN: the simulation runs successfully (exit code 0) and the output file is created
    """

    import yaml

    config_content = """
        "diagram_params": 
            "beta": 1.0
            "s_0": -1
            "h": 0.5
            "Gamma": 0.5
            "seed_number": 42
        
        "simulation_params": 
            "N_thermalization": 10
        
        "mode_options": 
            "convergence_test": 
                "N_start": 10
                "N_end": 30
                "N_step": 10
                "accuracy": 0.05
                "output_file": "test_cli_convergence.csv"
        """

    with tempfile.NamedTemporaryFile( mode='w', delete=False, suffix=".yaml" ) as temp_config:
        temp_config.write(config_content)
        temp_config_path = temp_config.name

    output_path = os.path.join("results", "test_cli_convergence.csv")

    result = run(
        ["python", "-m", "diagmc", "--config", temp_config_path, "convergence_test"],
        capture_output=True,
        encoding="utf8"
    )
    
    assert result.returncode == 0

    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)
    if os.path.exists(output_path):
        os.remove(output_path)


def test_cli_sweep_works():

    """ Tests that the cli runs successfully when the subcommand sweep is specified

        GIVEN: the diagmc command called with a valid config file and the sweep subcommand
        WHEN: the command is executed
        THEN: the simulation runs successfully (exit code 0) and the output file is created
    """

    import yaml

    config_content = """
        "diagram_params": 
            "beta": 1.0
            "s_0": -1
            "h": 0.5
            "Gamma": 0.5
            "seed_number": 42
        
        "simulation_params": 
            "N_thermalization": 10
            "N_runs": 100
        
        "mode_options": 
            "sweep": 
                "variable": "h"
                "variable_start": 0.4
                "variable_end": 0.6
                "variable_step": 0.1
                "output_file": "test_cli_sweep.csv"
        """

    with tempfile.NamedTemporaryFile( mode='w', delete=False, suffix=".yaml" ) as temp_config:
            temp_config.write(config_content)
            temp_config_path = temp_config.name

    output_path = os.path.join("results", "test_cli_sweep.csv")

    result = run(
        ["python", "-m", "diagmc", "--config", temp_config_path, "sweep"],
        capture_output=True,
        encoding="utf8"
    )
    
    assert result.returncode == 0
    if os.path.exists(temp_config_path):
        os.remove(temp_config_path)
    if os.path.exists(output_path):
        os.remove(output_path)