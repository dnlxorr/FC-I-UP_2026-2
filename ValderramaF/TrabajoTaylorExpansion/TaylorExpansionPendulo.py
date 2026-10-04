"""
Física Computacional I - Laboratorio #2
Series de Taylor y Péndulo No Lineal
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import ellipk

EPS = np.finfo(float).eps  # épsilon de máquina (~2.2e-16)


# ==========================================
# PARTE A: Algoritmo de Taylor
# ==========================================
def sin_taylor(x, N):
    """
    Aproxima sen(x) con los primeros N términos de la serie de Maclaurin.

    Usa la recurrencia  T_n = -T_{n-1} * x^2 / (2n (2n+1)),  con T_0 = x,
    por lo que no calcula factoriales ni potencias (sin overflow, costo O(N)).

    Parámetros
    ----------
    x : float o array_like   Ángulo en radianes (admite arreglos).
    N : int                  Número de términos (N = 1 devuelve solo x).
    """
    x = np.asarray(x, dtype=float)
    if N <= 0:
        return np.zeros_like(x)[()]

    termino = x.copy()  # T_0 (copia: no se modifica la entrada)
    suma = x.copy()
    x2 = x * x          # se calcula una sola vez

    for n in range(1, N):
        termino = -termino * x2 / (2 * n * (2 * n + 1))
        suma = suma + termino

    return suma[()]  # escalar si x era escalar


def sin_taylor_reducido(x, N=10):
    """
    Extra: sen(x) para |x| grande usando simetrías del seno.
    Periodicidad + imparidad + reflexión llevan x a [0, π/2].
    """
    x = np.asarray(x, dtype=float)
    y = np.mod(x, 2 * np.pi)
    signo = np.where(y > np.pi, -1.0, 1.0)
    y = np.where(y > np.pi, y - np.pi, y)
    y = np.where(y > np.pi / 2, np.pi - y, y)
    return (signo * sin_taylor(y, N))[()]


# ==========================================
# PARTE B: Análisis de Error Numérico
# ==========================================
def error_absoluto(x, N):
    """E(N) = |sin_taylor(x, N) - sin_numpy(x)|"""
    return abs(sin_taylor(x, N) - np.sin(x))


def analisis_error_taylor(N_max=20, tol=1e-10, guardar=None):
    puntos = {"π/4": np.pi / 4, "π": np.pi, "3π": 3 * np.pi}
    rango_N = np.arange(1, N_max + 1)

    plt.figure(figsize=(10, 6))
    print(f"\nPrimer N con E(N) < {tol:g}:")
    for etiqueta, x in puntos.items():
        E = np.array([error_absoluto(x, N) for N in rango_N])

        ok = np.where(E < tol)[0]
        n_min = rango_N[ok[0]] if ok.size else f"> {N_max}"
        print(f"  x = {etiqueta:>3}: N = {n_min}")

        # Piso de 1e-17 solo para poder dibujar errores exactamente nulos en escala log
        plt.semilogy(rango_N, np.maximum(E, 1e-17), "o-", ms=5, label=f"x = {etiqueta}")

    plt.axhline(EPS, color="gray", ls=":", lw=1.2, label="épsilon de máquina")
    plt.title("Error absoluto de la serie de Taylor para sen(x)")
    plt.xlabel("Número de términos N")
    plt.ylabel("Error absoluto E(N)  (escala logarítmica)")
    plt.xticks(rango_N)
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    if guardar:
        plt.savefig(guardar, dpi=150)


def barrido_redondeo(x, N_max=80):
    """Pregunta 2: E(N) para N grande. Muestra el piso impuesto por el redondeo."""
    rango_N = np.arange(1, N_max + 1)
    return rango_N, np.array([error_absoluto(x, N) for N in rango_N])


def analisis_redondeo(N_max=80, guardar=None):
    puntos = {"π": np.pi, "3π": 3 * np.pi, "10π": 10 * np.pi}
    plt.figure(figsize=(10, 6))
    print(f"\nError de Taylor directo para N grande (N = {N_max}):")
    for etiqueta, x in puntos.items():
        N, E = barrido_redondeo(x, N_max)
        print(f"  x = {etiqueta:>3}: mínimo {E.min():.2e} (N = {N[np.argmin(E)]}), "
              f"E({N_max}) = {E[-1]:.2e}")
        plt.semilogy(N, np.maximum(E, 1e-17), "o-", ms=3, label=f"x = {etiqueta}")
    plt.axhline(EPS, color="gray", ls=":", lw=1.2, label="épsilon de máquina")
    plt.title("Error para N grande: el redondeo fija un piso")
    plt.xlabel("Número de términos N")
    plt.ylabel("Error absoluto E(N)")
    plt.grid(True, which="both", ls="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    if guardar:
        plt.savefig(guardar, dpi=150)


def demo_reduccion_rango():
    """Pregunta final de la tabla: x grande con y sin reducción de rango."""
    print("\nx grande: Taylor directo (N=20) vs. con reducción de rango (N=10)")
    print(f"{'x':>10} {'directo':>14} {'reducido':>20} {'numpy':>20}")
    for x in (3 * np.pi, 10 * np.pi + 0.5, 50.0, 1000.0):
        print(f"{x:10.3f} {sin_taylor(x, 20):14.3e} "
              f"{sin_taylor_reducido(x, 10):20.15f} {np.sin(x):20.15f}")


# ==========================================
# PARTE C: Modelación del Péndulo No Lineal
# ==========================================
def razon_periodo(theta0):
    """T(θ0)/T0 con la corrección de Taylor de segundo orden (θ0 en radianes)."""
    th = np.asarray(theta0, dtype=float)
    return 1 + th**2 / 16 + 11 * th**4 / 3072


def razon_periodo_exacta(theta0):
    """T(θ0)/T0 exacta: (2/π) K(k), k = sin(θ0/2). Referencia para medir errores."""
    th = np.asarray(theta0, dtype=float)
    return 2 / np.pi * ellipk(np.sin(th / 2) ** 2)  # ellipk usa m = k²


def analisis_pendulo(guardar=None):
    grados = np.arange(1, 91)
    theta0 = np.radians(grados)

    exacta = razon_periodo_exacta(theta0)
    taylor = razon_periodo(theta0)

    # Error porcentual respecto al período exacto
    err_T0 = 100 * np.abs(exacta - 1) / exacta          # armónico simple
    err_taylor = 100 * np.abs(exacta - taylor) / exacta  # corregida por Taylor

    # Amplitud máxima con error < 1 % usando T0 (malla fina)
    fino = np.linspace(0.01, 90, 90000)
    tf = np.radians(fino)
    ef = 100 * np.abs(razon_periodo_exacta(tf) - 1) / razon_periodo_exacta(tf)
    lim_1pct = fino[np.argmax(ef > 1)]
    print(f"\nCon T0 el error supera 1 % desde θ0 ≈ {lim_1pct:.2f}°")
    print(f"Error a 90°: T0 = {err_T0[-1]:.2f} %  |  Taylor = {err_taylor[-1]:.3f} %")

    fig, axs = plt.subplots(1, 2, figsize=(13, 5))

    axs[0].plot(grados, exacta, "k-", lw=2, label="Exacta (integral elíptica)")
    axs[0].plot(grados, taylor, "r--", lw=2, label="Taylor 2.º orden")
    axs[0].axhline(1, color="b", ls=":", label="Armónico simple (T/T0 = 1)")
    axs[0].set(xlabel="Amplitud inicial θ0 (grados)", ylabel="T(θ0) / T0",
               title="Razón de períodos", xlim=(0, 90))
    axs[0].grid(True, alpha=0.4)
    axs[0].legend()

    axs[1].semilogy(grados, err_T0, "b-", lw=2, label="Aprox. armónica simple (T0)")
    axs[1].semilogy(grados, err_taylor, "r-", lw=2, label="Corregida por Taylor")
    axs[1].axhline(1, color="gray", ls="--", label="Límite 1 %")
    axs[1].axvline(lim_1pct, color="b", ls=":", lw=1)
    axs[1].annotate(f"{lim_1pct:.1f}°", (lim_1pct, 1), xytext=(lim_1pct + 2, 2),
                    color="b")
    axs[1].set(xlabel="Amplitud inicial θ0 (grados)", ylabel="Error porcentual (%)",
               title="Error en el período vs. amplitud", xlim=(0, 90))
    axs[1].grid(True, which="both", alpha=0.4)
    axs[1].legend()

    plt.tight_layout()
    if guardar:
        plt.savefig(guardar, dpi=150)


# ==========================================
# Programa principal
# ==========================================
if __name__ == "__main__":
    # Verificación rápida de la Parte A
    for x in (np.pi / 4, 1.0, np.pi / 2):
        print(f"x = {x:.4f}  Taylor(N=10) = {sin_taylor(x, 10):.15f}  "
              f"numpy = {np.sin(x):.15f}")

    print("\nParte B: convergencia de Taylor")
    analisis_error_taylor(guardar="grafica_error_vs_N.png")

    print("\nPregunta 2: error de redondeo para N grande")
    analisis_redondeo(guardar="grafica_redondeo.png")
    demo_reduccion_rango()

    print("\nParte C: péndulo no lineal")
    analisis_pendulo(guardar="grafica_pendulo.png")

    plt.show()