# ============================================================
# ACTIVIDAD 3 - SERIES DE TAYLOR
# Física Computacional
#
# Aproximación de:
# 1. Seno
# 2. Coseno
#
# Comparación con las funciones de Python:
# math.sin()
# math.cos()
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

import math
import matplotlib.pyplot as plt


# ============================================================
# 2. FUNCIÓN SENO MEDIANTE SERIE DE TAYLOR
# ============================================================

def seno_taylor(x, numero_terminos):

    # Inicializamos la suma en cero.
    resultado = 0

    # Recorremos la cantidad de términos solicitada.
    for n in range(numero_terminos):

        # Exponente:
        #
        # 2n + 1
        #
        # genera:
        #
        # 1, 3, 5, 7, 9, ...

        exponente = 2 * n + 1

        # Calculamos el término de Taylor.
        termino = (
            (-1) ** n
            * x ** exponente
            / math.factorial(exponente)
        )

        # Sumamos el término.
        resultado += termino

    # Devolvemos la aproximación.
    return resultado


# ============================================================
# 3. FUNCIÓN COSENO MEDIANTE SERIE DE TAYLOR
# ============================================================

def coseno_taylor(x, numero_terminos):

    # Inicializamos la suma en cero.
    resultado = 0

    # Recorremos la cantidad de términos.
    for n in range(numero_terminos):

        # Exponente:
        #
        # 2n
        #
        # genera:
        #
        # 0, 2, 4, 6, 8, ...

        exponente = 2 * n

        # Calculamos el término de Taylor.
        termino = (
            (-1) ** n
            * x ** exponente
            / math.factorial(exponente)
        )

        # Sumamos el término.
        resultado += termino

    # Devolvemos la aproximación.
    return resultado


# ============================================================
# 4. VALOR DE x
# ============================================================

# Utilizamos 45 grados.
#
# Pero las series de Taylor trabajan con radianes.
#
# 45 grados = π/4 radianes.

x = math.pi / 4


# ============================================================
# 5. VALORES DE REFERENCIA
# ============================================================

# Utilizamos las funciones de la biblioteca math.

seno_real = math.sin(x)
coseno_real = math.cos(x)


print("================================================")
print("       SERIES DE TAYLOR - SENO Y COSENO")
print("================================================")

print("Ángulo utilizado:", x, "radianes")
print()

print("Valor de math.sin(x):", seno_real)
print("Valor de math.cos(x):", coseno_real)

print()


# ============================================================
# 6. COMPARACIÓN CON DIFERENTES CANTIDADES DE TÉRMINOS
# ============================================================

# Listas para guardar los resultados.

terminos_lista = []

errores_seno = []
errores_coseno = []

resultados_seno = []
resultados_coseno = []


# Probamos desde 1 hasta 10 términos.

for numero_terminos in range(1, 11):

    # --------------------------------------------
    # SENO
    # --------------------------------------------

    aproximacion_seno = seno_taylor(
        x,
        numero_terminos
    )

    # Error absoluto del seno.

    error_seno = abs(
        seno_real - aproximacion_seno
    )


    # --------------------------------------------
    # COSENO
    # --------------------------------------------

    aproximacion_coseno = coseno_taylor(
        x,
        numero_terminos
    )

    # Error absoluto del coseno.

    error_coseno = abs(
        coseno_real - aproximacion_coseno
    )


    # --------------------------------------------
    # GUARDAR LOS RESULTADOS
    # --------------------------------------------

    terminos_lista.append(numero_terminos)

    resultados_seno.append(
        aproximacion_seno
    )

    resultados_coseno.append(
        aproximacion_coseno
    )

    errores_seno.append(
        error_seno
    )

    errores_coseno.append(
        error_coseno
    )


# ============================================================
# 7. MOSTRAR RESULTADOS EN PANTALLA
# ============================================================

print("================================================")
print("              RESULTADOS")
print("================================================")

print()

for i in range(len(terminos_lista)):

    print("Número de términos:",
          terminos_lista[i])

    print("Seno Taylor:",
          resultados_seno[i])

    print("Error del seno:",
          errores_seno[i])

    print("Coseno Taylor:",
          resultados_coseno[i])

    print("Error del coseno:",
          errores_coseno[i])

    print("-----------------------------------------------")


# ============================================================
# 8. GRÁFICA DEL ERROR DEL SENO
# ============================================================

plt.figure()

plt.plot(
    terminos_lista,
    errores_seno,
    marker="o"
)

plt.xlabel("Número de términos")
plt.ylabel("Error absoluto")

plt.title(
    "Error de la serie de Taylor para sin(x)"
)

plt.grid()

plt.show()


# ============================================================
# 9. GRÁFICA DEL ERROR DEL COSENO
# ============================================================

plt.figure()

plt.plot(
    terminos_lista,
    errores_coseno,
    marker="o"
)

plt.xlabel("Número de términos")
plt.ylabel("Error absoluto")

plt.title(
    "Error de la serie de Taylor para cos(x)"
)

plt.grid()

plt.show()


# ============================================================
# 10. COMPARACIÓN DE SENO
# ============================================================

plt.figure()

plt.plot(
    terminos_lista,
    resultados_seno,
    marker="o",
    label="Taylor"
)

plt.axhline(
    seno_real,
    linestyle="--",
    label="math.sin(x)"
)

plt.xlabel("Número de términos")
plt.ylabel("Valor de sin(x)")

plt.title(
    "Comparación entre Taylor y math.sin(x)"
)

plt.legend()

plt.grid()

plt.show()


# ============================================================
# 11. COMPARACIÓN DE COSENO
# ============================================================

plt.figure()

plt.plot(
    terminos_lista,
    resultados_coseno,
    marker="o",
    label="Taylor"
)

plt.axhline(
    coseno_real,
    linestyle="--",
    label="math.cos(x)"
)

plt.xlabel("Número de términos")
plt.ylabel("Valor de cos(x)")

plt.title(
    "Comparación entre Taylor y math.cos(x)"
)

plt.legend()

plt.grid()

plt.show()