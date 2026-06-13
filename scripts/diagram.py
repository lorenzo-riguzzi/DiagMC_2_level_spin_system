from typing import Optional
import math
class Diagram():
    
    """ This class implements the Feynman diagram of a single spin 1/2 particle. 
    
        Attributes:
            beta: inverse temperature (gives the length of the diagram)
            s_0: spin of the initial spin of the first segment of the diagram (can be either +/-1, the default value is set arbitrary to -1)
            vertices: list of vertices in the diagram (where the spin flips occur, the default value is an empty list)
            Gamma: external field along the x axis
            h: external field along the z axis
    """
    
    def __init__(
            self, 
            beta: float,
            s_0: int = -1,
            vertices: Optional[list[float]] = None,
            Gamma: float = 0,
            h: float = 0
        ):
        
        if beta <= 0:
            raise ValueError(f"Beta must be a positive number. Current value is {beta}.")
        if s_0 not in [-1, 1]:
            raise ValueError(f"s_0 must be either -1 or 1. Current value is {s_0}.")
        if vertices is not None and len(vertices) % 2 != 0:
            raise ValueError(f"The number of vertices must be even, since odd order diagrams have zero weight contribution. Current number of vertices is {len(vertices)}.")
        
        self.beta = beta
        self.s_0 = s_0
        if vertices is None:
            self.vertices = []
        else:
            if max(list(vertices)) >= beta or min(list(vertices)) <= 0:
                raise ValueError(f"All vertices must be positive and less than beta, since beta is the length of the diagram.")
            self.vertices = sorted(list(vertices))
        self.Gamma = Gamma
        self.h = h
        
        #evaluate the sum with alternating sign of the vertices, needed for the evaluation of m_z
        self.sum_with_alternating_sign = sum((-1)**(i+1) * v for i, v in enumerate(self.vertices)) #the +1 is needed because the sum starts from 1
        self.number_vertices = len(self.vertices) #Number of vertices of the diagram
    
    def evaluate_mz_of_diagram(self) -> float:
        """ Evaluate the magnetization along the z axis of the diagram.
            
            PARAMETERS (taken from the class):
            s_0: spin of the initial segment
            beta: inverse temperature
            sum_with_alternating_sign: sum of the vertices with alternating sign       
        """
        m_z =self.s_0 - 2* self.s_0 * self.sum_with_alternating_sign / self.beta
        return m_z
    
    def evaluate_m_x_of_diagram(self) -> float:
        """ Evaluate the magnetization along the x axis of the diagram.
            
            PARAMETERS (taken from the class):
            Gamma: external field along the x axis
            beta: inverse temperature
        """
        if self.Gamma == 0.0:
            m_x = 0.0
            return m_x
        else:
            m_x = self.number_vertices / (self.Gamma * self.beta)
            return m_x
    
    def acceptance_rate_flip(self) -> float:
        """ Evaluate the acceptance rate for a spin flip
            
            PARAMETERS (taken from the class):
            beta: inverse temperature
            s_0: spin of the initial segment
            h: field along the z direction
            sum_with_alternating_sign: sum of the vertices with alternating sign
        """
        
        weight_ratio = math.exp(2*self.h*self.s_0*(self.beta+2*self.sum_with_alternating_sign)) 
        alpha_flip = min(1, weight_ratio)
        return alpha_flip
    
    def acceptance_rate_add_segment(self, tau_i: float, tau_f: float, tau_after_f: float, segment_spin: int,) -> float:
        """ Evaluate the acceptance rate for adding a segment to the diagram
            
            PARAMETERS (taken from the class):
            beta: inverse temperature
            h: field along the z direction
            Gamma: field along the x direction
            number_vertices: number of vertices of the diagram
            
            EXTERNAL PARAMETERS:
            tau_i: beginning of the new added segment
            tau_f: end of the new added segment
            segment_spin: spin of the new added segment (can be either +/-1)
            tau_after_f: position of the vertex located after tau_f
        """
        
        weight_ratio = self.Gamma**2*math.exp(-2*self.h*segment_spin*(tau_f-tau_i))
        q_ratio = self.beta*(tau_after_f-tau_i) / (self.number_vertices+1) #ratio between the proposal distributions
        alpha_add = min(1, weight_ratio * q_ratio)
        return alpha_add
    
    def acceptance_rate_remove_segment(self, tau_i: float, tau_f: float, tau_after_f: float, segment_spin: int) -> float:
        """ Evaluate the acceptance rate for adding a segment to the diagram
            
            PARAMETERS (taken from the class):
            beta: inverse temperature
            h: field along the z direction
            Gamma: field along the x direction
            number_vertices: number of vertices of the diagram
            
            EXTERNAL PARAMETERS:
            tau_i: beginning of the removed segment
            tau_f: end of the removed segment
            segment_spin: spin of the removed segment (can be either +/-1)
            tau_after_f: position of the vertex located after tau_f
        """
        
        weight_ratio = self.Gamma**(-2)*math.exp(2*self.h*segment_spin*(tau_f-tau_i))
        q_ratio = (self.number_vertices-1) / (self.beta*(tau_after_f-tau_i)) #ratio between the proposal distributions
        alpha_remove = min(1, weight_ratio * q_ratio)
        return alpha_remove
    
    def try_flip_spin(self, random_number: float) -> None:
        """ Try to flip the spin of the diagram, by comparing a random number with the acceptance rate of the flip. 
            
            EXTERNAL PARAMETERS:
            random_number: random number between 0 and 1 used to decide whether to accept or reject the flip
        """
        
        if random_number < 0 or random_number > 1:
            raise ValueError(f"Random number must be between 0 and 1. Current value is {random_number}.")
        
        alpha_flip = self.acceptance_rate_flip()
        if random_number < alpha_flip:
            self.s_0 *= -1
        else:
            return
    
    def try_add_segment(self, random_number: float, tau_f: float, tau_i: float) -> None:
        """ Try to add a segment to the diagram, by comparing a random number with the acceptance rate of adding a segment. 
            
            EXTERNAL PARAMETERS:
            random_number: random number between 0 and 1 used to decide whether to accept or reject the addition of the segment
            tau_i: beginning of the new added segment
            tau_f: end of the new added segment
        """
        
        if random_number < 0 or random_number > 1:
            raise ValueError(f"Random number must be between 0 and 1. Current value is {random_number}.")
        
        if tau_f < tau_i:
            raise ValueError(f"tau_f must be greater than tau_i. Current values are tau_f={tau_f} and tau_i={tau_i}.")
        
        """Finds the vertex right after tau_f and its index.
            The index correspond to the one of tau_i once it's inserted.
            If no match is found the vertex next to tau_f is beta and its index is number_vertices+1.
        """
        
        index : int
        tau_after_f : float
        
        index, tau_after_f = next(((i, tau) for i, tau in enumerate(self.vertices) if tau > tau_f), (self.number_vertices, self.beta))
        
        segment_spin = self.s_0 * (-1)**(index + 1)
        
        alpha_add = self.acceptance_rate_add_segment(tau_i, tau_f, tau_after_f, segment_spin)
        
        if random_number < alpha_add:
            self.sum_with_alternating_sign += (-1)**(index + 1) * tau_i + (-1)**(index + 2) * tau_f
            self.number_vertices += 2
            self.vertices.insert(index, tau_i)
            self.vertices.insert(index + 1, tau_f)
        else:
            return
    
    def try_remove_segment(self, random_number: float, remove_index : int) -> None:
        """ Try to remove a segment from the diagram, by comparing a random number with the acceptance rate of removing a segment.
            The update is discarded automatically if the diagram has no vertices (nothing can be removed).
            
            EXTERNAL PARAMETERS:
            random_number: random number between 0 and 1 used to decide whether to accept or reject the removal of the segment
            remove_index: index of the first vertex to remove
        """
        
        if self.number_vertices == 0:
            return
        else:
            if random_number < 0 or random_number > 1:
                raise ValueError(f"Random number must be between 0 and 1. Current value is {random_number}.")
            
            if remove_index < 0 or remove_index >= self.number_vertices - 1:
                raise ValueError(f"remove_index must be a valid index for the diagram.")
            
            tau_i = self.vertices[remove_index]
            tau_f = self.vertices[remove_index + 1]
            tau_after_f = self.vertices[remove_index + 2] if remove_index + 2 < self.number_vertices else self.beta
            segment_spin = self.s_0 * (-1)**(remove_index + 1)
            
            alpha_remove = self.acceptance_rate_remove_segment(tau_i, tau_f, tau_after_f, segment_spin)
            
            if random_number < alpha_remove:
                self.sum_with_alternating_sign -= (-1)**(remove_index + 1) * tau_i + (-1)**(remove_index + 2) * tau_f
                self.number_vertices -= 2
                del self.vertices[remove_index:remove_index + 1]
            else:
                return