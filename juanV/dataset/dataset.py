# ============================================================
#          DATASET - EXPERIMENTO DEL PÉNDULO SIMPLE
# ============================================================
#
# OBJETIVO:
# Crear un dataset basado en un experimento del péndulo simple.
#
# Vamos a simular:
# - 10 longitudes diferentes
# - 10 mediciones para cada longitud
# - 100 mediciones en total
#
# También calcularemos:
# - Tiempo de 10 oscilaciones
# - Período de oscilación
# - Período al cuadrado
# - Gravedad experimental
#
# ============================================================


# ============================================================
# 1. IMPORTAR LAS LIBRERÍAS
# ============================================================

# NumPy permite realizar cálculos matemáticos y generar
# números aleatorios para simular errores experimentales.
import numpy as np

# Pandas permite crear y organizar datos en forma de tabla.
import pandas as pd

# ============================================================
# 2. DEFINIR LA GRAVEDAD TEÓRICA
# ============================================================

# Aceleración de la gravedad terrestre.
#
# Unidad:
# metros por segundo al cuadrado (m/s²)
#
# Este valor se utilizará para calcular el período teórico
# del péndulo.
g = 9.81

# ============================================================
# 3. DEFINIR LAS LONGITUDES DEL PÉNDULO
# ============================================================

# Creamos una lista con las longitudes que vamos a utilizar.
#
# Todas las longitudes están expresadas en metros.
#
# Tenemos 10 longitudes:
# 0.20 m, 0.30 m, 0.40 m, ..., 1.10 m

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

# ============================================================
# 4. DEFINIR EL NÚMERO DE MEDICIONES
# ============================================================

# Para cada longitud vamos a realizar 10 mediciones.
#
# Tenemos:
#
# 10 longitudes × 10 mediciones = 100 mediciones

numero_mediciones = 10

# ============================================================
# 5. CREAR UNA LISTA PARA GUARDAR LOS DATOS
# ============================================================

# Esta lista estará vacía inicialmente.
#
# En ella iremos almacenando cada medición realizada.
datos = []

# ============================================================
# 6. FIJAR LA SEMILLA DE LOS NÚMEROS ALEATORIOS
# ============================================================

# Utilizamos una semilla para que los resultados aleatorios
# sean siempre los mismos cada vez que ejecutemos el programa.
#
# Esto permite reproducir exactamente el mismo dataset.

np.random.seed(42)

# ============================================================
# 7. CREAR EL IDENTIFICADOR DE LAS MEDICIONES
# ============================================================

# Cada medición tendrá un número identificador.
#
# La primera medición será:
# ID = 1
#
# La última será:
# ID = 100

ID = 1

# ============================================================
# 8. RECORRER TODAS LAS LONGITUDES
# ============================================================

# El ciclo for toma una longitud de la lista cada vez.
#
# Por ejemplo:
#
# Primera vuelta  → 0.20 m
# Segunda vuelta  → 0.30 m
# Tercera vuelta  → 0.40 m
# ...
#
for longitud in longitudes:

    # ========================================================
    # 9. CALCULAR EL PERÍODO TEÓRICO
    # ========================================================

    # Para un péndulo simple utilizamos:
    #
    # T = 2π √(L/g)
    #
    # Donde:
    #
    # T = período de oscilación
    # L = longitud del péndulo
    # g = gravedad
    #
    # np.pi representa π.
    #
    # np.sqrt() calcula la raíz cuadrada.

    periodo_teorico = (
            2 * np.pi * np.sqrt(longitud / g)
    )

    # ========================================================
    # 10. REALIZAR LAS 10 MEDICIONES
    # ========================================================

    # Repetimos el experimento 10 veces para cada longitud.
    #
    # range(1, 11) genera:
    #
    # 1, 2, 3, ..., 10

    for medicion in range(1, numero_mediciones + 1):
        # ====================================================
        # 11. CALCULAR EL TIEMPO TEÓRICO DE 10 OSCILACIONES
        # ====================================================

        # El período representa el tiempo necesario para
        # realizar una oscilación.
        #
        # Por lo tanto, para 10 oscilaciones:
        #
        # Tiempo = 10 × período

        tiempo_teorico = 10 * periodo_teorico

        # ====================================================
        # 12. SIMULAR EL ERROR EXPERIMENTAL
        # ====================================================

        # En un experimento real las mediciones no son perfectas.
        #
        # Por ejemplo, al medir con un cronómetro podríamos
        # obtener:
        #
        # 14.20 s
        # 14.23 s
        # 14.18 s
        #
        # aunque el valor teórico sea aproximadamente 14.21 s.
        #
        # np.random.normal() genera un valor aleatorio
        # siguiendo una distribución normal.
        #
        # El primer número (0) es la media del error.
        # El segundo número (0.05) es la desviación estándar.

        error = np.random.normal(0, 0.05)

        # ====================================================
        # 13. OBTENER EL TIEMPO EXPERIMENTAL
        # ====================================================

        # Sumamos el error al tiempo teórico.
        #
        # Esto simula una medición obtenida en un laboratorio.

        tiempo_10 = tiempo_teorico + error

        # ====================================================
        # 14. CALCULAR EL PERÍODO EXPERIMENTAL
        # ====================================================

        # El tiempo anterior corresponde a 10 oscilaciones.
        #
        # Para encontrar el período de UNA oscilación:
        #
        # T = Tiempo de 10 oscilaciones / 10

        periodo = tiempo_10 / 10

        # ====================================================
        # 15. CALCULAR EL PERÍODO AL CUADRADO
        # ====================================================

        # Elevamos el período al cuadrado.
        #
        # En Python:
        #
        # x ** 2
        #
        # significa x elevado a la segunda potencia.

        periodo_cuadrado = periodo ** 2

        # ====================================================
        # 16. CALCULAR LA GRAVEDAD EXPERIMENTAL
        # ====================================================

        # Partimos de la ecuación del péndulo:
        #
        # T = 2π √(L/g)
        #
        # Elevando al cuadrado:
        #
        # T² = 4π²L/g
        #
        # Despejando g:
        #
        # g = 4π²L/T²
        #
        # Utilizamos:
        #
        # L = longitud
        # T = período experimental

        gravedad = (
                           4 * np.pi ** 2 * longitud
                   ) / periodo_cuadrado

        # ====================================================
        # 17. GUARDAR LA MEDICIÓN
        # ====================================================

        # Agregamos una nueva fila a nuestra lista.
        #
        # Cada fila tendrá 7 valores:
        #
        # 1. ID
        # 2. Longitud
        # 3. Número de medición
        # 4. Tiempo de 10 oscilaciones
        # 5. Período
        # 6. Período²
        # 7. Gravedad experimental

        datos.append([
            ID,
            longitud,
            medicion,
            tiempo_10,
            periodo,
            periodo_cuadrado,
            gravedad
        ])

        # ====================================================
        # 18. AUMENTAR EL ID
        # ====================================================

        # Después de guardar la medición aumentamos el ID
        # en una unidad.
        #
        # Por ejemplo:
        #
        # 1 → 2 → 3 → 4 → ... → 100

        ID += 1

