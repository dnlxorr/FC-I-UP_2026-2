"""
Semana 4 - Actividad 4

Análisis de los resultados de las actividades 1, 2 y 3
mediante gráficas y cálculo numérico.

Este programa necesita tener en la misma carpeta los archivos:
- FiguraGeometrica.py
- SerieTaylor.py

De esos archivos se importan las clases, funciones y series de Taylor
que se utilizan en esta actividad.
"""

# Importa la librería math para utilizar:
# - cos()
# - sin()
# - sqrt()
# - pi
# - exp()
# - fsum()
# entre otras funciones matemáticas.
import math

# Permite trabajar con archivos y rutas del sistema.
import os

# Permite modificar elementos relacionados con el sistema
# y las rutas de búsqueda de Python.
import sys

# Permite medir el tiempo que tarda en ejecutarse una operación.
import timeit


# Importamos matplotlib para crear las gráficas.
import matplotlib

# Se selecciona el backend "Agg", que permite generar imágenes
# sin necesidad de abrir una ventana gráfica.
matplotlib.use("Agg")

# Importa pyplot, que contiene las funciones para construir las gráficas.
import matplotlib.pyplot as plt


# Agrega la carpeta donde se encuentra este archivo
# a la lista de rutas donde Python busca módulos.
#
# Esto permite importar FiguraGeometrica.py y SerieTaylor.py
# aunque el programa se ejecute desde otra ubicación.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


# Importa desde FiguraGeometrica:
# - Circulo: clase para representar un círculo.
# - FiguraGeometrica: clase base o abstracta.
# - obtener_area: función que calcula el área validando el tipo de objeto.
from FiguraGeometrica import Circulo, FiguraGeometrica, obtener_area


# Importa desde SerieTaylor:
# - exp_taylor: aproximación de e^x mediante Taylor.
# - sin_taylor: aproximación de sen(x) mediante Taylor.
# - terminos_necesarios: calcula cuántos términos se necesitan
#   para alcanzar una tolerancia determinada.
from SerieTaylor import (
    exp_taylor,
    sin_taylor,
    terminos_necesarios
)


# Es un valor mínimo utilizado para evitar que aparezca
# un cero al representar errores en escala logarítmica.
#
# En una gráfica logarítmica no se puede representar el valor 0.
PISO = 1e-18


# ---------------------------------------------------------------
# Función piso
# ---------------------------------------------------------------

def piso(v):
    """
    Devuelve el mayor valor entre v y PISO.

    Su objetivo es evitar valores iguales a 0 cuando se trabaja
    con gráficas logarítmicas.
    """
    return max(v, PISO)


# ---------------------------------------------------------------
# Gráfica 1:
# Acumulación del error de redondeo
# Actividad 1
# ---------------------------------------------------------------

def datos_acumulacion():
    """
    Calcula cómo aumenta el error cuando se suma 0.1
    muchas veces utilizando aritmética de punto flotante.
    """

    # Crea los valores:
    # 10, 100, 1000, 10000, 100000 y 1000000
    #
    # Estos serán los diferentes números de sumas que se realizarán.
    checkpoints = [10 ** k for k in range(1, 7)]

    # suma:
    # acumulador de la suma de 0.1

    # i:
    # cuenta cuántas veces se ha realizado la suma.

    # errs:
    # guardará el error para cada cantidad de sumas.
    suma, i, errs = 0.0, 0, []

    # Recorre cada uno de los puntos de control.
    for cp in checkpoints:

        # Sigue sumando 0.1 hasta llegar al número de sumas
        # indicado por cp.
        while i < cp:
            suma += 0.1
            i += 1

        # math.fsum() realiza una suma con mayor precisión.
        #
        # Se utiliza como referencia para comparar con la suma
        # realizada normalmente.
        #
        # abs() obtiene el error absoluto.
        errs.append(abs(suma - math.fsum([0.1] * cp)))

    # Devuelve:
    # - cantidad de sumas
    # - errores correspondientes
    return checkpoints, errs


# ---------------------------------------------------------------
# Gráfica 2:
# Cancelación catastrófica
# Actividad 1
# ---------------------------------------------------------------

