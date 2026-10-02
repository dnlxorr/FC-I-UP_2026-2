# ============================================================
#     GRÁFICAS Y VISUALIZACIÓN - EXPERIMENTO DEL PÉNDULO
# ============================================================
#
# Este programa utiliza el dataset generado del experimento
# del péndulo simple para construir cuatro tipos de gráficas:
#
# 1. Gráfica en 2D
# 2. Gráfica de dispersión
# 3. Gráfica de densidad
# 4. Gráfica en 3D
#
# ============================================================


# ============================================================
# 1. IMPORTAR LAS LIBRERÍAS
# ============================================================

# NumPy:
# Se utiliza para realizar cálculos matemáticos.
import numpy as np

# Pandas:
# Se utiliza para trabajar con tablas y datasets.
import pandas as pd

# Matplotlib:
# Se utiliza para crear las gráficas.
import matplotlib.pyplot as plt

# mpl_toolkits:
# Nos permite crear gráficas tridimensionales.
from mpl_toolkits.mplot3d import Axes3D


# ============================================================
# 2. CREAR EL DATASET
# ============================================================

# Valor teórico de la gravedad terrestre.
g = 9.81


# Longitudes utilizadas en el experimento.
longitudes = [
    0.20,
    0.30,
    0.40,
    0.50,
    0.60,
    0.70,
    0.80,
    0.90,
    1.00,
    1.10
]


# Número de mediciones realizadas para cada longitud.
numero_mediciones = 10


# Lista donde vamos a guardar todas las mediciones.
datos = []


# Fijamos una semilla para que los números aleatorios
# sean siempre los mismos.
np.random.seed(42)


# Identificador de cada medición.
ID = 1


# ============================================================
# 3. GENERAR LAS MEDICIONES
# ============================================================

# Recorremos cada longitud del péndulo.
for longitud in longitudes:

    # --------------------------------------------------------
    # Período teórico del péndulo
    #
    # T = 2π √(L/g)
    # --------------------------------------------------------

    periodo_teorico = (
        2 * np.pi * np.sqrt(longitud / g)
    )


    # Realizamos 10 mediciones para cada longitud.
    for medicion in range(1, numero_mediciones + 1):

        # Tiempo teórico de 10 oscilaciones.
        tiempo_teorico = 10 * periodo_teorico


        # Simulamos un pequeño error experimental.
        error = np.random.normal(0, 0.05)


        # Tiempo experimental de 10 oscilaciones.
        tiempo_10 = tiempo_teorico + error


        # Calculamos el período experimental.
        periodo = tiempo_10 / 10


        # Calculamos el período al cuadrado.
        periodo_cuadrado = periodo ** 2


        # Calculamos la gravedad experimental:
        #
        # g = 4π²L/T²

        gravedad = (
            4 * np.pi ** 2 * longitud
        ) / periodo_cuadrado


        # Guardamos todos los datos.
        datos.append([
            ID,
            longitud,
            medicion,
            tiempo_10,
            periodo,
            periodo_cuadrado,
            gravedad
        ])


        # Aumentamos el ID.
        ID += 1


# ============================================================
# 4. CREAR EL DATAFRAME
# ============================================================

dataset = pd.DataFrame(
    datos,
    columns=[
        "ID",
        "Longitud del pendulo (m)",
        "Numero de medicion",
        "Tiempo de 10 oscilaciones (s)",
        "Periodo de oscilacion (s)",
        "Periodo al cuadrado (s²)",
        "Gravedad experimental (m/s²)"
    ]
)


# Redondeamos los valores para que sean más fáciles de leer.
dataset = dataset.round({
    "Longitud del pendulo (m)": 2,
    "Tiempo de 10 oscilaciones (s)": 3,
    "Periodo de oscilacion (s)": 3,
    "Periodo al cuadrado (s²)": 4,
    "Gravedad experimental (m/s²)": 3
})


# ============================================================
# 5. MOSTRAR EL DATASET
# ============================================================

print("\n")
print("=" * 80)
print("       DATASET - EXPERIMENTO DEL PÉNDULO SIMPLE")
print("=" * 80)

print(dataset.to_string(index=False))

print("=" * 80)

print(f"\nNúmero de mediciones: {dataset.shape[0]}")
print(f"Número de variables: {dataset.shape[1]}")


# ============================================================
# 6. GRÁFICA 1 - GRÁFICA EN 2D
# ============================================================
#
# Vamos a representar:
#
# Eje X → Longitud del péndulo
# Eje Y → Período de oscilación
#
# Esto permite observar cómo aumenta el período cuando
# aumenta la longitud del péndulo.
#
# ============================================================


# Creamos una nueva figura.
plt.figure(figsize=(10, 6))


# ------------------------------------------------------------
# Datos experimentales
# ------------------------------------------------------------

plt.scatter(
    dataset["Longitud del pendulo (m)"],
    dataset["Periodo de oscilacion (s)"],
    label="Datos experimentales"
)


# ------------------------------------------------------------
# Curva teórica
# ------------------------------------------------------------

# Creamos muchos valores de longitud para que la curva
# teórica se vea suave.

