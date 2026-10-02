import math
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Serie de Taylor de e^x centrada en a = 0
# ---------------------------------------------------------

def exponencial_taylor(x, n):
    """
    Aproximación de e^x mediante la serie de Taylor
    centrada en a = 0 hasta el orden n.
    """
    suma = 0.0

    for k in range(n + 1):
        suma += x**k / math.factorial(k)

    return suma


# ---------------------------------------------------------
# Parámetros
# ---------------------------------------------------------

# Intervalo donde se evaluará la función
x_min = -2
x_max = 2

# Número de puntos
num_puntos = 1000

# Órdenes de Taylor: n < 6
ordenes = range(6)

# Generar valores de x
x_values = [
    x_min + i * (x_max - x_min) / (num_puntos - 1)
    for i in range(num_puntos)
]


# ---------------------------------------------------------
# Calcular errores
# ---------------------------------------------------------

errores = {}

for n in ordenes:

    error_absoluto = []
    error_relativo = []

    for x in x_values:

        # Valor aproximado mediante Taylor
        aproximacion = exponencial_taylor(x, n)

        # Valor "exacto" usando math.exp
        exacto = math.exp(x)

        # Error absoluto
        error = abs(exacto - aproximacion)

        # Error relativo porcentual
        if exacto != 0:
            error_porcentual = (error / abs(exacto)) * 100
        else:
            error_porcentual = 0

        error_absoluto.append(error)
        error_relativo.append(error_porcentual)

    errores[n] = {
        "absoluto": error_absoluto,
        "relativo": error_relativo
    }


# ---------------------------------------------------------
# Gráfica de las aproximaciones
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

# Función exacta
y_exacta = [math.exp(x) for x in x_values]

plt.plot(
    x_values,
    y_exacta,
    label="math.exp(x)",
    linewidth=2
)

# Aproximaciones de Taylor
for n in ordenes:

    y_taylor = [
        exponencial_taylor(x, n)
        for x in x_values
    ]

    plt.plot(
        x_values,
        y_taylor,
        label=f"Taylor n={n}"
    )

plt.xlabel("x")
plt.ylabel("$e^x$")
plt.title("Serie de Taylor de $e^x$ vs math.exp(x)")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("comparacion_taylor_exp.png", dpi=300)

plt.show()


# ---------------------------------------------------------
# Gráfica del error absoluto
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

for n in ordenes:

    plt.plot(
        x_values,
        errores[n]["absoluto"],
        label=f"n={n}"
    )

plt.xlabel("x")
plt.ylabel("Error absoluto")
plt.title("Error absoluto de la serie de Taylor")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.savefig("error_absoluto_taylor.png", dpi=300)

plt.show()


# ---------------------------------------------------------
# Gráfica del error relativo porcentual
# ---------------------------------------------------------

plt.figure(figsize=(10, 6))

for n in ordenes:

    plt.plot(
        x_values,
        errores[n]["relativo"],
        label=f"n={n}"
    )

plt.xlabel("x")
plt.ylabel("Error relativo (%)")
plt.title("Error relativo porcentual de la serie de Taylor")
plt.grid(True)
plt.legend()
plt.tight_layout()

plt.show()


# ---------------------------------------------------------
# Mostrar el error máximo para cada n
# ---------------------------------------------------------

print("\nERROR MÁXIMO PARA CADA ORDEN")
print("-" * 50)

for n in ordenes:

    error_max = max(errores[n]["absoluto"])
    error_rel_max = max(errores[n]["relativo"])

    print(
        f"n = {n}: "
        f"Error absoluto máximo = {error_max:.10e}, "
        f"Error relativo máximo = {error_rel_max:.10e} %"
    )