def datos_cancelacion():
    """
    Compara dos formas de calcular:

        (1 - cos(x)) / x²

    para valores muy pequeños de x.

    La primera forma puede sufrir cancelación catastrófica.
    La segunda forma es numéricamente más estable.
    """

    # k toma los valores de 1 a 9.
    ks = list(range(1, 10))

    # Listas para guardar los errores de ambas expresiones.
    directa, estable = [], []

    # Se analiza cada valor de k.
    for k in ks:

        # Define x = 10^(-k).
        #
        # Por lo tanto:
        # x = 0.1, 0.01, 0.001, ..., 0.000000001
        x = 10.0 ** (-k)

        # Calcula una aproximación de referencia basada
        # en la serie de Taylor de:
        #
        # (1 - cos(x)) / x²
        #
        # para valores pequeños de x.
        ref = (
            0.5
            - x**2 / 24
            + x**4 / 720
            - x**6 / 40320
        )

        # Forma directa de calcular la expresión.
        #
        # Esta forma puede producir pérdida de precisión
        # cuando x es muy pequeño.
        d = (1 - math.cos(x)) / x**2

        # Forma algebraicamente equivalente pero más estable:
        #
        # 1 - cos(x) = 2 sen²(x/2)
        #
        # Por tanto:
        #
        # (1 - cos(x))/x² = 2 sen²(x/2)/x²
        e = 2 * math.sin(x / 2) ** 2 / x**2

        # Calcula el error relativo de la forma directa.
        directa.append(abs(d - ref) / ref)

        # Calcula el error relativo de la forma estable.
        estable.append(abs(e - ref) / ref)

    # Devuelve:
    # - los valores de k
    # - errores de la forma directa
    # - errores de la forma estable
    return ks, directa, estable


# ---------------------------------------------------------------
# Gráfica 3:
# Truncamiento de e^x según x y número de términos
# Actividad 3
# ---------------------------------------------------------------

def datos_exp():
    """
    Calcula el error relativo de la aproximación de e^x
    utilizando diferentes cantidades de términos de Taylor.
    """

    # Genera valores de x desde 0.25 hasta 10.
    #
    # 1*0.25 = 0.25
    # 2*0.25 = 0.50
    # ...
    # 40*0.25 = 10
    xs = [i * 0.25 for i in range(1, 41)]

    # Se crea un diccionario donde cada clave es el número
    # de términos utilizados en la serie.
    #
    # Para cada n se calcula el error relativo:
    #
    # |Taylor - valor real| / valor real
    return xs, {
        n: [
            piso(
                abs(exp_taylor(x, n) - math.exp(x))
                / math.exp(x)
            )
            for x in xs
        ]
        for n in (5, 10, 15, 25)
    }


# ---------------------------------------------------------------
# Gráfica 4:
# sen(x) con Taylor directo vs reducción de argumento
# ---------------------------------------------------------------

def datos_sin():
    """
    Compara dos métodos para aproximar sen(x):

    1. Utilizar directamente la serie de Taylor.
    2. Reducir primero el argumento al intervalo [-π, π].
    """

    # Genera valores desde 0.5 hasta 40.
    xs = [i * 0.5 for i in range(1, 81)]

    # -----------------------------------------------------------
    # Método directo
    # -----------------------------------------------------------

    # Para cada x se calcula sen(x) usando 60 términos
    # de la serie de Taylor y se compara con math.sin(x).
    directo = [
        piso(
            abs(
                sin_taylor(x, 60) - math.sin(x)
            )
        )
        for x in xs
    ]

    # -----------------------------------------------------------
    # Método con reducción de argumento
    # -----------------------------------------------------------

    # Primero se transforma x para llevarlo a un valor
    # equivalente dentro del intervalo [-π, π].
    #
    # La expresión:
    #
    # x - 2π round(x / 2π)
    #
    # reduce el argumento aprovechando la periodicidad
    # de la función seno.
    #
    # Después se utilizan únicamente 12 términos de Taylor.
    reducido = [
        piso(
            abs(
                sin_taylor(
                    x - 2 * math.pi * round(x / (2 * math.pi)),
                    12
                )
                - math.sin(x)
            )
        )
        for x in xs
    ]

    # Devuelve:
    # - valores de x
    # - error del método directo
    # - error del método reducido
    return xs, directo, reducido


# ---------------------------------------------------------------
# Gráfica 5:
# Términos necesarios para error < 1e-10
# ---------------------------------------------------------------