L_teorica = np.linspace(0.20, 1.10, 200)


# Calculamos el período teórico para cada longitud.

T_teorico = 2 * np.pi * np.sqrt(L_teorica / g)


# Dibujamos la curva teórica.

plt.plot(
    L_teorica,
    T_teorico,
    label="Modelo teórico"
)


# ------------------------------------------------------------
# Títulos y etiquetas
# ------------------------------------------------------------

plt.title(
    "Período del péndulo en función de la longitud"
)

plt.xlabel(
    "Longitud del péndulo (m)"
)

plt.ylabel(
    "Período de oscilación (s)"
)


# Mostramos la leyenda.
plt.legend()


# Activamos la cuadrícula.
plt.grid(True)


# Ajustamos automáticamente los elementos.
plt.tight_layout()


# Mostramos la gráfica.
plt.show()


# ============================================================
# 7. GRÁFICA 2 - GRÁFICA DE DISPERSIÓN
# ============================================================
#
# Vamos a representar:
#
# Eje X → Longitud L
# Eje Y → Período² T²
#
# La ecuación:
#
# T² = (4π²/g)L
#
# indica que T² y L tienen una relación aproximadamente
# lineal.
#
# ============================================================


plt.figure(figsize=(10, 6))


# Creamos la gráfica de dispersión.

plt.scatter(
    dataset["Longitud del pendulo (m)"],
    dataset["Periodo al cuadrado (s²)"],
    label="Mediciones experimentales"
)


# ------------------------------------------------------------
# Línea de tendencia
# ------------------------------------------------------------

# Ajustamos una recta a los datos:
#
# T² = mL + b
#
# np.polyfit encuentra los valores de m y b.

pendiente, intercepto = np.polyfit(
    dataset["Longitud del pendulo (m)"],
    dataset["Periodo al cuadrado (s²)"],
    1
)


# Creamos valores de longitud para dibujar la recta.

L_ajuste = np.linspace(0.20, 1.10, 100)


# Calculamos T² utilizando la recta obtenida.

T2_ajuste = (
    pendiente * L_ajuste
    + intercepto
)


# Dibujamos la línea de tendencia.

plt.plot(
    L_ajuste,
    T2_ajuste,
    label="Ajuste lineal"
)


# ------------------------------------------------------------
# Etiquetas
# ------------------------------------------------------------

plt.title(
    "Relación entre la longitud y el período al cuadrado"
)

plt.xlabel(
    "Longitud del péndulo L (m)"
)

plt.ylabel(
    "Período al cuadrado T² (s²)"
)


plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 8. GRÁFICA 3 - GRÁFICA DE DENSIDAD
# ============================================================
#
# Una gráfica de densidad permite observar dónde se concentran
# los valores de nuestros datos.
#
# Aquí vamos a analizar la gravedad experimental.
#
# ============================================================


plt.figure(figsize=(10, 6))


# Utilizamos un histograma para representar la distribución
# de los valores de gravedad experimental.
#
# density=True convierte las cantidades en una densidad
# de probabilidad.

plt.hist(
    dataset["Gravedad experimental (m/s²)"],
    bins=12,
    density=True,
    alpha=0.7
)


# Línea vertical indicando la gravedad teórica.

plt.axvline(
    g,
    linestyle="--",
    label="Gravedad teórica = 9.81 m/s²"
)


# ------------------------------------------------------------
# Etiquetas
# ------------------------------------------------------------

plt.title(
    "Densidad de la gravedad experimental"
)

plt.xlabel(
    "Gravedad experimental (m/s²)"
)

plt.ylabel(
    "Densidad"
)


plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()


# ============================================================
# 9. GRÁFICA 4 - GRÁFICA EN 3D
# ============================================================
#
# En esta gráfica utilizaremos tres variables:
#
# X → Longitud del péndulo
# Y → Número de medición
# Z → Gravedad experimental
#
# Esto permite observar simultáneamente tres variables.
#
# ============================================================


# Creamos la figura.

fig = plt.figure(figsize=(11, 8))


# Creamos un sistema de ejes tridimensionales.

ax = fig.add_subplot(
    111,
    projection="3d"
)


# ------------------------------------------------------------
# Datos para los tres ejes
# ------------------------------------------------------------

X = dataset[
    "Longitud del pendulo (m)"
]

Y = dataset[
    "Numero de medicion"
]

Z = dataset[
    "Gravedad experimental (m/s²)"
]


# ------------------------------------------------------------
# Crear la gráfica de dispersión 3D
# ------------------------------------------------------------

ax.scatter(
    X,
    Y,
    Z
)


# ------------------------------------------------------------
# Etiquetas de los ejes
# ------------------------------------------------------------

ax.set_xlabel(
    "Longitud del péndulo (m)"
)

ax.set_ylabel(
    "Número de medición"
)

ax.set_zlabel(
    "Gravedad experimental (m/s²)"
)


# Título.

ax.set_title(
    "Gravedad experimental del péndulo - Gráfica 3D"
)


# Mostramos la gráfica.

plt.tight_layout()

plt.show()


# ============================================================
#                         FIN
# ============================================================