"""
Errores computacionales: redondeo y truncamiento.

Este programa muestra diferentes tipos de errores que aparecen
cuando se realizan cálculos numéricos en un computador.

Se estudian principalmente:
- Errores de redondeo.
- Errores de truncamiento.
- El compromiso entre ambos tipos de error.
"""

# math contiene funciones matemáticas como:
# sin(), cos(), exp(), isclose(), sqrt(), etc.
import math

# sys permite acceder a información del sistema,
# por ejemplo al epsilon de máquina.
import sys

# Decimal permite mostrar con mayor detalle cómo Python
# representa ciertos números decimales.
from decimal import Decimal


# matplotlib se utiliza para realizar la gráfica final.
import matplotlib

# "Agg" permite guardar la gráfica directamente como imagen
# sin abrir una ventana.
matplotlib.use("Agg")

import matplotlib.pyplot as plt


# ===============================================================
# MEDIDAS DE ERROR
# ===============================================================

# ---------------------------------------------------------------
# ERROR ABSOLUTO
# ---------------------------------------------------------------

def error_absoluto(exacto, aprox):
    """
    Calcula el error absoluto entre un valor exacto
    y un valor aproximado.

    Error absoluto = |exacto - aproximación|
    """

    # abs() calcula el valor absoluto de la diferencia.
    return abs(exacto - aprox)


# ---------------------------------------------------------------
# ERROR RELATIVO
# ---------------------------------------------------------------

def error_relativo(exacto, aprox):
    """
    Calcula el error relativo.

    Error relativo = |exacto - aproximación| / |exacto|

    Si el valor exacto es cero, no se puede dividir entre cero,
    así que se devuelve NaN.
    """

    return (
        abs(exacto - aprox) / abs(exacto)
        if exacto != 0
        else float("nan")
    )


# ===============================================================
# ERRORES DE REDONDEO
# ===============================================================

