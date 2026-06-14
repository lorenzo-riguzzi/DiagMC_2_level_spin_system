# DiagMC_2_level_spin_system
This program implements a Diagrammatic Monte Carlo (DMC) simulation of a two level spin system exploiting Markov Chain Monte Carlo and the Metropolis-Hastings algorithm. DMC is used to sample the Feynman diagrams of different orders that appear in the partition function of the system. The simulation aims at obtaining estimators for the magnetization along the longitudinal and transverse direction and at comparing them with their exact analytical expressions. This work aims at proving the validity of the method in order to justify its usage for more complex problems, which do not have an analytical solution.

## Installation and tests

Type errors are checked with mypy

## Theoretical background

### Analytical solution

The starting point of the simulation is the Hamiltonian of a single spin in an external magnetic field with an $x$ and a $z$ component:

$$ \hat{H}=\hat{H}_0+\hat{H}_1=h\sigma_z+\Gamma\sigma_x $$

where $\sigma_x$, $\sigma_z$ are Pauli matrices and $h$ and $\Gamma$ are the strength of the field along the $z$ and $x$ direction respectively. The Hamiltonian can be written in the basis of eigenstates of $\sigma_z$: $\ket{\uparrow}$ and $\ket{\downarrow}$ and can be diagonalized, finding its two eigenvalues: $E_{\pm}=\pm\sqrt{h^2+\Gamma^2}=\pm E$ and their corresponding eigenstates $\ket{\Psi_+}$ and $\ket{\Psi_-}$.\\

With these the partition function is given by:

$$ Z=\text{Tr}[e^{-\beta \hat{H}}]=\bra{\Psi_+}e^{-\beta \hat{H}}\ket{\Psi_+}+\bra{\Psi_-}e^{-\beta \hat{H}}\ket{\Psi_-}=2\cosh{\beta E}  $$
