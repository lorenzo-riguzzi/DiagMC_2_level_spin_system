import pytest
from scripts.diagram import Diagram, Diagram_Random

"""Tests for the Diagram class"""

def test_negative_beta():
    
    """ Tests that a negative beta value raises a ValueError since beta is an inverse temperature

        GIVEN: a diagram with a negative value of beta
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since beta must be positive
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=-1.0)
        
def test_zero_beta():
    
    """ Tests that a zero beta value raises a ValueError since beta cannot be zero

        GIVEN: a diagram with a zero value of beta
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since beta must be greater than zero
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=0.0)

def test_s_0_equal_0():
    
    """ Tests that if s_0 is 0 a ValueError is raised

        GIVEN: a diagram with s_0 equal to 0
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since s_0 must be either -1 or +1
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=0)

def test_s_0_greater_than_1():
    
    """ Tests that if s_0 is greater than 1 a ValueError is raised

        GIVEN: a diagram with s_0 greater than 1
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since s_0 must be either -1 or +1
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=2)
        
def test_s_0_lower_than_minus_1():
    
    """ Tests that if s_0 is lower than -1 a ValueError is raised

        GIVEN: a diagram with s_0 lower than -1
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since s_0 must be either -1 or +1
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=-2)

def test_number_of_vertices_is_even():
    
    """ Tests that if the number of vertices is odd, a ValueError is raised

        GIVEN: a diagram with an odd number of vertices
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since the number of vertices must be even (diagrams with odd number of vertices have weight equal to zero)
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, s_0=1, vertices=[0.2, 0.5, 0.8])

def test_max_vertex_equal_beta():
    
    """ Tests that if any vertex is equal to beta, a ValueError is raised

        GIVEN: a diagram with a vertex equal to beta
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since every vertex must be lower than beta
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.5, 1.0])

def test_max_vertex_greater_than_beta():
    
    """ Tests that if any vertex is greater than beta, a ValueError is raised

        GIVEN: a diagram with a vertex greater than beta
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since every vertex must be lower than beta
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.9, 1.5, 0.6, 0.2])

