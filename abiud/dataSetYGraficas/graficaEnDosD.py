import pandas as pd
import matplotlib.pyplot as plt

# Lectura del dataset
datos = pd.read_csv("dataset.csv")

plt.plot(
    datos["t_s"],
    datos["theta_rad_clean"],
    marker=".",
    markersize=2,
    label="Ángulo"
)

plt.xlabel("Tiempo (s)")
plt.ylabel("Ángulo (rad)")
plt.title("Movimiento angular del péndulo")

plt.grid()
plt.legend()
plt.savefig("resultados/graficaEnDosD.png")
plt.show()