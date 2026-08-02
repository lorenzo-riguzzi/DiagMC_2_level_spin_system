import os
from setuptools import setup, find_packages
import pathlib


""" Setup script to install all the required dependencies for the simulation.
    The required packages are read from the requirements.txt file (DO NOT DELETE IT!).
    The script generates the diagmc command to run the simulation from command line (see documentation for details).
"""

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()

def get_requirements():
    reqpath = pathlib.Path("./requirements.txt")
    
    if not reqpath.exists():
        return []
    
    return [line.strip() for line in reqpath.read_text().splitlines() if line.strip()]

project_name = "diagmc"

setup(
    name = project_name,
    version = "0.1.0",
    author = "Lorenzo Riguzzi",
    author_email = "loririguz2002@gmail.com",
    description = "Diagrammatic Monte Carlo simulation of a 2 level spin system",
    url = "https://github.com/lorenzo-riguzzi/DiagMC_2_level_spin_system",
    packages=find_packages(),
    install_requires= get_requirements(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "diagmc = diagmc.__main__:main",
        ],
    }
)