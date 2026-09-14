import pandas as pd
import matplotlib.pyplot as plt

# Lectura del dataset
datos = pd.read_csv("dataset.csv")

# Creacion de la figura 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Grafica en tres dimensiones
ax.scatter(
    datos["t_s"],
    datos["theta_rad_clean"],
    datos["omega_rad_s_clean"],
    s=5
)

ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Ángulo (rad)")
ax.set_zlabel("Velocidad angular (rad/s)")
ax.set_title("Movimiento del péndulo en tres dimensiones")
# Guardar la grafica en resultados
plt.savefig("resultados/graficaEnTresD.png")
plt.show()