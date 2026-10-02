# ============================================================
#          LEY DE ENFRIAMIENTO DE NEWTON
#     SIMULACIÓN + MÉTODOS DE BÚSQUEDA
# ============================================================


# ============================================================
# FUNCIÓN PARA PEDIR UNA TEMPERATURA
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
            r = float(input("Ingrese la constante de enfriamiento r (0 < r < 1): "))

            if 0 < r < 1:
                return r
            else:
                print("Error: r debe ser mayor que 0 y menor que 1.")

        except ValueError:
            print("Error: debe ingresar un número válido.")


# ============================================================
# FUNCIÓN PARA PEDIR DELTA t
# Se verifica la estabilidad numérica.
#
# Condición utilizada:
# r * delta_t < 1
#
# Es una condición conservadora para evitar comportamientos
# numéricos no deseados en el método de Euler.
# ============================================================

def pedir_delta_t(r):

    while True:
        try:
            delta_t = float(input("Ingrese el paso de tiempo Δt: "))

            if delta_t <= 0:
                print("Error: Δt debe ser mayor que 0.")

            elif r * delta_t >= 1:
                print("Error de estabilidad: debe cumplirse r * Δt < 1.")

            else:
                return delta_t

        except ValueError:
            print("Error: debe ingresar un número válido.")


# ============================================================
# FUNCIÓN PARA PEDIR EL NÚMERO DE PASOS
# Restricción: N >= 100
# ============================================================

def pedir_N():

    while True:
        try:
            N = int(input("Ingrese el número de pasos N (N >= 100): "))

            if N >= 100:
                return N
            else:
                print("Error: N debe ser mayor o igual a 100.")

        except ValueError:
            print("Error: debe ingresar un número entero.")


# ============================================================
# FUNCIÓN PRINCIPAL DE SIMULACIÓN
# ============================================================

def simular_enfriamiento(T0, Tamb, r, delta_t, N):

    # Listas donde se guardarán los resultados
    tiempos = []
    temperaturas = []

    # Condición inicial
    tiempo = 0
    temperatura = T0

    # Guardamos el estado inicial
    tiempos.append(tiempo)
    temperaturas.append(temperatura)

    # Variable para saber si ya encontramos el equilibrio
    equilibrio_encontrado = False

    # --------------------------------------------------------
    # MÉTODO DE EULER
    # --------------------------------------------------------

    for paso in range(1, N + 1):

        # Cambio de temperatura
        delta_T = -r * (temperatura - Tamb) * delta_t

        # Nueva temperatura
        temperatura = temperatura + delta_T

        # Nuevo tiempo
        tiempo = tiempo + delta_t

        # Guardamos los resultados
        tiempos.append(tiempo)
        temperaturas.append(temperatura)

        # ----------------------------------------------------
        # BÚSQUEDA DEL EQUILIBRIO DURANTE LA SIMULACIÓN
        # ----------------------------------------------------

        if abs(temperatura - Tamb) < 0.1 and not equilibrio_encontrado:

            print()
            print(">>> EQUILIBRIO TÉRMICO ENCONTRADO <<<")
            print("Tiempo de equilibrio:", round(tiempo, 4))
            print("Temperatura:", round(temperatura, 4), "°C")

            equilibrio_encontrado = True

    return tiempos, temperaturas


# ============================================================
# MÉTODO DE BÚSQUEDA LINEAL
# Buscar una temperatura correspondiente a un tiempo dado
# ============================================================

def buscar_tiempo(tiempos, tiempo_buscado):

    tolerancia = 0.000001

    for i in range(len(tiempos)):

        if abs(tiempos[i] - tiempo_buscado) < tolerancia:
            return i

    return -1


# ============================================================
# MÉTODO DE BÚSQUEDA
# Buscar la temperatura máxima
# ============================================================

def buscar_temperatura_maxima(temperaturas):

    indice_maximo = 0

    for i in range(1, len(temperaturas)):

        if temperaturas[i] > temperaturas[indice_maximo]:
            indice_maximo = i

    return indice_maximo


# ============================================================
# MÉTODO DE BÚSQUEDA
# Buscar la temperatura mínima
# ============================================================

def buscar_temperatura_minima(temperaturas):

    indice_minimo = 0

    for i in range(1, len(temperaturas)):

        if temperaturas[i] < temperaturas[indice_minimo]:
            indice_minimo = i

    return indice_minimo


# ============================================================
# MÉTODO DE BÚSQUEDA
# Buscar el primer punto de equilibrio
# ============================================================

def buscar_equilibrio(tiempos, temperaturas, Tamb):

    for i in range(len(temperaturas)):

        if abs(temperaturas[i] - Tamb) < 0.1:
            return i

    return -1


# ============================================================
# CALCULAR DIFERENCIA CON EL EQUILIBRIO
# ============================================================

def calcular_error_equilibrio(temperatura, Tamb):

    return abs(temperatura - Tamb)


