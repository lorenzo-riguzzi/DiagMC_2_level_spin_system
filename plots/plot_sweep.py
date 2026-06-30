import os
import pandas as pd
import matplotlib.pyplot as plt
import sys

def plot_sweep(results_file: str = "sweep_h.csv"):
    """
        Plots the results of the sweep simulation
        
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
    
    variable_name = dataframe.columns[0]
    
    fixed_var_1_name = dataframe.columns[5]
    fixed_var_1_value = dataframe[fixed_var_1_name].iloc[1]
    
    fixed_var_2_name = dataframe.columns[6]
    fixed_var_2_value = dataframe[fixed_var_2_name].iloc[1]
    
    fig_m_z, plt_mz = plt.subplots(figsize=(8, 5))
    
    plt_mz.scatter(dataframe[variable_name], dataframe["m_z (MC)"], label = "MC", color = "blue", s = 20)
    plt_mz.plot(dataframe[variable_name], dataframe["m_z (Analytical)"], label = "Analytical", color = "blue")
    
    plt_mz.grid(True, which="both", linestyle="--", alpha=0.5)
    
    """ The following dictionary is needed only to be able to plot beta and Gamma as greek letters in the plot while keeping h a normal letter """
    
    symbols = {
        "Gamma": r"\Gamma",
        "beta": r"\beta",
        "h": "h"
    }
    
    variable_symbol = symbols[variable_name]
    fix_var_1_symbol = symbols[fixed_var_1_name]
    fix_var_2_symbol = symbols[fixed_var_2_name]
    
    plt_mz.set_title(f"Sweep results over ${variable_symbol}$ of $m_z$ for ${fix_var_1_symbol}={fixed_var_1_value}$ and ${fix_var_2_symbol}={fixed_var_2_value}$")
    plt_mz.set_ylabel("$m_z$")
    plt_mz.set_xlabel(f"${variable_symbol}$")
    
    plt_mz.legend()
    
    output_name_m_z = os.path.splitext(results_file)[0] + "_m_z"
    output_path_m_z = os.path.join(project_root, "results", f"{output_name_m_z}.png")
    fig_m_z.savefig(output_path_m_z, dpi=300)
    
    fig_m_x, plt_mx = plt.subplots(figsize=(8, 5))
    
    plt_mx.scatter(dataframe[variable_name], dataframe["m_x (MC)"], label = "MC", color = "blue", s = 20)
    plt_mx.plot(dataframe[variable_name], dataframe["m_x (Analytical)"], label = "Analytical", color = "blue")
    
    plt_mx.grid(True, which="both", linestyle="--", alpha=0.5)
    
    plt_mx.set_title(f"Sweep results over ${variable_symbol}$ of $m_x$ for ${fix_var_1_symbol}={fixed_var_1_value}$ and ${fix_var_2_symbol}={fixed_var_2_value}$")
    plt_mx.set_ylabel("$m_x$")
    plt_mx.set_xlabel(f"${variable_symbol}$")
    
    plt_mx.legend()
    
    output_name_m_x = os.path.splitext(results_file)[0] + "_m_x"
    output_path_m_x = os.path.join(project_root, "results", f"{output_name_m_x}.png")
    fig_m_x.savefig(output_path_m_x, dpi=300)
    
    plt.show()
    
if __name__ == "__main__":
    if len(sys.argv) > 1:
        results_file = sys.argv[1]
        plot_sweep(results_file)
    else:
        plot_sweep()

