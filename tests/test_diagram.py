import os,sys,inspect

frame = inspect.currentframe()
assert frame is not None

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(frame)))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0,parent_dir) 

import pytest
from scripts.diagram import Diagram, Diagram_Random

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

def test_number_of_vertices_is_even():
    """Tests that if the number of vertices is odd, a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=1, vertices=[0.2, 0.5, 0.8])

def test_vertices_maximum():
    """Tests that if any vertex is greater than or equal to beta, a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.5, 1.0])
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.9, 1.5, 0.6, 0.2])

def test_vertices_minimum():
    """Tests that if any vertex is less than or equal to zero, a ValueError is raised"""
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.0, 0.5, 0.8, 0.9])
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[-0.1, 0.2, 0.3])

def test_vertices_sorting():
    """Tests that the vertices are correctly sorted when they are given in an unsorted way"""
    diagram = Diagram(beta=1.0, vertices=[0.5, 0.2, 0.8, 0.3])
    assert pytest.approx(diagram.vertices) == [0.2, 0.3, 0.5, 0.8]

def test_analytical_m_z():
    """Tests that the analytical value for the magnetization along the z axis is correctly calculated for a diagram with no vertices, which is the only case in which we can calculate it analytically"""
    diagram = Diagram(beta = 2.0)
    assert diagram.analytical_m_z() == 0
    
    diagram = Diagram(beta = 2.0, h = 0.6)
    assert pytest.approx(diagram.analytical_m_z()) == -0.833654607012
    
    diagram = Diagram(beta = 2.0, h = 0.6, Gamma = 0.8)
    assert pytest.approx(diagram.analytical_m_z()) == -0.578416548045
    
    diagram = Diagram(beta = 2.0, h = -0.6, Gamma = 0.8)
    assert pytest.approx(diagram.analytical_m_z()) == 0.578416548045

def test_analytical_m_x():
    """Tests that the analytical value for the magnetization along the x axis is correctly calculated for a diagram with no vertices, which is the only case in which we can calculate it analytically"""
    diagram = Diagram(beta = 2.0)
    assert diagram.analytical_m_x() == 0
    
    diagram = Diagram(beta = 2.0, Gamma = 0.6)
    assert pytest.approx(diagram.analytical_m_x()) == -0.833654607012
    
    diagram = Diagram(beta = 2.0, h = 0.8, Gamma = 0.6)
    assert pytest.approx(diagram.analytical_m_x()) == -0.578416548045
    
    diagram = Diagram(beta = 2.0, h = 0.8, Gamma = -0.6)
    assert pytest.approx(diagram.analytical_m_x()) == 0.578416548045

def test_m_z_calculation():
    """Tests the estimator for the magnetization along the z axis of a diagram"""
    diagram = Diagram(beta = 1.0, s_0=1)
    assert diagram.evaluate_m_z_of_diagram() == 1.0
    
    diagram = Diagram(beta = 1.0, s_0=-1)
    assert diagram.evaluate_m_z_of_diagram() == -1.0
    
    diagram = Diagram(beta = 5.0, s_0=1, vertices=[1.0, 2.0, 3.0, 3.5]) #tested with an already sorted list
    assert pytest.approx(diagram.evaluate_m_z_of_diagram()) == 0.4
    
    diagram = Diagram(beta = 5.0, s_0=-1, vertices=[3.0, 1.0, 3.5, 2.0]) #tested with an unsorted list   
    assert pytest.approx(diagram.evaluate_m_z_of_diagram()) == -0.4

def test_m_x_calculation():
    """Tests the estimator for the magnetization along the x axis of a diagram"""
    diagram = Diagram(beta = 1.0, Gamma=0, vertices = [0.2, 0.3]) #absence of field in the x direction
    assert diagram.evaluate_m_x_of_diagram() == 0.0 
    
    diagram = Diagram(beta = 1.0, Gamma=2.0) #absence of vertices
    assert diagram.evaluate_m_x_of_diagram() == 0
    
    diagram = Diagram(beta = 1.0, Gamma=2.0, vertices = [0.5, 0.7, 0.2, 0.8])
    assert pytest.approx(diagram.evaluate_m_x_of_diagram()) == -2.0

def test_acceptance_rate_flip():
    """Tests for the acceptance rate of a spin flip. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 0.3678794412
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 1

def test_acceptance_rate_add_segment():
    """Tests for the acceptance rate of adding a segment. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=-1))  == 1
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=1))  == 1
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=-1))  == 0.6749294
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=1))  == 0.3704091103
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[1.0, 1.5, 1.8, 2.0, 3.0, 4.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_add_segment(tau_i=4.2, tau_f = 4.8, tau_after_f=5.0, segment_spin=1))  == 0.3136066492


def test_acceptance_rate_remove_segment():
    """Tests for the acceptance rate of removing a segment. Ensure that the calculation is done correctly"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=-1))  == 0.2222454
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=2.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=1))  == 0.4049577
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=-1))  == 0.88898187
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=1.5, tau_f = 1.8, tau_after_f=2.0, segment_spin=1))  == 1
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=3.0, tau_f = 4.0, tau_after_f=4.5, segment_spin=-1))  == 0.2452529608
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    assert pytest.approx(diagram.acceptance_rate_remove_segment(tau_i=4.5, tau_f = 4.7, tau_after_f=5.0, segment_spin=-1))  == 0.9824769037


def test_try_flip_spin():
    """Tests that the try_flip_spin method correctly updates the diagram"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma = 1.0)
    
    with pytest.raises(ValueError):
        diagram.try_flip_spin(2.3) #Ensures a ValueError is raised if the random number is greater than 1
    
    diagram.try_flip_spin(0.37)
    assert diagram.s_0 == -1 #Ensures that the spin is not flipped since the acceptance rate is 0.0001234098041
    
    diagram.try_flip_spin(0.36)
    assert diagram.s_0 == 1 #Ensures that the spin is flipped since the acceptance rate is 0.0001234098041