def test_min_vertex_equal_zero():
    
    """ Tests that if any vertex is equal to zero, a ValueError is raised

        GIVEN: a diagram with a vertex equal to zero
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since every vertex must be positive
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[0.0, 0.5, 0.8, 0.9])

def test_min_vertex_less_than_zero():
    
    """ Tests that if any vertex is lower than zero, a ValueError is raised

        GIVEN: a diagram with a vertex lower than zero
        WHEN: the diagram constructor is called
        THEN: a ValueError is raised since every vertex must be positive
    """
    
    with pytest.raises(ValueError):
        Diagram(beta=1.0, vertices=[-0.1, 0.2, 0.3])

def test_vertices_sorting():
    
    """ Tests that the vertices are correctly sorted when they are given in an unsorted way to create a diagram
    
        GIVEN: a diagram with an unsorted list of vertices
        WHEN: the diagram constructor is called
        THEN: the vertices are sorted in ascending order
    """
    
    diagram = Diagram(beta=1.0, vertices=[0.5, 0.2, 0.8, 0.3])
    assert pytest.approx(diagram.vertices) == [0.2, 0.3, 0.5, 0.8]
    
def test_analytical_m_z_is_zero_for_zero_fields():
    
    """ Tests that the analytical value for m_z in the case of absent fields is correctly set to zero
        
            GIVEN: a diagram with h = Gamma = 0 and a certain beta
            WHEN: the analytical_m_z method is called
            THEN: the analytical value for the magnetization along the z axis is correctly set to 0
    """
    
    diagram = Diagram(beta = 2.0)
    assert diagram.analytical_m_z() == 0

def test_analytical_m_z():
    
    """ Tests that the analytical value for the magnetization along the z axis is correctly calculated
    
        GIVEN: a diagram with different values of beta, h and Gamma
        WHEN: the analytical_m_z method is called
        THEN: the analytical value for the magnetization along the z axis is correctly calculated
    """
    
    diagram = Diagram(beta = 2.0, h = 0.6)
    assert pytest.approx(diagram.analytical_m_z()) == -0.833654607012
    
    diagram = Diagram(beta = 2.0, h = 0.6, Gamma = 0.8)
    assert pytest.approx(diagram.analytical_m_z()) == -0.578416548045
    
    diagram = Diagram(beta = 2.0, h = -0.6, Gamma = 0.8)
    assert pytest.approx(diagram.analytical_m_z()) == 0.578416548045
    
def test_analytical_m_x_is_zero_for_zero_fields():
    
    """ Tests that the analytical value for m_x in the case of absent fields is correctly set to zero
            
                GIVEN: a diagram with h = Gamma = 0 and a certain beta
                WHEN: the analytical_m_x method is called
                THEN: the analytical value for the magnetization along the x axis is correctly set to 0
        """
    
    diagram = Diagram(beta = 2.0)
    assert diagram.analytical_m_x() == 0

def test_analytical_m_x():
    
    """ Tests that the analytical value for the magnetization along the x axis is correctly calculated

        GIVEN: a diagram with different values of beta, h and Gamma
        WHEN: the analytical_m_x method is called
        THEN: the analytical value for the magnetization along the x axis is correctly calculated
    """
    
    diagram = Diagram(beta = 2.0, Gamma = 0.6)
    assert pytest.approx(diagram.analytical_m_x()) == -0.833654607012
    
    diagram = Diagram(beta = 2.0, h = 0.8, Gamma = 0.6)
    assert pytest.approx(diagram.analytical_m_x()) == -0.578416548045
    
    diagram = Diagram(beta = 2.0, h = 0.8, Gamma = -0.6)
    assert pytest.approx(diagram.analytical_m_x()) == 0.578416548045

def test_m_z_calculation():
    
    """ Tests the estimator for the magnetization along the z axis of a diagram

        GIVEN: a diagram with different values of beta, s_0 and vertices
        WHEN: the evaluate_m_z_of_diagram method is called
        THEN: the estimator for the magnetization along the z axis gives the correct result
    """
    
    diagram = Diagram(beta = 1.0, s_0=1)
    assert diagram.evaluate_m_z_of_diagram() == 1.0
    
    diagram = Diagram(beta = 1.0, s_0=-1)
    assert diagram.evaluate_m_z_of_diagram() == -1.0
    
    diagram = Diagram(beta = 5.0, s_0=1, vertices=[1.0, 2.0, 3.0, 3.5]) #tested with an already sorted list
    assert pytest.approx(diagram.evaluate_m_z_of_diagram()) == 0.4
    
    diagram = Diagram(beta = 5.0, s_0=-1, vertices=[3.0, 1.0, 3.5, 2.0]) #tested with an unsorted list   
    assert pytest.approx(diagram.evaluate_m_z_of_diagram()) == -0.4

def test_m_x_calculation():
    
    """ Tests the estimator for the magnetization along the x axis of a diagram

        GIVEN: a diagram with different values of beta, Gamma and vertices
        WHEN: the evaluate_m_x_of_diagram method is called
        THEN: the estimator for the magnetization along the x axis gives the correct result
    """
    
    diagram = Diagram(beta = 1.0, Gamma=0, vertices = [0.2, 0.3]) #absence of field in the x direction
    assert diagram.evaluate_m_x_of_diagram() == 0.0 
    
    diagram = Diagram(beta = 1.0, Gamma=2.0) #absence of vertices
    assert diagram.evaluate_m_x_of_diagram() == 0
    
    diagram = Diagram(beta = 1.0, Gamma=2.0, vertices = [0.5, 0.7, 0.2, 0.8])
    assert pytest.approx(diagram.evaluate_m_x_of_diagram()) == -2.0

def test_acceptance_rate_flip():
    
    """ Tests for the acceptance rate of a spin flip. Ensure that the calculation is done correctly
    
        GIVEN: a diagram with different values of beta, s_0, vertices and h
        WHEN: the acceptance_rate_flip method is called
        THEN: the acceptance rate for the spin flip update is correctly calculated
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 0.3678794412
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5)
    assert pytest.approx(diagram.acceptance_rate_flip()) == 1

