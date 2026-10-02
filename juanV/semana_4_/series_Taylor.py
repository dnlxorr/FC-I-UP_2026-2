# ============================================================
# ACTIVIDAD 3: SERIES DE TAYLOR
# ============================================================

import math


# ============================================================
# SERIE DE TAYLOR DEL SENO
# ============================================================

def seno_taylor(x, n):

    suma = 0

    for i in range(n):

        exponente = 2 * i + 1

        termino = ((-1) ** i) * (x ** exponente) / math.factorial(exponente)

        suma += termino

    return suma


# ============================================================
# SERIE DE TAYLOR DEL COSENO
# ============================================================

def coseno_taylor(x, n):

    suma = 0

    for i in range(n):

        exponente = 2 * i

        termino = ((-1) ** i) * (x ** exponente) / math.factorial(exponente)

        suma += termino

    return suma


# ============================================================
# COMPARACION
# ============================================================

x = math.pi / 4

print("===== ACTIVIDAD 3 =====")

print("\nValor de x:")
print(x)

print("\nSENO")
print("-----------------------------")

valor_real_seno = math.sin(x)

for n in [1, 2, 3, 4, 5, 6, 10]:

    aproximacion = seno_taylor(x, n)

    error = abs(valor_real_seno - aproximacion)

    print("Términos:", n)
    print("Taylor:", aproximacion)
    print("Math:", valor_real_seno)
    print("Error:", error)
    print()


print("\nCOSENO")
print("-----------------------------")

valor_real_coseno = math.cos(x)

for n in [1, 2, 3, 4, 5, 6, 10]:

    aproximacion = coseno_taylor(x, n)

    error = abs(valor_real_coseno - aproximacion)

    print("Términos:", n)
    print("Taylor:", aproximacion)
    print("Math:", valor_real_coseno)
    print("Error:", error)
    print()