"""
Taylor (con la fórmula) vs. librería math de Python.
Requiere: pip install sympy numpy matplotlib

Uso interactivo:    python taylor_simple.py
Uso con argumentos: python taylor_simple.py -f "sin(x)" -a 0 -n 6 -x 2
"""
import argparse
import math

import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

x = sp.symbols("x")
PREC = 50  # dígitos usados para calcular la referencia exacta


def taylor(f, a, n_terminos):
    """Calcula los primeros términos no nulos de la serie de Taylor."""
    terminos, detalle = [], []
    deriv, k = f, 0

    # Calcula derivadas hasta obtener la cantidad de términos solicitada
    while len(terminos) < n_terminos and k < 10 * n_terminos + 200:
        valor = sp.simplify(deriv.subs(x, a))  # Evalúa la derivada en a

        if valor != 0:
            coef = valor / sp.factorial(k)       # f^(k)(a) / k!
            terminos.append(coef * (x - a) ** k)
            detalle.append((k, deriv, valor, sp.factorial(k), coef))

        deriv = sp.diff(deriv, x)                # Calcula la siguiente derivada

        if deriv == 0:                           # Si es un polinomio, termina
            break

        k += 1

    return terminos, detalle


def digitos_correctos(err, ref):
    """Calcula aproximadamente cuántos dígitos significativos son correctos."""
    err, ref = abs(float(err)), abs(float(ref))

    if err == 0:
        return float("inf")

    return max(0.0, -math.log10(err / ref)) if ref else -math.log10(err)


def pedir_datos():
    # Permite introducir los datos mediante argumentos o por teclado
    p = argparse.ArgumentParser()
    p.add_argument("-f", help="función, p. ej. 'sin(x)'")
    p.add_argument("-a", help="punto de expansión, p. ej. 0, 1, pi/4")
    p.add_argument("-n", type=int, help="número de términos no nulos")
    p.add_argument("-x", dest="xv", help="punto donde evaluar, p. ej. 1, pi/6")
    p.add_argument("--guardar", help="guardar la figura en este archivo")
    args = p.parse_args()

    texto = args.f or input("Función f(x) (ej: sin(x), exp(x), log(1+x)): ")
    a = sp.sympify(args.a or input("Punto de expansión a (ej: 0, 1, pi/4): ") or "0")
    n = args.n or int(input("Cuántos términos no nulos quieres: ") or "6")
    xv = args.xv

    # Pide x hasta que el usuario introduzca un valor
    while not (xv or "").strip():
        xv = input("Valor de x para evaluar (ej: 1, 0.5, pi/6): ")

    return sp.sympify(texto), a, n, sp.sympify(xv), args.guardar