def demo_redondeo():

    # Imprime una línea separadora.
    print("=" * 60)

    # Título de la sección.
    print("A) ERRORES DE REDONDEO")

    # Otra línea separadora.
    print("=" * 60)


    # ===========================================================
    # 1. REPRESENTACIÓN BINARIA IMPERFECTA
    # ===========================================================

    print("\n1. Representacion de 0.1 y suma 0.1 + 0.2")


    # Decimal(0.1) se utiliza para mostrar el valor real
    # que se obtiene al convertir el float 0.1 a Decimal.
    #
    # Esto permite observar que 0.1 en punto flotante
    # no se representa exactamente.
    print(
        f"   0.1 con 20 decimales : {Decimal(0.1)}"
    )


    # Realiza la suma de dos números de punto flotante.
    #
    # Aunque matemáticamente:
    #
    # 0.1 + 0.2 = 0.3
    #
    # internamente los números se almacenan de forma aproximada,
    # por lo que el resultado puede ser:
    #
    # 0.30000000000000004
    print(
        f"   0.1 + 0.2            = {0.1 + 0.2!r}"
    )


    # Comprueba si el resultado es exactamente igual a 0.3.
    #
    # En este caso normalmente devuelve False.
    print(
        f"   0.1 + 0.2 == 0.3 ?   "
        f"{0.1 + 0.2 == 0.3}"
    )


    # math.isclose() comprueba si dos números son
    # suficientemente cercanos.
    #
    # Es más apropiado para comparar resultados numéricos
    # que utilizar directamente ==.
    print(
        f"   math.isclose(...)    "
        f"{math.isclose(0.1 + 0.2, 0.3)}"
    )


    # ===========================================================
    # 2. EPSILON DE MÁQUINA
    # ===========================================================

    # sys.float_info.epsilon representa aproximadamente
    # la diferencia entre 1 y el siguiente número de punto flotante
    # representable por encima de 1.
    eps = sys.float_info.epsilon


    # Muestra el epsilon en notación científica.
    print(
        f"\n2. Epsilon de maquina: {eps:.3e}"
    )


    # eps/2 es tan pequeño que al sumarlo a 1,
    # el resultado puede volver a redondearse a 1.
    print(
        f"   1 + eps/2 == 1 ? "
        f"{1 + eps / 2 == 1}"
    )


    # Al sumar eps completo, ya se puede obtener
    # un número distinto de 1.
    print(
        f"   1 + eps   == 1 ? "
        f"{1 + eps == 1}"
    )


    # ===========================================================
    # 3. ACUMULACIÓN DEL ERROR
    # ===========================================================

    # Número de veces que se sumará 0.1.
    n = 1_000_000


    # Acumulador inicial.
    suma = 0.0


    # Repite la suma un millón de veces.
    for _ in range(n):

        # Cada vez se añade 0.1 al acumulador.
        suma += 0.1


    # Calcula una referencia multiplicando:
    #
    # n × 0.1
    #
    # En este programa se utiliza como valor esperado.
    exacto = n * 0.1


    # Muestra el título del experimento.
    print(
        f"\n3. Sumar 0.1 un millon de veces"
    )


    # Muestra el resultado de la suma repetida.
    print(
        f"   sum ingenua : {suma!r}"
    )


    # math.fsum() realiza la suma utilizando una estrategia
    # más precisa para reducir los errores de redondeo.
    print(
        f"   math.fsum   : "
        f"{math.fsum([0.1] * n)!r}"
    )


    # Muestra el valor utilizado como referencia.
    print(
        f"   exacto      : {exacto!r}"
    )


    # Calcula el error absoluto entre el resultado obtenido
    # y el valor de referencia.
    print(
        f"   error abs.  : "
        f"{error_absoluto(exacto, suma):.3e}"
    )


    # Calcula el error relativo.
    print(
        f"   error rel.  : "
        f"{error_relativo(exacto, suma):.3e}"
    )


    # ===========================================================
    # 4. CANCELACIÓN CATASTRÓFICA
    # ===========================================================

    # Se estudia la expresión:
    #
    # (1 - cos(x)) / x²
    #
    # cuyo límite cuando x tiende a 0 es 1/2.
    print(
        "\n4. Cancelacion catastrofica: "
        "(1 - cos x)/x^2  (limite = 0.5)"
    )


    # Encabezados de la tabla.
    print(
        f"   {'x':>10} "
        f"{'forma directa':>18} "
        f"{'forma estable':>18}"
    )


    # Prueba diferentes valores de x:
    #
    # 10^-1, 10^-2, ..., 10^-9
    for k in range(1, 10):

        # Define x = 10^(-k).
        x = 10.0 ** (-k)


        # Forma directa de calcular la expresión:
        #
        # (1 - cos(x))/x²
        #
        # Cuando x es muy pequeño, 1 y cos(x) son
        # números extremadamente cercanos.
        #
        # Al restarlos puede perderse precisión.
        directa = (1 - math.cos(x)) / x**2


        # Forma algebraicamente equivalente:
        #
        # 1 - cos(x) = 2 sin²(x/2)
        #
        # Entonces:
        #
        # (1 - cos(x))/x²
        # =
        # 2 sin²(x/2)/x²
        #
        # Esta forma suele ser más estable numéricamente.
        estable = (
            2 * math.sin(x / 2) ** 2
            / x**2
        )


        # Muestra ambos resultados.
        print(
            f"   {x:10.1e} "
            f"{directa:18.12f} "
            f"{estable:18.12f}"
        )


    # ===========================================================
    # 5. OVERFLOW Y UNDERFLOW
    # ===========================================================

    print("\n5. Overflow y underflow")


    # Overflow:
    #
    # 1e308 es un número muy grande.
    # Multiplicarlo por 10 supera aproximadamente
    # el máximo representable por un float.
    #
    # El resultado suele convertirse en inf.
    print(
        f"   1e308 * 10 = {1e308 * 10}"
    )


    # Underflow:
    #
    # 5e-324 está cerca del número positivo más pequeño
    # que puede representar un float.
    #
    # Al dividirlo entre 2 puede hacerse demasiado pequeño
    # y terminar convirtiéndose en 0.
    print(
        f"   5e-324 / 2 = {5e-324 / 2}"
    )


