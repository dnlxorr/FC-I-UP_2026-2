import math
import matplotlib.pyplot as plt

from serieDeTaylorVsMath import taylor_exp, taylor_sin, taylor_cos


# ---------- Gráfico 1: función vs Taylor ----------
def grafico_funcion_vs_taylor():
    x_vals = [i * 0.05 for i in range(-60, 61)]  # -3 a 3
    n_terminos = 6

    y_real = [math.sin(x) for x in x_vals]
    y_taylor = [taylor_sin(x, n_terminos) for x in x_vals]

    plt.figure(figsize=(9, 5))
    plt.plot(x_vals, y_real, label="math.sin(x)", linewidth=2)
    plt.plot(x_vals, y_taylor, "--", label=f"Taylor ({n_terminos} términos)")
    plt.title("Serie de Taylor de sen(x) vs math.sin")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------- Gráfico 2: error vs número de términos ----------
def grafico_error_vs_terminos():
    x = math.pi / 3
    terminos = list(range(1, 21))
    errores_exp = [abs(taylor_exp(x, n) - math.exp(x)) for n in terminos]
    errores_sin = [abs(taylor_sin(x, n) - math.sin(x)) for n in terminos]
    errores_cos = [abs(taylor_cos(x, n) - math.cos(x)) for n in terminos]

    plt.figure(figsize=(9, 5))
    plt.semilogy(terminos, errores_exp, "o-", label="Error e^x")
    plt.semilogy(terminos, errores_sin, "s-", label="Error sin(x)")
    plt.semilogy(terminos, errores_cos, "^-", label="Error cos(x)")
    plt.title(f"Error absoluto vs número de términos (x = {x:.3f})")
    plt.xlabel("Número de términos")
    plt.ylabel("Error absoluto (escala log)")
    plt.grid(True, which="both")
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------- Gráfico 3: convergencia según x ----------
def grafico_convergencia_por_x():
    x_vals = [i * 0.1 for i in range(1, 51)]  # 0.1 a 5
    n_terminos = 8
    errores = [abs(taylor_exp(x, n_terminos) - math.exp(x)) for x in x_vals]

    plt.figure(figsize=(9, 5))
    plt.plot(x_vals, errores, "r-")
    plt.title(f"Error de Taylor de e^x con {n_terminos} términos")
    plt.xlabel("x")
    plt.ylabel("Error absoluto")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    grafico_funcion_vs_taylor()
    grafico_error_vs_terminos()
    grafico_convergencia_por_x()