def datos_terminos():
    """
    Determina cuántos términos necesita cada serie
    para obtener un error menor que 1e-10.
    """

    # Valores de x que serán analizados.
    xs = [
        0.1, 0.2, 0.3, 0.4, 0.5,
        0.6, 0.7, 0.8, 0.9, 0.95
    ]

    # Diccionario donde se almacenarán los resultados.
    res = {}

    # Se estudian cuatro funciones:
    # exp, sin, cos y ln1p
    for nombre in ("exp", "sin", "cos", "ln1p"):

        # Para cada función y cada valor de x,
        # se calcula cuántos términos son necesarios
        # para alcanzar una tolerancia de 1e-10.
        #
        # 3000 representa el número máximo de términos permitidos.
        res[nombre] = [
            terminos_necesarios(
                nombre,
                x,
                1e-10,
                3000
            )
            for x in xs
        ]

    # Devuelve los valores de x y el diccionario con resultados.
    return xs, res


# ---------------------------------------------------------------
# Gráfica 6:
# Costo de utilizar clases abstractas
# Actividad 2
# ---------------------------------------------------------------

class CirculoPlano:
    """
    Representa un círculo utilizando una clase normal,
    sin utilizar una clase abstracta (ABC).
    """

    # Constructor de la clase.
    def __init__(self, radio):

        # Guarda el radio dentro del objeto.
        self.radio = radio

    # Método para calcular el área.
    def calcularArea(self):

        # Fórmula del área del círculo:
        #
        # A = πr²
        return math.pi * self.radio ** 2


# ---------------------------------------------------------------

def obtener_area_sin_validar(figura):
    """
    Calcula el área llamando directamente al método
    calcularArea(), sin comprobar el tipo del objeto.
    """
    return figura.calcularArea()


# ---------------------------------------------------------------

def datos_tiempos(n=500_000):
    """
    Mide cuánto tiempo tarda cada operación.

    n indica cuántas veces se repetirá cada operación
    para obtener una medición más representativa.
    """

    # Crea un objeto de la clase Circulo importada,
    # que utiliza la estructura abstracta.
    #
    # También crea un objeto de la clase plana,
    # que no utiliza ABC.
    abc_obj, plano = Circulo(2.0), CirculoPlano(2.0)

    # Diccionario donde se guardarán los tiempos.
    t = {}

    # -----------------------------------------------------------
    # Tiempo para crear un objeto de una clase normal
    # -----------------------------------------------------------

    t["Instanciar\nclase plana"] = timeit.timeit(
        lambda: CirculoPlano(2.0),
        number=n
    )

    # -----------------------------------------------------------
    # Tiempo para crear un objeto de una subclase ABC
    # -----------------------------------------------------------

    t["Instanciar\nsubclase ABC"] = timeit.timeit(
        lambda: Circulo(2.0),
        number=n
    )

    # -----------------------------------------------------------
    # Tiempo para ejecutar calcularArea() de una clase normal
    # -----------------------------------------------------------

    t["calcularArea\nplana"] = timeit.timeit(
        plano.calcularArea,
        number=n
    )

    # -----------------------------------------------------------
    # Tiempo para ejecutar calcularArea() de una clase ABC
    # -----------------------------------------------------------

    t["calcularArea\nABC"] = timeit.timeit(
        abc_obj.calcularArea,
        number=n
    )

    # -----------------------------------------------------------
    # Tiempo para obtener el área SIN comprobar el tipo
    # -----------------------------------------------------------

    t["obtener_area\n(sin validar)"] = timeit.timeit(
        lambda: obtener_area_sin_validar(abc_obj),
        number=n
    )

    # -----------------------------------------------------------
    # Tiempo para obtener el área CON isinstance
    # -----------------------------------------------------------

    t["obtener_area\n(con isinstance)"] = timeit.timeit(
        lambda: obtener_area(abc_obj),
        number=n
    )

    # Convierte el tiempo total de segundos a:
    #
    # nanosegundos por llamada
    #
    # tiempo / n * 10^9
    return {
        k: v / n * 1e9
        for k, v in t.items()
    }


# ---------------------------------------------------------------
# Función principal
# ---------------------------------------------------------------

