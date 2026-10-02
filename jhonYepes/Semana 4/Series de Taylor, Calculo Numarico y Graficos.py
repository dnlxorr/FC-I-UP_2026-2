# ==========================================
# 3 y 4. Series de Taylor y Análisis Gráfico
# ==========================================
import math
import numpy as np
import matplotlib.pyplot as plt


def taylor_seno(x, terminos):
    """Calcula sen(x) usando serie de Taylor con n términos."""
    aproximacion = 0
    for n in range(terminos):
        aproximacion += ((-1) ** n * x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return aproximacion


def taylor_exponencial(x, terminos):
    """Calcula e^x usando serie de Taylor con n términos."""
    aproximacion = 0
    for n in range(terminos):
        aproximacion += (x ** n) / math.factorial(n)
    return aproximacion


def analizar_y_graficar():
    # Rango de valores para evaluar (de -2pi a 2pi)
    x_vals = np.linspace(-2 * np.pi, 2 * np.pi, 100)

    # 1. Cálculo Numérico (Ejemplo en un punto específico x = 3.5)
    pto_eval = 3.5
    terminos = 5

    seno_real = math.sin(pto_eval)
    seno_taylor = taylor_seno(pto_eval, terminos)
    error_seno = abs(seno_real - seno_taylor)

    print("--- ANÁLISIS NUMÉRICO (x = 3.5, 5 términos) ---")
    print(f"Seno exacto (math): {seno_real:.6f}")
    print(f"Seno Taylor:        {seno_taylor:.6f}")
    print(f"Error Truncamiento: {error_seno:.6f}\n")

    # 2. Generación de Gráficas
    plt.figure(figsize=(12, 5))

    # Subplot 1: Seno
    plt.subplot(1, 2, 1)
    plt.plot(x_vals, np.sin(x_vals), label='math.sin(x) (Exacto)', color='black', linewidth=2)
    plt.plot(x_vals, [taylor_seno(x, 2) for x in x_vals], label='Taylor (2 terms)', linestyle='--')
    plt.plot(x_vals, [taylor_seno(x, 5) for x in x_vals], label='Taylor (5 terms)', linestyle='--')
    plt.title("Aproximación de sin(x) por Taylor")
    plt.ylim(-2, 2)
    plt.legend()
    plt.grid(True)

    # Subplot 2: Exponencial
    plt.subplot(1, 2, 2)
    plt.plot(x_vals, np.exp(x_vals), label='math.exp(x) (Exacto)', color='black', linewidth=2)
    plt.plot(x_vals, [taylor_exponencial(x, 3) for x in x_vals], label='Taylor (3 terms)', linestyle='--')
    plt.plot(x_vals, [taylor_exponencial(x, 6) for x in x_vals], label='Taylor (6 terms)', linestyle='--')
    plt.title("Aproximación de e^x por Taylor")
    plt.ylim(0, 100)
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analizar_y_graficar()