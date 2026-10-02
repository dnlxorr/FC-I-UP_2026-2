# Constante de la gravedad en m/s²
G = 9.81

def aceleracion(v: float, m: float, k: float) -> float:
    """Calcula la aceleracion neta: a(v) = -g - (k/m)*v"""
    return -G - (k / m) * v

def velocidad_terminal(m: float, k: float) -> float:
    """Calcula la velocidad terminal teorica: v_T = -(m*g)/k"""
    return -(m * G) / k

def validar_entrada(m: float, y0: float, k: float, dt: float):
    """Validacion de los parametros iniciales"""
    if m <= 0:
        return False, "La masa debe ser mayor que cero (m > 0)."
    elif y0 <= 0:
        return False, "La altura inicial debe ser mayor que cero (y0 > 0)."
    elif k <= 0:
        return False, "El coeficiente de arrastre debe ser positivo (k > 0)."
    elif dt <= 0:
        return False, "El paso de tiempo debe ser mayor que cero (dt > 0)."
    else:
        return True, "Datos validos."

def simular_caida(m: float, y0: float, k: float, dt: float):
    tiempo = []
    posiciones = []
    velocidades = []
    aceleraciones = []

    t = 0.0
    y = y0
    v = 0.0  # Se parte del reposo
    v_terminal = velocidad_terminal(m, k)

    maximo_pasos = 10000

    for _ in range(maximo_pasos):
        # 1. Aceleracion neta en el instante actual
        a = aceleracion(v, m, k)

        # 2. Guardar estado actual en el historial
        tiempo.append(t)
        posiciones.append(y)
        velocidades.append(v)
        aceleraciones.append(a)

        # 3. Evaluacion de la condicion de parada
        if y <= 0:
            posiciones[-1] = 0.0
            break

        # 4. Actualizacion del estado
        v = v + a * dt
        y = y + v * dt
        t = t + dt

    return tiempo, posiciones, velocidades, aceleraciones, v_terminal

def busqueda_binaria_altura(posiciones, altura_objetivo):
    """Como la lista 'posiciones' esta ordenada de mayor a menor (decreciente),
    adaptamos la busqueda binaria para listas ordenadas de forma descendente.
    Retorna el indice del elemento mas cercano """
    inicio = 0
    fin = len(posiciones) - 1

    # Si la altura buscada esta fuera del rango de la simulacion
    if altura_objetivo > posiciones[0] or altura_objetivo < posiciones[-1]:
        return None

    while inicio <= fin:
        medio = (inicio + fin) // 2

        # Al ser una lista decreciente:
        if abs(posiciones[medio] - altura_objetivo) < 1e-3:
            return medio
        elif posiciones[medio] < altura_objetivo:
            fin = medio - 1
        else:
            inicio = medio + 1

    # Si no hay coincidencia exacta, retorna la mejor aproximacion
    return min(
        range(len(posiciones)),
        key=lambda i: abs(posiciones[i] - altura_objetivo),
    )


def mostrar_resultados(
    tiempo, posiciones, velocidades, aceleraciones, v_terminal
):
    """Muestra el resumen final y los ultimos instantes."""
    print("\n"" RESULTADOS DE SIMULACIÓN ")
    print(f"Tiempo de impacto:           {tiempo[-1]:.3f} s")
    print(f"Velocidad de impacto:        {velocidades[-1]:.3f} m/s")
    print(f"Aceleracion al impactar:     {aceleraciones[-1]:.3f} m/s²")
    print(f"Velocidad terminal teorica:  {v_terminal:.3f} m/s")
    print(f"Magnitud velocidad terminal: {abs(v_terminal):.3f} m/s")


def main():
    # Estamentos de Entrada y Salida (E/S)
    try:
        m = float(input("Ingrese la masa [kg]: "))
        y0 = float(input("Ingrese la altura inicial [m]: "))
        k = float(input("Ingrese el coeficiente k [kg/s]: "))
        dt = float(input("Ingrese Δt [s]: "))

    except ValueError:
        print("\nError de tipo: Debe ingresar valores numericos validos.")
        return

    # Validacion de las condiciones fisicas
    valido, mensaje = validar_entrada(m, y0, k, dt)

    if not valido:
        print(f"\nError de validación: {mensaje}")
        return

    print(f"\nEstado de entrada: {mensaje}")

    # Ejecucion de la simulacion
    tiempo, posiciones, velocidades, aceleraciones, v_terminal = simular_caida(
        m, y0, k, dt
    )

    # Despliegue de resultados generales
    mostrar_resultados(
        tiempo, posiciones, velocidades, aceleraciones, v_terminal
    )

    # IMPLEMENTACIÓN DE BINARY SEARCH
    print("\n" " Busqueda por medio de Binary search ")
    try:
        altura_buscar = float(input(f"Ingrese la altura (m) a buscar en los datos (0 a {y0}): "))
        idx = busqueda_binaria_altura(posiciones, altura_buscar)

        if idx is not None:
            print(f"\n[Dato encontrado con Binary Search - Indice {idx}]:")
            print(f"  Tiempo transcurrido: {tiempo[idx]:.4f} s")
            print(f"  Altura registrada:    {posiciones[idx]:.4f} m")
            print(f"  Velocidad alcanzada:  {velocidades[idx]:.4f} m/s")
            print(f"  Aceleración:          {aceleraciones[idx]:.4f} m/s²")
        else:
            print(
                f"\nLa altura {altura_buscar} m está fuera del rango simulado (0 a {y0} m)."
            )

    except ValueError:
        print("\nError: Debe ingresar un valor numurico para la busqueda.")

if __name__ == "__main__":
    main()