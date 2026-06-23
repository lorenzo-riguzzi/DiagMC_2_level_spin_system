from scripts.diagram import Diagram_Random
import time
import pandas as pd
import os
import numpy as np

def single_run(config: dict) -> None:
    """ Execute a single Monte Carlo run and prints the results on terminal
        Takes the parameters from the config.yaml file
    """
    
    diagram_params = config["diagram_params"]
    simulation_params = config["simulation_params"]
    
    diagram = Diagram_Random(
        beta = diagram_params["beta"], 
        s_0 = diagram_params["s_0"],
        vertices = diagram_params.get("vertices", []),
        h = diagram_params["h"], 
        Gamma = diagram_params["Gamma"], 
        seed_number = diagram_params["seed_number"]
    )
    
    analytical_m_z = diagram.analytical_m_z()
    analytical_m_x = diagram.analytical_m_x()
    
    N_thermalization = simulation_params["N_thermalization"]
    N_runs = simulation_params["N_runs"]
    
    if N_thermalization < 0:
        raise ValueError("N_thermalization must be a non-negative integer.")
    if N_runs <= 0:
        raise ValueError("N_runs must be a positive non-null integer.")
    
    print("\n" + f"Ignoring the first {N_thermalization} runs to thermalize the system...")
    
    start_time = time.perf_counter()
    
    for i in range(N_thermalization):
        diagram.chose_update() 
    
    thermalization_time = time.perf_counter() - start_time
    print("\n" + f"Thermalization completed in {thermalization_time:.2f} seconds.")
    
    sum_m_z = 0.0
    sum_m_x = 0.0
    
    start_MC = time.perf_counter()
    
    print("\n" + f"Running the Monte Carlo simulation for {N_runs} runs...")
    
    for i in range(N_runs):
        diagram.chose_update()
        sum_m_z += diagram.evaluate_m_z_of_diagram()
        sum_m_x += diagram.evaluate_m_x_of_diagram()
    
    simulation_time = time.perf_counter() - start_MC
    
    print("\n" + f"Simulation completed in {simulation_time:.2f} seconds.")
    
    average_m_z = sum_m_z / N_runs
    average_m_x = sum_m_x / N_runs
    
    print("\n" + "="*59)
    print("        DIAGRAMMATIC MONTE CARLO: SINGLE RUN RESULTS")
    print("="*59)
    print(f"Observable |  MC Estimate  |  Analytical  |  Abs Difference")
    print("-"*59)
    print(f"   m_z     |  {average_m_z:11.5f}  |  {analytical_m_z:10.5f}  |  {abs(average_m_z - analytical_m_z):9.5f}")
    print(f"   m_x     |  {average_m_x:11.5f}  |  {analytical_m_x:10.5f}  |  {abs(average_m_x - analytical_m_x):9.5f}")
    print("="*59 + "\n")