# ============================================================
# CALCULAR ERROR NUMÉRICO
#
# Se compara la solución obtenida con Euler con la solución
# exacta de la Ley de Enfriamiento de Newton:
#
# T(t) = Tamb + (T0 - Tamb)e^(-r*t)
# ============================================================

def calcular_error_numerico(temperatura_numerica, tiempo, T0, Tamb, r):

    import math

    temperatura_exacta = Tamb + (T0 - Tamb) * math.exp(-r * tiempo)

    error = abs(temperatura_numerica - temperatura_exacta)

    return temperatura_exacta, error


# ============================================================
# MENÚ DE BÚSQUEDA
# ============================================================

def menu_busqueda(tiempos, temperaturas, T0, Tamb, r):

    while True:

        print()
        print("============================================================")
        print("                 MÉTODOS DE BÚSQUEDA")
        print("============================================================")
        print("1. Buscar temperatura en un tiempo específico")
        print("2. Buscar temperatura máxima")
        print("3. Buscar temperatura mínima")
        print("4. Buscar equilibrio térmico")
        print("5. Buscar error respecto al equilibrio")
        print("6. Buscar error numérico")
        print("7. Mostrar todos los resultados")
        print("8. Salir")
        print("============================================================")

        opcion = input("Seleccione una opción: ")

        # ----------------------------------------------------
        # OPCIÓN 1
        # ----------------------------------------------------

        if opcion == "1":

            try:

                tiempo_buscado = float(
                    input("Ingrese el tiempo que desea buscar: ")
                )

                indice = buscar_tiempo(tiempos, tiempo_buscado)

                if indice != -1:

                    print()
                    print("RESULTADO DE LA BÚSQUEDA")
                    print("------------------------")
                    print("Tiempo:", tiempos[indice])
                    print("Temperatura:", round(temperaturas[indice], 6), "°C")

                else:

                    print()
                    print("No se encontró exactamente ese tiempo.")
                    print("Los tiempos disponibles van desde",
                          tiempos[0], "hasta", tiempos[-1])

            except ValueError:

                print("Error: debe ingresar un número válido.")

        # ----------------------------------------------------
        # OPCIÓN 2
        # ----------------------------------------------------

        elif opcion == "2":

            indice = buscar_temperatura_maxima(temperaturas)

            print()
            print("TEMPERATURA MÁXIMA")
            print("------------------")
            print("Temperatura máxima:",
                  round(temperaturas[indice], 6), "°C")
            print("Ocurre en el tiempo:",
                  round(tiempos[indice], 6))

        # ----------------------------------------------------
        # OPCIÓN 3
        # ----------------------------------------------------

        elif opcion == "3":

            indice = buscar_temperatura_minima(temperaturas)

            print()
            print("TEMPERATURA MÍNIMA")
            print("------------------")
            print("Temperatura mínima:",
                  round(temperaturas[indice], 6), "°C")
            print("Ocurre en el tiempo:",
                  round(tiempos[indice], 6))

        # ----------------------------------------------------
        # OPCIÓN 4
        # ----------------------------------------------------

        elif opcion == "4":

            indice = buscar_equilibrio(
                tiempos,
                temperaturas,
                Tamb
            )

            print()

            if indice != -1:

                print("EQUILIBRIO TÉRMICO")
                print("------------------")
                print("Tiempo:",
                      round(tiempos[indice], 6))
                print("Temperatura:",
                      round(temperaturas[indice], 6), "°C")
                print("Temperatura ambiente:",
                      Tamb, "°C")
                print("Diferencia:",
                      round(abs(temperaturas[indice] - Tamb), 6), "°C")

            else:

                print("No se alcanzó el equilibrio térmico")
                print("dentro del tiempo de simulación.")

        # ----------------------------------------------------
        # OPCIÓN 5
        # Error respecto al equilibrio
        # ----------------------------------------------------

        elif opcion == "5":

            try:

                tiempo_buscado = float(
                    input("Ingrese el tiempo para calcular el error: ")
                )

                indice = buscar_tiempo(tiempos, tiempo_buscado)

                if indice != -1:

                    error = calcular_error_equilibrio(
                        temperaturas[indice],
                        Tamb
                    )

                    print()
                    print("ERROR RESPECTO AL EQUILIBRIO")
                    print("-----------------------------")
                    print("Tiempo:",
                          tiempos[indice])
                    print("Temperatura:",
                          round(temperaturas[indice], 6), "°C")
                    print("Temperatura ambiente:",
                          Tamb, "°C")
                    print("Error:",
                          round(error, 6), "°C")

                else:

                    print("No se encontró ese tiempo.")

            except ValueError:

                print("Error: debe ingresar un número válido.")

        # ----------------------------------------------------
        # OPCIÓN 6
        # Error numérico
        # ----------------------------------------------------

        elif opcion == "6":

            try:

                tiempo_buscado = float(
                    input("Ingrese el tiempo para calcular el error numérico: ")
                )

                indice = buscar_tiempo(tiempos, tiempo_buscado)

                if indice != -1:

                    temperatura_exacta, error = calcular_error_numerico(
                        temperaturas[indice],
                        tiempos[indice],
                        T0,
                        Tamb,
                        r
                    )

                    print()
                    print("ERROR NUMÉRICO")
                    print("--------------")
                    print("Tiempo:",
                          tiempos[indice])
                    print("Temperatura Euler:",
                          round(temperaturas[indice], 6), "°C")
                    print("Temperatura exacta:",
                          round(temperatura_exacta, 6), "°C")
                    print("Error absoluto:",
                          round(error, 10), "°C")

                else:

                    print("No se encontró ese tiempo.")

            except ValueError:

                print("Error: debe ingresar un número válido.")

        # ----------------------------------------------------
        # OPCIÓN 7
        # Mostrar todos los resultados
        # ----------------------------------------------------

        elif opcion == "7":

            print()
            print("============================================================")
            print("                    TABLA COMPLETA")
            print("============================================================")
            print(f"{'Paso':<8}{'Tiempo':<15}{'Temperatura (°C)':<20}")
            print("------------------------------------------------------------")

            for i in range(len(tiempos)):

                print(
                    f"{i:<8}"
                    f"{tiempos[i]:<15.4f}"
                    f"{temperaturas[i]:<20.6f}"
                )

            print("============================================================")

        # ----------------------------------------------------
        # OPCIÓN 8
        # ----------------------------------------------------

        elif opcion == "8":

            print()
            print("Programa finalizado.")
            break

        # ----------------------------------------------------
        # OPCIÓN INCORRECTA
        # ----------------------------------------------------

        else:

            print("Error: opción no válida.")


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