def test_acceptance_rate_add_segment():
    
    """ Tests for the acceptance rate of adding a segment. Ensure that the calculation is done correctly
    
        GIVEN: a diagram with different values of beta, s_0, vertices, h and Gamma
        WHEN: the acceptance_rate_add_segment method is called
        THEN: the acceptance rate for the addition of a segment update is correctly calculated
    """
    
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
    
    """ Tests for the acceptance rate of removing a segment. Ensure that the calculation is done correctly
    
        GIVEN: a diagram with different values of beta, s_0, vertices, h and Gamma
        WHEN: the acceptance_rate_remove_segment method is called
        THEN: the acceptance rate for the removal of a segment update is correctly calculated
    """
    
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

def test_try_flip_spin_ValueError():
    """ Tests that the try_flip_spin method raises a ValueError if the random number is greater than 1
    
        GIVEN: a diagram with different values of beta, s_0, vertices, h and Gamma and a chosen number gretaer than 1
        WHEN: the try_flip_spin method is called
        THEN: a ValueError is raised since the random number must be between 0 and 1
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma = 1.0)
        
    with pytest.raises(ValueError):
        diagram.try_flip_spin(2.3)

def test_try_flip_spin():
    
    """ Tests that the try_flip_spin method correctly updates the diagram
    
        GIVEN: a diagram with different values of beta, s_0, vertices, h and Gamma and a chosen number (which will be extracted randomly later)
        WHEN: the try_flip_spin method is called
        THEN: the spin is flipped if the chosen number is lower than the acceptance rate, otherwise the spin is not flipped
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma = 1.0)
    
    diagram.try_flip_spin(0.37)
    assert diagram.s_0 == -1 #Ensures that the spin is not flipped since the acceptance rate is 0.0001234098041
    
    diagram.try_flip_spin(0.36)
    assert diagram.s_0 == 1 #Ensures that the spin is flipped since the acceptance rate is 0.0001234098041

def test_try_add_segment_with_random_number_greater_than_1():
    """ Tests that the try_add_segment method raises a ValueError if the random number is greater than 1
    
        GIVEN: a diagram, a chosen number greater than 1, the vertices tau_i, tau_f and tau_after_f and the index where the segment should be added
        WHEN: the try_add_segment method is called
        THEN: a ValueError is raised since the random number must be between 0 and 1
    """
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
            diagram.try_add_segment(1.2, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1)

def test_try_add_segment_with_tau_f_lower_than_tau_i():
    """ Tests that the try_add_segment method raises a ValueError if tau_f is lower than tau_i
    
        GIVEN: a diagram, a chosen number between 0 and 1, the vertices tau_i, tau_f and tau_after_f and the index where the segment should be added
        WHEN: the try_add_segment method is called with tau_f lower than tau_i
        THEN: a ValueError is raised since tau_f must be greater than tau_i
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
            diagram.try_add_segment(0.5, tau_f=1.5, tau_i=1.8, tau_after_f=2.0, index=1)

def test_try_add_segment_with_tau_after_f_lower_than_tau_f():
    """ Tests that the try_add_segment method raises a ValueError if tau_after_f is lower than tau_f
    
        GIVEN: a diagram, a chosen number between 0 and 1, the vertices tau_i, tau_f and tau_after_f and the index where the segment should be added
        WHEN: the try_add_segment method is called with tau_after_f lower than tau_f
        THEN: a ValueError is raised since tau_after_f must be greater than tau_f
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError): 
            diagram.try_add_segment(0.5, tau_f=1.8, tau_i=1.5, tau_after_f=1.6, index=1)

