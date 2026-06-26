import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_convergence(results_file: str = "convergence_test_results.csv"):
    """ 
        Plots the convergence test for the magnetizations
        
        PARAMETERS:
        results_file = name of the file with the required results (the file must be in the results directory)
    """
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    project_root = os.path.dirname(script_dir)
    
    data_dir = os.path.join(project_root, "results")
    
    file_path = os.path.join(data_dir, results_file)
    
    if not os.path.exists(file_path):
        print(f"Error: Results file '{file_path}' not found.")
        return
    
    dataframe = pd.read_csv(file_path)
    
    fig_m_z, plt_mz = plt.subplots(figsize=(8, 5))
    
    plt_mz.plot(dataframe["N"], dataframe["error_m_z"], label = "Simulation results", color = "blue")
    
    plt_mz.grid(True, which="both", linestyle="--", alpha=0.5)
    plt_mz.set_ylim(bottom=0)
    
    
    plt_mz.set_title("Convergence Test for $m_z$")
    plt_mz.set_ylabel("$|m_z(MC)-m_z(analytical)|$")
    plt_mz.set_xlabel("N")
    threshold = dataframe["threshold_m_z"].iloc[0]
    plt_mz.axhline(y=threshold, color="red", linestyle="--", label="Accuracy threshold")
    plt_mz.axhspan(0, threshold, color="red", alpha=0.15)
    
    plt_mz.legend()
    
    output_name_m_z = os.path.splitext(results_file)[0] + "_m_z"
    output_path_m_z = os.path.join(project_root, "results", f"{output_name_m_z}.png")
    fig_m_z.savefig(output_path_m_z, dpi=300)
    
    fig_m_x, plt_mx = plt.subplots(figsize=(8, 5))
    
    plt_mx.plot(dataframe["N"], dataframe["error_m_x"], label = "Simulation results", color = "blue")
    
    plt_mx.grid(True, which="both", linestyle="--", alpha=0.5)
    plt_mx.set_ylim(bottom=0)
    
    
    plt_mx.set_title("Convergence Test for $m_x$")
    plt_mx.set_ylabel("$|m_x(MC)-m_x(analytical)|$")
    plt_mx.set_xlabel("N")
    threshold = dataframe["threshold_m_x"].iloc[0]
    plt_mx.axhline(y=threshold, color="red", linestyle="--", label="Accuracy threshold")
    plt_mx.axhspan(0, threshold, color="red", alpha=0.15)
    
    plt_mx.legend()
    
    output_name_m_x = os.path.splitext(results_file)[0] + "_m_x"
    output_path_m_x = os.path.join(project_root, "results", f"{output_name_m_x}.png")
    fig_m_x.savefig(output_path_m_x, dpi=300)
    
    plt.show()
    


if __name__ == "__main__":
    plot_convergence()