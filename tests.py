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

def test_vertices_maximum():
    """Tests that if any vertex is greater than or equal to beta, a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.5, 1.0])
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.9, 1.5, 0.6])

def test_vertices_minimum():
    """Tests that if any vertex is less than or equal to zero, a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.0, 0.5, 0.8])
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[-0.1, 0.2, 0.3])

def test_vertices_sorting():
    """Tests that the vertices are correctly sorted when they are given in an unsorted way"""
    diagram = Diagram(beta=1.0, vertices=[0.5, 0.2, 0.8, 0.3])
    assert pytest.approx(diagram.vertices) == [0.2, 0.3, 0.5, 0.8]

def test_mz_calculation():
    """Tests the estimator for the magnetization along the z axis of a diagram"""
    diagram = Diagram(beta = 1.0, s_0=1)
    assert diagram.evaluate_mz_of_diagram() == 1.0
    
    diagram = Diagram(beta = 1.0, s_0=-1)
    assert diagram.evaluate_mz_of_diagram() == -1.0
    
    diagram = Diagram(beta = 5.0, s_0=1, vertices=[1.0, 2.0, 3.0]) #tested with an already sorted list
    assert pytest.approx(diagram.evaluate_mz_of_diagram()) == 1.8
    
    diagram = Diagram(beta = 5.0, s_0=-1, vertices=[3.0, 1.0, 2.0]) #tested with an unsorted list   
    assert pytest.approx(diagram.evaluate_mz_of_diagram()) == -1.8