print("============================================================")
print("             LEY DE ENFRIAMIENTO DE NEWTON")
print("============================================================")

# Pedimos los datos al usuario

T0 = pedir_temperatura(
    "Ingrese la temperatura inicial T0 (°C): "
)

Tamb = pedir_temperatura(
    "Ingrese la temperatura ambiente Tamb (°C): "
)

r = pedir_r()

delta_t = pedir_delta_t(r)

N = pedir_N()


# ============================================================
# COMPROBACIÓN DE LOS DATOS
# ============================================================

print()
print("============================================================")
print("                    DATOS INGRESADOS")
print("============================================================")
print("Temperatura inicial T0:", T0, "°C")
print("Temperatura ambiente Tamb:", Tamb, "°C")
print("Constante r:", r)
print("Paso de tiempo Δt:", delta_t)
print("Número de pasos N:", N)
print("Condición de estabilidad: r * Δt =", r * delta_t)


# ============================================================
# EJECUTAMOS LA SIMULACIÓN
# ============================================================

tiempos, temperaturas = simular_enfriamiento(
    T0,
    Tamb,
    r,
    delta_t,
    N
)


# ============================================================
# MOSTRAR TABLA DE RESULTADOS
# ============================================================

print()
print("============================================================")
print("                 RESULTADOS DE LA SIMULACIÓN")
print("============================================================")

print(f"{'Paso':<8}{'Tiempo':<15}{'Temperatura (°C)':<20}")
print("------------------------------------------------------------")

for i in range(len(tiempos)):

    print(
        f"{i:<8}"
        f"{tiempos[i]:<15.4f}"
        f"{temperaturas[i]:<20.6f}"
    )


# ============================================================
# ANÁLISIS FINAL
# ============================================================

temperatura_final = temperaturas[-1]

diferencia_final = abs(
    temperatura_final - Tamb
)

print()
print("============================================================")
print("                     ANÁLISIS FINAL")
print("============================================================")

print(
    "Temperatura final:",
    round(temperatura_final, 6),
    "°C"
)

print(
    "Temperatura ambiente:",
    Tamb,
    "°C"
)

print(
    "Diferencia final:",
    round(diferencia_final, 6),
    "°C"
)


# ============================================================
# COMPROBAR SI SE ALCANZÓ EL EQUILIBRIO
# ============================================================

indice_equilibrio = buscar_equilibrio(
    tiempos,
    temperaturas,
    Tamb
)

if indice_equilibrio != -1:

    print()
    print("El sistema alcanzó el equilibrio térmico.")

    print(
        "Primer equilibrio en t =",
        round(tiempos[indice_equilibrio], 6)
    )

    print(
        "Temperatura =",
        round(temperaturas[indice_equilibrio], 6),
        "°C"
    )

else:

    print()
    print("El sistema NO alcanzó el equilibrio térmico")
    print("durante la simulación.")


# ============================================================
# MENÚ FINAL DE MÉTODOS DE BÚSQUEDA
# ============================================================

menu_busqueda(
    tiempos,
    temperaturas,
    T0,
    Tamb,
    r
)