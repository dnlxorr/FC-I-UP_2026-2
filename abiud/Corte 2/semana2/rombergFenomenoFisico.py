
"""
Método de Romberg aplicado al trabajo de una fuerza variable.
Se muestran los intervalos de integración y la convergencia.
"""

import numpy as np
import matplotlib.pyplot as plt

# Parámetros físicos del modelo
F0 = 10.0
ALPHA = 0.5
A = 0.0
B = 4.0


def fuerza(x):
    """Fuerza variable en newtons."""
    return F0 * np.exp(-ALPHA * np.asarray(x))


def trabajo_exacto(a=A, b=B):
    """Solución analítica de referencia."""
    return (F0 / ALPHA) * (
        np.exp(-ALPHA * a) - np.exp(-ALPHA * b)
    )


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
    k_max = 4

    trabajo, tabla = romberg(A, B, k_max)
    referencia = trabajo_exacto()
    error_abs = abs(trabajo - referencia)
    error_rel = error_abs / abs(referencia) * 100

    print("TRABAJO — MÉTODO DE ROMBERG")
    print(f"Trabajo aproximado: {trabajo:.12f} J")
    print(f"Trabajo exacto:     {referencia:.12f} J")
    print(f"Error absoluto:     {error_abs:.6e} J")
    print(f"Error relativo:     {error_rel:.6e} %")

    print("\nTABLA DE ROMBERG")
    print("Cada fila corresponde a un nivel de refinamiento.")
    print(tabla)

    # --------------------------------------------------
    # GRÁFICA 1: Fuerza e intervalos de Romberg
    # --------------------------------------------------
    x = np.linspace(A, B, 500)
    y = fuerza(x)

    nivel = k_max - 1
    numero_intervalos = 2**nivel
    nodos = np.linspace(A, B, numero_intervalos + 1)
    fuerzas_nodos = fuerza(nodos)

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        x, y,
        color="green",
        linewidth=2.5,
        label="F(x) = F₀ exp(-αx)"
    )

    ax.fill_between(
        x, y, 0,
        color="green",
        alpha=0.12,
        label=f"Trabajo calculado = {trabajo:.6f} J"
    )

    # Líneas verticales que muestran la partición final
    for i, nodo in enumerate(nodos):
        ax.axvline(
            x=nodo,
            color="red",
            linestyle="--",
            linewidth=0.9,
            alpha=0.55
        )

    # Puntos donde se evalúa la fuerza en la malla final
    ax.scatter(
        nodos,
        fuerzas_nodos,
        color="red",
        edgecolors="black",
        s=45,
        zorder=3,
        label=f"Nodos del nivel {k_max} ({len(nodos)} puntos)"
    )

    ax.set_xlabel("Desplazamiento x (m)")
    ax.set_ylabel("Fuerza F(x) (N)")
    ax.set_title(
        "Romberg: fuerza e intervalos de integración"
    )
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()

    # --------------------------------------------------
    # GRÁFICA 2: Convergencia de Romberg
    # --------------------------------------------------
    niveles = np.arange(1, k_max + 1)
    aproximaciones = np.array([
        tabla[i, i] for i in range(k_max)
    ])

    errores = np.abs(aproximaciones - referencia)

    fig, ax = plt.subplots(figsize=(9, 5.5))

    ax.plot(
        niveles,
        aproximaciones,
        marker="o",
        markersize=7,
        linewidth=2,
        color="blue",
        label="Aproximación diagonal de Romberg"
    )

    ax.axhline(
        referencia,
        color="black",
        linestyle="--",
        linewidth=1.5,
        label=f"Valor exacto = {referencia:.8f} J"
    )

    for n, valor in zip(niveles, aproximaciones):
        ax.annotate(
            f"{valor:.6f}",
            (n, valor),
            xytext=(0, 9),
            textcoords="offset points",
            ha="center",
            fontsize=8
        )

    ax.set_xticks(niveles)
    ax.set_xlabel("Nivel de refinamiento")
    ax.set_ylabel("Trabajo aproximado (J)")
    ax.set_title("Convergencia del método de Romberg")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()
