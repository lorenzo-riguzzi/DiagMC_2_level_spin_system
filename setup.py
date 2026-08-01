import os
from setuptools import setup, find_packages
import pathlib

# view filename
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def get_requirements():
    reqpath = pathlib.Path("./requirements.txt")
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
    entry_points={
        "console_scripts": [
            "diagmc = main:main",
        ],
    }
)