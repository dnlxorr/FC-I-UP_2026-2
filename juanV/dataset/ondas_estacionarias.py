
"""
PROYECTO DE FISICA COMPUTACIONAL

Titulo:
Analisis comparativo de los metodos de integracion numerica
de Romberg y Gauss-Legendre para calcular la energia de una
onda estacionaria en una cuerda.

Bibliotecas necesarias:
    pip install numpy scipy matplotlib

Modelo fisico:
    y(x,t) = A sen(k*x) cos(omega*t)

    k = n*pi/L
    v = sqrt(T/mu)
    omega = k*v

Densidad lineal de energia:
    u(x,t) = 1/2*mu*(dy/dt)^2 + 1/2*T*(dy/dx)^2

Energia total:
    E(t) = integral desde 0 hasta L de u(x,t) dx

Solucion analitica:
    E_exacta = T*A^2*k^2*L/4
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.special import roots_legendre


# ============================================================
# 1. PARAMETROS FISICOS Y MODELO DE LA ONDA
# ============================================================

def calcular_parametros(A, L, mu, T, n):
    """
    Calcula los parametros principales de la onda.

    A  : amplitud (m)
    L  : longitud de la cuerda (m)
    mu : densidad lineal de masa (kg/m)
    T  : tension de la cuerda (N)
    n  : numero del modo de vibracion
    """

    if A <= 0 or L <= 0 or mu <= 0 or T <= 0 or n < 1:
        raise ValueError(
            "A, L, mu y T deben ser positivos, y n debe ser >= 1."
        )

    k = n * np.pi / L
    v = np.sqrt(T / mu)
    omega = k * v
    frecuencia = omega / (2 * np.pi)
    periodo = 1 / frecuencia

    return k, v, omega, frecuencia, periodo


def desplazamiento(x, t, A, k, omega):
    """
    Calcula el desplazamiento transversal de la cuerda.

    y(x,t) = A sen(k*x) cos(omega*t)
    """
    return A * np.sin(k * x) * np.cos(omega * t)


def velocidad_transversal(x, t, A, k, omega):
    """
    Derivada del desplazamiento respecto al tiempo.

    dy/dt = -A*omega*sen(k*x)*sen(omega*t)
    """
    return -A * omega * np.sin(k * x) * np.sin(omega * t)


def pendiente_cuerda(x, t, A, k, omega):
    """
    Derivada del desplazamiento respecto a la posicion.

    dy/dx = A*k*cos(k*x)*cos(omega*t)
    """
    return A * k * np.cos(k * x) * np.cos(omega * t)


# ============================================================
# 2. DENSIDAD DE ENERGIA
# ============================================================

def energia_cinetica_lineal(x, t, A, mu, k, omega):
    """
    Energia cinetica por unidad de longitud.

    Ec_lineal = 1/2*mu*(dy/dt)^2

    Unidad: J/m
    """
    vy = velocidad_transversal(x, t, A, k, omega)
    return 0.5 * mu * vy**2


def energia_potencial_lineal(x, t, A, T, k, omega):
    """
    Energia potencial elastica por unidad de longitud.

    Ep_lineal = 1/2*T*(dy/dx)^2

    Unidad: J/m
    """
    pendiente = pendiente_cuerda(x, t, A, k, omega)
    return 0.5 * T * pendiente**2


def densidad_energia(x, t, A, mu, T, k, omega):
    """
    Densidad lineal de energia mecanica total.

    u(x,t) = Ec_lineal + Ep_lineal

    Unidad: J/m
    """
    ec = energia_cinetica_lineal(
        x, t, A, mu, k, omega
    )

    ep = energia_potencial_lineal(
        x, t, A, T, k, omega
    )

    return ec + ep


# ============================================================
# 3. SOLUCION ANALITICA DE LA ENERGIA TOTAL
# ============================================================

def energia_analitica(A, T, k, L):
    """
    Energia mecanica total exacta de la cuerda ideal.

    E = T*A^2*k^2*L/4

    Esta energia es constante en el tiempo para el modelo ideal.
    """
    return T * A**2 * k**2 * L / 4


# ============================================================
# 4. METODO DE INTEGRACION DE ROMBERG
# ============================================================

def romberg(funcion, a, b, niveles=6):
    """
    Calcula una integral definida utilizando Romberg.

    a, b   : limites de integracion.
    niveles: numero de filas de la tabla de Romberg.

    Retorna:
        integral aproximada,
        numero de evaluaciones de la funcion,
        tabla de Romberg.
    """

    if b <= a:
        raise ValueError("El limite b debe ser mayor que a.")

    if niveles < 1:
        raise ValueError("Los niveles deben ser >= 1.")

    tabla = np.zeros((niveles, niveles))

    # Primera aproximacion: regla del trapecio.
    fa = funcion(a)
    fb = funcion(b)

    evaluaciones = 2

    tabla[0, 0] = (b - a) * (fa + fb) / 2

    # Refinamiento de la regla del trapecio.
    for i in range(1, niveles):

        numero_nuevos = 2**(i - 1)
        paso = (b - a) / (2**i)

        suma = 0.0

        # Solo se calculan los puntos nuevos.
        for j in range(numero_nuevos):

            x = a + (2*j + 1) * paso
            suma += funcion(x)

        evaluaciones += numero_nuevos

        tabla[i, 0] = (
            0.5 * tabla[i - 1, 0]
            + paso * suma
        )

        # Extrapolacion de Richardson.
        for j in range(1, i + 1):

            tabla[i, j] = (
                tabla[i, j - 1]
                + (
                    tabla[i, j - 1]
                    - tabla[i - 1, j - 1]
                ) / (4**j - 1)
            )

    aproximacion = tabla[niveles - 1, niveles - 1]

    return aproximacion, evaluaciones, tabla


# ============================================================
# 5. CUADRATURA DE GAUSS-LEGENDRE
# ============================================================

def gauss_legendre(
    funcion,
    a,
    b,
    puntos=4,
    subintervalos=1
):
    """
    Calcula una integral con cuadratura de Gauss-Legendre.

    puntos:
        Numero de nodos de Gauss por subintervalo.

    subintervalos:
        Numero de partes en que se divide el intervalo.

    Retorna:
        integral aproximada y numero de evaluaciones.
    """

    if b <= a:
        raise ValueError("El limite b debe ser mayor que a.")

    if puntos < 1 or subintervalos < 1:
        raise ValueError(
            "puntos y subintervalos deben ser >= 1."
        )

    # Nodos y pesos en el intervalo [-1, 1].
    nodos, pesos = roots_legendre(puntos)

    # Division del intervalo original.
    bordes = np.linspace(a, b, subintervalos + 1)

    integral = 0.0

    for i in range(subintervalos):

        izquierda = bordes[i]
        derecha = bordes[i + 1]

        # Transformacion de [-1,1] al subintervalo.
        x = (
            0.5 * (derecha - izquierda) * nodos
            + 0.5 * (derecha + izquierda)
        )

        valores = np.array([
            funcion(float(xi)) for xi in x
        ])

        integral += (
            0.5
            * (derecha - izquierda)
            * np.dot(pesos, valores)
        )

    evaluaciones = puntos * subintervalos

    return integral, evaluaciones


# ============================================================
# 6. CALCULO DE ERRORES
# ============================================================

def error_absoluto(exacto, aproximado):
    """Diferencia absoluta entre la referencia y el resultado."""
    return abs(exacto - aproximado)


def error_relativo_porcentual(exacto, aproximado):
    """Error relativo expresado como porcentaje."""

    if np.isclose(exacto, 0.0):
        return np.nan

    return abs(exacto - aproximado) / abs(exacto) * 100


# ============================================================
# 7. MEDICION DEL TIEMPO DE EJECUCION
# ============================================================

def medir_tiempo(funcion_calculo, repeticiones=30):
    """
    Calcula el tiempo promedio de ejecucion.

    Se repite el calculo para reducir el efecto de variaciones
    muy pequenas en los tiempos medidos.
    """

    inicio = time.perf_counter()

    for _ in range(repeticiones):
        funcion_calculo()

    fin = time.perf_counter()

    return (fin - inicio) / repeticiones


# ============================================================
# 8. PRESENTACION DE RESULTADOS
# ============================================================

def imprimir_resultado(
    nombre,
    aproximacion,
    exacto,
    evaluaciones,
    tiempo
):

    print("\n" + "=" * 65)
    print(nombre)
    print("=" * 65)

    print(f"Resultado numerico:       {aproximacion:.14e} J")
    print(f"Resultado analitico:      {exacto:.14e} J")

    print(
        f"Error absoluto:           "
        f"{error_absoluto(exacto, aproximacion):.6e} J"
    )

    print(
        f"Error relativo:           "
        f"{error_relativo_porcentual(exacto, aproximacion):.6e} %"
    )

    print(f"Evaluaciones:             {evaluaciones}")
    print(f"Tiempo promedio:          {tiempo:.6e} segundos")


# ============================================================
# 9. PROGRAMA PRINCIPAL
# ============================================================

def main():

    # --------------------------------------------------------
    # PARAMETROS FISICOS
    # Puedes cambiar estos valores para realizar experimentos.
    # --------------------------------------------------------

    A = 0.020       # Amplitud en metros
    L = 1.20        # Longitud de la cuerda en metros
    mu = 0.010      # Densidad lineal en kg/m
    T = 50.0        # Tension en newtons
    n = 3           # Modo de vibracion
    t = 0.035       # Tiempo en segundos

    # --------------------------------------------------------
    # LIMITES DE INTEGRACION
    # --------------------------------------------------------

    a = 0.0
    b = L

    # --------------------------------------------------------
    # CONFIGURACION NUMERICA
    # --------------------------------------------------------

    niveles_romberg = 7

    puntos_gauss = 4
    subintervalos_gauss = 3

    # --------------------------------------------------------
    # CALCULO DE PARAMETROS
    # --------------------------------------------------------

    k, v, omega, frecuencia, periodo = calcular_parametros(
        A, L, mu, T, n
    )

    # Solucion analitica de referencia.
    E_exacto = energia_analitica(A, T, k, L)

    # Funcion que integraremos en el intervalo [0,L].
    funcion = lambda x: densidad_energia(
        x, t, A, mu, T, k, omega
    )

    # --------------------------------------------------------
    # INTEGRACION POR ROMBERG
    # --------------------------------------------------------

    E_romberg, eval_romberg, tabla = romberg(
        funcion,
        a,
        b,
        niveles_romberg
    )

    # --------------------------------------------------------
    # INTEGRACION POR GAUSS-LEGENDRE
    # --------------------------------------------------------

    E_gauss, eval_gauss = gauss_legendre(
        funcion,
        a,
        b,
        puntos_gauss,
        subintervalos_gauss
    )

    # --------------------------------------------------------
    # TIEMPOS DE EJECUCION
    # --------------------------------------------------------

    tiempo_romberg = medir_tiempo(
        lambda: romberg(
            funcion, a, b, niveles_romberg
        )
    )

    tiempo_gauss = medir_tiempo(
        lambda: gauss_legendre(
            funcion,
            a,
            b,
            puntos_gauss,
            subintervalos_gauss
        )
    )

    # --------------------------------------------------------
    # INFORMACION DEL SISTEMA FISICO
    # --------------------------------------------------------

    print("\n")
    print("#" * 70)
    print("ONDAS ESTACIONARIAS: ROMBERG VS GAUSS-LEGENDRE")
    print("#" * 70)

    print("\nPARAMETROS FISICOS")
    print("-" * 65)

    print(f"Amplitud A:               {A:.6f} m")
    print(f"Longitud L:               {L:.6f} m")
    print(f"Densidad lineal mu:       {mu:.6f} kg/m")
    print(f"Tension T:                {T:.6f} N")
    print(f"Modo de vibracion n:      {n}")
    print(f"Numero de onda k:         {k:.8f} rad/m")
    print(f"Rapidez de onda v:        {v:.8f} m/s")
    print(f"Frecuencia:               {frecuencia:.8f} Hz")
    print(f"Periodo:                  {periodo:.8f} s")
    print(f"Tiempo analizado:         {t:.6f} s")
    print(f"Intervalo de integracion: [{a:.2f}, {b:.2f}] m")
    print(f"Energia analitica:        {E_exacto:.14e} J")

    # Mostrar resultados de ambos metodos.
    imprimir_resultado(
        "METODO DE ROMBERG",
        E_romberg,
        E_exacto,
        eval_romberg,
        tiempo_romberg
    )

    imprimir_resultado(
        "CUADRATURA DE GAUSS-LEGENDRE",
        E_gauss,
        E_exacto,
        eval_gauss,
        tiempo_gauss
    )

    # --------------------------------------------------------
    # TABLA DE ROMBERG
    # --------------------------------------------------------

    print("\nTABLA DE ROMBERG")
    print("-" * 65)

    for i in range(niveles_romberg):

        fila = []

        for j in range(i + 1):
            fila.append(f"{tabla[i, j]:.10e}")

        print("   ".join(fila))

    # ========================================================
    # 10. ANALISIS DE CONVERGENCIA DE ROMBERG
    # ========================================================

    niveles = list(range(1, 9))

    errores_romberg = []
    evaluaciones_romberg = []

    for nivel in niveles:

        resultado, numero_eval, _ = romberg(
            funcion, a, b, nivel
        )

        err = error_absoluto(E_exacto, resultado)

        # Evitar log(0) en las graficas.
        errores_romberg.append(max(err, 1e-30))

        evaluaciones_romberg.append(numero_eval)

    # ========================================================
    # 11. ANALISIS DE CONVERGENCIA DE GAUSS
    # ========================================================

    ordenes_gauss = [1, 2, 3, 4, 5, 6, 8, 10, 12]

    errores_gauss = []
    evaluaciones_gauss = []

    for orden in ordenes_gauss:

        resultado, numero_eval = gauss_legendre(
            funcion,
            a,
            b,
            puntos=orden,
            subintervalos=1
        )

        err = error_absoluto(E_exacto, resultado)

        errores_gauss.append(max(err, 1e-30))
        evaluaciones_gauss.append(numero_eval)

    # ========================================================
    # 12. DATOS PARA LAS GRAFICAS FISICAS
    # ========================================================

    x = np.linspace(0, L, 1000)

    y = desplazamiento(x, t, A, k, omega)

    ec = energia_cinetica_lineal(
        x, t, A, mu, k, omega
    )

    ep = energia_potencial_lineal(
        x, t, A, T, k, omega
    )

    u = ec + ep

    # ========================================================
    # 13. GRAFICAS
    # ========================================================

    fig, ejes = plt.subplots(
        2, 2,
        figsize=(14, 10)
    )

    # Grafica 1: forma de la cuerda.
    ejes[0, 0].plot(x, y, linewidth=2)

    ejes[0, 0].set_title(
        "1. Forma de la cuerda en un instante"
    )

    ejes[0, 0].set_xlabel("Posicion x (m)")
    ejes[0, 0].set_ylabel("Desplazamiento y (m)")
    ejes[0, 0].grid(True)

    # Grafica 2: distribucion de energia.
    ejes[0, 1].plot(
        x, ec,
        label="Energia cinetica por longitud"
    )

    ejes[0, 1].plot(
        x, ep,
        label="Energia potencial por longitud"
    )

    ejes[0, 1].plot(
        x, u,
        label="Energia total por longitud",
        linewidth=2
    )

    ejes[0, 1].set_title(
        "2. Densidad de energia a lo largo de la cuerda"
    )

    ejes[0, 1].set_xlabel("Posicion x (m)")
    ejes[0, 1].set_ylabel("Densidad de energia (J/m)")
    ejes[0, 1].legend()
    ejes[0, 1].grid(True)

    # Grafica 3: error frente al refinamiento.
    ejes[1, 0].semilogy(
        niveles,
        errores_romberg,
        "o-",
        label="Romberg"
    )

    ejes[1, 0].semilogy(
        ordenes_gauss,
        errores_gauss,
        "s-",
        label="Gauss-Legendre"
    )

    ejes[1, 0].set_title(
        "3. Convergencia del error absoluto"
    )

    ejes[1, 0].set_xlabel(
        "Nivel de Romberg / orden de Gauss"
    )

    ejes[1, 0].set_ylabel("Error absoluto (J)")
    ejes[1, 0].legend()
    ejes[1, 0].grid(True, which="both")

    # Grafica 4: error frente al numero de evaluaciones.
    ejes[1, 1].loglog(
        evaluaciones_romberg,
        errores_romberg,
        "o-",
        label="Romberg"
    )

    ejes[1, 1].loglog(
        evaluaciones_gauss,
        errores_gauss,
        "s-",
        label="Gauss-Legendre"
    )

    ejes[1, 1].set_title(
        "4. Error frente al costo de evaluacion"
    )

    ejes[1, 1].set_xlabel(
        "Numero de evaluaciones de la funcion"
    )

    ejes[1, 1].set_ylabel("Error absoluto (J)")
    ejes[1, 1].legend()
    ejes[1, 1].grid(True, which="both")

    fig.suptitle(
        "Integracion numerica de la energia de una onda estacionaria",
        fontsize=15
    )

    plt.tight_layout()

    # Guardar las graficas como imagen.
    plt.savefig(
        "resultados_ondas_estacionarias.png",
        dpi=180,
        bbox_inches="tight"
    )

    print(
        "\nSe guardaron las graficas en "
        "'resultados_ondas_estacionarias.png'."
    )

    plt.show()


# ============================================================
# 14. EJECUCION DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    main()
