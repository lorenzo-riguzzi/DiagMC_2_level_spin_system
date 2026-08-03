""" Tests for the methods in the simulation.py file """

import pytest
import pandas as pd
import os
import numpy as np
from scripts.simulation import single_run, convergence_test, sweep
from scripts.diagram import Diagram


def test_single_run_invalid_beta():
    
    """ Tests that, if the beta in the config.yaml file is negative, a ValueError is raised 
    
        GIVEN: a config dictionary with a negative beta
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config_beta = {
        "mode": "single_run",
        "diagram_params": {
            "beta": -1.0, 
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
        

def test_single_run_invalid_s_0():
    
    """ Tests that, if the s_0 in the config.yaml file is not +/- 1, a ValueError is raised 
    
        GIVEN: a config dictionary with an invalid s_0 (non-integer)
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config_s_0 = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 0.5,
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
    
def test_single_run_negative_vertex():
    
    """ Tests that, if a vertex in the config.yaml file is negative, a ValueError is raised 
    
        GIVEN: a config dictionary with a negative vertex in the vertices list
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config_negative_vertex = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [-0.1, 0.2, 0.3, 0.4],
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
        
def test_single_run_vertex_greater_than_beta():
        
    """ Tests that, if a vertex in the config.yaml file is greater than beta, a ValueError is raised 
    
        GIVEN: a config dictionary with a vertex greater than beta in the vertices list
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config_vertex_greater_than_beta = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [0.1, 0.2, 0.4, 2.3],
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

def test_single_run_odd_number_of_vertices():
        
    """ Tests that, if the number of vertices in the config.yaml file is odd, a ValueError is raised 
    
        GIVEN: a config dictionary with an odd number of vertices in the vertices list
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config_odd_vertices = {
        "mode": "single_run",
        "diagram_params": {
            "beta": 1.0,
            "s_0": 1,
            "vertices": [0.1, 0.2, 0.4],
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
    
    
def test_single_run_invalid_N_thermalization():
    
    """ Tests that, if the N_thermalization in the config.yaml file is negative, a ValueError is raised 
    
        GIVEN: a config dictionary with a negative N_thermalization
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
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
            "N_thermalization": -100, 
            "N_runs": 1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_negative_N_thermalization)

def test_single_run_invalid_N_runs():
    
    """ Tests that, if the N_runs in the config.yaml file is negative, a ValueError is raised 
    
        GIVEN: a config dictionary with a negative N_runs
        WHEN: the single_run method is called with this config
        THEN: a ValueError is raised
    """
    
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
            "N_runs": -1000 
        }
    }
    
    with pytest.raises(ValueError): 
        single_run(invalid_config_negative_N_runs)
    
def test_single_run_empty_config():
    
    """ Tests that a KeyError is raised when an empty config dictionary is passed to single_run 
    
        GIVEN: an empty config dictionary
        WHEN: the single_run method is called with this config
        THEN: a KeyError is raised
    """
    
    empty_config = {}
    
    with pytest.raises(KeyError):
        single_run(empty_config)

def test_single_run_is_deterministic():
    
    """ Tests that, if the seed is fixed, the results of single_run are deterministic 
    
        GIVEN: a valid config dictionary with a fixed seed
        WHEN: the single_run method is called twice with this config
        THEN: the outputs of both runs are identical
    """
    
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
    
    average_m_z_1, average_m_x_1 = single_run(config)
    
    average_m_z_2, average_m_x_2 = single_run(config)
    
    assert average_m_z_1 == average_m_z_2
    assert average_m_x_1 == average_m_x_2