def main():

    # ===========================================================
    # GRÁFICA 1
    # ===========================================================

    # Obtiene los datos del error acumulado.
    ns, errs = datos_acumulacion()

    # Crea una figura de 9 x 6 pulgadas.
    plt.figure(figsize=(9, 6))

    # Gráfica logarítmica en ambos ejes.
    #
    # Se representa:
    # número de sumas vs error.
    plt.loglog(
        ns,
        [piso(e) for e in errs],
        "o-",
        color="tab:red",
        label="sum ingenua"
    )

    # Dibuja una línea horizontal que representa
    # el límite PISO utilizado para evitar el cero.
    plt.loglog(
        ns,
        [PISO] * len(ns),
        "s--",
        color="tab:green",
        label="math.fsum (exacto)"
    )

    # Título de la gráfica.
    plt.title(
        "1. Acumulación de error al sumar 0.1 n veces"
    )

    # Nombre del eje x.
    plt.xlabel("n (numero de sumas)")

    # Nombre del eje y.
    plt.ylabel("Error absoluto")

    # Muestra la leyenda.
    plt.legend()

    # Activa una cuadrícula.
    # which="both" incluye líneas para escalas mayores y menores.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Ajusta automáticamente los elementos de la figura.
    plt.tight_layout()

    # Guarda la gráfica como una imagen PNG.
    plt.savefig(
        "grafica_1.png",
        dpi=140
    )

    # Cierra la figura para liberar memoria.
    plt.close()


    # ===========================================================
    # GRÁFICA 2
    # ===========================================================

    # Obtiene los errores calculados anteriormente.
    ks, d, e = datos_cancelacion()

    # Convierte k en valores de x:
    #
    # x = 10^(-k)
    hs = [10.0 ** -k for k in ks]

    # Crea una nueva figura.
    plt.figure(figsize=(9, 6))

    # Representa el error de la forma directa.
    plt.loglog(
        hs,
        [piso(v) for v in d],
        "o-",
        color="tab:red",
        label="(1 - cos x)/x² directa"
    )

    # Representa el error de la forma estable.
    plt.loglog(
        hs,
        [piso(v) for v in e],
        "s-",
        color="tab:green",
        label="2 sen²(x/2)/x² estable"
    )

    # Invierte el eje x para que los valores más pequeños
    # aparezcan hacia la derecha.
    plt.gca().invert_xaxis()

    # Título.
    plt.title("2. Cancelación catastrófica")

    # Eje x.
    plt.xlabel("x")

    # Eje y.
    plt.ylabel("Error relativo")

    # Muestra la leyenda.
    plt.legend()

    # Activa la cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Ajusta los elementos de la figura.
    plt.tight_layout()

    # Guarda la gráfica.
    plt.savefig(
        "grafica_2.png",
        dpi=140
    )

    # Cierra la figura.
    plt.close()


    # ===========================================================
    # GRÁFICA 3
    # ===========================================================

    # Obtiene los valores de x y las curvas de error.
    xs, curvas = datos_exp()

    # Crea una nueva figura.
    plt.figure(figsize=(9, 6))

    # Recorre cada cantidad de términos y sus errores.
    for n, ys in curvas.items():

        # semilogy utiliza una escala logarítmica
        # solamente en el eje y.
        plt.semilogy(
            xs,
            ys,
            label=f"n = {n}"
        )

    # Título.
    plt.title(
        "3. Truncamiento de e^x: error vs x"
    )

    # Eje x.
    plt.xlabel("x")

    # Eje y.
    plt.ylabel("Error relativo")

    # Leyenda.
    plt.legend()

    # Cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Ajusta la figura.
    plt.tight_layout()

    # Guarda la imagen.
    plt.savefig(
        "grafica_3.png",
        dpi=140
    )

    # Cierra la figura.
    plt.close()


    # ===========================================================
    # GRÁFICA 4
    # ===========================================================

    # Obtiene los errores del seno mediante ambos métodos.
    xs, directo, reducido = datos_sin()

    # Crea la figura.
    plt.figure(figsize=(9, 6))

    # Gráfica del error utilizando Taylor directamente
    # con 60 términos.
    plt.semilogy(
        xs,
        directo,
        color="tab:red",
        label="Taylor directo (60 terminos)"
    )

    # Gráfica del error utilizando reducción de argumento
    # y solamente 12 términos.
    plt.semilogy(
        xs,
        reducido,
        color="tab:green",
        label="Con reduccion a [-π, π] (12 terminos)"
    )

    # Título.
    plt.title(
        "4. sen(x): efecto de la reducción de argumento"
    )

    # Eje x.
    plt.xlabel("x")

    # Eje y.
    plt.ylabel("Error absoluto")

    # Leyenda.
    plt.legend()

    # Cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Ajusta la figura.
    plt.tight_layout()

    # Guarda la gráfica.
    plt.savefig(
        "grafica_4.png",
        dpi=140
    )

    # Cierra la figura.
    plt.close()


    # ===========================================================
    # GRÁFICA 5
    # ===========================================================

    # Obtiene los valores de x y los términos necesarios.
    xs, res = datos_terminos()

    # Crea la figura.
    plt.figure(figsize=(9, 6))

    # Recorre cada función y los términos necesarios.
    for nombre, ys in res.items():

        # Representa el número de términos necesarios
        # para cada valor de x.
        plt.semilogy(
            xs,
            ys,
            "o-",
            label=nombre
        )

    # Título.
    plt.title(
        "5. Términos necesarios para error < 1e-10"
    )

    # Eje x.
    plt.xlabel("x")

    # Eje y.
    plt.ylabel("Número de términos")

    # Leyenda.
    plt.legend()

    # Cuadrícula.
    plt.grid(
        True,
        which="both",
        alpha=0.3
    )

    # Ajusta la figura.
    plt.tight_layout()

    # Guarda la imagen.
    plt.savefig(
        "grafica_5.png",
        dpi=140
    )

    # Cierra la figura.
    plt.close()


    # ===========================================================
    # GRÁFICA 6
    # ===========================================================

    # Obtiene los tiempos de ejecución.
    t = datos_tiempos()

    # Crea una nueva figura.
    plt.figure(figsize=(10, 6))

    # Crea una gráfica de barras.
    plt.bar(
        list(t.keys()),
        list(t.values()),

        # Define colores diferentes para las barras.
        color=[
            "tab:blue",
            "tab:orange",
            "tab:blue",
            "tab:orange",
            "tab:gray",
            "tab:purple"
        ]
    )

    # Título.
    plt.title(
        "6. Costo de las clases abstractas"
    )

    # Etiqueta del eje y.
    plt.ylabel("Tiempo por llamada (ns)")

    # Gira ligeramente los nombres del eje x
    # para que sean más fáciles de leer.
    plt.xticks(
        rotation=15,
        fontsize=8
    )

    # Agrega cuadrícula solamente en el eje y.
    plt.grid(
        True,
        axis="y",
        alpha=0.3
    )

    # Ajusta la figura.
    plt.tight_layout()

    # Guarda la imagen.
    plt.savefig(
        "grafica_6.png",
        dpi=140
    )

    # Cierra la figura.
    plt.close()


    # ===========================================================
    # RESUMEN NUMÉRICO
    # ===========================================================

    # Título del resumen.
    print("RESUMEN NUMERICO")
    print("-" * 60)

    # -----------------------------------------------------------
    # Resultado de la gráfica 1
    # -----------------------------------------------------------

    print(
        f"1. Error de sum ingenua con n=1e6: "
        f"{errs[-1]:.3e}"
    )

    # -----------------------------------------------------------
    # Resultado de la gráfica 2
    # -----------------------------------------------------------

    print(
        f"2. Error relativo de forma directa en x=1e-8: "
        f"{d[7]:.3e} | estable: {e[7]:.3e}"
    )

    # -----------------------------------------------------------
    # Resultado de la gráfica 3
    # -----------------------------------------------------------

    print(
        f"3. e^x con n=10: error rel. en x=1: "
        f"{abs(exp_taylor(1, 10) - math.exp(1)) / math.exp(1):.3e}, "
        f"en x=10: "
        f"{abs(exp_taylor(10, 10) - math.exp(10)) / math.exp(10):.3e}"
    )

    # -----------------------------------------------------------
    # Resultado de la gráfica 4
    # -----------------------------------------------------------

    print(
        f"4. sen(x) en x=40: "
        f"directo {directo[-1]:.3e} | "
        f"reducido {reducido[-1]:.3e}"
    )

    # -----------------------------------------------------------
    # Resultado de la gráfica 5
    # -----------------------------------------------------------

    print(
        "5. Terminos para tol 1e-10 en x=0.9: "
        + ", ".join(
            f"{k}={v[8]}"
            for k, v in res.items()
        )
    )

    # -----------------------------------------------------------
    # Resultado de la gráfica 6
    # -----------------------------------------------------------

    print("6. Tiempos (ns por llamada):")

    # Recorre cada operación y su tiempo.
    for k, v in t.items():

        # chr(10) representa el salto de línea.
        #
        # replace() lo cambia por un espacio para que
        # el nombre aparezca en una sola línea.
        print(
            f"     {k.replace(chr(10), ' '):<32} "
            f"{v:8.1f}"
        )

    # -----------------------------------------------------------
    # Sobrecosto de usar isinstance
    # -----------------------------------------------------------

    # Divide el tiempo de obtener_area() con validación
    # entre el tiempo de obtener_area() sin validación.
    #
    # Si el resultado fuera, por ejemplo, 1.20,
    # significaría que la versión con isinstance tarda
    # 1.20 veces lo que tarda la versión sin validar.
    sobrecosto = (
        t["obtener_area\n(con isinstance)"] /
        t["obtener_area\n(sin validar)"]
    )

    # Muestra el resultado del cálculo anterior.
    print(
        f"   Sobrecosto de validar con isinstance: "
        f"x{sobrecosto:.2f}"
    )

    # -----------------------------------------------------------
    # Nombres de las gráficas generadas
    # -----------------------------------------------------------

    print("\nGráficas guardadas:")

    print("grafica_1.png")
    print("grafica_2.png")
    print("grafica_3.png")
    print("grafica_4.png")
    print("grafica_5.png")
    print("grafica_6.png")


