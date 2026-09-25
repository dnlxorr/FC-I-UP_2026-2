# ============================================================
# ACTIVIDAD 1 - ERRORES COMPUTACIONALES
# Física Computacional
#
# Se estudiarán:
# 1. Error por truncamiento
# 2. Error por redondeo
# ============================================================


# ============================================================
# 1. IMPORTAR LIBRERÍAS
# ============================================================

import math
import matplotlib.pyplot as plt


# math
# ------------------------------------------------------------
# La biblioteca math contiene funciones matemáticas.
#
# En este trabajo utilizaremos:
# math.sin() -> calcula el seno de un número
# math.pi   -> proporciona el valor de pi
# math.factorial() -> calcula factoriales
#
# ------------------------------------------------------------

# matplotlib.pyplot
# ------------------------------------------------------------
# Esta biblioteca permite crear gráficas.
#
# La llamamos "plt" para poder escribir:
#
# plt.plot()
# plt.xlabel()
# plt.ylabel()
# plt.show()
#
# ------------------------------------------------------------


# ============================================================
# 2. FUNCIÓN PARA CALCULAR EL SENO MEDIANTE TAYLOR
# ============================================================

def seno_taylor(x, numero_terminos):

    # Comenzamos con el resultado igual a cero.
    resultado = 0

    # Recorremos la cantidad de términos solicitada.
    for n in range(numero_terminos):

        # Calculamos el exponente:
        #
        # Para n = 0 -> 1
        # Para n = 1 -> 3
        # Para n = 2 -> 5
        #
        # Por eso utilizamos:
        #
        # 2*n + 1
        #
        exponente = 2 * n + 1

        # Calculamos el término de Taylor:
        #
        # (-1)^n * x^(2n+1) / (2n+1)!
        #
        termino = ((-1) ** n) * (x ** exponente) / math.factorial(exponente)

        # Sumamos el término al resultado.
        resultado = resultado + termino

    # Devolvemos el resultado final.
    return resultado


# ============================================================
# 3. VALOR DE x
# ============================================================

# Vamos a trabajar con:
#
# x = 0.5 radianes
#
# Es importante utilizar radianes porque las series de Taylor
# para las funciones trigonométricas están expresadas en
# términos de radianes.

x = 0.5


# ============================================================
# 4. VALOR DE REFERENCIA
# ============================================================

# Calculamos el seno utilizando la función incorporada
# de Python.

valor_real = math.sin(x)

print("==============================================")
print("      ERROR POR TRUNCAMIENTO")
print("==============================================")

print("Valor de x:", x)
print("Valor de referencia:", valor_real)
print()


# ============================================================
# 5. CALCULAR EL ERROR UTILIZANDO DIFERENTES TÉRMINOS
# ============================================================

# Creamos listas vacías para guardar los resultados.

numero_terminos_lista = []
errores_truncamiento = []
resultados_taylor = []


# Probamos desde 1 hasta 10 términos.

for numero_terminos in range(1, 11):

    # Calculamos la aproximación mediante Taylor.
    aproximacion = seno_taylor(x, numero_terminos)

    # Calculamos el error absoluto.
    #
    # Error absoluto =
    # |valor real - valor aproximado|
    #
    error = abs(valor_real - aproximacion)

    # Guardamos los valores.
    numero_terminos_lista.append(numero_terminos)
    resultados_taylor.append(aproximacion)
    errores_truncamiento.append(error)

    # Mostramos los resultados.
    print("Número de términos:", numero_terminos)
    print("Aproximación:", aproximacion)
    print("Error absoluto:", error)
    print("----------------------------------------------")


# ============================================================
# 6. GRÁFICA DEL ERROR POR TRUNCAMIENTO
# ============================================================

plt.figure()

plt.plot(
    numero_terminos_lista,
    errores_truncamiento,
    marker="o"
)

plt.xlabel("Número de términos")
plt.ylabel("Error absoluto")

plt.title(
    "Error por truncamiento en la aproximación de sin(x)"
)

plt.grid()

plt.show()


# ============================================================
# 7. ERROR POR REDONDEO
# ============================================================

print()
print("==============================================")
print("          ERROR POR REDONDEO")
print("==============================================")


# Utilizamos pi como ejemplo.

valor_original = math.pi

print("Valor original de π:", valor_original)
print()


# Creamos listas para guardar:
#
# cantidad de decimales
# error producido

decimales_lista = []
errores_redondeo = []


# Probamos desde 1 hasta 10 cifras decimales.

for decimales in range(1, 11):

    # Redondeamos el número.
    valor_redondeado = round(valor_original, decimales)

    # Calculamos el error absoluto.
    error = abs(valor_original - valor_redondeado)

    # Guardamos los resultados.
    decimales_lista.append(decimales)
    errores_redondeo.append(error)

    # Mostramos los resultados.
    print("Decimales utilizados:", decimales)
    print("Valor redondeado:", valor_redondeado)
    print("Error absoluto:", error)
    print("----------------------------------------------")


# ============================================================
# 8. GRÁFICA DEL ERROR POR REDONDEO
# ============================================================

plt.figure()

plt.plot(
    decimales_lista,
    errores_redondeo,
    marker="o"
)

plt.xlabel("Cantidad de cifras decimales")
plt.ylabel("Error absoluto")

plt.title(
    "Error por redondeo en la representación de π"
)

plt.grid()

plt.show()