# ===============================================================
# ERRORES DE TRUNCAMIENTO
# ===============================================================

# ---------------------------------------------------------------
# SERIE DE TAYLOR DE e^x
# ---------------------------------------------------------------

def exp_taylor(x, n):
    """
    Aproxima e^x utilizando n términos de la serie de Maclaurin.

    e^x = 1 + x + x²/2! + x³/3! + ...
    """

    # suma almacena la suma acumulada.
    #
    # termino comienza en 1 porque:
    #
    # x^0 / 0! = 1
    suma, termino = 0.0, 1.0


    # Repite n veces.
    for k in range(n):

        # Añade el término actual.
        suma += termino


        # Calcula el siguiente término a partir del anterior.
        #
        # Si tenemos:
        #
        # x^k / k!
        #
        # el siguiente es:
        #
        # x^(k+1)/(k+1)!
        #
        # Por eso se multiplica por x/(k+1).
        termino *= x / (k + 1)


    # Devuelve la aproximación.
    return suma


# ===============================================================
# DEMOSTRACIÓN DEL TRUNCAMIENTO
# ===============================================================

def demo_truncamiento():

    print("\n" + "=" * 60)
    print("B) ERRORES DE TRUNCAMIENTO")
    print("=" * 60)


    # ===========================================================
    # 1. SERIE DE TAYLOR DE e^x TRUNCADA
    # ===========================================================

    # Punto donde se evaluará la función.
    x = 1.0


    # Valor de referencia utilizando math.exp().
    exacto = math.exp(x)


    # Muestra el título del experimento.
    print(
        f"\n1. e^{x} con n terminos de Taylor "
        f"(exacto = {exacto!r})"
    )


    # Encabezados de la tabla.
    print(
        f"   {'n':>3} "
        f"{'aproximacion':>20} "
        f"{'error abs.':>12} "
        f"{'error rel.':>12}"
    )


    # Prueba desde 1 hasta 15 términos.
    for n in range(1, 16):

        # Calcula la aproximación de e^x.
        a = exp_taylor(x, n)


        # Muestra:
        # - número de términos
        # - aproximación
        # - error absoluto
        # - error relativo
        print(
            f"   {n:3d} "
            f"{a:20.15f} "
            f"{error_absoluto(exacto, a):12.3e} "
            f"{error_relativo(exacto, a):12.3e}"
        )


    # ===========================================================
    # 2. DERIVADA POR DIFERENCIAS FINITAS
    # ===========================================================

    # f representa la función seno.
    #
    # df representa su derivada exacta:
    #
    # d/dx [sen(x)] = cos(x)
    f, df = math.sin, math.cos


    # Punto donde se calculará la derivada.
    x0 = 1.0


    # Título del experimento.
    print(
        f"\n2. Derivada de sen(x) en x={x0} "
        f"por diferencias hacia adelante"
    )


    # Encabezados.
    print(
        f"   {'h':>10} "
        f"{'aproximacion':>18} "
        f"{'error abs.':>12}"
    )


    # Prueba diferentes tamaños de paso.
    #
    # h = 0.1, 0.01, 0.001, ...
    for k in range(1, 6):

        # Define h = 10^(-k).
        h = 10.0 ** (-k)


        # Aproximación de la derivada mediante diferencia hacia adelante:
        #
        # f'(x) ≈ [f(x+h) - f(x)] / h
        d = (
            f(x0 + h) - f(x0)
        ) / h


        # Muestra:
        # - h
        # - aproximación de la derivada
        # - error respecto a cos(x0)
        print(
            f"   {h:10.1e} "
            f"{d:18.12f} "
            f"{error_absoluto(df(x0), d):12.3e}"
        )


# ===============================================================
# COMPROMISO ENTRE TRUNCAMIENTO Y REDONDEO
# ===============================================================

