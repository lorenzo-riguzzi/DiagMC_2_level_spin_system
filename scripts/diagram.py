from typing import Optional

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
    
    def evaluate_mz_of_diagram(self) -> float:
        """ Evaluate the magnetization m_z along the z axis of the diagram.
            
            PARAMETERS (taken from the class):
            s_0: spin of the initial segment
            beta: inverse temperature
            vertices[i]: time intervals at which the flips occur       
        """
        m_z =self.s_0 - 2* self.s_0 * self.sum_with_alternating_sign / self.beta
        return m_z