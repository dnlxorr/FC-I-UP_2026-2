# ==========================================
# JhonAlexanderYepesArias: Tiro Parabólico 2D
# ==========================================
import math


def calcular_posicion(t, v0, theta_rad):
    g = 9.81
    x = v0 * math.cos(theta_rad) * t
    y = v0 * math.sin(theta_rad) * t - 0.5 * g * t ** 2
    return x, y


def simular_tiro():
    print("--- Simulación de Tiro Parabólico ---")
    v0 = float(input("Ingrese la velocidad inicial (m/s): "))
    theta_grados = float(input("Ingrese el ángulo de lanzamiento (grados, 0-90): "))

    if v0 <= 0 or theta_grados < 0 or theta_grados > 90:
        print("Error: Velocidad debe ser > 0 y el ángulo entre 0 y 90 grados.")
        return

    theta_rad = math.radians(theta_grados)
    dt = 0.01

    t_list, x_list, y_list = [], [], []
    y_max = 0
    x_max = 0

    for i in range(10000):  # Límite de seguridad
        t = i * dt
        x, y = calcular_posicion(t, v0, theta_rad)

        # Condición para detectar el suelo
        if y < 0 and i > 0:
            break

        t_list.append(t)
        x_list.append(x)
        y_list.append(y)

        # Detectar altura máxima
        if y > y_max:
            y_max = y
        # Guardar el último x como alcance máximo
        x_max = x

    print(f"\nResultados del Lanzamiento:")
    print(f"Altura máxima alcanzada: {y_max:.2f} m")
    print(f"Alcance horizontal máximo: {x_max:.2f} m")
    print(f"Tiempo total de vuelo: {t_list[-1]:.2f} s")


simular_tiro()