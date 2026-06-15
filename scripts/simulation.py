from diagram import Diagram_Random

N_thermalization = 50000
N_runs = 1000000

diagram = Diagram_Random(beta = 2.0, h= 0.5, Gamma = 0.6, seed_number = 42)

analytical_m_z = diagram.analytical_m_z()
analytical_m_x = diagram.analytical_m_x()

for i in range(N_thermalization):
    diagram.chose_update()

sum_m_z_estimate = 0.0
sum_m_x_estimate = 0.0

for i in range(N_runs):
    diagram.chose_update()
    
    sum_m_z_estimate += diagram.evaluate_m_z_of_diagram()
    sum_m_x_estimate += diagram.evaluate_m_x_of_diagram()

average_m_z = sum_m_z_estimate / N_runs
average_m_x = sum_m_x_estimate / N_runs 

print(f"Estimated m_z: {average_m_z}, Analytical m_z: {analytical_m_z}")
print(f"Estimated m_x: {average_m_x}, Analytical m_x: {analytical_m_x}")