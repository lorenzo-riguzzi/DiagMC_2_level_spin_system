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

def test_m_z_calculation():
    """Tests the estimator for the magnetization along the z axis of a diagram"""
    diagram = Diagram(beta = 1.0, s_0=1)
    assert diagram.evaluate_mz_of_diagram() == 1.0
    
    diagram = Diagram(beta = 1.0, s_0=-1)
    assert diagram.evaluate_mz_of_diagram() == -1.0
    
    diagram = Diagram(beta = 5.0, s_0=1, vertices=[1.0, 2.0, 3.0]) #tested with an already sorted list
    assert pytest.approx(diagram.evaluate_mz_of_diagram()) == 1.8
    
    diagram = Diagram(beta = 5.0, s_0=-1, vertices=[3.0, 1.0, 2.0]) #tested with an unsorted list   
    assert pytest.approx(diagram.evaluate_mz_of_diagram()) == -1.8

def test_m_x_calculation():
    """Tests the estimator for the magnetization along the x axis of a diagram"""
    diagram = Diagram(beta = 1.0, Gamma=0) #absence of field in the x direction
    assert diagram.evaluate_m_x_of_diagram() == 0.0 
    
    diagram = Diagram(beta = 1.0, Gamma=2.0) #absence of vertices
    assert diagram.evaluate_m_x_of_diagram() == 0
    
    diagram = Diagram(beta = 1.0, Gamma=2.0, vertices = [0.5, 0.7, 0.2])
    assert pytest.approx(diagram.evaluate_m_x_of_diagram()) == 1.5

def test_acceptance_rate_flip():
    """Tests for the acceptance rate of a spin flip. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 0.36787944117144
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 1

def test_acceptance_rate_add_segment():
    """Tests for the acceptance rate of adding a segment. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, segment_spin=-1, tau_after_f=2.0))  == 1
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, segment_spin=1, tau_after_f=2.0))  == 1
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, segment_spin=-1, tau_after_f=2.0))  == 0.84366175
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, segment_spin=1, tau_after_f=2.0))  == 0.46301139

def test_acceptance_rate_remove_segment():
    """Tests for the acceptance rate of removing a segment. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, segment_spin=-1, tau_after_f=2.0))  == 0.1481636
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, segment_spin=1, tau_after_f=2.0))  == 0.2699718
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, segment_spin=-1, tau_after_f=2.0))  == 0.59265458
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, segment_spin=1, tau_after_f=2.0))  == 1