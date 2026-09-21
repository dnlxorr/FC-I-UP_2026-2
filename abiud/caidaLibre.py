import math

# Constante de la gravedad en m/s²
G = 9.81

def aceleracion(v: float, m: float, k: float) -> float:
    """Calcula la aceleracion neta descendente considerando la gravedad
    y la resistencia del aire lineal: a(v) = g - (k/m)*v. """
    return G - (k / m) * v

def velocidad_terminal(m: float, k: float) -> float:
    """Calcula la magnitud de la velocidad terminal teorica: v_T = (m * g) / k. """
    return (m * G) / k

def validar_entrada(m: float, y0: float, k: float, dt: float):
    """Validacion de los parametros iniciales. """
    if m <= 0:
        return False, "La masa debe ser mayor que cero (m > 0)."
    elif y0 <= 0:
        return False, "La altura inicial debe ser mayor que cero (y0 > 0)."
    elif k <= 0:
        return False, "El coeficiente de arrastre debe ser positivo (k > 0)."
    elif dt <= 0:
        return False, "El paso de tiempo debe ser mayor que cero (dt > 0)."
    else:
        return True, "Datos válidos."


def simular_caida(m: float, y0: float, k: float, dt: float):
    """Simula iterativamente la caida libre con resistencia del aire
    utilizando un bucle 'for' con limite maximo de pasos de tiempo. """

    tiempo = []
    posiciones = []
    velocidades = []
    aceleraciones = []

    t = 0.0
    y = y0
    v = 0.0  # Se parte del reposo (magnitud positiva)

    v_terminal = velocidad_terminal(m, k)
    maximo_pasos = 100000

    for _ in range(maximo_pasos):
        # 1. Aceleración neta en el instante actual
        a = aceleracion(v, m, k)
        # 2. Guardar estado actual en el historial
        tiempo.append(t)
        posiciones.append(y)
        velocidades.append(v)
        aceleraciones.append(a)
        # 3. Evaluación de la condicion de parada (impacto contra el suelo)
        if y <= 0:
            posiciones[-1] = 0.0  # Ajuste estetico a cero exacto
            break
        # 4. Actualizacion del estado (Metodo numerico de Euler-Cromer)
        v = v + a * dt
        y = y - v * dt  # La altura disminuye al avanzar la simulacion
        t = t + dt
    return tiempo, posiciones, velocidades, aceleraciones, v_terminal

def mostrar_resultados(
    tiempo, posiciones, velocidades, aceleraciones, v_terminal
):
    """Muestra el resumen final estructurado e imprime la tabla de los ultimos instantes."""
    print("\n" + "=" * 45)
    print(" RESULTADOS ")
    print("=" * 45)

    print(f"Tiempo de impacto:           {tiempo[-1]:.4f} s")
    print(f"Velocidad de impacto:        {velocidades[-1]:.4f} m/s")
    print(f"Aceleracion al impactar:     {aceleraciones[-1]:.4f} m/s²")
    print(f"Velocidad terminal teorica:  {v_terminal:.4f} m/s")
    print("\nUltimos instantes:")
    print("-" * 45)
    print(f"{'Tiempo (s)':<12}{'Altura (m)':<15}{'Velocidad (m/s)':<15}")
    print("-" * 45)

    inicio = max(0, len(tiempo) - 5)
    for i in range(inicio, len(tiempo)):
        print(
            f"{tiempo[i]:<12.4f}{posiciones[i]:<15.4f}{velocidades[i]:<15.4f}"
        )
    print("-" * 45)

def main():
    # Estamentos de Entrada y Salida (E/S) con captura de excepciones
    try:
        m = float(input("Ingrese la masa [kg]: "))
        y0 = float(input("Ingrese la altura inicial [m]: "))
        k = float(input("Ingrese el coeficiente k [kg/s]: "))
        dt = float(input("Ingrese Δt [s]: "))
    except ValueError:
        print("\nError de tipo: Debe ingresar valores numéricos válidos.")
        return
    # Estamentos de Control: Validacion de condiciones fisicas
    valido, mensaje = validar_entrada(m, y0, k, dt)
    if not valido:
        print(f"\nError de validación: {mensaje}")
        return

    print(f"\nEstado de entrada: {mensaje}")

    # Ejecucion de la simulacion
    resultados = simular_caida(m, y0, k, dt)

    # Despliegue de resultados
    mostrar_resultados(*resultados)

if __name__ == "__main__":
    main()