def demo_compromiso():

    print("\n" + "=" * 60)
    print("C) COMPROMISO ENTRE TRUNCAMIENTO Y REDONDEO")
    print("=" * 60)


    # Se utiliza:
    #
    # f(x) = e^x
    #
    # cuya derivada también es:
    #
    # f'(x) = e^x
    f, df = math.exp, math.exp


    # Punto donde se evalúa la derivada.
    x0 = 1.0


    # Valor exacto de la derivada.
    exacto = df(x0)


    # Listas para almacenar:
    # - diferentes valores de h
    # - errores correspondientes
    hs, errs = [], []


    # Genera valores de h desde:
    #
    # 10^0 hasta 10^-16
    for i in range(0, 17):

        # Define el tamaño del paso.
        h = 10.0 ** (-i)


        # Aproxima la derivada mediante diferencia hacia adelante.
        d = (
            f(x0 + h) - f(x0)
        ) / h


        # Guarda h.
        hs.append(h)

        # Guarda el error absoluto.
        errs.append(
            error_absoluto(exacto, d)
        )


    # Busca la posición donde se encuentra
    # el menor error de toda la lista.
    #
    # range(len(errs)) produce los índices.
    #
    # key=lambda i: errs[i] indica que queremos
    # encontrar el índice asociado al menor error.
    mejor = min(
        range(len(errs)),
        key=lambda i: errs[i]
    )


    # Muestra el tamaño de h que produjo el menor error
    # dentro de los valores probados.
    print(
        f"   h optimo aproximado = {hs[mejor]:.0e} "
        f"(error = {errs[mejor]:.2e})"
    )


    # Según la teoría, el valor óptimo de h para una diferencia
    # hacia adelante está relacionado aproximadamente con:
    #
    # h_opt ~ sqrt(epsilon)
    #
    # donde epsilon es el epsilon de máquina.
    print(
        "   Teoria: h_opt ~ sqrt(eps) = "
        f"{math.sqrt(sys.float_info.epsilon):.1e}"
    )


    # ===========================================================
    # GRÁFICA DEL COMPROMISO
    # ===========================================================

    # Crea una figura.
    plt.figure(figsize=(7, 4.5))


    # -----------------------------------------------------------
    # Error total
    # -----------------------------------------------------------

    # Muestra el error total obtenido para cada h.
    plt.loglog(
        hs,
        errs,
        "o-",
        label="Error total"
    )


    # -----------------------------------------------------------
    # Error de truncamiento
    # -----------------------------------------------------------

    # Representa aproximadamente:
    #
    # Error de truncamiento ~ O(h)
    #
    # En este caso se utiliza:
    #
    # h * exacto / 2
    #
    # como una curva de referencia proporcional a h.
    plt.loglog(
        hs,
        [h * exacto / 2 for h in hs],
        "--",
        label="Truncamiento ~ O(h)"
    )


    # -----------------------------------------------------------
    # Error de redondeo
    # -----------------------------------------------------------

    # Representa aproximadamente:
    #
    # Error de redondeo ~ epsilon / h
    #
    # Cuando h se hace demasiado pequeño,
    # este término comienza a aumentar.
    plt.loglog(
        hs,
        [
            sys.float_info.epsilon * exacto / h
            for h in hs
        ],
        "--",
        label="Redondeo ~ eps/h"
    )


    # Nombre del eje x.
    plt.xlabel("h")


    # Nombre del eje y.
    plt.ylabel("Error absoluto")


    # Título.
    plt.title(
        "Derivada numerica de e^x en x=1"
    )


    # Activa la cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )


    # Muestra la leyenda.
    plt.legend()


    # Ajusta automáticamente los elementos.
    plt.tight_layout()


    # Guarda la gráfica como una imagen.
    plt.savefig(
        "compromiso_errores.png",
        dpi=150
    )


    # Informa que la imagen fue guardada.
    print(
        "   Grafica guardada: compromiso_errores.png"
    )


# ===============================================================
# EJECUCIÓN DEL PROGRAMA
# ===============================================================

# Esta condición hace que los experimentos se ejecuten
# únicamente cuando el archivo se ejecuta directamente.
if __name__ == "__main__":

    # Ejecuta la demostración de errores de redondeo.
    demo_redondeo()

    # Ejecuta la demostración de errores de truncamiento.
    demo_truncamiento()

    # Ejecuta la demostración del compromiso entre
    # truncamiento y redondeo.
    demo_compromiso()