# ===============================================================
# OBSERVACIONES Y CONCLUSIONES
# ===============================================================

# Imprime el título de esta sección.
print("\nOBSERVACIONES Y CONCLUSIONES")
print("-" * 60)


# Conclusión 1:
# La suma repetida de 0.1 genera pequeñas diferencias
# debido a que 0.1 no puede representarse exactamente
# en el formato de punto flotante utilizado por Python.
print(
    "1. La suma repetida de 0.1 acumula error de redondeo debido "
    "a la representación de los números reales en punto flotante."
)


# Conclusión 2:
# Para valores pequeños de x, la resta:
#
# 1 - cos(x)
#
# puede involucrar dos valores muy cercanos.
#
# Esa resta puede perder precisión.
print(
    "2. La forma estable de calcular (1-cos(x))/x^2 presenta menor "
    "error para valores pequeños de x, evitando la cancelación "
    "catastrófica."
)


# Conclusión 3:
# Aumentar el número de términos de la serie de Taylor
# normalmente mejora la aproximación.
#
# Sin embargo, también aumenta el trabajo computacional.
print(
    "3. En la serie de Taylor de e^x, aumentar el numero de terminos "
    "mejora la aproximación, aunque esto aumenta el costo de calculo."
)


# Conclusión 4:
# Como el seno es una función periódica, se puede reducir
# el valor de x a un intervalo más pequeño antes de aplicar Taylor.
#
# De esta manera se necesitan menos términos.
print(
    "4. La reduccion de argumento permite aproximar sen(x) con menos "
    "terminos y mantener un error pequeño para valores grandes de x."
)


