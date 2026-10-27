
# ================================================================
# CUERPO NEGRO: INTEGRACION NUMERICA DE ALTA PRECISION
# Metodos:
# 1. Integracion de Romberg
# 2. Cuadratura compuesta de Gauss-Legendre
# 3. Referencia mediante scipy.integrate.quad
#
# Genera unicamente cinco graficas:
# 1. Espectro de Planck
# 2. Convergencia de Romberg
# 3. Convergencia de Gauss-Legendre
# 4. Comparacion de errores
# 5. Validacion con Stefan-Boltzmann
# ================================================================

import argparse
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from numpy.polynomial.legendre import leggauss


# ================================================================
# 1. CONSTANTES FISICAS
# ================================================================

H = 6.62607015e-34
C = 299792458.0
K_B = 1.380649e-23
SIGMA = 5.670374419e-8

PI = np.pi
INTEGRAL_TEORICA = PI**4 / 15.0


# ================================================================
# 2. FUNCION ADIMENSIONAL DE PLANCK
# ================================================================

def funcion_planck_adimensional(x):
    """
    f(x) = x^3 / (exp(x) - 1)
    """

    x = np.asarray(x, dtype=float)
    resultado = np.zeros_like(x)

    mascara = x > 0.0
    xm = x[mascara]

    valores = np.zeros_like(xm)
    mascara_grande = xm < 700.0

    valores[mascara_grande] = (
        xm[mascara_grande]**3
        / np.expm1(xm[mascara_grande])
    )

    resultado[mascara] = valores

    if resultado.ndim == 0:
        return float(resultado)

    return resultado


# ================================================================
# 3. TRANSFORMACION DE LA INTEGRAL
# ================================================================

def transformar_limites(temperatura, lambda_min, lambda_max):
    """
    x = h*c / (lambda*k_B*T)
    """

    x_min = H * C / (lambda_max * K_B * temperatura)
    x_max = H * C / (lambda_min * K_B * temperatura)

    return x_min, x_max


def factor_fisico(temperatura):
    """
    Convierte la integral adimensional en flujo emisivo (W/m^2).
    """

    return (
        2.0 * PI * K_B**4 * temperatura**4
        / (H**3 * C**2)
    )


def potencia_espectral_lambda(longitud_onda, temperatura):
    """
    Ley espectral de Planck.

    Resultado en W/(m^2 m).
    """

    longitud_onda = np.asarray(longitud_onda, dtype=float)

    x = H * C / (longitud_onda * K_B * temperatura)

    resultado = np.zeros_like(longitud_onda)
    mascara = x < 700.0

    resultado[mascara] = (
        2.0 * PI * H * C**2
        / longitud_onda[mascara]**5
        / np.expm1(x[mascara])
    )

    return resultado


# ================================================================
# 4. INTEGRACION DE ROMBERG
# ================================================================

def romberg(funcion, a, b, tol_abs=1e-12,
            tol_rel=1e-11, niveles_max=20):

    if not a < b:
        raise ValueError("Se requiere que a sea menor que b.")

    tabla = []

    h = b - a
    r00 = 0.5 * h * (funcion(a) + funcion(b))

    tabla.append([r00])
    resultado_anterior = r00

    for nivel in range(1, niveles_max):

        numero_nuevos = 2**(nivel - 1)
        h = (b - a) / (2**nivel)

        puntos_nuevos = (
            a + (2 * np.arange(numero_nuevos) + 1) * h
        )

        suma_nuevos = np.sum(funcion(puntos_nuevos))

        trapecio = (
            0.5 * tabla[nivel - 1][0]
            + h * suma_nuevos
        )

        fila = [trapecio]

        for orden in range(1, nivel + 1):

            valor = fila[orden - 1] + (
                fila[orden - 1]
                - tabla[nivel - 1][orden - 1]
            ) / (4**orden - 1)

            fila.append(valor)

        tabla.append(fila)

        resultado = fila[-1]
        error = abs(resultado - resultado_anterior)

        tolerancia = tol_abs + tol_rel * abs(resultado)

        if error <= tolerancia:
            break

        resultado_anterior = resultado

    historial = np.array([fila[-1] for fila in tabla])

    return tabla[-1][-1], tabla, historial


