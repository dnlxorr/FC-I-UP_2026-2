# ==========================================
# 1. Errores Computacionales
# ==========================================
import math


def demostrar_errores():
    print("--- 1. ERROR DE REDONDEO ---")
    # En matemáticas matemáticas puras, 0.1 + 0.2 = 0.3
    suma = 0.1 + 0.2
    print(f"0.1 + 0.2 = {suma}")
    print(f"¿0.1 + 0.2 es exactamente 0.3? {suma == 0.3}")
    print("Conclusión: Al convertir a binario, se pierden decimales y se añade 'basura' en el decimal 17.\n")

    print("--- 2. ERROR DE TRUNCAMIENTO ---")
    # El valor exacto de e^1 es math.e
    exacto = math.e

    # Aproximación de e^1 usando solo los primeros 4 términos de su Serie de Taylor:
    # e^x = 1 + x + x^2/2! + x^3/3! + ...
    x = 1
    aproximacion = 1 + x + (x ** 2 / math.factorial(2)) + (x ** 3 / math.factorial(3))

    error_truncamiento = abs(exacto - aproximacion)
    print(f"Valor exacto de e: {exacto}")
    print(f"Aproximación (truncada a 4 términos): {aproximacion}")
    print(f"Error por truncamiento: {error_truncamiento}")
    print(
        "Conclusión: Al 'truncar' (cortar) la serie infinita, nuestro resultado tiene un margen de error frente al real.")


demostrar_errores()