"""
Funciones trascendentales con series de Taylor (Maclaurin)
comparadas con las funciones de la librería math.

En este programa se construyen las aproximaciones de:
- e^x
- sen(x)
- cos(x)
- ln(1+x)

utilizando series de Taylor y se comparan con los valores
calculados por la librería math de Python.
"""

# Importa la librería math, que contiene funciones matemáticas
# como exp(), sin(), cos(), log1p(), pi, etc.
import math


# Importa matplotlib para realizar las gráficas.
import matplotlib

# Utiliza el backend "Agg", que permite guardar las gráficas
# como imágenes sin abrir una ventana en pantalla.
matplotlib.use("Agg")

# Importa pyplot, que contiene las funciones utilizadas
# para crear y guardar las gráficas.
import matplotlib.pyplot as plt



# ===============================================================
# SERIES DE MACLAURIN
# ===============================================================

# En todas estas funciones:
# n representa el número de términos que se van a utilizar.
#
# Se calcula cada término a partir del anterior para evitar
# calcular factoriales grandes directamente.


# ---------------------------------------------------------------
# Serie de Taylor de e^x
# ---------------------------------------------------------------

def exp_taylor(x, n):
    """
    Aproxima e^x utilizando n términos de la serie de Maclaurin.

    e^x = 1 + x + x²/2! + x³/3! + ...
    """

    # suma almacenará el resultado de la serie.
    #
    # termino comienza en 1 porque el primer término de la serie
    # de e^x es:
    #
    # x^0 / 0! = 1
    suma, termino = 0.0, 1.0

    # Repite el proceso n veces.
    for k in range(n):

        # Añade el término actual a la suma.
        suma += termino

        # Calcula el siguiente término a partir del actual.
        #
        # Si el término actual es:
        # x^k / k!
        #
        # el siguiente es:
        # x^(k+1) / (k+1)!
        #
        # Por eso se multiplica por x/(k+1).
        termino *= x / (k + 1)

    # Devuelve la aproximación de e^x.
    return suma


# ---------------------------------------------------------------
# Serie de Taylor de sen(x)
# ---------------------------------------------------------------

def sin_taylor(x, n):
    """
    Aproxima sen(x) utilizando n términos de la serie de Maclaurin.

    sen(x) = x - x³/3! + x⁵/5! - x⁷/7! + ...
    """

    # El primer término de la serie es x.
    suma, termino = 0.0, x

    # Repite n veces.
    for k in range(n):

        # Añade el término actual a la suma.
        suma += termino

        # Calcula el siguiente término.
        #
        # La sucesión de términos es:
        #
        # x
        # -x³/3!
        # x⁵/5!
        # -x⁷/7!
        #
        # La expresión utilizada transforma directamente
        # un término en el siguiente.
        termino *= -x * x / ((2 * k + 2) * (2 * k + 3))

    # Devuelve la aproximación de sen(x).
    return suma


# ---------------------------------------------------------------
# Serie de Taylor de cos(x)
# ---------------------------------------------------------------

def cos_taylor(x, n):
    """
    Aproxima cos(x) utilizando n términos de la serie de Maclaurin.

    cos(x) = 1 - x²/2! + x⁴/4! - x⁶/6! + ...
    """

    # El primer término de la serie es 1.
    suma, termino = 0.0, 1.0

    # Repite n veces.
    for k in range(n):

        # Añade el término actual.
        suma += termino

        # Calcula el siguiente término usando el anterior.
        #
        # Pasa de:
        # x^(2k)/(2k)!
        #
        # a:
        # -x^(2k+2)/(2k+2)!
        termino *= -x * x / ((2 * k + 1) * (2 * k + 2))

    # Devuelve la aproximación de cos(x).
    return suma


# ---------------------------------------------------------------
# Serie de Taylor de ln(1+x)
# ---------------------------------------------------------------

