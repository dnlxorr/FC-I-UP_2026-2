import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("ENB2012_data.xlsx")

fig = plt.figure(figsize=(9, 6.5))
ax = fig.add_subplot(111, projection="3d")

grafica = ax.scatter(
    df["X2"],
    df["X5"],
    df["Y2"],
    c=df["Y2"],
    s=30,
    alpha=0.7
)

ax.set_title("Gráfica 3D: Área superficial, altura y carga de refrigeración")
ax.set_xlabel("Área superficial, X2 (m²)")
ax.set_ylabel("Altura total, X5 (m)")
ax.set_zlabel("Carga de refrigeración, Y2")

fig.colorbar(grafica, ax=ax, label="Carga de refrigeración")
plt.tight_layout()
plt.show()
