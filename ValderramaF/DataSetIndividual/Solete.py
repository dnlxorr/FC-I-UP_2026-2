import random
import math

random.seed(42)

# Un solo dataset con variables meteorológicas y de energía solar
dataset = {
    "Medición": [],
    "Temperatura (°C)": [],
    "Humedad (%)": [],
    "Presión (hPa)": [],
    "Velocidad Viento (m/s)": [],
    "Irradiancia Solar (W/m²)": [],
    "Potencia Solar (W)": []
}

# Generar 100 mediciones
for i in range(100):

    # Número de medición
    medicion = i + 1

    # Temperatura del ambiente
    temperatura = round(random.uniform(15.0, 35.0), 2)

    # Humedad relativa
    humedad = round(random.uniform(30.0, 90.0), 2)

    # Presión atmosférica
    presion = round(random.uniform(990.0, 1030.0), 2)

    # Velocidad del viento
    velocidad_viento = round(random.uniform(0.0, 15.0), 2)

    # Irradiancia solar
    # Durante el día puede variar aproximadamente entre 100 y 1000 W/m²
    irradiancia = round(random.uniform(100.0, 1000.0), 2)

    # Eficiencia aproximada del panel solar
    eficiencia = random.uniform(0.15, 0.22)

    # Influencia de la temperatura sobre la eficiencia
    # Los paneles suelen perder eficiencia cuando aumenta la temperatura
    factor_temperatura = 1 - 0.004 * (temperatura - 25)

    # Pequeña influencia del viento en el enfriamiento del panel
    factor_viento = 1 + 0.002 * velocidad_viento

    # Calcular potencia solar
    potencia = (
        irradiancia
        * eficiencia
        * factor_temperatura
        * factor_viento
    )

    # Agregar un pequeño ruido para simular mediciones reales
    potencia = potencia * (1 + random.gauss(0, 0.03))

    potencia = round(max(potencia, 0), 2)

    # Agregar los datos al dataset
    dataset["Medición"].append(medicion)
    dataset["Temperatura (°C)"].append(temperatura)
    dataset["Humedad (%)"].append(humedad)
    dataset["Presión (hPa)"].append(presion)
    dataset["Velocidad Viento (m/s)"].append(velocidad_viento)
    dataset["Irradiancia Solar (W/m²)"].append(irradiancia)
    dataset["Potencia Solar (W)"].append(potencia)


# Mostrar el dataset con títulos
print("\n       DATASET SOLETE: ENERGÍA SOLAR Y VARIABLES METEOROLÓGICAS")
print("=" * 120)

print(
    f"{'Medición':^10}"
    f"{'Temperatura (°C)':^20}"
    f"{'Humedad (%)':^15}"
    f"{'Presión (hPa)':^18}"
    f"{'Viento (m/s)':^17}"
    f"{'Irradiancia (W/m²)':^22}"
    f"{'Potencia Solar (W)':^21}"
)

print("-" * 120)

# Mostrar las 100 filas
for i in range(100):
    print(
        f"{dataset['Medición'][i]:^10}"
        f"{dataset['Temperatura (°C)'][i]:^20}"
        f"{dataset['Humedad (%)'][i]:^15}"
        f"{dataset['Presión (hPa)'][i]:^18}"
        f"{dataset['Velocidad Viento (m/s)'][i]:^17}"
        f"{dataset['Irradiancia Solar (W/m²)'][i]:^22}"
        f"{dataset['Potencia Solar (W)'][i]:^21}"
    )
