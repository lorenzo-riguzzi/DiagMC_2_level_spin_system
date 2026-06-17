from scripts.diagram import Diagram_Random
import time

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

