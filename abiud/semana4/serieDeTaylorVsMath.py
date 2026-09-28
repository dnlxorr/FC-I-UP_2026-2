import math

def taylor_exp(x: float, n_terminos: int) -> float:
    """e^x = sum_{k=0}^{inf} x^k / k!"""
    suma = 0.0
    termino = 1.0  # x^0 / 0!
    for k in range(n_terminos):
        suma += termino
        termino *= x / (k + 1)
    return suma


def taylor_sin(x: float, n_terminos: int) -> float:
    """sin(x) = sum_{k=0}^{inf} (-1)^k x^(2k+1) / (2k+1)!"""
    suma = 0.0
    termino = x  # primer término
    for k in range(n_terminos):
        suma += termino
        termino *= -x * x / ((2 * k + 2) * (2 * k + 3))
    return suma


def taylor_cos(x: float, n_terminos: int) -> float:
    """cos(x) = sum_{k=0}^{inf} (-1)^k x^(2k) / (2k)!"""
    suma = 0.0
    termino = 1.0  # primer término
    for k in range(n_terminos):
        suma += termino
        termino *= -x * x / ((2 * k + 1) * (2 * k + 2))
    return suma


def comparar(func_taylor, func_math, nombre, x, lista_terminos):
    print("=" * 70)
    print(f"{nombre} evaluada en x = {x}")
    print("=" * 70)
    valor_real = func_math(x)
    print(f"Valor real (math): {valor_real:.15f}\n")
    print(f"{'Términos':<12}{'Taylor':<22}{'Error absoluto':<20}")
    print("-" * 60)
    for n in lista_terminos:
        aprox = func_taylor(x, n)
        error = abs(aprox - valor_real)
        print(f"{n:<12}{aprox:<22.15f}{error:<20.3e}")
    print()


if __name__ == "__main__":
    x = math.pi / 4  # 45 grados
    terminos = [1, 2, 3, 4, 5, 8, 10, 15, 20]

    comparar(taylor_exp, math.exp, "e^x", 1.0, terminos)
    comparar(taylor_sin, math.sin, "sin(x)", x, terminos)
    comparar(taylor_cos, math.cos, "cos(x)", x, terminos)