def convergence_test(config: dict) -> None:
    """ Execute a convergence test for the Monte Carlo simulation and prints the results in .csv format
        Takes the parameters from the config.yaml file
    """
    
    diagram_params = config["diagram_params"]
    simulation_params = config["simulation_params"]
    
    diagram = Diagram_Random(
        beta = diagram_params["beta"], 
        s_0 = diagram_params["s_0"],
        vertices = diagram_params.get("vertices", []),
        h = diagram_params["h"], 
        Gamma = diagram_params["Gamma"], 
        seed_number = diagram_params["seed_number"]
    )
    
    analytical_m_z = diagram.analytical_m_z()
    analytical_m_x = diagram.analytical_m_x()
    
    if abs(analytical_m_z) < 1e-7: 
        print("m_z is too small to define a relative error. The threshold will be automatically set to 1e-6")
        
    if abs(analytical_m_x) < 1e-7:
        print("m_x is too small to define a relative error. The threshold will be automatically set to 1e-6")

    N_thermalization = simulation_params["N_thermalization"]
    
    convergence_test_params = config["mode_options"]["convergence_test"]
    
    N_start = convergence_test_params["N_start"]
    N_end = convergence_test_params["N_end"]
    N_step = convergence_test_params["N_step"]
    accuracy = convergence_test_params["accuracy"]
    output_name_m_z = convergence_test_params["output_file_m_z"]
    output_name_m_x = convergence_test_params["output_file_m_x"]
    
    threshold_m_z = 1e-6 if abs(analytical_m_z) < 1e-7 else abs(analytical_m_z) * accuracy
    threshold_m_x = 1e-6 if abs(analytical_m_x) < 1e-7 else abs(analytical_m_x) * accuracy

    if N_thermalization < 0:
        raise ValueError("N_thermalization must be a non-negative integer.")
    if N_start <= 0 or N_end <= 0 or N_step <= 0:
        raise ValueError("N_start, N_end and N_step must be positive non-null integers.")
    if N_start > N_end:
        raise ValueError("N_start must be less than or equal to N_end.")
    
    data_m_z = []
    data_m_x = []
    
    performed_runs = 0
    
    sum_m_z = 0.0
    sum_m_x = 0.0
    performed_runs = 0
    
    start_time = time.perf_counter()
    
    for i in range(N_thermalization):
            diagram.chose_update()
    
    for N in range(1, N_end + 1): 
        
        diagram.chose_update()
        performed_runs += 1
        
        sum_m_z += diagram.evaluate_m_z_of_diagram()
        sum_m_x += diagram.evaluate_m_x_of_diagram()
        
        if N == N_start or (N > N_start and (N - N_start) % N_step == 0):
        
            average_m_z = sum_m_z / performed_runs
            average_m_x = sum_m_x / performed_runs
            
            error_m_z = abs(average_m_z - analytical_m_z)
            error_m_x = abs(average_m_x - analytical_m_x)
            
            data_row_m_z ={
                "N": N,
                "m_z": average_m_z,
                "error": error_m_z
            }

            data_row_m_x ={
                "N": N,
                "m_x": average_m_x,
                "error": error_m_x
            }
            
            data_m_z.append(data_row_m_z)
            data_m_x.append(data_row_m_x)
    
    data_frame_m_z = pd.DataFrame(data_m_z)
    data_frame_m_x = pd.DataFrame(data_m_x)
    
    output_dir = "results" 
    os.makedirs(output_dir, exist_ok=True)    
    
    output_file_m_z = os.path.join(output_dir, output_name_m_z)
    data_frame_m_z.to_csv(output_file_m_z, index=False)
    output_file_m_x = os.path.join(output_dir, output_name_m_x) 
    data_frame_m_x.to_csv(output_file_m_x, index=False)
    
    failed_convergence_m_z = data_frame_m_z[data_frame_m_z["error"] > threshold_m_z]
    failed_convergence_m_x = data_frame_m_x[data_frame_m_x["error"] > threshold_m_x]
    
    if failed_convergence_m_z.empty:
        print('\n' + f"m_z converged successfully within the threshold of {accuracy*100:.2f}%.")
    else:
        last_failed_index_m_z = failed_convergence_m_z.index[-1]
        if last_failed_index_m_z == len(data_frame_m_z) - 1:
            print('\n' + f"m_z did not converge within the threshold of {accuracy*100:.2f}% within {N_end} runs. Increase N_end or decrease the accuracy threshold.")
        else:
            convergence_point_m_z = data_frame_m_z.loc[last_failed_index_m_z + 1, "N"] 
            print('\n' + f"m_z converged successfully within the threshold of {accuracy*100:.2f}% after {convergence_point_m_z} runs.")
    
    if failed_convergence_m_x.empty:
        print('\n' + f"m_x converged successfully within the threshold of {accuracy*100:.2f}%.")
    else:
        last_failed_index_m_x = failed_convergence_m_x.index[-1]
        if last_failed_index_m_x == len(data_frame_m_x) - 1:
            print('\n' + f"m_x did not converge within the threshold of {accuracy*100:.2f}% within {N_end} runs. Increase N_end or decrease the accuracy threshold.")
        else:
            convergence_point_m_x = data_frame_m_x.loc[last_failed_index_m_x + 1, "N"] 
            print('\n' + f"m_x converged successfully within the threshold of {accuracy*100:.2f}% after {convergence_point_m_x} runs.")
    
    convergence_test_time = time.perf_counter() - start_time

    print('\n' + f"Convergence test performed successfully in {convergence_test_time:.2f} seconds!" + "\n")