def ln1p_taylor(x, n):
    """
    Aproxima ln(1+x) utilizando n términos de la serie.

    ln(1+x) = x - x²/2 + x³/3 - x⁴/4 + ...

    La serie converge para |x| < 1.
    """

    # suma acumula los términos de la serie.
    #
    # potencia comienza en 1 para después calcular x, x², x³...
    suma, potencia = 0.0, 1.0

    # k comienza en 1 porque el primer término es:
    #
    # x/1
    #
    # y termina en n.
    for k in range(1, n + 1):

        # Calcula la siguiente potencia:
        #
        # 1 -> x -> x² -> x³ -> ...
        potencia *= x

        # Añade el término correspondiente.
        #
        # (-1)^(k+1) produce el cambio de signo:
        #
        # k=1  -> +
        # k=2  -> -
        # k=3  -> +
        # k=4  -> -
        #
        # y después se divide entre k.
        suma += (-1) ** (k + 1) * potencia / k

    # Devuelve la aproximación de ln(1+x).
    return suma


# ===============================================================
# DICCIONARIO DE FUNCIONES
# ===============================================================

# Guarda en un solo lugar las funciones de Taylor y
# las funciones de referencia de la librería math.
#
# Cada elemento tiene:
#
# "nombre": (función de Taylor, función de math)
FUNCIONES = {
    "exp":   (exp_taylor,   math.exp),
    "sin":   (sin_taylor,   math.sin),
    "cos":   (cos_taylor,   math.cos),
    "ln1p":  (ln1p_taylor,  math.log1p),
}


# ===============================================================
# CÁLCULO DEL ERROR ABSOLUTO
# ===============================================================

def err_abs(exacto, aprox):
    """
    Calcula el error absoluto.

    Error absoluto = |valor exacto - valor aproximado|
    """

    # abs() devuelve el valor absoluto de la diferencia.
    return abs(exacto - aprox)


# ===============================================================
# CÁLCULO DEL ERROR RELATIVO
# ===============================================================

def err_rel(exacto, aprox):
    """
    Calcula el error relativo.

    Error relativo = |exacto - aproximado| / |exacto|

    Si el valor exacto es 0, se devuelve NaN
    porque no se puede dividir entre cero.
    """

    return (
        abs(exacto - aprox) / abs(exacto)
        if exacto != 0
        else float("nan")
    )



# ===============================================================
# 1. COMPARACIÓN EN UN PUNTO CON DIFERENTES TÉRMINOS
# ===============================================================

def tabla_terminos(nombre, x, terminos):
    """
    Compara la aproximación de Taylor con math
    utilizando diferentes números de términos.

    nombre:
        Nombre de la función, por ejemplo "exp" o "sin".

    x:
        Punto donde se evalúa la función.

    terminos:
        Lista con las diferentes cantidades de términos.
    """

    # Busca en el diccionario la función de Taylor
    # y la función de referencia.
    taylor, ref = FUNCIONES[nombre]

    # Calcula el valor considerado exacto utilizando math.
    exacto = ref(x)

    # Imprime el nombre de la función y su valor de referencia.
    print(f"\n{nombre}({x})  -  math: {exacto!r}")

    # Imprime los encabezados de la tabla.
    print(
        f"   {'n':>3} "
        f"{'Taylor':>22} "
        f"{'error abs.':>12} "
        f"{'error rel.':>12}"
    )

    # Recorre cada cantidad de términos.
    for n in terminos:

        # Calcula la aproximación mediante Taylor.
        a = taylor(x, n)

        # Muestra:
        # - número de términos
        # - aproximación
        # - error absoluto
        # - error relativo
        print(
            f"   {n:3d} "
            f"{a:22.15f} "
            f"{err_abs(exacto, a):12.3e} "
            f"{err_rel(exacto, a):12.3e}"
        )



# ===============================================================
# 2. COMPARACIÓN EN VARIOS PUNTOS CON n FIJO
# ===============================================================

def tabla_puntos(nombre, xs, n):
    """
    Compara Taylor y math en varios valores de x,
    manteniendo fijo el número de términos.
    """

    # Obtiene la función de Taylor y la función de referencia.
    taylor, ref = FUNCIONES[nombre]

    # Indica en pantalla el número fijo de términos.
    print(f"\n{nombre} con n = {n} terminos")

    # Encabezados de la tabla.
    print(
        f"   {'x':>6} "
        f"{'Taylor':>22} "
        f"{'math':>22} "
        f"{'error abs.':>12}"
    )

    # Recorre todos los valores de x.
    for x in xs:

        # Calcula:
        # a = aproximación de Taylor
        # e = valor de referencia obtenido mediante math
        a, e = taylor(x, n), ref(x)

        # Imprime los resultados.
        print(
            f"   {x:6.2f} "
            f"{a:22.14f} "
            f"{e:22.14f} "
            f"{err_abs(e, a):12.3e}"
        )



