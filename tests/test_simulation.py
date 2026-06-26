import os,sys,inspect
import pandas as pd
import copy

frame = inspect.currentframe()
assert frame is not None

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(frame)))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir) 

import pytest
from scripts.simulation import single_run, convergence_test, sweep

""" Tests for the methods in the simulation.py file """


def test_single_run_input_parameters_value_errors():
    """ Tests that, if the input parameters in the config.yaml file are invalid, ValueError is raised """
    
    invalid_config_beta = {
        "mode": "single_run",
        "diagram_params": {
            "beta": -1.0,  # Invalid negative beta
            "s_0": 1,
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100,  
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_beta)
    
    invalid_config_s_0 = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 0.5, # Invalid non-integer s_0
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100,  
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_s_0)
    
    invalid_config_negative_vertex = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [-0.1, 0.2, 0.3, 0.4], # Invalid negative vertex
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100,  
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_negative_vertex)
    
    invalid_config_vertex_greater_than_beta = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [0.1, 0.2, 0.4, 2.3], # Invalid vertex greater than beta
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100,  
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_vertex_greater_than_beta)
    
    invalid_config_odd_vertices = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [0.1, 0.2, 0.4], # Invalid odd number of vertices
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100,  
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_odd_vertices)
    
    invalid_config_negative_N_thermalization = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": -100, # Invalid negative N_thermalization 
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_negative_N_thermalization)
    
    invalid_config_negative_N_runs = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 100, 
            "N_runs": -1000 # Invalid negative N_runs
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_negative_N_runs)
    
    empty_config = {}
    
    with pytest.raises(KeyError):
        single_run(empty_config)

def test_single_run_is_deterministic(capsys):
    """ Tests that, if the seed is fixed, the results of single_run are deterministic """
    
    config = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "h": 1.0,
            "Gamma": 0.5,
            "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 10,  
            "N_runs": 100 
        }
    }
    
    single_run(config)  
    captured_1 = capsys.readouterr()
    output_1 = captured_1.out
    
    single_run(config)  
    captured_2 = capsys.readouterr()
    output_2 = captured_2.out
    
    assert output_1 == output_2

valid_config_convergence = {
    "diagram_params": {
        "beta": 1.0, "s_0": -1, "vertices": [], "h": 0.5, "Gamma": 0.5, "seed_number": 42
    },
    "simulation_params": {
        "N_thermalization": 5
    },
    "mode_options": {
        "convergence_test": {
            "N_start": 10,
            "N_end": 30,
            "N_step": 10,
            "accuracy": 0.05,
            "output_file": "test_conv.csv",
        }
    }
}

def test_convergence_test_input_parameters_value_errors():
    wrong_config = copy.deepcopy(valid_config_convergence)
    wrong_config["mode_options"]={
        "convergence_test": {
            "N_start": -10, # Invalid negative N_start
            "N_end": 30,
            "N_step": 10,
            "accuracy": 0.05,
            "output_file": "test_conv.csv"
        }
    }
    
    with pytest.raises(ValueError, match="must be positive non-null integers"):
        convergence_test(wrong_config)
    
    
    wrong_config["mode_options"]={
        "convergence_test": {
            "N_start": 40,
            "N_end": 30,
            "N_step": 10,
            "accuracy": 0.05,
            "output_file": "test_conv.csv"
        }
    }
    
    with pytest.raises(ValueError):
        convergence_test(wrong_config)

def test_convergence_test_output_files_created():
    """ Verifies that the .csv output files are created after running convergence_test with valid parameters """
    
    convergence_test(valid_config_convergence)
    
    output_path = os.path.join("results", "test_conv.csv")
    
    assert os.path.exists(output_path)
    
    dataframe = pd.read_csv(output_path)
    
    assert "N" in dataframe.columns
    assert "m_z" in dataframe.columns
    assert "error_m_z" in dataframe.columns
    assert "threshold_m_z" in dataframe.columns
    assert "m_x" in dataframe.columns
    assert "error_m_x" in dataframe.columns
    assert "threshold_m_x" in dataframe.columns
    
    
    if os.path.exists(output_path):
        os.remove(output_path)

valid_config_sweep = {
    "diagram_params": {
        "beta": 1.0, "s_0": -1, "vertices": [], "h": 0.5, "Gamma": 0.5, "seed_number": 42
    },
    "simulation_params": {
        "N_runs": 100,
        "N_thermalization": 5
    },
    "mode_options": {
        "sweep": {
            "variable": "beta",
            "variable_start": 0.1,
            "variable_end": 2.0,
            "variable_step": 0.1,
            "output_file": "test_sweep.csv"
        }
    }
}

def test_invalid_sweep_variable():
    """ Test that a ValueError is raised when an invalid variable is provided """
    
    invalid_config = copy.deepcopy(valid_config_sweep)
    invalid_config["mode_options"]["sweep"]["variable"] = "s_0"
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_invalid_sweep_test():
    """ Tests that a ValueError is raised when variable_step <= 0 """
    
    invalid_config = copy.deepcopy(valid_config_sweep)
    invalid_config["mode_options"]["sweep"]["variable_step"] = -0.1
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_invalid_sweep_range():
    """ Tests that a ValueError is raised when variable_start >= variable_end """
    
    invalid_config = copy.deepcopy(valid_config_sweep)
    invalid_config["mode_options"]["sweep"]["variable_start"] = 2.0
    invalid_config["mode_options"]["sweep"]["variable_end"] = 0.1
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_negative_N_runs_sweep():
    """ Tests that a ValueError is raised when N_runs is negative in the config for sweep """
    
    invalid_config = copy.deepcopy(valid_config_sweep)
    invalid_config["simulation_params"]["N_runs"] = -100
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_negative_N_thermalization_sweep():
    """ Tests that a ValueError is raised when N_thermalization is negative in the config for sweep """
    
    invalid_config = copy.deepcopy(valid_config_sweep)
    invalid_config["simulation_params"]["N_thermalization"] = -5
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_sweep_output_files_created():
    """ Verifies that the .csv output files are created after running sweep with valid parameters """
    
    sweep(valid_config_sweep)
    
    variable = valid_config_sweep["mode_options"]["sweep"]["variable"]
    
    output_path = os.path.join("results", "test_sweep.csv")
    
    assert os.path.exists(output_path)
    
    dataframe = pd.read_csv(output_path)
    
    assert variable in dataframe.columns
    assert "m_z (MC)" in dataframe.columns
    assert "m_z (Analytical)" in dataframe.columns
    assert "m_x (MC)" in dataframe.columns
    assert "m_x (Analytical)" in dataframe.columns
    assert "h" in dataframe.columns
    assert "Gamma" in dataframe.columns
    assert len(dataframe) == 20
    
    if os.path.exists(output_path):
        os.remove(output_path)


