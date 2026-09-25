# ============================================================
#       LEY DE ENFRIAMIENTO DE NEWTON
# ============================================================
#
# Objetivo:
# Simular cómo cambia la temperatura de un cuerpo cuando
# está expuesto a un ambiente que mantiene una temperatura
# constante.
#
# Modelo iterativo utilizado:
#
# ΔT = -r (T - Tamb) Δt
#
# T_nueva = T + ΔT
#
# Donde:
# T     = temperatura actual del cuerpo [°C]
# Tamb  = temperatura ambiental [°C]
# r     = constante de enfriamiento [1/unidad de tiempo]
# Δt    = paso de tiempo
#
# Criterio de equilibrio térmico:
#
# |T - Tamb| < 0.1 °C
#
# ============================================================


# ------------------------------------------------------------
# FUNCIÓN PARA SOLICITAR UN NÚMERO POSITIVO
# ------------------------------------------------------------
def pedir_positivo(mensaje):
    """
    Solicita al usuario un número positivo.

    Parámetros:
        mensaje: texto que se mostrará en la consola.

    Retorna:
        Un número de tipo float mayor que cero.
    """

    while True:

        try:
            valor = float(input(mensaje))

            # Verificamos que el valor sea mayor que cero
            if valor > 0:
                return valor

            else:
                print("Error: el valor debe ser mayor que cero.")

        except ValueError:
            print("Error: debe ingresar un número válido.")


# ------------------------------------------------------------
# FUNCIÓN PARA SOLICITAR UNA TEMPERATURA
# ------------------------------------------------------------
def pedir_temperatura(mensaje):
    """
    Solicita una temperatura al usuario.

    Las temperaturas pueden ser positivas o negativas,
    por lo tanto no exigimos que sean mayores que cero.

    Retorna:
        Temperatura en grados Celsius.
    """

    while True:

        try:
            temperatura = float(input(mensaje))
            return temperatura

        except ValueError:
            print("Error: debe ingresar una temperatura válida.")


# ------------------------------------------------------------
# FUNCIÓN DE SIMULACIÓN
# ------------------------------------------------------------
def simular_enfriamiento(T0, Tamb, r, delta_t, N):
    """
    Realiza la simulación de la Ley de Enfriamiento de Newton.

    Parámetros:
        T0      : temperatura inicial del cuerpo [°C]
        Tamb    : temperatura ambiental [°C]
        r       : constante de enfriamiento
        delta_t : paso de tiempo
        N       : número de pasos

    Retorna:
        tiempos       : lista con los tiempos de simulación
        temperaturas  : lista con las temperaturas calculadas
    """

    # Creamos las listas donde guardaremos los resultados
    tiempos = []
    temperaturas = []

    # Inicializamos el tiempo y la temperatura
    tiempo = 0
    temperatura = T0

    # Guardamos el estado inicial
    tiempos.append(tiempo)
    temperaturas.append(temperatura)

    # Variable para saber si ya encontramos el equilibrio
    equilibrio_encontrado = False

    # --------------------------------------------------------
    # CICLO PRINCIPAL DE LA SIMULACIÓN
    # --------------------------------------------------------
    for paso in range(1, N + 1):

        # ----------------------------------------------------
        # Calculamos el cambio de temperatura:
        #
        # ΔT = -r (T - Tamb) Δt
        # ----------------------------------------------------
        delta_T = -r * (temperatura - Tamb) * delta_t

        # Actualizamos la temperatura
        temperatura = temperatura + delta_T

        # Actualizamos el tiempo
        tiempo = tiempo + delta_t

        # Guardamos los nuevos valores en las listas
        tiempos.append(tiempo)
        temperaturas.append(temperatura)

        # ----------------------------------------------------
        # CALCULAMOS LA DIFERENCIA CON EL AMBIENTE
        # ----------------------------------------------------
        diferencia = abs(temperatura - Tamb)

        # ----------------------------------------------------
        # DETECCIÓN DEL EQUILIBRIO TÉRMICO
        # ----------------------------------------------------
        if diferencia < 0.1 and not equilibrio_encontrado:

            print("\n*** EQUILIBRIO TÉRMICO ALCANZADO ***")
            print(f"Tiempo aproximado: {tiempo:.2f}")
            print(f"Temperatura del cuerpo: {temperatura:.2f} °C")
            print(f"Temperatura ambiente: {Tamb:.2f} °C")
            print(f"Diferencia: {diferencia:.4f} °C")

            equilibrio_encontrado = True

    return tiempos, temperaturas


# ------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ------------------------------------------------------------

print("=" * 60)
print("        LEY DE ENFRIAMIENTO DE NEWTON")
print("=" * 60)



# ------------------------------------------------------------
# SOLICITAR DATOS AL USUARIO
# ------------------------------------------------------------

T0 = pedir_temperatura(
    "Ingrese la temperatura inicial del cuerpo T0 [°C]: "
)

Tamb = pedir_temperatura(
    "Ingrese la temperatura ambiental Tamb [°C]: "
)

r = pedir_positivo(
    "Ingrese la constante de enfriamiento r: "
)

delta_t = pedir_positivo(
    "Ingrese el paso de tiempo Δt: "
)

N = int(pedir_positivo(
    "Ingrese el número de pasos N: "
))


# ------------------------------------------------------------
# VALIDACIÓN FÍSICA
# ------------------------------------------------------------

if T0 == Tamb:

    print("\nEl cuerpo ya se encuentra a la temperatura ambiente.")
    print("No existe diferencia de temperatura inicial.")

else:

    print("\nLos datos ingresados son físicamente válidos.")
    print("Se iniciará la simulación...")


# ------------------------------------------------------------
# EJECUTAMOS LA SIMULACIÓN
# ------------------------------------------------------------

tiempos, temperaturas = simular_enfriamiento(
    T0,
    Tamb,
    r,
    delta_t,
    N
)


# ------------------------------------------------------------
# MOSTRAR RESULTADOS
# ------------------------------------------------------------

print("\n" + "=" * 60)
print("                 RESULTADOS")
print("=" * 60)

print("\nTiempo        Temperatura")
print("(unidades)       (°C)")
print("-" * 30)


# Mostramos los resultados almacenados en las listas
for i in range(len(tiempos)):

    print(
        f"{tiempos[i]:8.2f}       "
        f"{temperaturas[i]:10.2f}"
    )


# ------------------------------------------------------------
# ANÁLISIS FINAL
# ------------------------------------------------------------

temperatura_final = temperaturas[-1]
diferencia_final = abs(temperatura_final - Tamb)

print("\n" + "=" * 60)
print("              ANÁLISIS FINAL")
print("=" * 60)

print(f"Temperatura inicial : {T0:.2f} °C")
print(f"Temperatura ambiente: {Tamb:.2f} °C")
print(f"Temperatura final   : {temperatura_final:.2f} °C")
print(f"Diferencia final    : {diferencia_final:.4f} °C")


# ------------------------------------------------------------
# CONDICIÓN FINAL DE EQUILIBRIO
# ------------------------------------------------------------

if diferencia_final < 0.1:

    print("\nEl cuerpo se encuentra en equilibrio térmico")
    print("según el criterio establecido: |T - Tamb| < 0.1 °C.")

else:

    print("\nEl cuerpo todavía NO alcanza el equilibrio térmico")
    print("dentro del número de pasos seleccionado.")

print("\nSimulación finalizada.")