def test_try_add_segment():
    """Tests that the try_add_segment method correctly updates the diagram"""
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_add_segment(1.2, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1) #Ensures a ValueError is raised if the random number is greater than 1
    
    with pytest.raises(ValueError):
        diagram.try_add_segment(0.5, tau_f=1.5, tau_i=1.8, tau_after_f=2.0, index=1) #Ensures a ValueError is raised if tau_f < tau_i
    
    with pytest.raises(ValueError): 
        diagram.try_add_segment(0.5, tau_f=1.8, tau_i=1.5, tau_after_f=1.6, index=1) #Ensures a ValueError is raised if tau_after_f < tau_f
    
    diagram.try_add_segment(0.7, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 3.0, 4.0] #Ensures that the segment is not added since the acceptance rate is 0.6749294
    
    diagram.try_add_segment(0.6, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0] #Ensures that the segment is added since the acceptance rate is 0.6749294
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.7 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 6 #Ensures that the number of vertices is correctly updated
    
    """check how the method works when the segment is added at the end of the list
    Ensures that, finding tau_after_f and index in the same way in which they are found int he random method random_try_add_segment, they are chosen correctly to be beta and number_vertices """
    
    tau_i = 4.2
    tau_f = 4.8
    index, tau_after_f = next(((i, tau) for i, tau in enumerate(diagram.vertices) if tau > tau_i), (diagram.number_vertices, diagram.beta))
    
    diagram.try_add_segment(0.32, tau_f, tau_i, tau_after_f, index)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0] #Ensures that the segment is not added since the acceptance rate is 0.3136066492
        
    diagram.try_add_segment(0.3, tau_f, tau_i, tau_after_f, index)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0, 4.2, 4.8] #Ensures that the segment is added since the acceptance rate is 0.3136066492
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 2.3 
    
    assert diagram.number_vertices == 8

def test_try_remove_segment():
    """Tests that the try_remove_segment method correctly updates the diagram"""
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(1.2, remove_index=2) #Ensures a ValueError is raised if the random number is greater than 1
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=-2) #Ensures a ValueError is raised if the remove index is negative
    
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=5) #Ensures a ValueError is raised if the remove index is the last index of the list
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=7) #Ensures a ValueError is raised if the remove index is greater than the last index of the list
    
    diagram.try_remove_segment(0.25, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 3.0, 4.0, 4.5, 4.7] #Ensures that the segment is not removed since the acceptance rate is 0.2452529608
    
    diagram.try_remove_segment(0.24, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 4.5, 4.7] #Ensures that the segment is removed since the acceptance rate is 0.2452529608
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.2 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 4 #Ensures that the number of vertices is correctly updated
    
    """We ensure that, if we remove the last possible segment, tau_after_f = beta """
    
    diagram.try_remove_segment(0.99, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 4.5, 4.7] #Ensures that the segment is not removed since the acceptance rate is 0.9824769037
    
    diagram.try_remove_segment(0.98, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0] #Ensures that the segment is removed since the acceptance rate is 0.982476903
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.0 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 2 #Ensures that the number of vertices is correctly updated


""" Tests for the Diagram_Random class """

def test_random_try_spin_flip():
    """Asserts that the random_try_spin_flip method is deterministic once the seed is fixed """
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_spin_flip()
    diagram2.random_try_spin_flip()
    
    assert diagram1.s_0 == diagram2.s_0

def test_random_try_add_segment():
    """Asserts that the random_try_add_segment method is deterministic once the seed is fixed """
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_add_segment()
    diagram2.random_try_add_segment()
    
    assert pytest.approx(diagram1.vertices) == diagram2.vertices

def test_random_try_remove_segment():
    """Checks that nothing happens if we start with a diagram with no vertices"""
    
    diagram = Diagram_Random(beta = 5.0, s_0= -1, h=0.5, Gamma=1.0, seed_number=42)
    
    diagram.random_try_remove_segment() 
    assert diagram.vertices == []
    
    """Asserts that the random_try_remove_segment method is deterministic once the seed is fixed """
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, vertices = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],  h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, vertices = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],  h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_remove_segment()
    diagram2.random_try_remove_segment()
    
    assert pytest.approx(diagram1.vertices) == diagram2.vertices

def test_chose_update():
    """Asserts that the chose_update method is deterministic once the seed is fixed """
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.chose_update()
    diagram2.chose_update()
    
    assert diagram1.s_0 == diagram2.s_0
    assert pytest.approx(diagram1.vertices) == diagram2.vertices
    
    diagram1.chose_update()
    diagram2.chose_update()
    
    assert diagram1.s_0 == diagram2.s_0
    assert pytest.approx(diagram1.vertices) == diagram2.vertices
    
    diagram1.chose_update()
    diagram2.chose_update()
    
    assert diagram1.s_0 == diagram2.s_0
    assert pytest.approx(diagram1.vertices) == diagram2.vertices