# ============================================================
#          LEY DE ENFRIAMIENTO DE NEWTON
# ============================================================

def pedir_temperatura(mensaje):

    while True:
        try:
            temperatura = float(input(mensaje))
            return temperatura

        except ValueError:
            print("Error: debe ingresar una temperatura válida.")


# ============================================================
# FUNCIÓN PARA PEDIR r
# Restricción: 0 < r < 1
# ============================================================

def pedir_r():

    while True:
        try:
            r = float(
                input(
                    "Ingrese la constante de enfriamiento r "
                    "(0 < r < 1): "
                )
            )

            if r > 0 and r < 1:
                return r

            else:
                print("Error: r debe ser mayor que 0 y menor que 1.")

        except ValueError:
            print("Error: debe ingresar un número válido.")


# ============================================================
# FUNCIÓN PARA PEDIR Δt
# Restricciones:
# Δt > 0
# r * Δt < 1
# ============================================================

def pedir_delta_t(r):

    while True:
        try:
            delta_t = float(
                input(
                    "Ingrese el paso de tiempo Δt "
                    "(mayor que 0): "
                )
            )

            if delta_t <= 0:
                print("Error: Δt debe ser mayor que 0.")
                continue

            # Verificación de estabilidad numérica
            if r * delta_t >= 1:

                print("\nError de estabilidad numérica.")
                print(f"r * Δt = {r * delta_t:.4f}")
                print("Debe cumplirse: r * Δt < 1")
                print("Ingrese un Δt más pequeño.")

                continue

            return delta_t

        except ValueError:
            print("Error: debe ingresar un número válido.")


# ============================================================
# FUNCIÓN PARA PEDIR N
# Restricción: N >= 100
# ============================================================

def pedir_N():

    while True:
        try:
            N = int(
                input(
                    "Ingrese el número de pasos N "
                    "(N >= 100): "
                )
            )

            if N >= 100:
                return N

            else:
                print("Error: N debe ser mayor o igual que 100.")

        except ValueError:
            print("Error: debe ingresar un número entero.")


# ============================================================
# FUNCIÓN DE SIMULACIÓN
# ============================================================

def simular_enfriamiento(T0, Tamb, r, delta_t, N):

    tiempos = []
    temperaturas = []

    # Condiciones iniciales
    tiempo = 0
    temperatura = T0

    # Guardamos el estado inicial
    tiempos.append(tiempo)
    temperaturas.append(temperatura)

    equilibrio_encontrado = False

    # ========================================================
    # BUCLE DE SIMULACIÓN
    # ========================================================

    for paso in range(1, N + 1):

        # Modelo iterativo:
        #
        # ΔT = -r(T - Tamb)Δt

        delta_T = -r * (temperatura - Tamb) * delta_t

        # Actualizamos la temperatura
        temperatura = temperatura + delta_T

        # Actualizamos el tiempo
        tiempo = tiempo + delta_t

        # Guardamos los resultados
        tiempos.append(tiempo)
        temperaturas.append(temperatura)

        # Diferencia con la temperatura ambiente
        diferencia = abs(temperatura - Tamb)

        # Verificación del equilibrio térmico
        if diferencia < 0.1 and not equilibrio_encontrado:

            print("\n*** EQUILIBRIO TÉRMICO ALCANZADO ***")

            print(f"Tiempo aproximado: {tiempo:.2f}")
            print(f"Temperatura del cuerpo: {temperatura:.2f} °C")
            print(f"Temperatura ambiente: {Tamb:.2f} °C")
            print(f"Diferencia: {diferencia:.4f} °C")

            equilibrio_encontrado = True

    return tiempos, temperaturas


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print("=" * 60)
print("           LEY DE ENFRIAMIENTO DE NEWTON")
print("=" * 60)

print(
    "\nSimulación mediante el método iterativo de Euler."
)

print(
    "Condición de estabilidad: r * Δt < 1."
)

print(
    "Criterio de equilibrio: |T - Tamb| < 0.1 °C.\n"
)


# ============================================================
# ENTRADA DE DATOS
# ============================================================

T0 = pedir_temperatura(
    "Ingrese la temperatura inicial del cuerpo T0 [°C]: "
)

Tamb = pedir_temperatura(
    "Ingrese la temperatura ambiental Tamb [°C]: "
)

r = pedir_r()

delta_t = pedir_delta_t(r)

N = pedir_N()


# ============================================================
# DATOS DE LA SIMULACIÓN
# ============================================================

print("\n" + "=" * 60)
print("              DATOS DE LA SIMULACIÓN")
print("=" * 60)

print(f"Temperatura inicial : {T0:.2f} °C")
print(f"Temperatura ambiente: {Tamb:.2f} °C")
print(f"Constante r         : {r}")
print(f"Paso de tiempo Δt   : {delta_t}")
print(f"Número de pasos N   : {N}")
print(f"Producto r * Δt     : {r * delta_t:.4f}")


# ============================================================
# COMPROBACIÓN INICIAL
# ============================================================

if T0 == Tamb:

    print(
        "\nEl cuerpo ya se encuentra a la "
        "temperatura ambiente."
    )

    print("La diferencia inicial es 0 °C.")

else:

    print("\nLos datos ingresados son válidos.")
    print("La condición de estabilidad se cumple.")
    print("Se iniciará la simulación...")


# ============================================================
# EJECUTAR SIMULACIÓN
# ============================================================

tiempos, temperaturas = simular_enfriamiento(
    T0,
    Tamb,
    r,
    delta_t,
    N
)


# ============================================================
# TABLA DE RESULTADOS
# ============================================================

print("\n" + "=" * 60)
print("                 TABLA DE RESULTADOS")
print("=" * 60)

print(
    f"{'Paso':>6}"
    f"{'Tiempo':>12}"
    f"{'Temperatura':>18}"
)

print("-" * 40)


for i in range(len(tiempos)):

    print(
        f"{i:>6}"
        f"{tiempos[i]:>12.2f}"
        f"{temperaturas[i]:>15.2f} °C"
    )


# ============================================================
# TEMPERATURA FINAL
# ============================================================

temperatura_final = temperaturas[-1]


# ============================================================
# DIFERENCIA FINAL
# ============================================================

diferencia_final = abs(
    temperatura_final - Tamb
)


# ============================================================
# ANÁLISIS FINAL
# ============================================================

print("\n" + "=" * 60)
print("                  ANÁLISIS FINAL")
print("=" * 60)

print(f"Temperatura inicial : {T0:.2f} °C")
print(f"Temperatura ambiente: {Tamb:.2f} °C")
print(f"Temperatura final   : {temperatura_final:.2f} °C")
print(f"Diferencia final    : {diferencia_final:.4f} °C")


# ============================================================
# VERIFICACIÓN DEL EQUILIBRIO
# ============================================================

if diferencia_final < 0.1:

    print("\nEl cuerpo alcanzó el equilibrio térmico.")
    print("Se cumple el criterio:")
    print("|T - Tamb| < 0.1 °C")

else:

    print(
        "\nEl cuerpo todavía NO alcanzó "
        "el equilibrio térmico."
    )

    print("Puede aumentar el número de pasos N.")


# ============================================================
# FIN
# ============================================================

print("\nSimulación finalizada.")