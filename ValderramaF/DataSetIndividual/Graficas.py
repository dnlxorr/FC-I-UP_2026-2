"""
Gráficas y visualización en Python II
Dataset: SOLETE - Energía Solar y Variables Meteorológicas

Se piden 4 tipos de gráficas:
  1. Gráficas en 2D
  2. Gráficas de dispersión (scatter)
  3. Gráficas de densidad
  4. Gráficas en 3D
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401  (necesario para proyección '3d')
from scipy.stats import gaussian_kde, pearsonr, linregress

# ---------------------------------------------------------------------------
# 1. GENERACIÓN DEL DATASET (código original del usuario, sin modificaciones)
# ---------------------------------------------------------------------------
random.seed(42)

dataset = {
    "Medición": [],
    "Temperatura (°C)": [],
    "Humedad (%)": [],
    "Presión (hPa)": [],
    "Velocidad Viento (m/s)": [],
    "Irradiancia Solar (W/m²)": [],
    "Potencia Solar (W)": []
}

for i in range(100):
    medicion = i + 1
    temperatura = round(random.uniform(15.0, 35.0), 2)
    humedad = round(random.uniform(30.0, 90.0), 2)
    presion = round(random.uniform(990.0, 1030.0), 2)
    velocidad_viento = round(random.uniform(0.0, 15.0), 2)
    irradiancia = round(random.uniform(100.0, 1000.0), 2)
    eficiencia = random.uniform(0.15, 0.22)
    factor_temperatura = 1 - 0.004 * (temperatura - 25)
    factor_viento = 1 + 0.002 * velocidad_viento
    potencia = irradiancia * eficiencia * factor_temperatura * factor_viento
    potencia = potencia * (1 + random.gauss(0, 0.03))
    potencia = round(max(potencia, 0), 2)

    dataset["Medición"].append(medicion)
    dataset["Temperatura (°C)"].append(temperatura)
    dataset["Humedad (%)"].append(humedad)
    dataset["Presión (hPa)"].append(presion)
    dataset["Velocidad Viento (m/s)"].append(velocidad_viento)
    dataset["Irradiancia Solar (W/m²)"].append(irradiancia)
    dataset["Potencia Solar (W)"].append(potencia)

# Convertimos las listas a arreglos de numpy: no cambia los valores, solo
# permite usar operaciones vectorizadas (filtros, máscaras, etc.) que
# matplotlib/scipy manejan de forma más directa que las listas de Python.
medicion       = np.array(dataset["Medición"])
temperatura    = np.array(dataset["Temperatura (°C)"])
humedad        = np.array(dataset["Humedad (%)"])
presion        = np.array(dataset["Presión (hPa)"])
viento         = np.array(dataset["Velocidad Viento (m/s)"])
irradiancia    = np.array(dataset["Irradiancia Solar (W/m²)"])
potencia       = np.array(dataset["Potencia Solar (W)"])

plt.rcParams.update({"font.size": 10})

# ---------------------------------------------------------------------------
# 2. GRÁFICAS EN 2D
# ---------------------------------------------------------------------------
# Un gráfico "2D" clásico muestra una variable en función de otra mediante
# líneas o barras. Aquí usamos el número de medición como eje horizontal
# (es el único índice ordenado y natural del dataset: no hay una columna de
# tiempo explícita, y "Medición" ya numera cada observación de 1 a 100).
fig, axs = plt.subplots(2, 2, figsize=(12, 8))
fig.suptitle("Gráficas en 2D — Variables vs. Número de Medición", fontsize=14, fontweight="bold")

axs[0, 0].plot(medicion, temperatura, color="tab:red")
axs[0, 0].set_title("Temperatura")
axs[0, 0].set_xlabel("Medición")
axs[0, 0].set_ylabel("Temperatura (°C)")
axs[0, 0].grid(alpha=0.3)

axs[0, 1].plot(medicion, irradiancia, color="tab:orange")
axs[0, 1].set_title("Irradiancia Solar")
axs[0, 1].set_xlabel("Medición")
axs[0, 1].set_ylabel("Irradiancia (W/m²)")
axs[0, 1].grid(alpha=0.3)

axs[1, 0].plot(medicion, potencia, color="tab:green")
axs[1, 0].set_title("Potencia Solar generada")
axs[1, 0].set_xlabel("Medición")
axs[1, 0].set_ylabel("Potencia (W)")
axs[1, 0].grid(alpha=0.3)

axs[1, 1].plot(medicion, viento, color="tab:blue")
axs[1, 1].set_title("Velocidad del Viento")
axs[1, 1].set_xlabel("Medición")
axs[1, 1].set_ylabel("Viento (m/s)")
axs[1, 1].grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("graficas_2D.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# 3. GRÁFICAS DE DISPERSIÓN (SCATTER)
# ---------------------------------------------------------------------------
# Para que la dispersión sea físicamente correcta (no solo "bonita"), cada
# panel se acompaña de un ajuste por mínimos cuadrados y su estadística
# (r de Pearson, p-valor), en vez de solo mostrar los puntos.
#
# Panel A: Potencia vs. Irradiancia.
#   Esta es la ÚNICA relación fuerte y significativa del modelo, porque en
#   el generador la potencia es proporcional a la irradiancia
#   (potencia = irradiancia * eficiencia * factor_T * factor_viento), y ese
#   factor de proporcionalidad (eficiencia*factor_T*factor_viento) varía
#   poco (~0.15-0.24) frente al rango de irradiancia (100-1000 W/m²).
#   Por eso se ajusta una recta P = m*G + b y se reporta su R².
#
# Panel B: Eficiencia aparente (Potencia/Irradiancia) vs. Temperatura.
#   NO se compara Potencia vs. Temperatura directamente, porque eso mezclaría
#   el efecto de la irradiancia (dominante) con el de la temperatura (que es
#   lo que realmente se quiere probar). Al dividir por la irradiancia se
#   aísla la cantidad que el modelo dice que depende de T:
#   factor_temperatura = 1 - 0.004*(T-25).
#   Aun así, se comprobó numéricamente que esta relación NO es significativa
#   en estos 100 datos (r=-0.15, p=0.15): el término aleatorio 'eficiencia'
#   (sorteado independiente entre 0.15 y 0.22, ±23%) tiene mucha más
#   variabilidad que el efecto determinista de la temperatura (máximo ±4%
#   en el rango 15-35°C), así que el ruido entierra la señal física. Se
#   grafica igual, mostrando el ajuste y el r/p explícitamente: un resultado
#   "sin relación significativa" es un resultado físico válido y hay que
#   reportarlo, no ocultarlo.
fig, axs = plt.subplots(1, 2, figsize=(13, 5.5))
fig.suptitle("Gráficas de Dispersión", fontsize=14, fontweight="bold")

# --- Panel A: Potencia vs Irradiancia ---
m, b, r_a, p_a, _ = linregress(irradiancia, potencia)
x_fit = np.linspace(irradiancia.min(), irradiancia.max(), 200)
sc1 = axs[0].scatter(irradiancia, potencia, c=temperatura, cmap="plasma",
                      s=35, edgecolor="k", linewidth=0.3, zorder=2)
axs[0].plot(x_fit, m * x_fit + b, color="black", linewidth=1.8, linestyle="--",
            zorder=3, label=f"Ajuste: P = {m:.4f}·G + {b:.2f}\n$R^2$ = {r_a**2:.3f}")
axs[0].set_xlabel("Irradiancia Solar G (W/m²)")
axs[0].set_ylabel("Potencia Solar P (W)")
axs[0].set_title("Potencia vs. Irradiancia\n(color = Temperatura)")
axs[0].legend(loc="upper left", fontsize=9, framealpha=0.9)
axs[0].grid(alpha=0.25)
cbar1 = fig.colorbar(sc1, ax=axs[0])
cbar1.set_label("Temperatura (°C)")

# --- Panel B: eficiencia aparente vs Temperatura ---
efic_aparente = potencia / irradiancia
m2, b2, r_b, p_b, _ = linregress(temperatura, efic_aparente)
x_fit2 = np.linspace(temperatura.min(), temperatura.max(), 200)
sc2 = axs[1].scatter(temperatura, efic_aparente, c=viento, cmap="viridis",
                      s=35, edgecolor="k", linewidth=0.3, zorder=2)
axs[1].plot(x_fit2, m2 * x_fit2 + b2, color="black", linewidth=1.8, linestyle="--",
            zorder=3, label=f"Ajuste: r = {r_b:.3f}, p = {p_b:.3f}\n(no significativo, p>0.05)")
axs[1].set_xlabel("Temperatura (°C)")
axs[1].set_ylabel("Eficiencia aparente P/G (adim.)")
axs[1].set_title("Eficiencia aparente vs. Temperatura\n(color = Viento)")
axs[1].legend(loc="upper right", fontsize=9, framealpha=0.9)
axs[1].grid(alpha=0.25)
cbar2 = fig.colorbar(sc2, ax=axs[1])
cbar2.set_label("Viento (m/s)")

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("graficas_dispersion.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# 4. GRÁFICAS DE DENSIDAD
# ---------------------------------------------------------------------------
# Densidad univariada (KDE): estima la forma de la distribución de una sola
# variable, suavizando el histograma. Usamos gaussian_kde de scipy en vez de
# un histograma simple porque con 100 datos un histograma es "ruidoso"
# (depende mucho del número de barras); el KDE da una curva continua que
# representa mejor la tendencia real de la distribución subyacente.
#
# Densidad bivariada (KDE 2D, no hexbin): un hexbin solo cuenta observaciones
# por celda (es un histograma 2D disfrazado), mientras que lo que
# corresponde a "gráfica de densidad" es estimar una función de densidad de
# probabilidad continua. Por eso se usa gaussian_kde en 2 dimensiones
# (Irradiancia, Potencia) y se dibuja como mapa de contornos, igual que se
# hizo en 1D para la Potencia sola.
fig, axs = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle("Gráficas de Densidad", fontsize=14, fontweight="bold")

# --- Densidad univariada de la Potencia Solar ---
kde = gaussian_kde(potencia)
x_vals = np.linspace(potencia.min(), potencia.max(), 300)
axs[0].hist(potencia, bins=15, density=True, alpha=0.4, color="tab:green", edgecolor="k")
axs[0].plot(x_vals, kde(x_vals), color="darkgreen", linewidth=2)
axs[0].set_title("Densidad de la Potencia Solar")
axs[0].set_xlabel("Potencia Solar (W)")
axs[0].set_ylabel("Densidad")
axs[0].grid(alpha=0.25)

# --- Densidad bivariada Irradiancia-Potencia (KDE 2D) ---
xy = np.vstack([irradiancia, potencia])
kde2d = gaussian_kde(xy)
xg = np.linspace(irradiancia.min(), irradiancia.max(), 120)
yg = np.linspace(potencia.min(), potencia.max(), 120)
Xg, Yg = np.meshgrid(xg, yg)
Zg = kde2d(np.vstack([Xg.ravel(), Yg.ravel()])).reshape(Xg.shape)

cf = axs[1].contourf(Xg, Yg, Zg, levels=15, cmap="inferno")
axs[1].scatter(irradiancia, potencia, s=8, color="white", alpha=0.5, linewidth=0)
axs[1].set_title("Densidad conjunta (KDE 2D):\nIrradiancia vs. Potencia")
axs[1].set_xlabel("Irradiancia Solar (W/m²)")
axs[1].set_ylabel("Potencia Solar (W)")
cbar3 = fig.colorbar(cf, ax=axs[1])
cbar3.set_label("Densidad de probabilidad")

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("graficas_densidad.png", dpi=150)
plt.close(fig)

# ---------------------------------------------------------------------------
# 5. GRÁFICAS EN 3D
# ---------------------------------------------------------------------------
# Se eligen 3 variables con relación física directa según el propio modelo
# de generación: Temperatura, Irradiancia y Potencia (la potencia es función
# de ambas). Un scatter 3D permite ver simultáneamente cómo la potencia
# (altura/color) cambia al mover dos variables independientes a la vez,
# algo que un 2D no puede mostrar sin sacrificar una dimensión.
fig = plt.figure(figsize=(12, 5.5))
fig.suptitle("Gráficas en 3D", fontsize=14, fontweight="bold")

ax1 = fig.add_subplot(1, 2, 1, projection="3d")
p = ax1.scatter(temperatura, irradiancia, potencia, c=potencia, cmap="plasma", s=30)
ax1.set_xlabel("Temperatura (°C)")
ax1.set_ylabel("Irradiancia (W/m²)")
ax1.set_zlabel("Potencia (W)")
ax1.set_title("Dispersión 3D")
fig.colorbar(p, ax=ax1, shrink=0.6, label="Potencia (W)")

# Superficie 3D: se interpola sobre una malla regular para poder dibujar
# una superficie continua, ya que los datos originales no están sobre una
# grilla (son 100 puntos generados al azar). La interpolación es SOLO para
# visualizar una tendencia suave; no reemplaza ni corrige los datos reales,
# que siguen viéndose como puntos en el panel izquierdo.
#
# 'griddata' con method="linear" deja como NaN las celdas que quedan FUERA
# del casco convexo de los puntos originales (no puede interpolar donde no
# hay vecinos que "encierren" ese punto). Con solo 100 muestras dispersas,
# eso deja ~10% de la malla vacía y la superficie se ve "cortada" en los
# bordes. Para evitarlo, se rellenan esas celdas con method="nearest"
# (el valor del punto real más cercano). Esto es una segunda simplificación,
# más fuerte que la interpolación lineal: en los bordes ya no se interpola,
# solo se copia el vecino más próximo. Se acepta aquí porque el objetivo es
# solo visual (mostrar una superficie continua); para análisis cuantitativo
# esas zonas de borde no deberían usarse sin más datos.
from scipy.interpolate import griddata
ti = np.linspace(temperatura.min(), temperatura.max(), 40)
ii = np.linspace(irradiancia.min(), irradiancia.max(), 40)
T, I = np.meshgrid(ti, ii)
P_lineal = griddata((temperatura, irradiancia), potencia, (T, I), method="linear")
P_nearest = griddata((temperatura, irradiancia), potencia, (T, I), method="nearest")
P = np.where(np.isnan(P_lineal), P_nearest, P_lineal)

ax2 = fig.add_subplot(1, 2, 2, projection="3d")
surf = ax2.plot_surface(T, I, P, cmap="viridis", edgecolor="none", alpha=0.9)
ax2.set_xlabel("Temperatura (°C)")
ax2.set_ylabel("Irradiancia (W/m²)")
ax2.set_zlabel("Potencia (W)")
ax2.set_title("Superficie interpolada")
fig.colorbar(surf, ax=ax2, shrink=0.6, label="Potencia (W)")

plt.tight_layout(rect=[0, 0, 1, 0.93])
plt.savefig("graficas_3D.png", dpi=150)
plt.close(fig)

print("Listo: se generaron 4 archivos PNG con las gráficas solicitadas.")
#Codigo de todas las gráficas
