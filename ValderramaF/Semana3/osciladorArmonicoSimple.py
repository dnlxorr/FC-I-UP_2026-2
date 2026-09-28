import math


# Calcula la posición del oscilador armónico simple en un instante t.
# Fórmula: x(t) = A cos(wt)
def calcular_x(t, A, w):
    """Posición x(t) = A cos(wt)."""
    return A * math.cos(w * t)


# Calcula la velocidad del oscilador en un instante t.
# La velocidad se obtiene derivando la posición:
# v(t) = -A w sin(wt)
def calcular_v(t, A, w):
    """Velocidad v(t) = -A w sin(wt)."""
    return -A * w * math.sin(w * t)


# Calcula las tres formas de energía del sistema:
# 1. Energía cinética: Ec = 1/2 m v²
# 2. Energía potencial elástica: Ep = 1/2 k x²
# 3. Energía total: Et = Ec + Ep
def calcular_energia(m, k, x, v):
    """Devuelve (E_cinética, E_potencial, E_total)."""

    # Energía cinética asociada al movimiento de la masa
    e_cin = 0.5 * m * v ** 2

    # Energía potencial almacenada en el resorte
    e_pot = 0.5 * k * x ** 2

    # La energía total es la suma de la energía cinética y potencial
    return e_cin, e_pot, e_cin + e_pot


# Se solicita un número positivo.
# Si el dato es incorrecto se repite hasta que el usuario introduzca un valor correcto.
def leer_positivo(mensaje):
    """Pide un número real finito y estrictamente positivo; repite hasta que sea válido."""

    # while True hace que la pregunta se repita indefinidamente
    # hasta que se introduzca un valor válido.
    while True:
        try:
            # Convierte lo que escribe el usuario a número decimal
            valor = float(input(mensaje))

        except ValueError:
            # Este error ocurre si el usuario escribe algo que no se puede convertir a un número.
            print("Error: ingrese un número válido.")
            continue

        # Verifica que el número sea finito y mayor que cero.
        # No se permiten:
        # - números negativos
        # - cero
        # - nan
        # - infinito
        if not math.isfinite(valor) or valor <= 0:
            print("Error: el valor debe ser un número finito estrictamente positivo.")

        else:
            # Si el valor es correcto, se devuelve.
            return valor