def test_try_add_segment():
    
    """ Tests that the try_add_segment method correctly updates the diagram
    
        GIVEN: aa diagram, a chosen number between 0 and 1, the vertices tau_i, tau_f and tau_after_f and the index where the segment should be added
        WHEN: the try_add_segment method is called
        THEN: the segment is added if the chosen number is lower than the acceptance rate, otherwise the segment is not added
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 4.0], h=0.5, Gamma=1.0)
    
    diagram.try_add_segment(0.7, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 3.0, 4.0] #Ensures that the segment is not added since the acceptance rate is 0.6749294
    
    diagram.try_add_segment(0.6, tau_f=1.8, tau_i=1.5, tau_after_f=2.0, index=1)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0] #Ensures that the segment is added since the acceptance rate is 0.6749294
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.7 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 6 #Ensures that the number of vertices is correctly updated

def test_choice_of_index_and_tau_after_f():
    """ Checks that the index and tau_after_f, calculated in the same way as it will be done in random_try_add_segment, are correctly chosen when tau_i is greater than the last vertex in the list
    
        GIVEN: a diagram with different values of beta, s_0, vertices, h, Gamma and tau_i greater than the last one of the diagram
        WHEN: the index and tau_after_f are calculated as they will be in the random_try_add_segment method
        THEN: the index is equal to the number of vertices and tau_after_f is equal to beta
    """
    
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 1.5, 1.8, 4.0], h=0.5, Gamma=1.0)
        
    tau_i = 4.2
    index, tau_after_f = next(((i, tau) for i, tau in enumerate(diagram.vertices) if tau > tau_i), (diagram.number_vertices, diagram.beta))
    
    assert index == diagram.number_vertices
    assert tau_after_f == diagram.beta
    
def test_try_add_segment_at_the_end_of_the_list():
    
    """ Checks how the method works when the segment is added at the end of the list.
        
        GIVEN: a diagram with different values of beta, s_0, vertices, h and Gamma and a chosen number (which will be extracted randomly later)
        WHEN: the try_add_segment method is called with tau_i and tau_f greater than the last vertex in the list
        THEN: the segment is added if the chosen number is lower than the acceptance rate, otherwise the segment is not added.
    """
    diagram = Diagram(beta = 5.0, s_0= -1, vertices=[3.0, 1.0, 2.0, 1.5, 1.8, 4.0], h=0.5, Gamma=1.0)
    
    tau_i = 4.2
    tau_f = 4.8
    index, tau_after_f = next(((i, tau) for i, tau in enumerate(diagram.vertices) if tau > tau_i), (diagram.number_vertices, diagram.beta))
    
    diagram.try_add_segment(0.32, tau_f, tau_i, tau_after_f, index)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0] #Ensures that the segment is not added since the acceptance rate is 0.3136066492
        
    diagram.try_add_segment(0.3, tau_f, tau_i, tau_after_f, index)
    assert pytest.approx(diagram.vertices) == [1.0, 1.5, 1.8, 2.0, 3.0, 4.0, 4.2, 4.8] #Ensures that the segment is added since the acceptance rate is 0.3136066492
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 2.3 
    
    assert diagram.number_vertices == 8

def test_try_remove_segment_with_random_number_greater_than_1():
    """ Tests that the try_remove_segment method raises a ValueError if the random number is greater than 1
    
        GIVEN: a diagram, a chosen number greater than 1 and the index of the segment to be removed
        WHEN: the try_remove_segment method is called
        THEN: a ValueError is raised since the random number must be between 0 and 1
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(1.2, remove_index=2)

def test_try_remove_segment_with_negative_index():
    """ Tests that the try_remove_segment method raises a ValueError if the remove index is negative
    
        GIVEN: a diagram, a chosen number between 0 and 1 and a negative remove index
        WHEN: the try_remove_segment method is called
        THEN: a ValueError is raised since the remove index must be a non-negative integer
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=-2)

def test_try_remove_segment_with_last_index_of_the_list():
    """ Tests that the try_remove_segment method raises a ValueError if the remove index is the last index of the list
    
        GIVEN: a diagram, a chosen number between 0 and 1 and the remove index equal to the last index of the list
        WHEN: the try_remove_segment method is called
        THEN: a ValueError is raised since the remove index must be lower than the last index of the list
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=5)

def test_try_remove_segment_with_index_greater_than_last_index_of_the_list():
    """ Tests that the try_remove_segment method raises a ValueError if the remove index is greater than the last index of the list
    
        GIVEN: a diagram, a chosen number between 0 and 1 and the remove index greater than the last index of the list
        WHEN: the try_remove_segment method is called
        THEN: a ValueError is raised since the remove index must be lower than the last index of the list
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    with pytest.raises(ValueError):
        diagram.try_remove_segment(0.5, remove_index=7)

def test_try_remove_segment():
    
    """ Tests that the try_remove_segment method correctly updates the diagram
    
        GIVEN: a diagram, a chosen number between 0 and 1 and the index of the segment to be removed
        WHEN: the try_remove_segment method is called
        THEN: the segment is removed if the chosen number is lower than the acceptance rate, otherwise the segment is not removed
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 3.0, 4.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    diagram.try_remove_segment(0.25, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 3.0, 4.0, 4.5, 4.7] #Ensures that the segment is not removed since the acceptance rate is 0.2452529608
    
    diagram.try_remove_segment(0.24, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 4.5, 4.7] #Ensures that the segment is removed since the acceptance rate is 0.2452529608
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.2 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 4 #Ensures that the number of vertices is correctly updated

