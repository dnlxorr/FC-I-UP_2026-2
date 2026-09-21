import math


def calcular_x(t, A, w):
    """Posición x(t) = A cos(wt)."""
    return A * math.cos(w * t)


def calcular_v(t, A, w):
    """Velocidad v(t) = -A w sin(wt)."""
    return -A * w * math.sin(w * t)


def calcular_energia(m, k, x, v):
    """Devuelve (E_cinética, E_potencial, E_total)."""
    e_cin = 0.5 * m * v ** 2
    e_pot = 0.5 * k * x ** 2
    return e_cin, e_pot, e_cin + e_pot


def leer_positivo(mensaje):
    """Pide un número real finito y estrictamente positivo; repite hasta que sea válido."""
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:  # El usuario escribió texto no numérico
            print("Error: ingrese un número válido.")
            continue
        if not math.isfinite(valor) or valor <= 0:  # Rechaza nan, inf, cero y negativos
            print("Error: el valor debe ser un número finito estrictamente positivo.")
        else:
            return valor


def simular_oscilador():
    print("--- Simulación de Oscilador Armónico Simple ---")

    # Entrada de datos (validados)
    m = leer_positivo("Ingrese la masa (kg): ")
    k = leer_positivo("Ingrese la constante elástica (N/m): ")
    A = leer_positivo("Ingrese la amplitud (m): ")
    T_total = leer_positivo("Ingrese el tiempo total de simulación (s): ")

    # Parámetros del sistema y de la simulación
    w = math.sqrt(k / m)              # Frecuencia angular
    periodo = 2 * math.pi / w         # Período de oscilación
    dt = 0.01                         # Paso de tiempo (s)
    pasos = round(T_total / dt)       # round evita errores de truncamiento

    # Límite para no saturar la memoria con tiempos absurdamente largos
    if pasos > 1_000_000:
        print("Error: el tiempo total es demasiado grande (máx. 10 000 s).")
        return

    # Historial de la simulación
    t_list, x_list, v_list = [], [], []
    ecin_list, epot_list, etot_list = [], [], []

    energia_inicial = 0.5 * k * A ** 2       # E = (1/2) k A²
    tolerancia = 0.01 * energia_inicial      # Margen: 1 % de E inicial
    violaciones = 0                          # Pasos donde se excede la tolerancia

    # Lazo principal: calcula y almacena el estado en cada instante
    for i in range(pasos + 1):
        t = i * dt
        x = calcular_x(t, A, w)
        v = calcular_v(t, A, w)
        e_cin, e_pot, e_tot = calcular_energia(m, k, x, v)

        t_list.append(t)
        x_list.append(x)
        v_list.append(v)
        ecin_list.append(e_cin)
        epot_list.append(e_pot)
        etot_list.append(e_tot)

        # Verificación de conservación de energía
        if abs(e_tot - energia_inicial) > tolerancia:
            violaciones += 1

    # Resumen final: parámetros y tabla de ~20 filas
    print(f"\nω = {w:.4f} rad/s | Período = {periodo:.4f} s")
    print(f"\n{'t (s)':>8}{'x (m)':>10}{'v (m/s)':>10}{'Ecin (J)':>11}{'Epot (J)':>11}{'Etot (J)':>11}")
    salto = max(1, len(t_list) // 20)  # Cada cuántos datos se imprime una fila
    for j in range(0, len(t_list), salto):
        print(f"{t_list[j]:8.2f}{x_list[j]:10.4f}{v_list[j]:10.4f}"
              f"{ecin_list[j]:11.4f}{epot_list[j]:11.4f}{etot_list[j]:11.4f}")

    # Conclusión sobre la conservación de la energía
    if violaciones == 0:
        print(f"\nLa energía total se conserva: {energia_inicial:.4f} J.")
    else:
        print(f"\nAdvertencia: la energía se desvió de la tolerancia en {violaciones} pasos.")


if __name__ == "__main__":
    simular_oscilador()
