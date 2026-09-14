import pandas as pd
import matplotlib.pyplot as plt

# Lectura del dataset
datos = pd.read_csv("dataset.csv")

# Gráfica de dispersion
plt.scatter(
    datos["theta_rad_clean"],
    datos["omega_rad_s_clean"],
    s=10,
    label="Datos"
)

plt.xlabel("Ángulo (rad)")
plt.ylabel("Velocidad angular (rad/s)")
plt.title("Dispersión: ángulo vs. velocidad angular")

plt.grid()
plt.legend()
# Guardar la grafica en resultados
plt.savefig("resultados/graficaDeDispersion.png")
plt.show()