def main():
    # Obtiene los datos introducidos por el usuario
    f, a, n, xv, archivo = pedir_datos()

    # Calcula los términos de Taylor
    terminos, detalle = taylor(f, a, n)
    n = len(terminos)

    if n == 0:
        print("No se encontraron términos no nulos.")
        return

    # Muestra las derivadas, factoriales y coeficientes
    print(f"\nf(x) = {f}   expandida en a = {a}   ({n} términos)\n")
    print(f"{'k':>3} | {'f^(k)(x)':<22} | {'f^(k)(a)':<10} | {'k!':<12} | coeficiente")
    print("-" * 75)

    for k, d, v, fact, c in detalle:
        fact_txt = str(fact) if len(str(fact)) <= 12 else f"{float(fact):.3e}"
        print(f"{k:>3} | {str(d)[:22]:<22} | {str(v)[:10]:<10} | {fact_txt:<12} | {c}")

    # Construye y muestra el polinomio de Taylor
    polinomio = sp.Add(*terminos)
    print("\nf(x) ≈ " + sp.sstr(polinomio, order="rev-lex").replace("**", "^"))

    # Convierte x al formato float que utiliza math
    xf = float(xv)

    # Usa exactamente ese mismo valor para la referencia de alta precisión
    xr = sp.Rational(xf)

    # Convierte la función de SymPy en una función de math
    f_math = sp.lambdify(x, f, "math")
    val_math = f_math(xf)

    # Calcula el valor de referencia con mayor precisión
    exacto = sp.N(f.subs(x, xr), PREC)

    # Compara Taylor con math término por término
    print(f"\nEvaluando en x = {xf!r}      math da: {val_math!r}\n")
    print(f"{'Términos':>8} | {'Término k':<18} | {'Suma Taylor':<20} | "
          f"{'|Taylor - math|':<16} | Díg. correctos")
    print("-" * 90)

    suma = sp.Integer(0)
    sumas, dif_math, err_taylor = [], [], []

    for i, t in enumerate(terminos, start=1):
        # Evalúa cada término y lo suma
        val = sp.N(t.subs(x, xr), PREC)
        suma += val

        sumas.append(suma)

        # Error entre Taylor y math
        dif_math.append(abs(float(suma) - val_math))

        # Error entre Taylor y el valor de referencia
        err_taylor.append(abs(float(exacto - suma)))

        # Calcula los dígitos correctos
        dig = digitos_correctos(exacto - suma, exacto)

        print(f"{i:>8} | {float(val):<18.10g} | {float(suma):<20.15g} | "
              f"{dif_math[-1]:<16.3e} | {dig:5.1f}")

    # Calcula el error de math respecto al valor de referencia
    err_math = abs(float(exacto - sp.Rational(val_math)))

    print("\n" + "=" * 60)
    print(f" Valor exacto (sympy) : {sp.N(exacto, 20)}")
    print(f" Taylor ({n} términos)  : {sp.N(suma, 20)}")
    print(f" math (float64)       : {val_math!r}")
    print("-" * 60)
    print(f" Error de Taylor : {err_taylor[-1]:.3e}   "
          f"({digitos_correctos(exacto - suma, exacto):.1f} díg. correctos)")
    print(f" Error de math   : {err_math:.3e}   "
          f"({digitos_correctos(exacto - sp.Rational(val_math), exacto):.1f} díg. correctos)")

    # Indica cuál tiene menor error para este caso
    if err_taylor[-1] > err_math:
        print(" >>> math es más preciso que la serie con esos términos.")
    else:
        print(" >>> La serie igualó a math: ambos están al límite de float64 (~16 díg.).")

    # Prepara los valores para las gráficas
    af = float(a)
    xs = np.linspace(af - 5, af + 5, 600)

    # Calcula la función usando math
    y_math = np.full_like(xs, np.nan)

    for i, v in enumerate(xs):
        try:
            y_math[i] = f_math(float(v))
        except (ValueError, ZeroDivisionError, OverflowError, TypeError):
            pass

    # Calcula el polinomio de Taylor
    with np.errstate(all="ignore"):
        y_tay = np.array(sp.lambdify(x, polinomio, "numpy")(xs), dtype=float) * np.ones_like(xs)

    # Crea las dos gráficas
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # Primera gráfica: función original vs Taylor
    ax1.plot(xs, y_math, "k", lw=2, label="math (función real)")
    ax1.plot(xs, y_tay, "tab:red", ls="--", lw=1.5, label=f"Taylor ({n} términos)")

    fin = y_math[np.isfinite(y_math)]

    if fin.size:
        lo, hi = np.percentile(fin, [2, 98])
        m = (hi - lo) * 0.5 or 1
        ax1.set_ylim(lo - m, hi + m)

    ax1.axvline(af, color="gray", lw=0.5, ls="--")
    ax1.set_title("Taylor (fórmula) vs. math")
    ax1.legend()
    ax1.grid(alpha=0.3)

    # Segunda gráfica: error de Taylor y error de math
    piso = 1e-60

    ax2.semilogy(range(1, n + 1), np.maximum(err_taylor, piso), "tab:red",
                 marker="o", ms=3, label="Error de Taylor")

    ax2.axhline(max(err_math, piso), color="tab:blue", ls="--", label="Error de math")
    ax2.set_xlabel("Número de términos")
    ax2.set_ylabel("Error absoluto")
    ax2.set_title(f"Precisión en x = {xf:g}")
    ax2.legend()
    ax2.grid(alpha=0.3, which="both")

    # Ajusta la distribución de las gráficas
    plt.tight_layout()

    # Guarda la figura o la muestra en pantalla
    if archivo:
        plt.savefig(archivo, dpi=130)
        print(f"\nFigura guardada en {archivo}")
    else:
        plt.show()


if __name__ == "__main__":
    main()