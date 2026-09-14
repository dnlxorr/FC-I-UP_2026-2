import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
import numpy as np

df = pd.read_excel("ENB2012_data.xlsx")

valores = df["Y1"].dropna().to_numpy()
kde = gaussian_kde(valores)

x = np.linspace(valores.min(), valores.max(), 300)
y = kde(x)

plt.figure(figsize=(9, 5.5))
plt.plot(x, y, linewidth=2)
plt.fill_between(x, y, alpha=0.25)
plt.title("Gráfica de densidad: Carga de calefacción")
plt.xlabel("Carga de calefacción, Y1")
plt.ylabel("Densidad")
plt.grid(True)
plt.tight_layout()
plt.show()
