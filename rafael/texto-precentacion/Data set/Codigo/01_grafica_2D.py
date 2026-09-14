import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("ENB2012_data.xlsx")

datos_2d = df.groupby("X2", as_index=False)["Y1"].mean()
datos_2d = datos_2d.sort_values("X2")

plt.figure(figsize=(9, 5.5))
plt.plot(datos_2d["X2"], datos_2d["Y1"], marker="o", linewidth=2)
plt.title("Gráfica 2D: Área superficial vs. carga de calefacción")
plt.xlabel("Área superficial, X2 (m²)")
plt.ylabel("Carga de calefacción, Y1")
plt.grid(True)
plt.tight_layout()
plt.show()
