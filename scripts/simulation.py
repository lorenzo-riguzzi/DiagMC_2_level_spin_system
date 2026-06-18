from scripts.diagram import Diagram_Random
import time
import pandas as pd
import os

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
    
    print("\n" + f"Running the Monte Carlo simulation for {N_runs} runs...")
    
    for i in range(N_runs):
        diagram.chose_update()
        sum_m_z += diagram.evaluate_m_z_of_diagram()
        sum_m_x += diagram.evaluate_m_x_of_diagram()
    
    simulation_time = time.perf_counter() - start_time
    
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
    """ Execute a convergence test for the Monte Carlo simulation and prints the results on terminal
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
    
    if abs(analytical_m_z) < 1e-9: 
        print("m_z is too small to define a relative error. The threshold will be automatically set to 0.01")
        
    if abs(analytical_m_x) < 1e-9:
        print("m_x is too small to define a relative error. The threshold will be automatically set to 0.01")

    N_thermalization = simulation_params["N_thermalization"]
    
    convergence_test_params = config["mode_options"]["convergence_test"]
    
    N_start = convergence_test_params["N_start"]
    N_end = convergence_test_params["N_end"]
    N_step = convergence_test_params["N_step"]
    accuracy = convergence_test_params["accuracy"]
    output_name_m_z = convergence_test_params["output_file_m_z"]
    output_name_m_x = convergence_test_params["output_file_m_x"]
    
    threshold_m_z = 0.01 if abs(analytical_m_z) < 1e-9 else abs(analytical_m_z) * accuracy
    threshold_m_x = 0.01 if abs(analytical_m_x) < 1e-9 else abs(analytical_m_x) * accuracy

    if N_thermalization < 0:
        raise ValueError("N_thermalization must be a non-negative integer.")
    if N_start <= 0 or N_end <= 0 or N_step <= 0:
        raise ValueError("N_start, N_end and N_step must be positive non-null integers.")
    
    data_m_z = []
    data_m_x = []
    
    performed_runs = 0
    
    sum_m_z = 0.0
    sum_m_x = 0.0
    
    for i in range(N_thermalization):
            diagram.chose_update()
    
    for N in range(N_start, N_end + 1, N_step): 
        
        steps_to_run = N_start if performed_runs == 0 else N_step
        
        for i in range(steps_to_run):
            diagram.chose_update()
            sum_m_z += diagram.evaluate_m_z_of_diagram()
            sum_m_x += diagram.evaluate_m_x_of_diagram()
        
        performed_runs += steps_to_run
        
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
    
    print("CONVERGENCE TEST PERFORMED SUCCESSFULLY!")
