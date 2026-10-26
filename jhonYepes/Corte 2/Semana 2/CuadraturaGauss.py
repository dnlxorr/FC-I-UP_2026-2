# ====================================================================
# JhonAlexanderYepesArias: Altura de Cohete usando Cuadratura de Gauss
# ====================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- PARÁMETROS FÍSICOS DEL COHETE ---
u = 2000.0
m0 = 150000.0
q = 2500.0
g = 9.81
t_final = 40.0


def velocidad(t):
    """Función de velocidad v(t) del cohete."""
    return u * np.log(m0 / (m0 - q * t)) - g * t


def cuadratura_gauss(f, a, b, n_puntos):
    """Calcula la integral usando Gauss-Legendre con n puntos."""
    # Obtener raíces (x) y pesos (w) estándar en [-1, 1]
    x, w = np.polynomial.legendre.leggauss(n_puntos)

    # Mapeo del intervalo [-1, 1] al intervalo [a, b]
    t = 0.5 * (b - a) * x + 0.5 * (b + a)
    pesos = 0.5 * (b - a) * w

    integral = np.sum(pesos * f(t))
    return integral


def ejecutar_analisis_gauss():
    print("\n[INFO] Ejecutando análisis de Cuadratura de Gauss-Legendre...")
    a, b = 0.0, t_final
    puntos_evaluacion = np.array([2, 3, 4, 5, 6, 7, 8])

    # Referencia exacta
    I_exacta, _ = quad(velocidad, a, b)

    print("\n" + "=" * 65)
    print(" TABLA DE CONVERGENCIA DE GAUSS-LEGENDRE")
    print("=" * 65)
    print(f"{'N° Puntos':<10} | {'Altura Calculada (m)':<25} | {'Error Absoluto (m)':<20}")
    print("-" * 65)

    errores = []

    for n in puntos_evaluacion:
        I_gauss = cuadratura_gauss(velocidad, a, b, n)
        error = abs(I_gauss - I_exacta)
        errores.append(error + 1e-16)  # Evitar log(0)
        print(f"{n:<10} | {I_gauss:<25.8f} | {error:.2e}")

    print("-" * 65)
    print(f"[REFERENCIA] Altura exacta (SciPy): {I_exacta:.8f} m\n")

    # Gráfica
    plt.figure(figsize=(8, 5))
    plt.semilogy(puntos_evaluacion, errores, marker='s', color='#9b59b6', linewidth=2, label='Error Gauss-Legendre')
    plt.title('Convergencia del Error - Cuadratura de Gauss', fontweight='bold')
    plt.xlabel('Número de Puntos Evaluados (N)')
    plt.ylabel('Error Absoluto (m) [Log]')
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ejecutar_analisis_gauss()