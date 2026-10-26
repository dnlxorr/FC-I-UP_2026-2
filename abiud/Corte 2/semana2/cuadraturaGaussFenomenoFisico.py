
"""
Cuadratura de Gauss-Legendre aplicada al trabajo de una fuerza variable.
Se muestran los nodos, sus pesos y la aproximación de la integral.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros físicos del modelo
F0 = 10.0
ALPHA = 0.5
A = 0.0
B = 4.0


def fuerza(x):
    """Fuerza variable, en newtons."""
    return F0 * np.exp(-ALPHA * np.asarray(x))


def trabajo_exacto(a=A, b=B):
    """Solución analítica usada como referencia."""
    return (F0 / ALPHA) * (
        np.exp(-ALPHA * a) - np.exp(-ALPHA * b)
    )


def cuadratura_gauss(a, b, n):
    """Aproxima la integral mediante Gauss-Legendre."""

    nodos, pesos = np.polynomial.legendre.leggauss(n)

    # Transformación del intervalo [-1, 1] a [a, b]
    x = 0.5 * (b - a) * nodos + 0.5 * (b + a)
    pesos_transformados = 0.5 * (b - a) * pesos

    fuerzas_nodos = fuerza(x)
    contribuciones = pesos_transformados * fuerzas_nodos

    aproximacion = np.sum(contribuciones)

    return (
        float(aproximacion),
        x,
        pesos_transformados,
        fuerzas_nodos,
        contribuciones
    )


def main():
    n = 4

    trabajo, nodos, pesos, fuerzas_nodos, contribuciones = (
        cuadratura_gauss(A, B, n)
    )

    referencia = trabajo_exacto()
    error_abs = abs(trabajo - referencia)
    error_rel = error_abs / abs(referencia) * 100

    print("TRABAJO — CUADRATURA DE GAUSS-LEGENDRE")
    print(f"Trabajo aproximado: {trabajo:.12f} J")
    print(f"Trabajo exacto:     {referencia:.12f} J")
    print(f"Error absoluto:     {error_abs:.6e} J")
    print(f"Error relativo:     {error_rel:.6e} %")

    print("\nNODOS Y PESOS DE GAUSS-LEGENDRE")
    print("Nodo x (m) | Fuerza (N) | Peso transformado | Contribución (J)")

    for x_i, f_i, w_i, c_i in zip(
        nodos, fuerzas_nodos, pesos, contribuciones
    ):
        print(
            f"{x_i:10.6f} | {f_i:10.6f} | "
            f"{w_i:17.6f} | {c_i:16.6f}"
        )

    # --------------------------------------------------
    # GRÁFICA 1: Fuerza, nodos y pesos de Gauss
    # --------------------------------------------------
    x = np.linspace(A, B, 500)
    y = fuerza(x)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        x, y,
        color="blue",
        linewidth=2.5,
        label="F(x) = F₀ exp(-αx)"
    )

    ax.fill_between(
        x, y, 0,
        color="blue",
        alpha=0.12,
        label=f"Trabajo calculado = {trabajo:.6f} J"
    )

    # Líneas verticales: posiciones de los nodos de Gauss
    for i, nodo in enumerate(nodos):
        ax.axvline(
            nodo,
            color="red",
            linestyle="--",
            linewidth=1.2,
            alpha=0.7
        )

    # Marcadores: valores de la fuerza en cada nodo
    ax.scatter(
        nodos,
        fuerzas_nodos,
        color="red",
        edgecolors="black",
        s=75,
        zorder=4,
        label=f"{n} nodos de Gauss"
    )

    # Etiquetas de los nodos
    for i, (nodo, valor) in enumerate(zip(nodos, fuerzas_nodos)):
        ax.annotate(
            f"x{i + 1} = {nodo:.3f} m",
            (nodo, valor),
            xytext=(5, 12),
            textcoords="offset points",
            fontsize=8,
            rotation=15
        )

    ax.set_xlabel("Desplazamiento x (m)")
    ax.set_ylabel("Fuerza F(x) (N)")
    ax.set_title("Gauss-Legendre: nodos de cuadratura")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    # --------------------------------------------------
    # GRÁFICA 2: Contribución de cada nodo
    # --------------------------------------------------
    fig, ax = plt.subplots(figsize=(9, 5.5))

    barras = ax.bar(
        np.arange(1, n + 1),
        contribuciones,
        width=0.65,
        color="cornflowerblue",
        edgecolor="black"
    )

    ax.set_xticks(np.arange(1, n + 1))
    ax.set_xlabel("Nodo de Gauss")
    ax.set_ylabel("Contribución al trabajo (J)")
    ax.set_title("Contribución ponderada de cada nodo")
    ax.grid(axis="y", alpha=0.3)

    ax.bar_label(barras, fmt="%.4f", padding=3)

    ax.text(
        0.98, 0.95,
        f"Trabajo total = {trabajo:.8f} J",
        transform=ax.transAxes,
        ha="right",
        va="top",
        bbox=dict(facecolor="white", alpha=0.85)
    )

    fig.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
