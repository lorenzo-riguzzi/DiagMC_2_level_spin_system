import pytest
from scripts.diagram import Diagram

"""Tests for the Diagram class"""

def test_negative_beta():
    """Tests that a negative beta value raises a ValueError since beta is an inverse temperature"""
    with pytest.raises(ValueError):
        Diagram(beta=-1.0)
        
def test_zero_beta():
    """Tests that a zero beta value raises a ValueError since beta cannot be zero"""
    with pytest.raises(ValueError):
        Diagram(beta=0.0)

def test_s_0_value():
    """Tests that if s_0 is not -1 (spin down) or +1 (spin up) a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=0)
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=2)

def test_mz_calculation():
    """Tests the estimator for the magnetization along the z axis of a diagram"""
    diagram = Diagram(beta = 1.0, s_0=1)
    assert diagram.evaluate_mz_of_diagram() == 1.0
    
    diagram = Diagram(beta = 1.0, s_0=-1)
    assert diagram.evaluate_mz_of_diagram() == -1.0
    
    diagram = Diagram(beta = 5.0, s_0=1, vertices=[1, 2, 3])
    assert pytest.approx(diagram.evaluate_mz_of_diagram()) == 1.8

#NEED TO ADD THE TESTS FOR THE VALIDITY OF THE VERTICES (CORRECTLY SORTED AND ALL VERTICES LOWER THAN BETA)
