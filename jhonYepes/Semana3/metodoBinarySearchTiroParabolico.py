# ==========================================
# JhonAlexanderYepesArias: Tiro Parabólico 2D
# ==========================================
import math

#g = representa la gravedad de la tierra
#t = representa el tiempo transcurrido en segundos
#v0 = representa la veocidad inicial del proyectil
#theta_rad = representa la conversion del angulo en radianes que ingresa el usuario en grados
def calcular_posicion(t, v0, theta_rad):
    g = 9.81
    x = v0 * math.cos(theta_rad) * t
    y = v0 * math.sin(theta_rad) * t - 0.5 * g * t ** 2
    return x, y


def busqueda_binaria_tiempo(lista_t, t_objetivo):
    """Implementa Binary Search para encontrar el índice del tiempo más cercano."""
    izquierda, derecha = 0, len(lista_t) - 1

    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if lista_t[medio] == t_objetivo:
            return medio
        elif lista_t[medio] < t_objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1

    # Retorna el índice más cercano si el número no es exacto
    return min(max(izquierda, 0), len(lista_t) - 1)


def simular_tiro():
    print("--- Simulación de Tiro Parabólico ---")

    try:
        v0 = float(input("Ingrese la velocidad inicial (m/s): "))
        theta_grados = float(input("Ingrese el ángulo de lanzamiento (grados, 0-90): "))
    except ValueError:
        print("Error crítico: Por favor, ingrese solo valores numéricos.")
        return

    if v0 <= 0 or theta_grados < 0 or theta_grados > 90:
        print("Error: Velocidad debe ser > 0 y el ángulo entre 0 y 90 grados.")
        return

    theta_rad = math.radians(theta_grados)
    dt = 0.01
    t_list, x_list, y_list = [], [], []

    # 1. Generación de datos (Simulación pura)
    for i in range(10000):
        t = i * dt
        x, y = calcular_posicion(t, v0, theta_rad)

        if y < 0 and i > 0:
            break

        t_list.append(t)
        x_list.append(x)
        y_list.append(y)

    # 2. Menú de Opciones
    print("\n==========================================")
    print("¿Qué desea hacer con los datos generados?")
    print("1. Ver resultados generales (Máximos y tiempo total)")
    print("2. Buscar historial de posiciones por rango de tiempo")
    print("==========================================")

    opcion = input("Seleccione una opción (1 o 2): ")

    if opcion == "1":
        # Búsqueda de máximos
        y_max = max(y_list)
        x_max = x_list[-1]
        t_max = t_list[-1]

        print(f"\n--- Resultados Generales ---")
        print(f"Altura máxima alcanzada: {y_max:.2f} m")
        print(f"Alcance horizontal máximo: {x_max:.2f} m")
        print(f"Tiempo total de vuelo: {t_max:.2f} s")

    elif opcion == "2":
        t_final = t_list[-1]
        print(f"\n[INFO] El vuelo duró desde 0.00 s hasta {t_final:.2f} s.")

        try:
            t_inicio = float(input("Ingrese el tiempo inicial a buscar (s): "))
            t_fin = float(input("Ingrese el tiempo final a buscar (s): "))
        except ValueError:
            print("Error: Debe ingresar tiempos en formato numérico.")
            return

        # Validar lógica del rango
        if t_inicio > t_fin or t_inicio < 0 or t_fin > t_final:
            print("Error: Rango de tiempo inválido o fuera del tiempo de vuelo.")
            return

        # 3. Ejecución de la Búsqueda Binaria
        idx_inicio = busqueda_binaria_tiempo(t_list, t_inicio)
        idx_fin = busqueda_binaria_tiempo(t_list, t_fin)

        # 4. Impresión de resultados encontrados
        print(f"\n--- Datos encontrados entre {t_inicio}s y {t_fin}s ---")
        print(f"{'Tiempo (s)':<12} | {'Posición X (m)':<15} | {'Posición Y (m)':<15}")
        print("-" * 48)

        for i in range(idx_inicio, idx_fin + 1):
            print(f"{t_list[i]:<12.2f} | {x_list[i]:<15.2f} | {y_list[i]:<15.2f}")

    else:
        print("Opción no válida. Simulación terminada.")


simular_tiro()