@pytest.fixture
def valid_config_convergence():
    
    """ Provides a valid configuration dictionary for testing the convergence_test method """
    
    return {
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

def test_convergence_test_negative_N_start(valid_config_convergence):
    
    """ Tests that, if the N_start in the config.yaml file is negative, a ValueError is raised 
    
        GIVEN: a config dictionary with a negative N_start
        WHEN: the convergence_test method is called with this config
        THEN: a ValueError is raised
    """
    
    wrong_config_negative_N_start = valid_config_convergence
    wrong_config_negative_N_start["mode_options"]={
        "convergence_test": {
            "N_start": -10,
            "N_end": 30,
            "N_step": 10,
            "accuracy": 0.05,
            "output_file": "test_conv.csv"
        }
    }
    
    with pytest.raises(ValueError, match="must be positive non-null integers"):
        convergence_test(wrong_config_negative_N_start)
    

def test_convergence_test_N_end_lower_than_N_start(valid_config_convergence):
    
    """ Tests that, if the N_end in the config.yaml file is lower than N_start, a ValueError is raised 
    
        GIVEN: a config dictionary with N_end lower than N_start
        WHEN: the convergence_test method is called with this config
        THEN: a ValueError is raised
    """
    
    wrong_config_N_end_lower_than_N_start = valid_config_convergence
    wrong_config_N_end_lower_than_N_start["mode_options"]={
        "convergence_test": {
            "N_start": 40,
            "N_end": 30,
            "N_step": 10,
            "accuracy": 0.05,
            "output_file": "test_conv.csv"
        }
    }
    
    with pytest.raises(ValueError):
        convergence_test(wrong_config_N_end_lower_than_N_start)

def test_convergence_test_output_files_created(valid_config_convergence):
    
    """ Verifies that the .csv output files are created after running convergence_test with valid parameters 
    
        GIVEN: a valid config dictionary for convergence_test
        WHEN: the convergence_test method is called with this config
        THEN: the output .csv file is created and contains the expected columns
    """
    
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

@pytest.fixture
def valid_config_sweep():
    
    """ Provides a valid configuration dictionary for testing the sweep method """
    
    return {
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

def test_invalid_sweep_variable(valid_config_sweep):
    
    """ Tests that a ValueError is raised when an invalid variable is given as input 
    
        GIVEN: a config dictionary with an invalid variable for sweep (for example "s_0")
        WHEN: the sweep method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config = valid_config_sweep
    invalid_config["mode_options"]["sweep"]["variable"] = "s_0"
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_invalid_sweep_test(valid_config_sweep):
    
    """ Tests that a ValueError is raised when variable_step <= 0 
    
        GIVEN: a config dictionary with variable_step <= 0
        WHEN: the sweep method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config = valid_config_sweep
    invalid_config["mode_options"]["sweep"]["variable_step"] = -0.1
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_invalid_sweep_range(valid_config_sweep):
    
    """ Tests that a ValueError is raised when variable_start >= variable_end 
    
        GIVEN: a config dictionary with variable_start >= variable_end
        WHEN: the sweep method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config = valid_config_sweep
    invalid_config["mode_options"]["sweep"]["variable_start"] = 2.0
    invalid_config["mode_options"]["sweep"]["variable_end"] = 0.1
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_negative_N_runs_sweep(valid_config_sweep):
    
    """ Tests that a ValueError is raised when N_runs is negative in the config for sweep 
    
        GIVEN: a config dictionary with a negative N_runs
        WHEN: the sweep method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config = valid_config_sweep
    invalid_config["simulation_params"]["N_runs"] = -100
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_negative_N_thermalization_sweep(valid_config_sweep):
    
    """ Tests that a ValueError is raised when N_thermalization is negative in the config for sweep 
    
        GIVEN: a config dictionary with a negative N_thermalization
        WHEN: the sweep method is called with this config
        THEN: a ValueError is raised
    """
    
    invalid_config = valid_config_sweep
    invalid_config["simulation_params"]["N_thermalization"] = -5
    with pytest.raises(ValueError):
        sweep(invalid_config)

def test_sweep_output_files_created(valid_config_sweep):
    
    """ Verifies that the .csv output files are created after running sweep with valid parameters 
    
        GIVEN: a valid config dictionary for the sweep
        WHEN: the sweep method is called with this config
        THEN: the .csv output files are created and they contain the expected columns
    """
    
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

# NEW POSITIVE TESTS FOR THE SIMULATION

def test_single_run_magnetizations_converge_to_analytical():
    
    """ Tests that the m_z and m_x values obtained from single_run converge to the analytical values within a sensitive threshold of 5%
    
        GIVEN: a valid config dictionary for single_run
        WHEN: the single_run method is called with this config
        THEN: the m_z and m_x values obtained from single_run converge to the analytical values within 5%
    """
    
    config = {
        "diagram_params": {
            "beta": 5.0, "s_0": -1, "h": 0.5,
            "Gamma": 0.6, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    m_z, m_x = single_run(config)
    
    diagram = Diagram(beta=5.0, h=0.5, Gamma=0.6)
    
    analytical_m_z = diagram.analytical_m_z()
    analytical_m_x = diagram.analytical_m_x()   
    
    assert abs(m_z - analytical_m_z) < 0.05 * abs(analytical_m_z)
    assert abs(m_x - analytical_m_x) < 0.05 * abs(analytical_m_x)

def test_simulation_mz_is_zero_at_zero_field():
    
    """ Tests that the magnetization m_z is close to zero when the external field h is set to zero
    
        GIVEN: a valid config dictionary for single_run with h=0.0
        WHEN: single_run is called
        THEN: the estimated mz is close to zero by symmetry, within absolute tolerance 0.05
    """
    
    config = {
        "diagram_params": {
            "beta": 2.0, "s_0": -1, "h": 0.0,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 10_000,
            "N_runs": 500_000
        }
    }
    
    mz, _ = single_run(config)
    
    assert abs(mz) < 0.005

def test_m_z_and_m_x_symmetry_with_h():
    
    """ Tests that the magnetization m_z is antisymmetric with respect to the external field h, while m_x is symmetric
    
        GIVEN: two valid config dictionaries for single_run, one with h and one with -h
        WHEN: single_run is called for both configs
        THEN: the estimated m_z values are approximately equal in magnitude but opposite in sign, while those of m_x are approximately equal
    """
    
    config_positive_h = {
        "diagram_params": {
            "beta": 2.0, "s_0": -1, "h": 0.5,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    config_negative_h = {
        "diagram_params": {
            "beta": 2.0, "s_0": -1, "h": -0.5,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz_1, mx_1 = single_run(config_positive_h)
    mz_2, mx_2 = single_run(config_negative_h)
    
    assert abs(mz_1 + mz_2) < 0.005
    assert abs(mx_1 - mx_2) < 0.005

def test_m_z_and_m_x_symmetry_with_Gamma():
    
    """ Tests that the magnetization m_x is antisymmetric with respect to the external field Gamma, while m_z is symmetric
    
        GIVEN: two valid config dictionaries for single_run, one with Gamma and one with -Gamma
        WHEN: single_run is called for both configs
        THEN: the estimated m_x values are approximately equal in magnitude but opposite in sign, while those of m_z are approximately equal
    """
    
    config_positive_h = {
        "diagram_params": {
            "beta": 2.0, "s_0": -1, "h": 0.5,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    config_negative_h = {
        "diagram_params": {
            "beta": 2.0, "s_0": -1, "h": 0.5,
            "Gamma": -0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz_1, mx_1 = single_run(config_positive_h)
    mz_2, mx_2 = single_run(config_negative_h)
    
    assert abs(mz_1 - mz_2) < 0.005
    assert abs(mx_1 + mx_2) < 0.005

def test_strong_h_limit():
    
    """ Tests that the magnetization m_z approaches -1 as the external field h is much larger than Gamma, while m_x approaches 0 (for a beta not too high)
    
        GIVEN: a valid config dictionary for single_run with a large h
        WHEN: single_run is called
        THEN: the estimated m_z is close to -1 within a threshold of 5% and m_x is close to 0
    """
    
    config = {
        "diagram_params": {
            "beta": 1.0, "s_0": -1, "h": 100.0,
            "Gamma": 0.1, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    assert abs(mz + 1.0) < 0.05
    assert abs(m_x) < 0.0005

def test_weak_h_limit():
    
    """ Tests that the magnetization m_z approaches 0 as the external field h is much smaller than Gamma, while m_x approaches -tanh(beta * Gamma)
    
        GIVEN: a valid config dictionary for single_run with a small h
        WHEN: single_run is called
        THEN: the estimated m_z is close to 0 and m_x is close to -tanh(beta * Gamma) within a threshold of 5%
    """
    
    config = {
        "diagram_params": {
            "beta": 5.0, "s_0": -1, "h": 0.01,
            "Gamma": 10.0, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    assert abs(mz) < 0.005
    assert abs(m_x + np.tanh(5.0 * 10.0)) < 0.05 * np.tanh(5.0 * 10.0)

def test_weak_Gamma_limit():
    
    """ Tests that the magnetization m_x approaches 0 as the transverse field Gamma is much smaller than h, while m_z approaches -tanh(beta * h)
    
        GIVEN: a valid config dictionary for single_run with a small Gamma
        WHEN: single_run is called
        THEN: the estimated m_x is close to 0 and m_z is close to -tanh(beta * h) within a threshold of 5%
    """
    
    config = {
        "diagram_params": {
            "beta": 5.0, "s_0": -1, "h": 10.0,
            "Gamma": 0.01, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    assert abs(m_x) < 0.005
    assert abs(mz + np.tanh(5.0 * 10.0)) < 0.05 * np.tanh(5.0 * 10.0)

def test_strong_Gamma_limit():
    
    """ Tests that the magnetization m_x approaches -1 as the transverse field Gamma is much larger than h, while m_z approaches 0 (for a beta not too high)
    
        GIVEN: a valid config dictionary for single_run with a large Gamma
        WHEN: single_run is called
        THEN: the estimated m_x is close to -1 within a threshold of 5% and m_z is close to 0
    """
    
    config = {
        "diagram_params": {
            "beta": 1.0, "s_0": -1, "h": 0.1,
            "Gamma": 100.0, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    assert abs(m_x + 1.0) < 0.05
    assert abs(mz) < 0.005
    
def test_high_beta_limit():
    
    """ Tests that the magnetizations m_z and m_x approach the expected limit values as beta is very large (low temperatures)
    
        GIVEN: a valid config dictionary for single_run with a large beta
        WHEN: single_run is called
        THEN: the estimated m_z and m_x are close to -h/E and -Gamma/E, respectively, with E=sqrt(h^2 + Gamma^2), within a threshold of 5%
    """
    
    config = {
        "diagram_params": {
            "beta": 100.0, "s_0": -1, "h": 0.5,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    limit_m_z = -0.5 / (0.5**2 + 0.4**2)**0.5
    limit_m_x = -0.4 / (0.5**2 + 0.4**2)**0.5
    
    assert abs(mz - limit_m_z) < 0.05 * abs(limit_m_z)
    assert abs(m_x - limit_m_x) < 0.05 * abs(limit_m_x)

def test_small_beta_limit():
    
    """ Tests that the magnetizations m_z and m_x approach zero as beta is very small (high temperatures)
    
        GIVEN: a valid config dictionary for single_run with a small beta
        WHEN: single_run is called
        THEN: the estimated m_z and m_x are close to 0
    """
    
    config = {
        "diagram_params": {
            "beta": 0.001, "s_0": -1, "h": 0.5,
            "Gamma": 0.4, "seed_number": 42
        },
        "simulation_params": {
            "N_thermalization": 5000,
            "N_runs": 100000
        }
    }
    
    mz, m_x = single_run(config)
    
    assert abs(mz) < 0.005
    assert abs(m_x) < 0.005

def test_convergence_test_error_is_small_at_large_N(valid_config_convergence):
    
    """ Tests that the error in m_z and m_x decreases as N increases in convergence_test
    
        GIVEN: a valid config dictionary for convergence_test, with h and Gamma different from zero (in order not to have zero thresholds)
        WHEN: convergence_test is called
        THEN: the error in m_z and m_x decreases as N increases, and is below 5% for the largest N
    """
    
    valid_config_convergence["mode_options"]["convergence_test"]["N_start"] = 500
    valid_config_convergence["mode_options"]["convergence_test"]["N_end"] = 100000
    valid_config_convergence["mode_options"]["convergence_test"]["N_step"] = 500
    valid_config_convergence["mode_options"]["convergence_test"]["output_file"] = "test_conv_large_N.csv"
    
    convergence_test(valid_config_convergence)
    
    output_path = os.path.join("results", "test_conv_large_N.csv")
    
    dataframe = pd.read_csv(output_path)
    
    last_row = dataframe.iloc[-1]
    
    assert last_row["error_m_z"] < 0.05 * abs(last_row["m_z"])
    assert last_row["error_m_x"] < 0.05 * abs(last_row["m_x"])
    
    if os.path.exists(output_path):
        os.remove(output_path)

def test_convergence_test_mean_error_decreases(valid_config_convergence):
    
    """ Tests that the mean error in m_z and m_x decreases as N increases in convergence_test
    
        GIVEN: a valid config dictionary for convergence_test, with h and Gamma different from zero (in order not to have zero thresholds)
        WHEN: convergence_test is called
        THEN: the mean error in m_z and m_x in the first half of the simulation is greater than the one in the second half of the simulation
    """
    
    valid_config_convergence["mode_options"]["convergence_test"]["N_start"] = 500
    valid_config_convergence["mode_options"]["convergence_test"]["N_end"] = 100000
    valid_config_convergence["mode_options"]["convergence_test"]["N_step"] = 500
    valid_config_convergence["mode_options"]["convergence_test"]["output_file"] = "test_conv_mean_error.csv"
    
    convergence_test(valid_config_convergence)
    
    output_path = os.path.join("results", "test_conv_mean_error.csv")
    
    dataframe = pd.read_csv(output_path)
    
    midpoint = len(dataframe) // 2
    
    errors_m_z_first_half = dataframe["error_m_z"].iloc[:midpoint].values
    errors_m_z_second_half = dataframe["error_m_z"].iloc[midpoint:].values
    errors_m_x_first_half = dataframe["error_m_x"].iloc[:midpoint].values
    errors_m_x_second_half = dataframe["error_m_x"].iloc[midpoint:].values
    
    mean_error_m_z_first_half = np.mean(errors_m_z_first_half)
    mean_error_m_z_second_half = np.mean(errors_m_z_second_half)
    mean_error_m_x_first_half = np.mean(errors_m_x_first_half)
    mean_error_m_x_second_half = np.mean(errors_m_x_second_half)
    
    assert mean_error_m_z_first_half > mean_error_m_z_second_half
    assert mean_error_m_x_first_half > mean_error_m_x_second_half
    
    if os.path.exists(output_path):
        os.remove(output_path)

def test_sweep_h(valid_config_sweep):

    """ Tests that the results of the sweep function with variable h are consistent with the analytical ones within a threshold of 5%

        GIVEN: a valid config dictionary for sweep with variable h
        WHEN: the sweep method is called with this config
        THEN: the estimated m_z and m_x values are close to the analytical ones within a threshold of 5%
        
        NOTE: Avoid the h = 0 point, where m_z = 0 to avoid having threshold equal to 0
    """
    
    valid_config_sweep["mode_options"]["sweep"]["variable"] = "h"
    valid_config_sweep["mode_options"]["sweep"]["variable_start"] = -1.0
    valid_config_sweep["mode_options"]["sweep"]["variable_end"] = 1.0
    valid_config_sweep["mode_options"]["sweep"]["variable_step"] = 0.4
    valid_config_sweep["mode_options"]["sweep"]["output_file"] = "test_sweep_h.csv"
    valid_config_sweep["simulation_params"]["N_runs"] = 100000
    valid_config_sweep["simulation_params"]["N_thermalization"] = 500
    
    sweep(valid_config_sweep)

    output_path = os.path.join("results", "test_sweep_h.csv")
    
    dataframe = pd.read_csv(output_path)
    
    evaluated_m_z = dataframe["m_z (MC)"].values
    analytical_m_z = dataframe["m_z (Analytical)"].values
    evaluated_m_x = dataframe["m_x (MC)"].values
    analytical_m_x = dataframe["m_x (Analytical)"].values
    
    errors_m_z = np.abs(evaluated_m_z - analytical_m_z)
    errors_m_x = np.abs(evaluated_m_x - analytical_m_x)
    
    assert (errors_m_z < 0.05 * np.abs(analytical_m_z)).all()
    assert (errors_m_x < 0.05 * np.abs(analytical_m_x)).all()
    
    os.remove(output_path)

def test_sweep_Gamma(valid_config_sweep):

    """ Tests that the results of the sweep function with variable Gamma are consistent with the analytical ones within a threshold of 5%

        GIVEN: a valid config dictionary for sweep with variable Gamma
        WHEN: the sweep method is called with this config
        THEN: the estimated m_z and m_x values are close to the analytical ones within a threshold of 5%
        
        NOTE: Avoid the Gamma = 0 point, where m_x = 0 to avoid having threshold equal to 0
    """
    
    valid_config_sweep["mode_options"]["sweep"]["variable"] = "Gamma"
    valid_config_sweep["mode_options"]["sweep"]["variable_start"] = -1.0
    valid_config_sweep["mode_options"]["sweep"]["variable_end"] = 1.0
    valid_config_sweep["mode_options"]["sweep"]["variable_step"] = 0.4
    valid_config_sweep["mode_options"]["sweep"]["output_file"] = "test_sweep_Gamma.csv"
    valid_config_sweep["simulation_params"]["N_runs"] = 100000
    valid_config_sweep["simulation_params"]["N_thermalization"] = 500
    
    sweep(valid_config_sweep)

    output_path = os.path.join("results", "test_sweep_Gamma.csv")
    
    dataframe = pd.read_csv(output_path)
    
    evaluated_m_z = dataframe["m_z (MC)"].values
    analytical_m_z = dataframe["m_z (Analytical)"].values
    evaluated_m_x = dataframe["m_x (MC)"].values
    analytical_m_x = dataframe["m_x (Analytical)"].values
    
    errors_m_z = np.abs(evaluated_m_z - analytical_m_z)
    errors_m_x = np.abs(evaluated_m_x - analytical_m_x)
    
    assert (errors_m_z < 0.05 * np.abs(analytical_m_z)).all()
    assert (errors_m_x < 0.05 * np.abs(analytical_m_x)).all()
    
    os.remove(output_path)


def test_sweep_beta(valid_config_sweep):

    """ Tests that the results of the sweep function with variable beta are consistent with the analytical ones within a threshold of 5%

        GIVEN: a valid config dictionary for sweep with variable beta
        WHEN: the sweep method is called with this config
        THEN: the estimated m_z and m_x values are close to the analytical ones within a threshold of 5%
    """
    
    valid_config_sweep["mode_options"]["sweep"]["variable"] = "beta"
    valid_config_sweep["mode_options"]["sweep"]["variable_start"] = 1.0
    valid_config_sweep["mode_options"]["sweep"]["variable_end"] = 5.0
    valid_config_sweep["mode_options"]["sweep"]["variable_step"] = 1.0
    valid_config_sweep["mode_options"]["sweep"]["output_file"] = "test_sweep_beta.csv"
    valid_config_sweep["simulation_params"]["N_runs"] = 100000
    valid_config_sweep["simulation_params"]["N_thermalization"] = 500
    
    sweep(valid_config_sweep)

    output_path = os.path.join("results", "test_sweep_beta.csv")
    
    dataframe = pd.read_csv(output_path)
    
    evaluated_m_z = dataframe["m_z (MC)"].values
    analytical_m_z = dataframe["m_z (Analytical)"].values
    evaluated_m_x = dataframe["m_x (MC)"].values
    analytical_m_x = dataframe["m_x (Analytical)"].values
    
    errors_m_z = np.abs(evaluated_m_z - analytical_m_z)
    errors_m_x = np.abs(evaluated_m_x - analytical_m_x)
    
    assert (errors_m_z < 0.05 * np.abs(analytical_m_z)).all()
    assert (errors_m_x < 0.05 * np.abs(analytical_m_x)).all()
    
    os.remove(output_path)