def sweep(config: dict) -> None:
    """ Performs the MC simulation for different values of the variable chosen in the config.yaml file (beta, Gamma, h).
        Prints the results in .csv format.
        Takes the input parameters from the config.yaml file
    """
    
    diagram_params = config["diagram_params"]
    simulation_params = config["simulation_params"]
    
    N_thermalization = simulation_params["N_thermalization"]
    N_runs = simulation_params["N_runs"]
    
    if N_thermalization < 0:
        raise ValueError("N_thermalization must be a non-negative integer.")
    if N_runs <= 0:
        raise ValueError("N_runs must be a positive non-null integer.")
    
    sweep_params = config["mode_options"]["sweep"]
    
    sweep_variable = sweep_params["variable"]
    sweep_start = sweep_params["variable_start"]
    sweep_end = sweep_params["variable_end"]
    sweep_step = sweep_params["variable_step"]
    output_name_m_z = sweep_params["output_file_m_z"]
    output_name_m_x = sweep_params["output_file_m_x"]
    
    if sweep_variable not in ["beta", "Gamma", "h"]:
        raise ValueError("Invalid sweep variable. Must be one of 'beta', 'Gamma' or 'h'.")
    if sweep_end <= sweep_start:
        raise ValueError("sweep_end must be greater than sweep_start.")
    if sweep_step <= 0:
        raise ValueError("sweep_step must be a positive non-null number.")
    
    sweep_values = np.arange(sweep_start, sweep_end + sweep_step, sweep_step)
    
    data_m_z = []
    data_m_x = []
    
    start_time = time.perf_counter()
    
    for value in sweep_values:
        
        diagram = Diagram_Random(
        beta = diagram_params["beta"], 
        s_0 = diagram_params["s_0"],
        vertices = diagram_params.get("vertices", []),
        h = diagram_params["h"], 
        Gamma = diagram_params["Gamma"], 
        seed_number = diagram_params["seed_number"]
        )
        
        setattr(diagram, sweep_variable, value)
        
        analytical_m_z = diagram.analytical_m_z()
        analytical_m_x = diagram.analytical_m_x()
        
        for i in range(N_thermalization):
            diagram.chose_update()
        
        sum_m_z = 0.0
        sum_m_x = 0.0
        
        for i in range(N_runs):
            diagram.chose_update()
            sum_m_z += diagram.evaluate_m_z_of_diagram()
            sum_m_x += diagram.evaluate_m_x_of_diagram()
        
        average_m_z = sum_m_z / N_runs
        average_m_x = sum_m_x / N_runs
        
        fixed_params = {
            param: getattr(diagram, param) for param in ["beta", "h", "Gamma"] if param != sweep_variable
        }
        
        
        data_row_m_z ={
                sweep_variable: value,
                "m_z (MC)": average_m_z,
                "m_z (Analytical)": analytical_m_z,
                **fixed_params
            }
        
        data_row_m_x ={
                sweep_variable: value,
                "m_x (MC)": average_m_x,
                "m_x (Analytical)": analytical_m_x,
                **fixed_params
            }
        
        data_m_z.append(data_row_m_z)
        data_m_x.append(data_row_m_x)
    
    sweep_time = time.perf_counter() - start_time
    
    print("\n" + f"Sweep over the variable {sweep_variable} performed successfully in {sweep_time:.2f} seconds.")
    
    data_frame_m_z = pd.DataFrame(data_m_z)
    data_frame_m_x = pd.DataFrame(data_m_x)
    
    output_dir = "results" 
    os.makedirs(output_dir, exist_ok=True)    
    
    output_file_m_z = os.path.join(output_dir, output_name_m_z)
    data_frame_m_z.to_csv(output_file_m_z, index=False)
    output_file_m_x = os.path.join(output_dir, output_name_m_x) 
    data_frame_m_x.to_csv(output_file_m_x, index=False)
    
    print("\n" + f"Sweep results saved successfully in '{output_dir}' directory as '{output_name_m_z}' and '{output_name_m_x}'" + "\n")