# Conclusión 5:
# Cada función y cada valor de x pueden necesitar
# una cantidad diferente de términos para llegar
# a la tolerancia especificada.
print(
    "5. El numero de terminos necesarios depende de la funcion y del "
    "valor de x. Para alcanzar una tolerancia pequeña se pueden "
    "necesitar cantidades diferentes de terminos."
)


# Conclusión 6:
# Las clases abstractas permiten establecer una estructura común
# y realizar comprobaciones sobre los objetos.
#
# Sin embargo, esas comprobaciones pueden añadir
# un pequeño costo de ejecución.
print(
    "6. Las clases abstractas permiten establecer una estructura comun "
    "y validar el tipo de objeto, pero estas comprobaciones pueden "
    "introducir un pequeño costo adicional de ejecucion."
)


# Conclusión general:
# Los resultados relacionan precisión numérica,
# cantidad de operaciones y costo computacional.
print(
    "En general, los resultados muestran que las tecnicas de calculo "
    "numerico y las decisiones de implementacion influyen tanto en "
    "la precision como en el costo computacional."
)


# ===============================================================
# INICIO DE LA EJECUCIÓN
# ===============================================================

# Esta condición comprueba si este archivo se está ejecutando
# directamente.
#
# Si es así, llama a la función main() y comienza todo el programa.
#
# Si este archivo se importa desde otro archivo, main()
# no se ejecuta automáticamente.
if __name__ == "__main__":
    main()