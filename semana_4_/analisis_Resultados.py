# ============================================================
# ACTIVIDAD 4
# ANÁLISIS NUMÉRICO DE LAS SERIES DE TAYLOR
# ============================================================

import math
import matplotlib.pyplot as plt


# ============================================================
# FUNCIÓN SENO DE TAYLOR
# ============================================================

def seno_taylor(x, numero_terminos):

    resultado = 0

    for n in range(numero_terminos):

        exponente = 2 * n + 1

        termino = (
            (-1) ** n
            * x ** exponente
            / math.factorial(exponente)
        )

        resultado += termino

    return resultado


# ============================================================
# FUNCIÓN COSENO DE TAYLOR
# ============================================================

def coseno_taylor(x, numero_terminos):

    resultado = 0

    for n in range(numero_terminos):

        exponente = 2 * n

        termino = (
            (-1) ** n
            * x ** exponente
            / math.factorial(exponente)
        )

        resultado += termino

    return resultado


# ============================================================
# VALOR DE x
# ============================================================

x = math.pi / 4


# ============================================================
# VALORES DE REFERENCIA
# ============================================================

seno_real = math.sin(x)
coseno_real = math.cos(x)


# ============================================================
# LISTAS PARA GUARDAR LOS RESULTADOS
# ============================================================

terminos = []

errores_seno = []
errores_coseno = []

errores_porcentaje_seno = []
errores_porcentaje_coseno = []


# ============================================================
# CÁLCULO DEL ERROR
# ============================================================

for n in range(1, 11):

    # --------------------------------------------
    # APROXIMACIONES
    # --------------------------------------------

    seno_aprox = seno_taylor(x, n)
    coseno_aprox = coseno_taylor(x, n)


    # --------------------------------------------
    # ERROR ABSOLUTO
    # --------------------------------------------

    error_seno = abs(
        seno_real - seno_aprox
    )

    error_coseno = abs(
        coseno_real - coseno_aprox
    )


    # --------------------------------------------
    # ERROR RELATIVO
    # --------------------------------------------

    error_relativo_seno = (
        error_seno / abs(seno_real)
    )

    error_relativo_coseno = (
        error_coseno / abs(coseno_real)
    )


    # --------------------------------------------
    # ERROR PORCENTUAL
    # --------------------------------------------

    error_porcentaje_seno = (
        error_relativo_seno * 100
    )

    error_porcentaje_coseno = (
        error_relativo_coseno * 100
    )


    # --------------------------------------------
    # GUARDAR DATOS
    # --------------------------------------------

    terminos.append(n)

    errores_seno.append(error_seno)
    errores_coseno.append(error_coseno)

    errores_porcentaje_seno.append(
        error_porcentaje_seno
    )

    errores_porcentaje_coseno.append(
        error_porcentaje_coseno
    )


# ============================================================
# MOSTRAR TABLA
# ============================================================

print("==========================================================")
print("              ANÁLISIS NUMÉRICO")
print("==========================================================")

print()

print(
    "Términos | Error seno (%) | Error coseno (%)"
)

print("----------------------------------------------------------")

for i in range(len(terminos)):

    print(
        f"{terminos[i]:7d} | "
        f"{errores_porcentaje_seno[i]:14.10f} | "
        f"{errores_porcentaje_coseno[i]:15.10f}"
    )


# ============================================================
# GRÁFICA 1
# ERROR ABSOLUTO DEL SENO
# ============================================================

plt.figure()

plt.plot(
    terminos,
    errores_seno,
    marker="o"
)

plt.xlabel("Número de términos")

plt.ylabel("Error absoluto")

plt.title(
    "Error absoluto de la serie de Taylor para sin(x)"
)

plt.grid()

plt.show()


# ============================================================
# GRÁFICA 2
# ERROR ABSOLUTO DEL COSENO
# ============================================================

plt.figure()

plt.plot(
    terminos,
    errores_coseno,
    marker="o"
)

plt.xlabel("Número de términos")

plt.ylabel("Error absoluto")

plt.title(
    "Error absoluto de la serie de Taylor para cos(x)"
)

plt.grid()

plt.show()


# ============================================================
# GRÁFICA 3
# ERROR PORCENTUAL DEL SENO
# ============================================================

plt.figure()

plt.plot(
    terminos,
    errores_porcentaje_seno,
    marker="o"
)

plt.xlabel("Número de términos")

plt.ylabel("Error porcentual (%)")

plt.title(
    "Error porcentual de la aproximación de sin(x)"
)

plt.grid()

plt.show()


# ============================================================
# GRÁFICA 4
# ERROR PORCENTUAL DEL COSENO
# ============================================================

plt.figure()

plt.plot(
    terminos,
    errores_porcentaje_coseno,
    marker="o"
)

plt.xlabel("Número de términos")

plt.ylabel("Error porcentual (%)")

plt.title(
    "Error porcentual de la aproximación de cos(x)"
)

plt.grid()

plt.show()