def test_try_remove_segment_with_tau__after_f_equal_beta():
    
    """ We ensure that, if we remove the last possible segment, tau_after_f = beta 
    
        GIVEN: a diagram, a chosen number between 0 and 1 and the index of the segment to be removed
        WHEN: the try_remove_segment method is called with the last possible segment to remove
        THEN: the segment is removed if the chosen number is lower than the acceptance rate, otherwise the segment is not removed
                with the acceptance rate correctly calculated with tau_after_f = beta
    """
    
    diagram = Diagram(beta = 5.0, s_0= 1, vertices = [1.0, 2.0, 4.5, 4.7], h=0.5, Gamma=1.0)
    
    diagram.try_remove_segment(0.99, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0, 4.5, 4.7] #Ensures that the segment is not removed since the acceptance rate is 0.9824769037
    
    diagram.try_remove_segment(0.98, remove_index=2)
    assert pytest.approx(diagram.vertices) == [1.0, 2.0] #Ensures that the segment is removed since the acceptance rate is 0.982476903
    
    assert pytest.approx(diagram.sum_with_alternating_sign) == 1.0 #Ensures that the sum with alternating sign is correctly updated
    
    assert diagram.number_vertices == 2 #Ensures that the number of vertices is correctly updated


""" Tests for the Diagram_Random class """

def test_random_try_spin_flip():
    
    """ Asserts that the random_try_spin_flip method is deterministic once the seed is fixed 
    
        GIVEN: two diagrams with the same parameters and the same seed
        WHEN: the random_try_spin_flip method is called on both diagrams
        THEN: the spin of both diagrams is flipped or not flipped in the same way, since the random number generated is the same
    """
    
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_spin_flip()
    diagram2.random_try_spin_flip()
    
    assert diagram1.s_0 == diagram2.s_0

def test_random_try_add_segment():
    
    """ Asserts that the random_try_add_segment method is deterministic once the seed is fixed
    
        GIVEN: two diagrams with the same parameters and the same seed
        WHEN: the random_try_add_segment method is called on both diagrams
        THEN: the segment is added or not added in the same way to both diagrams, since the random numbers generated are the same
    """
    
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_add_segment()
    diagram2.random_try_add_segment()
    
    assert pytest.approx(diagram1.vertices) == diagram2.vertices

def test_random_try_remove_segment_with_no_vertices():
    
    """ Checks that nothing happens if we start with a diagram with no vertices 
    
        GIVEN: a diagram with no vertices
        WHEN: the random_try_remove_segment method is called
        THEN: nothing happens and the diagram remains with no vertices
    """
    
    diagram = Diagram_Random(beta = 5.0, s_0= -1, h=0.5, Gamma=1.0, seed_number=42)
    
    diagram.random_try_remove_segment() 
    assert diagram.vertices == []
    
def test_random_try_remove_segment():
    
    """ Asserts that the random_try_remove_segment method is deterministic once the seed is fixed
    
        GIVEN: two diagrams with the same parameters and the same seed
        WHEN: the random_try_remove_segment method is called on both diagrams
        THEN: the segment is removed or not removed in the same way from both diagrams, since the random numbers generated are the same
    """
    
    diagram1 = Diagram_Random(beta=2.0, s_0=-1, vertices = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],  h=1.0, Gamma = 0.5, seed_number=42)
    diagram2 = Diagram_Random(beta=2.0, s_0=-1, vertices = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6],  h=1.0, Gamma = 0.5, seed_number=42)
    
    diagram1.random_try_remove_segment()
    diagram2.random_try_remove_segment()
    
    assert pytest.approx(diagram1.vertices) == diagram2.vertices

def test_chose_update():
    
    """ Asserts that the chose_update method is deterministic once the seed is fixed 
    
        GIVEN: two diagrams with the same parameters and the same seed
        WHEN: the chose_update method is called on both diagrams
        THEN: the same update is chosen for both diagrams, since the random number generated is the same
    """
    
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