# ================================================================
# 5. CUADRATURA COMPUESTA DE GAUSS-LEGENDRE
# ================================================================

def gauss_legendre(funcion, a, b, orden=16,
                   tol_abs=1e-12, tol_rel=1e-11,
                   max_subintervalos=16384):

    if not a < b:
        raise ValueError("Se requiere que a sea menor que b.")

    if orden < 1:
        raise ValueError("El orden de Gauss debe ser positivo.")

    nodos, pesos = leggauss(orden)

    subintervalos = 1
    estimaciones = []
    resultado_anterior = None

    while subintervalos <= max_subintervalos:

        bordes = np.linspace(a, b, subintervalos + 1)

        izquierda = bordes[:-1]
        derecha = bordes[1:]

        centros = 0.5 * (izquierda + derecha)
        semianchos = 0.5 * (derecha - izquierda)

        puntos = (
            centros[:, None]
            + semianchos[:, None] * nodos[None, :]
        )

        valores = funcion(puntos)

        integrales_locales = (
            semianchos
            * np.sum(valores * pesos[None, :], axis=1)
        )

        resultado = np.sum(integrales_locales)
        estimaciones.append(resultado)

        if resultado_anterior is not None:

            error = abs(resultado - resultado_anterior)
            tolerancia = tol_abs + tol_rel * abs(resultado)

            if error <= tolerancia:
                break

        resultado_anterior = resultado
        subintervalos *= 2

    historial = np.asarray(estimaciones)

    return historial[-1], historial, min(
        subintervalos // 2, max_subintervalos
    )


# ================================================================
# 6. REFERENCIA NUMERICA DE SCIPY
# ================================================================

def referencia_scipy(funcion, a, b):

    resultado, error = quad(
        funcion,
        a,
        b,
        epsabs=1e-13,
        epsrel=1e-13,
        limit=1000
    )

    return resultado, error


# ================================================================
# 7. FUNCIONES AUXILIARES
# ================================================================

def error_absoluto(valor, referencia):
    return abs(valor - referencia)


def error_relativo_porcentual(valor, referencia):

    if referencia == 0:
        return np.nan

    return 100.0 * abs(valor - referencia) / abs(referencia)


def crear_carpeta_graficas(carpeta):
    os.makedirs(carpeta, exist_ok=True)


def guardar_figura(nombre, carpeta, mostrar=False):

    ruta = os.path.join(carpeta, nombre)

    plt.tight_layout()
    plt.savefig(ruta, dpi=300, bbox_inches="tight")

    if mostrar:
        plt.show()

    plt.close()

    print(f"Grafica guardada: {ruta}")


# ================================================================
# 8. GRAFICA 1: ESPECTRO DE PLANCK
# ================================================================

def grafica_espectro(temperatura, lambda_min,
                     lambda_max, carpeta, mostrar=False):

    longitudes = np.linspace(lambda_min, lambda_max, 1500)

    espectro = potencia_espectral_lambda(
        longitudes, temperatura
    )

    # Convertir la densidad espectral por metro a densidad
    # espectral por micrometro.
    espectro_micrometro = espectro * 1e-6

    indice_maximo = np.argmax(espectro_micrometro)

    plt.figure(figsize=(10, 6))

    plt.plot(
        longitudes * 1e6,
        espectro_micrometro,
        linewidth=2.2,
        label="Ley de Planck"
    )

    plt.scatter(
        longitudes[indice_maximo] * 1e6,
        espectro_micrometro[indice_maximo],
        s=65,
        zorder=3,
        label="Maximo en el intervalo"
    )

    plt.annotate(
        f"{longitudes[indice_maximo] * 1e6:.3f} um",
        (
            longitudes[indice_maximo] * 1e6,
            espectro_micrometro[indice_maximo]
        ),
        xytext=(10, 12),
        textcoords="offset points"
    )

    plt.xlabel("Longitud de onda (micrometros)")
    plt.ylabel(r"Emision espectral (W m$^{-2}$ um$^{-1}$)")
    plt.title(f"Espectro de radiacion del cuerpo negro (T = {temperatura:g} K)")
    plt.grid(True, alpha=0.3)
    plt.legend()

    guardar_figura("01_espectro_planck.png", carpeta, mostrar)


