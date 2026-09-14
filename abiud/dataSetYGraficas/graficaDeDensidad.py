import pandas as pd
import matplotlib.pyplot as plt

# Lectura del dataset
datos = pd.read_csv("dataset.csv")

# Histograma de la velocidad angular
plt.hist(
    datos["omega_rad_s_clean"],
    bins=30,
    density=True,
    label="Densidad"
)

plt.xlabel("Velocidad angular (rad/s)")
plt.ylabel("Densidad")
plt.title("Densidad de la velocidad angular")

plt.grid()
plt.legend()
# Guardar la grafica en resultados
plt.savefig("resultados/graficaDeDensidad.png")
plt.show()