# DiagMC_2_level_spin_system
This program implements a Diagrammatic Monte Carlo (DMC) simulation of a two level spin system exploiting Markov Chain Monte Carlo and the Metropolis-Hastings algorithm. DMC is used to sample the Feynman diagrams of different orders that appear in the partition function of the system. The simulation aims at obtaining estimators for the magnetization along the longitudinal and transverse direction and at comparing them with their exact analytical expressions. This work aims at proving the validity of the method in order to justify its usage for more complex problems, which do not have an analytical solution.

## Installation and tests

TypeErrors are checked with mypy

## Structure of the code

### diagram.py

This file includes the **Diagram** class and the **Diagram_Random** class. The first one implements all the deterministic methods of the code. These include:

- The methods $evaluate\_m\_x$ and $evaluate\_m\_z$, which calculates the magnetizations of a single diagram;
- The methods $acceptance\_rate\_flip$, $acceptance\_rate\_add\_segment$ and $acceptance\_rate\_remove\_segment$, which calculate the acceptance ratii $\alpha_{flip}$, $\alpha_{add}$ and $\alpha_{rem}$;
- The methods $try\_flip\_spin$, $try\_add\_segment$ and $try\_remove\_segment$, which compare the acceptance ratii with a random number (that is here given as input parameter to the method) and apply the corresponding update if the random number is lower than the acceptance ratio.

The second class, inherits all the methods of the first one and introduces randomness by including the Mersenne Twister random number generator, allowing its functions $random\_try\_flip\_spin$, $random\_try\_add\_segment$ and $random\_try\_remove\_segment$ to randomly performs the three updates by using the previously described functions of the parent class.

## Theoretical background

Diagrammatic Monte Carlo is a powerful method which allows one to evaluate integrals which appear in the form of the diagrammatic series:

$$ Q(\{y\})=\sum_{n=0}^{\infty}\sum_{\xi_n}\int dx_1...\int dx_n D_n^{\xi_n}(\{y\}; x_1, ..., x_n) $$