# ===============================================================
# 3. TÉRMINOS NECESARIOS PARA UNA TOLERANCIA
# ===============================================================

def terminos_necesarios(nombre, x, tol=1e-10, nmax=200):
    """
    Busca el menor número de términos necesario
    para conseguir un error absoluto menor que tol.

    tol:
        tolerancia permitida.

    nmax:
        número máximo de términos que se probarán.
    """

    # Obtiene la función de Taylor y la referencia.
    taylor, ref = FUNCIONES[nombre]

    # Calcula el valor de referencia.
    exacto = ref(x)

    # Prueba desde 1 término hasta nmax términos.
    for n in range(1, nmax + 1):

        # Calcula la aproximación y compara su error
        # con la tolerancia.
        if err_abs(exacto, taylor(x, n)) < tol:

            # Cuando se encuentra la primera cantidad
            # que cumple la condición, se devuelve.
            return n

    # Si no se encuentra ninguna cantidad que cumpla
    # la condición, devuelve None.
    return None



# ===============================================================
# 4. GRÁFICA DE ERROR VS NÚMERO DE TÉRMINOS
# ===============================================================

def grafica_convergencia(x=0.5, nmax=15):
    """
    Genera una gráfica donde se observa cómo disminuye
    el error al aumentar el número de términos de Taylor.
    """

    # Crea una figura con tamaño de 7 x 4.5 pulgadas.
    plt.figure(figsize=(7, 4.5))

    # Recorre todas las funciones del diccionario.
    for nombre, (taylor, ref) in FUNCIONES.items():

        # Calcula el valor exacto o de referencia.
        exacto = ref(x)

        # Genera una lista:
        # 1, 2, 3, ..., nmax
        ns = list(range(1, nmax + 1))

        # Calcula el error para cada cantidad de términos.
        #
        # max(..., 1e-18) evita obtener un error igual a cero,
        # porque en escala logarítmica no se puede representar 0.
        errs = [
            max(
                err_abs(exacto, taylor(x, n)),
                1e-18
            )
            for n in ns
        ]

        # semilogy utiliza:
        # - escala normal en x
        # - escala logarítmica en y
        #
        # Así es más fácil observar errores muy pequeños.
        plt.semilogy(
            ns,
            errs,
            "o-",
            label=nombre
        )

    # Nombre del eje x.
    plt.xlabel("Numero de terminos n")

    # Nombre del eje y.
    plt.ylabel("Error absoluto")

    # Título indicando el valor de x utilizado.
    plt.title(
        f"Convergencia de las series de Taylor en x = {x}"
    )

    # Cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Muestra la leyenda con las cuatro funciones.
    plt.legend()

    # Ajusta automáticamente los espacios.
    plt.tight_layout()

    # Guarda la gráfica en la carpeta Actividades.
    plt.savefig(
        "../Actividades/taylor_convergencia.png",
        dpi=150
    )


# ===============================================================
# PROGRAMA PRINCIPAL
# ===============================================================

