import random
import math

random.seed(42)

# Un solo dataset con 5 columnas de características + el número de lanzamiento
dataset = {
    "Lanzamiento": [],
    "Masa (kg)": [],
    "Fuerza del disparo (N)": [],
    "Distancia X (m)": [],
    "Altura Y (m)": [],
    "Velocidad Final (m/s)": []
}

g = 9.81  # gravedad (m/s^2)

# Generar 100 lanzamientos (disparos de cañón)
for i in range(100):

    # Número del lanzamiento
    lanzamiento = i + 1

    # Masa del proyectil
    masa = round(random.uniform(3.0, 50.0), 2)

    # Fuerza del disparo (impulso que da el cañón al proyectil)
    fuerza = round(random.uniform(2000.0, 50000.0), 1)

    # Ángulo de disparo (no se guarda como columna, solo se usa para calcular)
    angulo_grados = random.uniform(15.0, 75.0)
    angulo_rad = math.radians(angulo_grados)

    # Longitud del cañón (tampoco se guarda, solo se usa para calcular)
    longitud_canon = random.uniform(1.5, 3.0)

    # Velocidad inicial por trabajo-energía: F * L = 1/2 * m * v0^2
    v0 = math.sqrt((2 * fuerza * longitud_canon) / masa)

    # Distancia X: alcance horizontal del tiro parabólico
    distancia_x = (v0 ** 2) * math.sin(2 * angulo_rad) / g

    # Altura Y: altura máxima alcanzada por el proyectil
    altura_y = ((v0 * math.sin(angulo_rad)) ** 2) / (2 * g)

    # Velocidad final: se pierde un poco de velocidad por la resistencia del aire
    perdida_aire = random.uniform(0.03, 0.10)
    velocidad_final = v0 * (1 - perdida_aire)

    # Ruido de medición (simula un sensor real, no una fórmula perfecta)
    distancia_x = round(distancia_x * (1 + random.gauss(0, 0.03)), 2)
    altura_y = round(altura_y * (1 + random.gauss(0, 0.03)), 2)
    velocidad_final = round(velocidad_final * (1 + random.gauss(0, 0.03)), 2)

    # Agregar los datos al dataset
    dataset["Lanzamiento"].append(lanzamiento)
    dataset["Masa (kg)"].append(masa)
    dataset["Fuerza del disparo (N)"].append(fuerza)
    dataset["Distancia X (m)"].append(distancia_x)
    dataset["Altura Y (m)"].append(altura_y)
    dataset["Velocidad Final (m/s)"].append(velocidad_final)


# Mostrar el dataset con títulos
print("\n         DATASET DE LANZAMIENTOS: LANZAMIENTO DE PROYECTILES (CAÑÓN)")
print("=" * 110)

print(
    f"{'Lanzamiento':^12}"
    f"{'Masa (kg)':^13}"
    f"{'Fuerza (N)':^16}"
    f"{'Distancia X (m)':^18}"
    f"{'Altura Y (m)':^16}"
    f"{'Velocidad Final (m/s)':^24}"
)

print("-" * 110)

# Mostrar las 100 filas
for i in range(100):
    print(
        f"{dataset['Lanzamiento'][i]:^12}"
        f"{dataset['Masa (kg)'][i]:^13}"
        f"{dataset['Fuerza del disparo (N)'][i]:^16}"
        f"{dataset['Distancia X (m)'][i]:^18}"
        f"{dataset['Altura Y (m)'][i]:^16}"
        f"{dataset['Velocidad Final (m/s)'][i]:^24}"
    )