# ================================================================
# 9. GRAFICA 2: CONVERGENCIA DE ROMBERG
# ================================================================

def grafica_romberg(historial, referencia, carpeta, mostrar=False):

    niveles = np.arange(1, len(historial) + 1)

    errores = np.abs(historial - referencia)
    errores = np.maximum(errores, np.finfo(float).tiny)

    fig, ejes = plt.subplots(2, 1, figsize=(10, 9))

    ejes[0].plot(
        niveles, historial,
        marker="o", linewidth=1.8,
        label="Romberg"
    )

    ejes[0].axhline(
        referencia, linestyle="--",
        label="Referencia SciPy"
    )

    ejes[0].set_xlabel("Nivel de Romberg")
    ejes[0].set_ylabel("Integral adimensional")
    ejes[0].set_title("Convergencia del resultado")
    ejes[0].grid(True, alpha=0.3)
    ejes[0].legend()

    ejes[1].semilogy(
        niveles, errores,
        marker="o", linewidth=1.8,
        label="Error absoluto"
    )

    ejes[1].set_xlabel("Nivel de Romberg")
    ejes[1].set_ylabel("Error absoluto frente a SciPy")
    ejes[1].set_title("Error numerico de Romberg")
    ejes[1].grid(True, which="both", alpha=0.3)
    ejes[1].legend()

    guardar_figura("02_convergencia_romberg.png", carpeta, mostrar)


# ================================================================
# 10. GRAFICA 3: CONVERGENCIA DE GAUSS-LEGENDRE
# ================================================================

def grafica_gauss(historial, referencia, orden,
                  carpeta, mostrar=False):

    subintervalos = 2**np.arange(len(historial))

    errores = np.abs(historial - referencia)
    errores = np.maximum(errores, np.finfo(float).tiny)

    fig, ejes = plt.subplots(2, 1, figsize=(10, 9))

    ejes[0].plot(
        subintervalos, historial,
        marker="s", linewidth=1.8,
        label="Gauss-Legendre"
    )

    ejes[0].axhline(
        referencia, linestyle="--",
        label="Referencia SciPy"
    )

    ejes[0].set_xscale("log", base=2)
    ejes[0].set_xlabel("Numero de subintervalos")
    ejes[0].set_ylabel("Integral adimensional")
    ejes[0].set_title(f"Convergencia de Gauss-Legendre (orden {orden})")
    ejes[0].grid(True, which="both", alpha=0.3)
    ejes[0].legend()

    ejes[1].loglog(
        subintervalos, errores,
        marker="s", linewidth=1.8,
        label="Error absoluto"
    )

    ejes[1].set_xlabel("Numero de subintervalos")
    ejes[1].set_ylabel("Error absoluto frente a SciPy")
    ejes[1].set_title("Error numerico de Gauss-Legendre")
    ejes[1].grid(True, which="both", alpha=0.3)
    ejes[1].legend()

    guardar_figura("03_convergencia_gauss.png", carpeta, mostrar)


# ================================================================
# 11. GRAFICA 4: COMPARACION DE ERRORES
# ================================================================