# Esta condición hace que el código siguiente se ejecute
# solamente cuando el archivo se ejecuta directamente.
if __name__ == "__main__":


    # ===========================================================
    # 1. ERROR VS NÚMERO DE TÉRMINOS
    # ===========================================================

    # Imprime una línea separadora.
    print("=" * 62)

    # Título de esta sección.
    print("1. ERROR vs NUMERO DE TERMINOS")

    # Otra línea separadora.
    print("=" * 62)


    # -----------------------------------------------------------
    # e^x en x = 1
    # -----------------------------------------------------------

    # Compara la serie de e^x utilizando diferentes
    # cantidades de términos.
    tabla_terminos(
        "exp",
        1.0,
        [2, 4, 6, 8, 10, 12, 15]
    )


    # -----------------------------------------------------------
    # sen(x) en x = 1
    # -----------------------------------------------------------

    tabla_terminos(
        "sin",
        1.0,
        [1, 2, 3, 4, 5, 6, 8]
    )


    # -----------------------------------------------------------
    # cos(x) en x = 1
    # -----------------------------------------------------------

    tabla_terminos(
        "cos",
        1.0,
        [1, 2, 3, 4, 5, 6, 8]
    )


    # -----------------------------------------------------------
    # ln(1+x) en x = 0.5
    # -----------------------------------------------------------

    tabla_terminos(
        "ln1p",
        0.5,
        [2, 5, 10, 20, 30, 40]
    )


    # ===========================================================
    # 2. ERROR VS PUNTO x
    # ===========================================================

    print("\n" + "=" * 62)
    print("2. ERROR vs PUNTO x (n fijo = 8)")
    print("=" * 62)


    # Comprueba cómo cambia el error de e^x
    # cuando cambia x pero se mantienen 8 términos.
    tabla_puntos(
        "exp",
        [0.1, 0.5, 1, 2, 5, 10],
        8
    )


    # Comprueba el comportamiento del seno
    # con 8 términos.
    tabla_puntos(
        "sin",
        [0.1, 0.5, 1, 2, 3, 5],
        8
    )


    # Comprueba el comportamiento de ln(1+x)
    # con 8 términos.
    tabla_puntos(
        "ln1p",
        [0.1, 0.5, 0.9, 0.99, 1.5],
        8
    )


    # ===========================================================
    # 3. TÉRMINOS NECESARIOS PARA ERROR < 1e-10
    # ===========================================================

    print("\n" + "=" * 62)
    print("3. TERMINOS NECESARIOS PARA ERROR < 1e-10")
    print("=" * 62)


    # Se analiza cada función junto con una lista
    # de valores de x.
    for nombre, xs in [
        ("exp", [0.5, 1, 5, 10]),
        ("sin", [0.5, 1, 5, 10]),
        ("cos", [0.5, 1, 5, 10]),
        ("ln1p", [0.1, 0.5, 0.9])
    ]:

        # Recorre los valores de x.
        for x in xs:

            # Busca cuántos términos se necesitan
            # para obtener un error menor que 1e-10.
            print(
                f"   {nombre:5s} "
                f"x={x:<5} "
                f"-> {terminos_necesarios(nombre, x)}"
            )


    # ===========================================================
    # 4. x GRANDE: sen(20)
    # ===========================================================

    print("\n" + "=" * 62)
    print(
        "4. x GRANDE: sen(20) por Taylor "
        "(truncamiento + cancelacion)"
    )
    print("=" * 62)


    # Calcula el valor de referencia usando math.sin().
    exacto = math.sin(20)

    # Muestra el valor de referencia.
    print(f"   math.sin(20) = {exacto!r}")


    # Prueba diferentes cantidades de términos
    # para aproximar sen(20).
    for n in [5, 10, 15, 20, 30, 40, 60]:

        # Calcula sen(20) mediante Taylor.
        a = sin_taylor(20, n)

        # Muestra:
        # - número de términos
        # - aproximación
        # - error absoluto
        print(
            f"   n={n:3d}  "
            f"Taylor = {a:22.10f}  "
            f"error abs. = {err_abs(exacto, a):.3e}"
        )


    # -----------------------------------------------------------
    # REDUCCIÓN DEL ARGUMENTO
    # -----------------------------------------------------------

    # Como el seno es periódico con período 2π,
    # podemos reemplazar un ángulo grande por otro equivalente
    # dentro de un intervalo más pequeño.
    print(
        "   Reduciendo el argumento (x mod 2*pi) "
        "el problema desaparece:"
    )


    # Calcula el resto de dividir 20 entre 2π.
    #
    # Esto produce un ángulo equivalente a 20 radianes,
    # pero mucho más pequeño.
    xr = math.fmod(20, 2 * math.pi)


    # Aproxima el seno del valor reducido utilizando
    # solamente 12 términos.
    a = sin_taylor(xr, 12)


    # Muestra:
    # - valor reducido
    # - aproximación
    # - error respecto a math.sin(20)
    print(
        f"   x reducido = {xr:.6f}, "
        f"Taylor n=12 = {a:.14f}, "
        f"error = {err_abs(exacto, a):.3e}"
    )


    # ===========================================================
    # CREACIÓN DE LA GRÁFICA
    # ===========================================================

    # Genera la gráfica de convergencia utilizando:
    #
    # x = 0.5
    # n = 1 hasta 15
    grafica_convergencia()


    # Informa que la gráfica fue guardada.
    print("\nGrafica guardada: taylor_convergencia.png")