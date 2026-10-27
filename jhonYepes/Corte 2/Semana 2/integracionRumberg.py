# ====================================================================
# JhonAlexanderYepesArias: Altura de Cohete usando Integración de Romberg
# ====================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- PARÁMETROS FÍSICOS DEL COHETE ---
u = 2000.0  # Velocidad de escape de gases (m/s)
m0 = 150000.0  # Masa inicial del cohete (kg)
q = 2500.0  # Tasa de consumo de combustible (kg/s)
g = 9.81  # Aceleración de la gravedad (m/s^2)
t_final = 40.0  # Tiempo de evaluación (s)


def velocidad(t):
    """Función de velocidad v(t) basada en la ecuación de Tsiolkovski."""
    return u * np.log(m0 / (m0 - q * t)) - g * t


def trapecio_recursivo(f, a, b, n, I_prev):
    """Calcula el nivel n de la regla del trapecio aprovechando el cálculo anterior."""
    if n == 0:
        return 0.5 * (b - a) * (f(a) + f(b))
    N = 2 ** (n - 1)
    h = (b - a) / N
    # Evaluamos solo en los puntos impares nuevos
    x = a + h / 2.0 + np.arange(N) * h
    return 0.5 * I_prev + (h / 2.0) * np.sum(f(x))


def tabla_romberg(f, a, b, niveles):
    """Construye la matriz de Romberg y retorna la matriz y el error relativo."""
    R = np.zeros((niveles, niveles))
    R[0, 0] = trapecio_recursivo(f, a, b, 0, 0)

    for i in range(1, niveles):
        R[i, 0] = trapecio_recursivo(f, a, b, i, R[i - 1, 0])
        for j in range(1, i + 1):
            R[i, j] = R[i, j - 1] + (R[i, j - 1] - R[i - 1, j - 1]) / ((4 ** j) - 1)

    return R


def leer_entero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: Ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Error: Entrada inválida. Use solo números enteros.")


def ejecutar_analisis_romberg():
    print("\n[INFO] Ejecutando análisis de Romberg...")
    a, b = 0.0, t_final
    niveles = 7

    # Referencia exacta
    I_exacta, _ = quad(velocidad, a, b)

    # Construcción de la matriz
    R = tabla_romberg(velocidad, a, b, niveles)

    print("\n" + "=" * 65)
    print(" TABLA DE CONVERGENCIA DE ROMBERG (Valores de la diagonal principal)")
    print("=" * 65)
    print(f"{'Nivel (i)':<10} | {'Altura Calculada (m)':<25} | {'Error Absoluto (m)':<20}")
    print("-" * 65)

    errores = []
    niveles_plot = np.arange(niveles)

    for i in range(niveles):
        mejor_estimacion = R[i, i]
        error = abs(mejor_estimacion - I_exacta)
        errores.append(error + 1e-16)  # Evitar log(0)
        print(f"{i:<10} | {mejor_estimacion:<25.8f} | {error:.2e}")

    print("-" * 65)
    print(f"[REFERENCIA] Altura exacta (SciPy): {I_exacta:.8f} m\n")

    # Gráfica
    plt.figure(figsize=(8, 5))
    plt.semilogy(niveles_plot, errores, marker='o', color='#2ecc71', linewidth=2, label='Error Romberg')
    plt.title('Convergencia del Error - Método de Romberg', fontweight='bold')
    plt.xlabel('Nivel de Iteración (Matriz Romberg)')
    plt.ylabel('Error Absoluto (m) [Log]')
    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    ejecutar_analisis_romberg()