def grafica_comparacion_errores(historial_romberg,
                                historial_gauss,
                                referencia, orden_gauss,
                                carpeta, mostrar=False):
    """
    Compara el error frente al numero aproximado de evaluaciones
    de la funcion, una medida mas justa del esfuerzo numerico.

    Romberg usa aproximadamente 2^nivel + 1 evaluaciones.
    Gauss compuesto usa orden * numero de subintervalos.
    """

    niveles_r = np.arange(len(historial_romberg))
    evaluaciones_r = 2**niveles_r + 1

    subintervalos_g = 2**np.arange(len(historial_gauss))
    evaluaciones_g = orden_gauss * subintervalos_g

    error_r = np.abs(historial_romberg - referencia)
    error_g = np.abs(historial_gauss - referencia)

    error_r = np.maximum(error_r, np.finfo(float).tiny)
    error_g = np.maximum(error_g, np.finfo(float).tiny)

    plt.figure(figsize=(10, 6))

    plt.loglog(
        evaluaciones_r,
        error_r,
        marker="o",
        linewidth=1.8,
        label="Romberg"
    )

    plt.loglog(
        evaluaciones_g,
        error_g,
        marker="s",
        linewidth=1.8,
        label=f"Gauss-Legendre (orden {orden_gauss})"
    )

    plt.xlabel("Evaluaciones aproximadas de la funcion")
    plt.ylabel("Error absoluto respecto a SciPy")
    plt.title("Comparacion de precision y esfuerzo numerico")
    plt.grid(True, which="both", alpha=0.3)
    plt.legend()

    guardar_figura("04_comparacion_errores.png", carpeta, mostrar)


# ================================================================
# 12. GRAFICA 5: VALIDACION DE STEFAN-BOLTZMANN
# ================================================================

def grafica_stefan_boltzmann(temperatura, flujo_banda,
                             factor, carpeta, mostrar=False):
    """
    Compara:
    - Flujo integrado en la banda de longitudes de onda elegida.
    - Flujo total obtenido de la integral teorica de Planck.
    - Ley de Stefan-Boltzmann.

    La integral teorica completa es pi^4/15.
    """

    flujo_total_planck = factor * INTEGRAL_TEORICA
    flujo_stefan = SIGMA * temperatura**4

    nombres = [
        "Banda espectral",
        "Planck total teorico",
        "Stefan-Boltzmann"
    ]

    valores = [
        flujo_banda,
        flujo_total_planck,
        flujo_stefan
    ]

    plt.figure(figsize=(10, 6))

    barras = plt.bar(nombres, valores)

    plt.ylabel(r"Flujo emisivo (W/m$^2$)")
    plt.title("Validacion del modelo mediante Stefan-Boltzmann")
    plt.grid(axis="y", alpha=0.3)

    for barra, valor in zip(barras, valores):
        plt.annotate(
            f"{valor:.5e}",
            (
                barra.get_x() + barra.get_width() / 2,
                barra.get_height()
            ),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9
        )

    guardar_figura("05_stefan_boltzmann.png", carpeta, mostrar)


# ================================================================
# 13. TABLA DE ROMBERG
# ================================================================

def imprimir_tabla_romberg(tabla):

    print("\nTABLA DE ROMBERG")
    print("-" * 100)

    for i, fila in enumerate(tabla):
        valores = " | ".join(f"{v:.12e}" for v in fila)
        print(f"Nivel {i + 1:2d}: {valores}")

    print("-" * 100)


# ================================================================
# 14. PROGRAMA PRINCIPAL
# ================================================================

