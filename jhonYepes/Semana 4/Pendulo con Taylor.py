import numpy as np
import matplotlib.pyplot as plt


# ==========================================
# PARTE A: Algoritmo de Taylor
# ==========================================
def sin_taylor(x, N):
    """
    Calcula sen(x) usando N términos de la Serie de Taylor.
    Utiliza la relación de recurrencia para evitar factoriales y desbordamiento de memoria.
    """
    if N <= 0:
        return 0.0

    termino = x  # Primer término (n=0)
    suma = termino

    for n in range(1, N):
        # Relación de recurrencia: Tn = -T(n-1) * [x^2 / (2n * (2n+1))]
        termino = -termino * (x ** 2) / ((2 * n) * (2 * n + 1))
        suma += termino

    return suma


# ==========================================
# PARTE B: Análisis de Error Numérico
# ==========================================
def analisis_error_taylor():
    valores_x = [np.pi / 4, np.pi, 3 * np.pi]
    etiquetas = ['π/4', 'π', '3π']
    rango_N = range(1, 21)  # N de 1 a 20

    plt.figure(figsize=(10, 6))

    for x, label in zip(valores_x, etiquetas):
        errores = []
        valor_exacto = np.sin(x)  # Valor de referencia con Numpy

        for N in rango_N:
            valor_aprox = sin_taylor(x, N)
            error_abs = abs(valor_aprox - valor_exacto)
            # Se usa un límite mínimo de 1e-16 para evitar errores matemáticos al graficar log(0)
            errores.append(error_abs if error_abs > 0 else 1e-16)

        plt.semilogy(rango_N, errores, marker='o', label=f'x = {label}')

    plt.title('Error absoluto de la Serie de Taylor para sen(x)')
    plt.xlabel('Número de términos (N)')
    plt.ylabel('Error Absoluto (Escala Logarítmica)')
    plt.xticks(rango_N)
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ==========================================
# PARTE C: Modelación del Péndulo No Lineal
# ==========================================
def analisis_pendulo():
    # Ángulos de amplitud inicial de 1° a 90°
    grados = np.arange(1, 91)
    radianes = np.radians(grados)

    # Cálculo de la razón T(θ0)/T0 con la expansión de Taylor de orden superior
    razon_T = 1 + (1 / 16) * (radianes ** 2) + (11 / 3072) * (radianes ** 4)

    # Error porcentual al usar la aproximación armónica simple (T0)
    # Error = ((T_real - T_simple) / T_simple) * 100
    error_porcentual = (razon_T - 1) * 100

    plt.figure(figsize=(10, 6))
    plt.plot(grados, error_porcentual, color='red', linewidth=2, label='Error por aproximación lineal')

    # Línea de referencia teórica para el 1% de error
    plt.axhline(y=1, color='blue', linestyle='--', label='Límite de error del 1%')

    plt.title('Error de la aproximación de pequeñas oscilaciones vs Amplitud')
    plt.xlabel('Amplitud inicial θ0 (grados)')
    plt.ylabel('Error Porcentual (%)')
    plt.xlim(0, 90)
    plt.grid(True, alpha=0.6)
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    print("Ejecutando Parte B: Generando gráfica de convergencia de Taylor...")
    analisis_error_taylor()

    print("Ejecutando Parte C: Generando gráfica de error del péndulo...")
    analisis_pendulo()