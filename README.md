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

where $\beta=1/T$ is the inverse temperature. With this result it is possible to evaluate the analytical values of the two magnetizations:

$$ m_z = \braket{\sigma_z} = -\frac{h}{E}\tanh{\beta E} $$

$$ m_x = \braket{\sigma_x} = -\frac{\Gamma}{E}\tanh{\beta E} $$

### DMC Approach

Diagrammatic Monte Carlo approaches the problem starting from the Path Integral formulation of the partition function in imaginary time:

$$  Z=\sum_{s=\uparrow,\downarrow}\sum_{n=0}^\infty (-1)^n\int_{0}^{\beta}d\tau_1 ... \int_{\tau_{n-1}}^{\beta} \bra{s}e^{-\beta\hat{H}_0}\hat{H}_1(\tau_1)...\hat{H_1}(\tau_n)\ket{s} $$

where, for the order $n=0$ we have no interaction Hamiltonian inside the expectation value and $\tau=it$ is the imaginary time, which is such that: $0< \tau_1 < \tau_2 < ... < \tau_n < \beta$. The interaction Hamiltonian is in the interaction representation:

$$ \hat{H}_1(\tau_k) = e^{\hat{H}_0\tau_k}\hat{H}_1 e^{-\hat{H}_0\tau_k} $$

The arguments of the integral give the weight of a diagram of order $n$ with initial spin $s$ and vertices $\tau_1, ...\tau_n$. It can be proved that odd order diagrams have weight zero, while for even order diagrams the weight can be evaluated to be:

$$ D_n^s=\Gamma^ne^{-\beta hs} \prod_{i=1}^n e^{-2hs(-1)^i\tau_i} $$

### DMC updates

The results obtained for odd and even order diagrams already tell us that the only update we are interested in are those where the order of the diagram is kept odd, so those that start from an odd order diagram and add or remove an odd number of vertices or that keep the order of the diagram fixed (spin flip or movement of a vertex). Since in a Monte Carlo simulation we aim at performing many runs to explore ergodically the space of all possible configurations, all the possible updates be reduced to the addition and the remotion of a pair of vertices. Always under the hypothesis of many runs and ergodicity all the possible updates which include the addition and remotion of vertices and the movement of a vertex without changing the order of the diagram can be constructed in terms of two minimal updates: the addition and the remotion of a segment (where for segment we mean a pair of vertices of extrema $\tau_k$ and $\tau_{k+1}$). The only update we need apart from these two si the spin flip update, which allows us to move from a configuration with $s=1$ ($s=\uparrow$), to a configuration with $s=-1$ ($s=\downarrow$). With our notation this last update corresponds to $s\rightarrow -s$.