def main():

    parser = argparse.ArgumentParser(
        description=(
            "Integracion numerica de la radiacion de un cuerpo negro "
            "con Romberg y Gauss-Legendre."
        )
    )

    parser.add_argument(
        "--temperatura", type=float, default=1500.0
    )

    parser.add_argument(
        "--lambda-min", type=float, default=0.5
    )

    parser.add_argument(
        "--lambda-max", type=float, default=5.0
    )

    parser.add_argument(
        "--area", type=float, default=1.0
    )

    parser.add_argument(
        "--tiempo", type=float, default=1.0
    )

    parser.add_argument(
        "--tol-abs", type=float, default=1e-12
    )

    parser.add_argument(
        "--tol-rel", type=float, default=1e-11
    )

    parser.add_argument(
        "--niveles-romberg", type=int, default=20
    )

    parser.add_argument(
        "--orden-gauss", type=int, default=16
    )

    parser.add_argument(
        "--max-subintervalos", type=int, default=16384
    )

    parser.add_argument(
        "--carpeta", type=str, default="graficas_cuerpo_negro"
    )

    parser.add_argument(
        "--tabla", action="store_true"
    )

    parser.add_argument(
        "--mostrar", action="store_true"
    )

    args = parser.parse_args()

    # ------------------------------------------------------------
    # Validacion
    # ------------------------------------------------------------

    if not np.isfinite(args.temperatura) or args.temperatura <= 0:
        parser.error("La temperatura debe ser positiva y finita.")

    if (
        not np.isfinite(args.lambda_min)
        or not np.isfinite(args.lambda_max)
        or args.lambda_min <= 0
        or args.lambda_max <= args.lambda_min
    ):
        parser.error(
            "Las longitudes de onda deben ser positivas y "
            "lambda-max debe ser mayor que lambda-min."
        )

    if not np.isfinite(args.area) or args.area <= 0:
        parser.error("El area debe ser positiva y finita.")

    if not np.isfinite(args.tiempo) or args.tiempo <= 0:
        parser.error("El tiempo debe ser positivo y finito.")

    if (
        not np.isfinite(args.tol_abs)
        or not np.isfinite(args.tol_rel)
        or args.tol_abs <= 0
        or args.tol_rel <= 0
    ):
        parser.error("Las tolerancias deben ser positivas y finitas.")

    if args.niveles_romberg < 2:
        parser.error("Se requieren al menos dos niveles de Romberg.")

    if args.orden_gauss < 1:
        parser.error("El orden de Gauss debe ser positivo.")

    if args.max_subintervalos < 1:
        parser.error("El maximo de subintervalos debe ser positivo.")

    # ------------------------------------------------------------
    # Parametros fisicos y limites
    # ------------------------------------------------------------

    temperatura = args.temperatura

    lambda_min = args.lambda_min * 1e-6
    lambda_max = args.lambda_max * 1e-6

    x_min, x_max = transformar_limites(
        temperatura, lambda_min, lambda_max
    )

    factor = factor_fisico(temperatura)

    crear_carpeta_graficas(args.carpeta)

    print("\n" + "=" * 72)
    print("INTEGRACION NUMERICA DE LA RADIACION DE UN CUERPO NEGRO")
    print("=" * 72)

    print(f"Temperatura:             {temperatura:.6f} K")
    print(f"Longitud de onda minima: {args.lambda_min:.6f} um")
    print(f"Longitud de onda maxima: {args.lambda_max:.6f} um")
    print(f"Area emisora:            {args.area:.6f} m^2")
    print(f"Tiempo de emision:       {args.tiempo:.6f} s")
    print(f"Intervalo transformado:  [{x_min:.8e}, {x_max:.8e}]")

    # ------------------------------------------------------------
    # Romberg
    # ------------------------------------------------------------

    resultado_romberg, tabla, historial_romberg = romberg(
        funcion_planck_adimensional,
        x_min,
        x_max,
        tol_abs=args.tol_abs,
        tol_rel=args.tol_rel,
        niveles_max=args.niveles_romberg
    )

    # ------------------------------------------------------------
    # Gauss-Legendre
    # ------------------------------------------------------------

    resultado_gauss, historial_gauss, subintervalos_finales = (
        gauss_legendre(
            funcion_planck_adimensional,
            x_min,
            x_max,
            orden=args.orden_gauss,
            tol_abs=args.tol_abs,
            tol_rel=args.tol_rel,
            max_subintervalos=args.max_subintervalos
        )
    )

    # ------------------------------------------------------------
    # Referencia SciPy
    # ------------------------------------------------------------

    resultado_scipy, error_scipy = referencia_scipy(
        funcion_planck_adimensional,
        x_min,
        x_max
    )

    # ------------------------------------------------------------
    # Resultados fisicos
    # ------------------------------------------------------------

    flujo_romberg = factor * resultado_romberg
    flujo_gauss = factor * resultado_gauss
    flujo_scipy = factor * resultado_scipy

    potencia_romberg = flujo_romberg * args.area
    potencia_gauss = flujo_gauss * args.area
    potencia_scipy = flujo_scipy * args.area

    energia_romberg = potencia_romberg * args.tiempo
    energia_gauss = potencia_gauss * args.tiempo
    energia_scipy = potencia_scipy * args.tiempo

    print("\nRESULTADOS DE LAS INTEGRALES")
    print("-" * 72)
    print(f"Romberg:          {resultado_romberg:.14e}")
    print(f"Gauss-Legendre:   {resultado_gauss:.14e}")
    print(f"Referencia SciPy: {resultado_scipy:.14e}")
    print(f"Error estimado de SciPy: {error_scipy:.6e}")

    print("\nFLUJO EMISIVO EN LA BANDA")
    print("-" * 72)
    print(f"Romberg:          {flujo_romberg:.12e} W/m^2")
    print(f"Gauss-Legendre:   {flujo_gauss:.12e} W/m^2")
    print(f"Referencia SciPy: {flujo_scipy:.12e} W/m^2")

    print("\nPOTENCIA EMITIDA")
    print("-" * 72)
    print(f"Romberg:          {potencia_romberg:.12e} W")
    print(f"Gauss-Legendre:   {potencia_gauss:.12e} W")
    print(f"Referencia SciPy: {potencia_scipy:.12e} W")

    print("\nENERGIA EMITIDA")
    print("-" * 72)
    print(f"Romberg:          {energia_romberg:.12e} J")
    print(f"Gauss-Legendre:   {energia_gauss:.12e} J")
    print(f"Referencia SciPy: {energia_scipy:.12e} J")

    print("\nERRORES RESPECTO A SCIPY")
    print("-" * 72)
    print(
        "Error absoluto Romberg: ",
        f"{error_absoluto(resultado_romberg, resultado_scipy):.6e}"
    )
    print(
        "Error absoluto Gauss:   ",
        f"{error_absoluto(resultado_gauss, resultado_scipy):.6e}"
    )
    print(
        "Error relativo Romberg: ",
        f"{error_relativo_porcentual(resultado_romberg, resultado_scipy):.6e} %"
    )
    print(
        "Error relativo Gauss:   ",
        f"{error_relativo_porcentual(resultado_gauss, resultado_scipy):.6e} %"
    )

    # ------------------------------------------------------------
    # Validacion de Stefan-Boltzmann
    # ------------------------------------------------------------

    flujo_total_planck = factor * INTEGRAL_TEORICA
    flujo_stefan = SIGMA * temperatura**4

    fraccion_banda = flujo_scipy / flujo_stefan

    print("\nVALIDACION DE STEFAN-BOLTZMANN")
    print("-" * 72)
    print(f"Flujo en la banda:       {flujo_scipy:.12e} W/m^2")
    print(f"Flujo total de Planck:   {flujo_total_planck:.12e} W/m^2")
    print(f"Flujo de Stefan:         {flujo_stefan:.12e} W/m^2")
    print(f"Fraccion en la banda:    {100.0 * fraccion_banda:.8f} %")
    print(
        "Diferencia relativa entre las leyes: "
        f"{error_relativo_porcentual(flujo_total_planck, flujo_stefan):.6e} %"
    )

    if args.tabla:
        imprimir_tabla_romberg(tabla)

    # ------------------------------------------------------------
    # SOLO LAS CINCO GRAFICAS SELECCIONADAS
    # ------------------------------------------------------------

    print("\nGENERANDO LAS CINCO GRAFICAS...")
    print("-" * 72)

    grafica_espectro(
        temperatura,
        lambda_min,
        lambda_max,
        args.carpeta,
        args.mostrar
    )

    grafica_romberg(
        historial_romberg,
        resultado_scipy,
        args.carpeta,
        args.mostrar
    )

    grafica_gauss(
        historial_gauss,
        resultado_scipy,
        args.orden_gauss,
        args.carpeta,
        args.mostrar
    )

    grafica_comparacion_errores(
        historial_romberg,
        historial_gauss,
        resultado_scipy,
        args.orden_gauss,
        args.carpeta,
        args.mostrar
    )

    grafica_stefan_boltzmann(
        temperatura,
        flujo_scipy,
        factor,
        args.carpeta,
        args.mostrar
    )

    print("\nProceso finalizado.")
    print(f"Las cinco graficas estan en: {os.path.abspath(args.carpeta)}")


# ================================================================
# 15. EJECUCION
# ================================================================

if __name__ == "__main__":
    main()
