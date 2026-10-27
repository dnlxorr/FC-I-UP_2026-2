
"""
Comparación de cuadratura de Gauss-Legendre y Romberg
aplicadas al trabajo realizado por una fuerza variable.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros físicos
F0 = 10.0
ALPHA = 0.5
A = 0.0
B = 4.0


def fuerza(x):
    """Fuerza variable en newtons."""
    return F0 * np.exp(-ALPHA * np.asarray(x))


def trabajo_exacto():
    """Solución analítica del trabajo."""
    return (F0 / ALPHA) * (
        np.exp(-ALPHA * A) - np.exp(-ALPHA * B)
    )


def cuadratura_gauss(a, b, n):
    """Calcula la integral mediante Gauss-Legendre."""
    nodos, pesos = np.polynomial.legendre.leggauss(n)

    x = 0.5 * (b - a) * nodos + 0.5 * (b + a)
    w = 0.5 * (b - a) * pesos

    valores = fuerza(x)
    trabajo = np.sum(w * valores)

    return float(trabajo), x, valores, n


def romberg(a, b, k_max=4):
    """Calcula la tabla de Romberg."""
    R = np.zeros((k_max, k_max))

    h = b - a
    R[0, 0] = 0.5 * h * (fuerza(a) + fuerza(b))

    for i in range(1, k_max):
        h /= 2.0

        suma = sum(
            fuerza(a + k * h)
            for k in range(1, 2**i, 2)
        )

        R[i, 0] = 0.5 * R[i - 1, 0] + h * suma

        for j in range(1, i + 1):
            R[i, j] = (
                R[i, j - 1]
                + (R[i, j - 1] - R[i - 1, j - 1])
                / (4**j - 1.0)
            )

    return R[k_max - 1, k_max - 1], R


def main():
    referencia = trabajo_exacto()

    # --------------------------------------------------
    # 1. Resultados finales de ambos métodos
    # --------------------------------------------------
    trabajo_gauss, nodos_gauss, valores_gauss, n_gauss = (
        cuadratura_gauss(A, B, n=4)
    )

    trabajo_romberg, tabla = romberg(A, B, k_max=4)

    error_gauss = abs(trabajo_gauss - referencia)
    error_romberg = abs(trabajo_romberg - referencia)

    print("=" * 58)
    print(" COMPARACIÓN: GAUSS-LEGENDRE Y ROMBERG")
    print("=" * 58)

    print(f"\nTrabajo exacto: {referencia:.12f} J")

    print("\nGAUSS-LEGENDRE")
    print(f"Trabajo aproximado: {trabajo_gauss:.12f} J")
    print(f"Error absoluto:     {error_gauss:.6e} J")
    print(f"Nodos utilizados:   {n_gauss}")

    print("\nROMBERG")
    print(f"Trabajo aproximado: {trabajo_romberg:.12f} J")
    print(f"Error absoluto:     {error_romberg:.6e} J")
    print(f"Niveles utilizados: {len(tabla)}")

    # Romberg reutiliza evaluaciones previas.
    # Con 4 niveles necesita 2**3 + 1 = 9 puntos distintos.
    evaluaciones_romberg = 2**(len(tabla) - 1) + 1

    print("\nEVALUACIONES DE LA FUERZA")
    print(f"Gauss-Legendre: {n_gauss}")
    print(f"Romberg:        {evaluaciones_romberg}")

    if error_gauss < error_romberg:
        print("\nMayor precisión en este cálculo: Gauss-Legendre")
    elif error_romberg < error_gauss:
        print("\nMayor precisión en este cálculo: Romberg")
    else:
        print("\nAmbos métodos presentan el mismo error.")

    # --------------------------------------------------
    # 2. Gráfica: nodos y partición de ambos métodos
    # --------------------------------------------------
    x = np.linspace(A, B, 500)
    y = fuerza(x)

    nodos_romberg = np.linspace(A, B, evaluaciones_romberg)
    valores_romberg = fuerza(nodos_romberg)

    fig, ax = plt.subplots(figsize=(11, 6))

    ax.plot(
        x, y,
        color="black",
        linewidth=2.2,
        label="F(x) = F₀ exp(-αx)"
    )

    # Nodos de Gauss
    ax.scatter(
        nodos_gauss,
        valores_gauss,
        color="blue",
        edgecolors="white",
        linewidths=0.8,
        s=90,
        zorder=4,
        label="Nodos de Gauss-Legendre"
    )

    for nodo in nodos_gauss:
        ax.axvline(
            nodo,
            color="blue",
            linestyle=":",
            alpha=0.45
        )

    # Nodos de la malla final de Romberg
    ax.scatter(
        nodos_romberg,
        valores_romberg,
        color="red",
        marker="x",
        s=65,
        linewidths=2,
        zorder=3,
        label="Nodos de la malla de Romberg"
    )

    for nodo in nodos_romberg:
        ax.axvline(
            nodo,
            color="red",
            linestyle="--",
            alpha=0.18
        )

    ax.set_xlabel("Desplazamiento x (m)")
    ax.set_ylabel("Fuerza F(x) (N)")
    ax.set_title("Comparación de los puntos de evaluación")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    # --------------------------------------------------
    # 3. Gráfica: convergencia de ambos métodos
    # --------------------------------------------------
    # Gauss: aumentar el número de nodos
    nodos_gauss_lista = list(range(2, 9))
    resultados_gauss = []
    errores_gauss = []

    for n in nodos_gauss_lista:
        resultado, _, _, _ = cuadratura_gauss(A, B, n)
        resultados_gauss.append(resultado)
        errores_gauss.append(abs(resultado - referencia))

    # Romberg: diagonal de cada tabla sucesiva
    niveles_romberg = list(range(1, 9))
    resultados_romberg = []
    errores_romberg = []

    for k in niveles_romberg:
        resultado, _ = romberg(A, B, k_max=k)
        resultados_romberg.append(resultado)
        errores_romberg.append(abs(resultado - referencia))

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        nodos_gauss_lista,
        errores_gauss,
        marker="o",
        linewidth=2,
        color="blue",
        label="Gauss-Legendre"
    )

    ax.plot(
        niveles_romberg,
        errores_romberg,
        marker="s",
        linewidth=2,
        color="red",
        label="Romberg"
    )

    ax.set_yscale("log")
    ax.set_xlabel("Número de nodos (Gauss) / niveles (Romberg)")
    ax.set_ylabel("Error absoluto (J, escala logarítmica)")
    ax.set_title("Convergencia y error de los métodos")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend()
    fig.tight_layout()

    # --------------------------------------------------
    # 4. Gráfica: comparación de resultados finales
    # --------------------------------------------------
    nombres = ["Valor exacto", "Gauss-Legendre", "Romberg"]
    resultados = [
        referencia,
        trabajo_gauss,
        trabajo_romberg
    ]

    fig, ax = plt.subplots(figsize=(9, 5.5))

    barras = ax.bar(
        nombres,
        resultados,
        color=["gray", "blue", "green"],
        edgecolor="black"
    )

    ax.bar_label(barras, fmt="%.8f", padding=4)
    ax.set_ylabel("Trabajo (J)")
    ax.set_title("Comparación de los valores calculados")
    ax.grid(axis="y", alpha=0.25)
    ax.set_ylim(0, max(resultados) * 1.12)
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()