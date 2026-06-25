import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_convergence(results_file: str = "convergence_test_results_m_x.csv"):
    """ 
        Plots the convergence test for the magnetizations (m_x or m_z depending on which is specified)
        
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
    
    plt.figure(figsize=(8, 5))
    
    plt.plot(dataframe["N"], dataframe["error"], label = "Simulation results", color = "blue")
    
    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.ylim(bottom=0)
    
    if "m_z" in dataframe.columns:
        plt.title("Convergence Test for $m_z$")
        plt.ylabel("$|m_z(MC)-m_z(analytical)|$")
        plt.xlabel("N")
        threshold = dataframe["threshold"].iloc[0]
        plt.axhline(y=threshold, color="red", linestyle="--", label="Accuracy threshold")
        plt.axhspan(0, threshold, color="red", alpha=0.15)
    elif "m_x" in dataframe.columns:
        plt.title("Convergence Test for $m_x$")
        plt.ylabel("$|m_x(MC)-m_x(analytical)|$")
        plt.xlabel("N")
        threshold = dataframe["threshold"].iloc[0]
        plt.axhline(y=threshold, color="red", linestyle="--", label="Accuracy threshold")
        plt.axhspan(0, threshold, color="red", alpha=0.15)
    else:
        print("Error: The results file does not contain the required columns for plotting.")
        return
    
    output_name = os.path.splitext(results_file)[0]
    output_path = os.path.join(project_root, "results", f"{output_name}.png")
    plt.savefig(output_path, dpi=300)
    
    plt.legend()
    plt.show()
    


if __name__ == "__main__":
    plot_convergence()