We are interested in obtaining the function $Q$ which is a function of a set of external variables $\{y\}$ (usually, this is a Green's function). $D_{n}^{\xi}(\{y\}; x_1, ..., x_n)$ represents the Feynmann diagrams of different order $n$ and of different topology $\xi_n$ and $x_i$ are the integration variables (in our case they will be imaginary time points).
In this simulation the method is used to study the simple problem of a two level spin system.

### Analytical solution

The starting point of the simulation is the Hamiltonian of a single spin in an external magnetic field with an $x$ and a $z$ component:

$$ \hat{H}=\hat{H}_0+\hat{H}_1=h\sigma_z+\Gamma\sigma_x $$

where $\sigma_x$, $\sigma_z$ are Pauli matrices and $h$ and $\Gamma$ are the strength of the field along the $z$ and $x$ direction respectively. The Hamiltonian can be written in the basis of eigenstates of $\sigma_z$: $\ket{\uparrow}$ and $\ket{\downarrow}$ and can be diagonalized, finding its two eigenvalues: $E_{\pm}=\pm\sqrt{h^2+\Gamma^2}=\pm E$ and their corresponding eigenstates $\ket{\Psi_+}$ and $\ket{\Psi_-}$.

With these the partition function is given by:

$$ Z=\text{Tr}[e^{-\beta \hat{H}}]=\bra{\Psi_+}e^{-\beta \hat{H}}\ket{\Psi_+}+\bra{\Psi_-}e^{-\beta \hat{H}}\ket{\Psi_-}=2\cosh{\beta E}  $$

where $\beta=1/T$ is the inverse temperature. With this result it is possible to evaluate the analytical values of the two magnetizations:

$$ m_z = \braket{\sigma_z} = -\frac{h}{E}\tanh{\beta E} $$

$$ m_x = \braket{\sigma_x} = -\frac{\Gamma}{E}\tanh{\beta E} $$

### DMC Approach

Diagrammatic Monte Carlo approaches the problem starting from the Path Integral formulation of the partition function in imaginary time:

$$  Z=\sum_{s=\uparrow,\downarrow}\sum_{n=0}^\infty (-1)^n\int_{0}^{\beta}d\tau_1 ... \int_{\tau_{n-1}}^{\beta} \bra{s}e^{-\beta\hat{H}_0}\hat{H}_1(\tau_n)...\hat{H_1}(\tau_1)\ket{s} $$

where, for the order $n=0$ we have no interaction Hamiltonian inside the expectation value and $\tau=it$ is the imaginary time, which is such that: $0< \tau_1 < \tau_2 < ... < \tau_n < \beta$. The interaction Hamiltonian is in the interaction representation:

$$ \hat{H}_1(\tau_k) = e^{\hat{H}_0\tau_k}\hat{H}_1 e^{-\hat{H}_0\tau_k} $$

The arguments of the integral give the weight of a diagram of order $n$ with initial spin $s$ and vertices $\tau_1, ...\tau_n$. It can be proved that odd order diagrams have weight zero, while for even order diagrams the weight can be evaluated to be:

$$ D_n^s=\Gamma^ne^{-\beta hs} \prod_{i=1}^n e^{2hs(-1)^i\tau_i} $$

### DMC updates

The results obtained for odd and even order diagrams already tell us that the only updates we are interested in are those where the order of the diagram is kept odd, so those that start from an odd order diagram and add or remove an odd number of vertices or that keep the order of the diagram fixed (spin flip or movement of a vertex). Since in a Monte Carlo simulation we aim at performing many runs to explore ergodically the space of all possible configurations, all the possible updates be reduced to the addition and the remotion of a pair of vertices. Always under the hypothesis of many runs and ergodicity all the possible updates which include the addition and remotion of vertices and the movement of a vertex without changing the order of the diagram can be constructed in terms of two minimal updates: the addition and the remotion of a segment (where for segment we mean a pair of vertices of extrema $\tau_k$ and $\tau_{k+1}$). The only update we need apart from these two si the spin flip update, which allows us to move from a configuration with $s=1$ ($s=\uparrow$), to a configuration with $s=-1$ ($s=\downarrow$). With our notation this last update corresponds to $s\rightarrow -s$. Notice that the presence of both the updates to add and remove a segment satisfies detailed balance, since they are one the inverse process of the other.
We want to implement a Markov-chain, where the different updates from an initial state $i$ to a final state $f$ are accepted with a probability that, from Metropolis-Hastings algorithm, is given by:

$$  \alpha = \min\left(1, \quad \frac{D_{n_f}^{s_f}(\{\tau\}_f)}{D_{n_i}^{s_i}(\{\tau\}_i)}\frac{p(i|f)}{p(f|i)}\right) $$

where $p(f|i)$ is the proposal distribution from which we chose the update to go from an initial configuration $i$ to a final configuration $f$. With this we can evaluate the transition probabilities of our updates:

- **Spin flip**: The update simply flips the spin of all the segments of the diagram and is already the opposite of itself. No random number has to extracted to find the final configuration since we only have to options, which means that we do not have a proposal distribution. The acceptance race is:

$$ \alpha_{flip}=\min\left(1,\quad \frac{D_{n}^{-s}(\tau_1, ..., \tau_n)}{D_{n}^{s}(\tau_1, ..., \tau_n)}\right)=\min\left(1, \quad e^{2\beta hs}e^{-4hs\sum_{i=1}^n (-1)^i\tau_i}\right) $$

- **Add segment**: The update adds two vertices at indices $j$ and $j+1$. The first vertex to be added is extracted from a uniform distribution between 0 and $\beta$ and the second one from a uniform distribution between $\tau_j$ and $\tau_{j+2}$, which means that $p(f|i)=U(0, \beta)U(\tau_j, \tau_{j+2})=1/\beta\cdot 1/(\tau_{j+2}-\tau_j)$. For the opposite process, instead, the first vertex to be removed is extracted uniformly from the $n+2$ vertices present in the final configuration (except for the last vertex since we can not remove $\beta$ from the diagram) and when the first is chosen the second one is constrained to be the next one, so that here the ratio between the proposal distributions is: $p(i|f)=1/(n+1)$. Putting everything together we get:

$$ \alpha_{add}=\min\left(1,\quad \frac{D_{n+2}^{s}(\tau_1, ...,\tau_j, \tau_{j+1}, ...,  \tau_{n})}{D_{n}^{s}(\tau_1, ..., \tau_n)}\frac{p(i|f)}{p(f|i)}\right)=\min\left(1, \quad \Gamma^2e^{-2hs(-1)^j(\tau_{j+1}-\tau_j)}\frac{\beta(\tau_{j+2}-\tau_j)}{n+1}\right) $$

- **Remove segment**: This update is the exact opposite of the previous one. In this case, when we chose the first vertex to be removed, we are extracting among the $n-1$ vertices of the diagram that can be removed, so that the acceptance rate in this case will be:

$$ \alpha_{rem}=\min\left(1,\quad \frac{D_{n-2}^{s}(\tau_1, ..., \tau_{n})}{D_{n-2}^{s}(\tau_1, ...,\tau_j, \tau_{j+1}, ...,  \tau_n)}\frac{p(i|f)}{p(f|i)}\right)=\min\left(1, \quad \Gamma^{-2}e^{2hs(-1)^j(\tau_{j+1}-\tau_j)}\frac{n-1}{\beta(\tau_{j+2}-\tau_j)}\right) $$

### Estimators for the magnetizations

During the simulation we will keep track of the transverse and the longitudinal magnetization, in order to compare them with the analytical solutions that we have obtained earlier. The estimators for the magnetizations of a specific diagram can be found to be:

$$ m_z=\frac{s}{\beta}\left(\beta-2\sum_{i=1}^n(-1)^i\tau_i\right) $$

$$ m_x=-\frac{n}{\Gamma\beta} $$

so that the DMC estimators are just the average values of these two quantities during the whole simulation: $\langle\sigma_z\rangle _{MC}=\langle m_z \rangle$ and $\langle \sigma_x \rangle _{MC}=-\langle n\rangle/\Gamma\beta$.