# ============================================================
# 19. CREAR EL DATAFRAME
# ============================================================

# Convertimos nuestra lista "datos" en una tabla de Pandas.
#
# Un DataFrame está compuesto por:
#
# FILAS    → mediciones
# COLUMNAS → variables
#
# En nuestro caso:
#
# 100 filas
# 7 columnas

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

# ============================================================
# 20. REDONDEAR LOS RESULTADOS
# ============================================================

# Los cálculos matemáticos pueden generar muchos decimales.
#
# Por ejemplo:
#
# 1.423847291845
#
# Para que la tabla sea más fácil de leer, redondeamos
# cada variable a un número determinado de decimales.

dataset = dataset.round({

    # Longitud:
    # 2 cifras decimales.
    "Longitud del pendulo (m)": 2,

    # Tiempo:
    # 3 cifras decimales.
    "Tiempo de 10 oscilaciones (s)": 3,

    # Período:
    # 3 cifras decimales.
    "Periodo de oscilacion (s)": 3,

    # Período²:
    # 4 cifras decimales.
    "Periodo al cuadrado (s²)": 4,

    # Gravedad:
    # 3 cifras decimales.
    "Gravedad experimental (m/s²)": 3
})

# ============================================================
# 21. MOSTRAR EL TÍTULO
# ============================================================

# "\n" genera un salto de línea.

print("\n")

# Creamos una línea visual de separación.

print("=" * 100)

# Mostramos el nombre del dataset.

print("              DATASET - EXPERIMENTO DEL PÉNDULO SIMPLE")

print("=" * 100)

# ============================================================
# 22. MOSTRAR LA TABLA
# ============================================================

# to_string() convierte el DataFrame en una tabla de texto.
#
# index=False evita mostrar el índice interno de Pandas.

print(dataset.to_string(index=False))

# Línea final de separación.

print("=" * 100)

# ============================================================
# 23. MOSTRAR INFORMACIÓN DEL DATASET
# ============================================================

# dataset.shape devuelve el tamaño de la tabla.
#
# Por ejemplo:
#
# (100, 7)
#
# significa:
#
# 100 filas
# 7 columnas
#
# dataset.shape[0] → número de filas
# dataset.shape[1] → número de columnas

print(f"\nNúmero de mediciones: {dataset.shape[0]}")

print(f"Número de variables: {dataset.shape[1]}")

# ============================================================
# 24. GUARDAR EL DATASET COMO ARCHIVO CSV
# ============================================================

# to_csv() permite guardar nuestro DataFrame
# como un archivo CSV.
#
# CSV significa:
#
# Comma-Separated Values
#
# Este formato puede abrirse con:
#
# - Excel
# - Google Sheets
# - Python
# - MATLAB
# - R
#
# index=False evita crear una columna adicional
# con el índice de Pandas.

dataset.to_csv(
    "dataset_pendulo_simple.csv",
    index=False
)

# ============================================================
# 25. CONFIRMAR QUE EL ARCHIVO FUE GUARDADO
# ============================================================

print("\nDataset guardado como: dataset_pendulo_simple.csv")

# ============================================================
#                       FIN DEL PROGRAMA
# ============================================================