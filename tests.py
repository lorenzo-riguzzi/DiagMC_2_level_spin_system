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