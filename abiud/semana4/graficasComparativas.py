import math
import matplotlib.pyplot as plt

# Importa tus funciones de serie de Taylor
from serieDeTaylorVsMath import taylor_exp, taylor_sin, taylor_cos


# ---------- Gráfico 1: función vs Taylor ----------
def grafico_funcion_vs_taylor():
    x_vals = [i * 0.05 for i in range(-60, 61)]  # -3 a 3
    n_terminos = 6

    y_real = [math.sin(x) for x in x_vals]
    y_taylor = [taylor_sin(x, n_terminos) for x in x_vals]

    plt.figure(figsize=(8, 4.5))

    plt.plot(
        x_vals,
        y_real,
        label="math.sin(x)",
        linewidth=2
    )

    plt.plot(
        x_vals,
        y_taylor,
        "--",
        label=f"Taylor ({n_terminos} términos)",
        linewidth=1.8
    )

    plt.title("Serie de Taylor de sin(x) vs math.sin")
    plt.xlabel("x (rad)")
    plt.ylabel("f(x)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------- Gráfico 2: error vs número de términos ----------
def grafico_error_vs_terminos():
    x = math.pi / 3
    terminos = list(range(1, 21))

    # Se usa max(..., 1e-16) para evitar log(0)
    errores_exp = [
        max(abs(taylor_exp(x, n) - math.exp(x)), 1e-16)
        for n in terminos
    ]

    errores_sin = [
        max(abs(taylor_sin(x, n) - math.sin(x)), 1e-16)
        for n in terminos
    ]

    errores_cos = [
        max(abs(taylor_cos(x, n) - math.cos(x)), 1e-16)
        for n in terminos
    ]

    plt.figure(figsize=(8, 4.5))

    plt.semilogy(
        terminos,
        errores_exp,
        "o-",
        label=r"Error $e^x$"
    )

    plt.semilogy(
        terminos,
        errores_sin,
        "s-",
        label=r"Error $\sin(x)$"
    )

    plt.semilogy(
        terminos,
        errores_cos,
        "^-",
        label=r"Error $\cos(x)$"
    )

    plt.title(r"Error absoluto vs Número de términos ($x = \pi/3$)")
    plt.xlabel(r"Número de términos ($N$)")
    plt.ylabel("Error absoluto (Escala Log)")

    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------- Gráfico 3: convergencia según x ----------
def grafico_convergencia_por_x():
    x_vals = [i * 0.1 for i in range(1, 51)]  # 0.1 a 5
    n_terminos = 8

    # Error de Taylor de e^x para diferentes valores de x
    errores = [
        max(
            abs(taylor_exp(x, n_terminos) - math.exp(x)),
            1e-16
        )
        for x in x_vals
    ]

    plt.figure(figsize=(8, 4.5))

    plt.semilogy(
        x_vals,
        errores,
        "r-",
        linewidth=2
    )

    plt.title(
        rf"Degradación del error de $e^x$ al alejar $x$ "
        rf"($N = {n_terminos}$)"
    )

    plt.xlabel(
        r"Distancia $x$ desde el punto de expansión ($a = 0$)"
    )

    plt.ylabel("Error absoluto (Escala Log)")

    plt.grid(True, which="both", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.show()


# ---------- Ejecución ----------
if __name__ == "__main__":
    grafico_funcion_vs_taylor()
    grafico_error_vs_terminos()
    grafico_convergencia_por_x()