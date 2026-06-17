import os,sys,inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir) 

import pytest
from scripts.simulation import single_run

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
    
    