# Función principal que realiza toda la simulación
def simular_oscilador():
    # Mensaje inicial del programa
    print("--- Simulación de Oscilador Armónico Simple ---")


    # ENTRADA DE DATOS


    # Se piden al usuario los valores necesarios
    # para describir el oscilador.
    m = leer_positivo("Ingrese la masa (kg): ")
    k = leer_positivo("Ingrese la constante elástica (N/m): ")
    A = leer_positivo("Ingrese la amplitud (m): ")
    T_total = leer_positivo("Ingrese el tiempo total de simulación (s): ")


    # PARÁMETROS DEL SISTEMA


    # Frecuencia angular:
    # w = √(k/m)
    # Indica qué tan rápido oscila el sistema.
    w = math.sqrt(k / m)

    # Período:
    # T = 2π/w
    # Es el tiempo que tarda el sistema en completar una oscilación.
    periodo = 2 * math.pi / w

    # dt representa el intervalo de tiempo entre dos cálculos.
    # Aquí se calcula el estado del sistema cada 0.01 segundos.
    dt = 0.01

    # Calcula cuántos pasos de tiempo serán necesarios.
    # Se utiliza round() para redondear al entero más cercano.
    pasos = round(T_total / dt)


    # LÍMITE DE LA SIMULACIÓN


    # Se evita que el programa intente almacenar una cantidad
    # excesivamente grande de datos.
    #
    # 1 000 000 pasos × 0.01 s = 10 000 s
    if pasos > 1_000_000:
        print("Error: el tiempo total es demasiado grande (máx. 10 000 s).")
        return


    # LISTAS PARA GUARDAR DATOS


    # Estas listas almacenarán los resultados de cada instante.
    t_list = []  # Tiempo
    x_list = []  # Posición
    v_list = []  # Velocidad
    ecin_list = []  # Energía cinética
    epot_list = []  # Energía potencial
    etot_list = []  # Energía total


    # ENERGÍA INICIAL


    # Cuando el oscilador está en la máxima amplitud,
    # la velocidad es cero y toda la energía es potencial.
    #
    # E = 1/2 k A²
    energia_inicial = 0.5 * k * A ** 2

    # Se permite una diferencia máxima del 1 %
    # respecto a la energía inicial.
    tolerancia = 0.01 * energia_inicial

    # Contará cuántas veces la energía total se aleja
    # más de la tolerancia permitida.
    violaciones = 0


    # SIMULACIÓN


    # El ciclo recorre todos los instantes de tiempo.
    #
    # range(pasos + 1) incluye también el instante inicial
    # t = 0 y el instante final.
    for i in range(pasos + 1):

        # Calcula el tiempo correspondiente al paso actual.
        t = i * dt

        # Calcula la posición en ese instante.
        x = calcular_x(t, A, w)

        # Calcula la velocidad en ese instante.
        v = calcular_v(t, A, w)

        # Calcula:
        # - energía cinética
        # - energía potencial
        # - energía total
        e_cin, e_pot, e_tot = calcular_energia(m, k, x, v)


        # GUARDAR RESULTADOS


        # Se agregan los valores calculados a sus respectivas listas.
        t_list.append(t)
        x_list.append(x)
        v_list.append(v)
        ecin_list.append(e_cin)
        epot_list.append(e_pot)
        etot_list.append(e_tot)


        # COMPROBAR CONSERVACIÓN
        # DE LA ENERGÍA


        # Se compara la energía total calculada-
        # con la energía inicial.
        #
        # abs() obtiene el valor absoluto de la diferencia.
        # Si la diferencia supera la tolerancia,
        # se cuenta como una violación.
        if abs(e_tot - energia_inicial) > tolerancia:
            violaciones += 1


    # MOSTRAR RESULTADOS


    # Muestra la frecuencia angular y el período.
    print(f"\nω = {w:.4f} rad/s | Período = {periodo:.4f} s")

    # Imprime los títulos de las columnas de la tabla.
    print(
        f"\n{'t (s)':>8}"
        f"{'x (m)':>10}"
        f"{'v (m/s)':>10}"
        f"{'Ecin (J)':>11}"
        f"{'Epot (J)':>11}"
        f"{'Etot (J)':>11}"
    )


    # SELECCIONAR DATOS PARA LA TABLA


    # La simulación puede tener miles de datos.
    # Para no imprimirlos todos, se calcula un salto
    # que permita mostrar aproximadamente 20 filas.
    salto = max(1, len(t_list) // 20)

    # Recorre la lista utilizando el salto calculado.
    for j in range(0, len(t_list), salto):
        # Imprime tiempo, posición, velocidad y energías.
        # Los números después de los dos puntos indican
        # cuántos espacios ocupará cada dato.
        print(
            f"{t_list[j]:8.2f}"
            f"{x_list[j]:10.4f}"
            f"{v_list[j]:10.4f}"
            f"{ecin_list[j]:11.4f}"
            f"{epot_list[j]:11.4f}"
            f"{etot_list[j]:11.4f}"
        )


    # CONCLUSIÓN


    # Si nunca se superó la tolerancia,
    # se considera que la energía se conserva.
    if violaciones == 0:
        print(f"\nLa energía total se conserva: {energia_inicial:.4f} J.")

    else:
        # Si hubo diferencias mayores al 1 %,
        # se muestra cuántos pasos tuvieron ese problema.
        print(
            f"\nAdvertencia: la energía se desvió "
            f"de la tolerancia en {violaciones} pasos."
        )



# PUNTO DE INICIO DEL PROGRAMA


# Esta condición hace que la simulación se ejecute
# solamente cuando este archivo se ejecuta directamente.
#
# Si el archivo se importa desde otro programa,
# esta función no se ejecutará automáticamente.
if __name__ == "__main__":
    simular_oscilador()