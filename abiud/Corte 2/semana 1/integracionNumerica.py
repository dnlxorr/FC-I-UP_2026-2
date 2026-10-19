import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# PARÁMETROS FÍSICOS
L = 1.0  # Longitud del péndulo (en metros)
g = 9.81  # Aceleración de la gravedad (m/s^2)
theta_0 = np.radians(60)  # Amplitud inicial convertida de grados a radianes
k = np.sin(theta_0 / 2.0)  # Parámetro k para la integral elíptica completa

def integrando(phi):
    """ Función f(phi) que representa el integrando de la integral elíptica completa de primera especie para el péndulo físico."""
    return 1.0 / np.sqrt(1.0 - (k ** 2) * (np.sin(phi) ** 2))

def trapecio_compuesto(f, a, b, n):
    """ Algoritmo de la Regla del Trapecio Compuesto para calcular el valor numérico de la integral utilizando 'n' subintervalos. """
    h = (b - a) / n  # Tamaño del paso (ancho de cada subintervalo)
    x = np.linspace(a, b, n + 1)  # Arreglo con los puntos de la partición
    y = f(x)  # Evaluación de la función en cada punto
    # Aplicación de la fórmula del Trapecio Compuesto con vectorización NumPy
    return (h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1])

def simpson_13_compuesto(f, a, b, n):
    """ Algoritmo de Simpson 1/3 Compuesto (requiere obligatoriamente que n sea PAR) para calcular la integral usando aproximación por parábolas. """
    if n % 2 != 0:
        raise ValueError("El número de subintervalos n debe ser PAR.")
    h = (b - a) / n  # Tamaño del paso h
    x = np.linspace(a, b, n + 1)  # Puntos de la malla
    y = f(x)  # Evaluación de la función

    # Separación de índices impares y pares según la fórmula de Simpson 1/3
    suma_impares = np.sum(y[1:-1:2])  # Coeficiente 4 para índices impares
    suma_pares = np.sum(y[2:-1:2])  # Coeficiente 2 para índices pares

    # Aplicación de la fórmula completa de Simpson 1/3
    return (h / 3.0) * (y[0] + 4.0 * suma_impares + 2.0 * suma_pares + y[-1])

# CÁLCULOS PARA LA SECCIÓN 6 DE LA GUÍA (Evaluación con n = 100)
n_test = 100
integral_trap = trapecio_compuesto(integrando, 0, np.pi / 2, n_test)  # Integral por Trapecio
integral_simp = simpson_13_compuesto(integrando, 0, np.pi / 2, n_test)  # Integral por Simpson 1/3

# Cálculo del Período Real T(60°) usando el resultado de la integral elíptica
periodo_real = 4.0 * np.sqrt(L / g) * integral_simp

# Cálculo del Período Lineal Aproximado T0 (pequeñas oscilaciones)
T_0 = 2.0 * np.pi * np.sqrt(L / g)

# Cálculo del porcentaje de error relativo / subestimación del modelo lineal
error_porcentual = abs(T_0 - periodo_real) / periodo_real * 100.0

# MOSTRAR LOS RESULTADOS EN FORMA DE TABLA EN LA TERMINAL
print("-" * 95)
print(f"{'Concepto':<35} | {'Valor Calculado':<18} | {'Unidades / Observación'}")
print("-" * 95)
print(f"{'Integral / (Trapecio, n=100)':<35} | {integral_trap:<18.8f} | Adimensional")
print(f"{'Integral / (Simpson 1/3, n=100)':<35} | {integral_simp:<18.8f} | Adimensional")
print(f"{'Período Real T(60°)':<35} | {periodo_real:<18.5f} | Segundos (s)")
print(f"{'Error Relativo vs T_0':<35} | {error_porcentual:<17.2f}% | % de subestimación del modelo lineal")
print("-" * 95)

# ANÁLISIS DE CONVERGENCIA (Para generar la Gráfica Log-Log)
n_valores = np.array([2, 4, 8, 16, 32, 64, 128, 256])  # Valores de n a evaluar
err_trap = []  # Lista para almacenar los errores absolutos del Trapecio
err_simp = []  # Lista para almacenar los errores absolutos de Simpson
eps = 1e-16  # Tolerancia mínima para evitar log(0) en escala logarítmica
I_exacto, _ = quad(integrando, 0, np.pi / 2)  # Valor de referencia de alta precisión con SciPy

for n in n_valores:
    I_t = trapecio_compuesto(integrando, 0, np.pi / 2, n)
    I_s = simpson_13_compuesto(integrando, 0, np.pi / 2, n)
    err_trap.append(max(abs(I_t - I_exacto), eps))
    err_simp.append(max(abs(I_s - I_exacto), eps))

# GENERACIÓN DE LA GRÁFICA LOG-LOG
plt.figure(figsize=(8, 5))
plt.loglog(n_valores, err_trap, 'o-', label=r'Trapecio Compuesto $\mathcal{O}(h^2)$')
plt.loglog(n_valores, err_simp, 's-', label=r'Simpson 1/3 Compuesto $\mathcal{O}(h^4)$')
plt.xlabel('Número de subintervalos (n)')
plt.ylabel('Error Absoluto')
plt.title('Convergencia de Métodos de Integración Numérica')
plt.grid(True, which="both", ls="--")
plt.legend()
plt.tight_layout()
plt.show()