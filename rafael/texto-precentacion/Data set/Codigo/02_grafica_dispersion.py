import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("ENB2012_data.xlsx")

plt.figure(figsize=(9, 5.5))
plt.scatter(df["X7"], df["Y2"], alpha=0.6)
plt.title("Gráfica de dispersión: Área acristalada vs. carga de refrigeración")
plt.xlabel("Área acristalada, X7")
plt.ylabel("Carga de refrigeración, Y2")
plt.grid(True)
plt.tight_layout()
plt.show()
