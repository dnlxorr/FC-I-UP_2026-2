# ==========================================
# JhonAlexanderYepesArias: Análisis del Péndulo No Lineal (Didáctico)
# ==========================================
import math
import numpy as np
import matplotlib.pyplot as plt


def leer_flotante(mensaje, minimo, maximo):
    """Manejo de errores para entradas numéricas con límites de grados."""
    while True:
        try:
            valor = float(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Error: Ingrese un valor entre {minimo} y {maximo} grados.")
        except ValueError:
            print("Error crítico: Entrada inválida. Use solo números enteros o decimales.")


def calcular_razon_periodo(grados):
    """Calcula T(θ0)/T0 usando la aproximación de Taylor de orden superior."""
    radianes = math.radians(grados)
    # T(θ0)/T0 = 1 + (1/16)*θ0^2 + (11/3072)*θ0^4
    return 1 + (1 / 16) * (radianes ** 2) + (11 / 3072) * (radianes ** 4)


def analizar_pendulo_interactivo():
    print("======================================================")
    print("      Análisis Didáctico: El Péndulo No Lineal        ")
    print("======================================================")
    print("En física básica nos enseñan que el período de un péndulo")
    print("(el tiempo que tarda en ir y volver) no depende de qué tan")
    print("alto lo soltemos. Pero eso solo es cierto para 'pequeñas oscilaciones'.")
    print("======================================================\n")

    print("[INFO sobre la Amplitud]:")
    print("Vamos a calcular qué tan equivocada está la fórmula clásica")
    print("cuando soltamos el péndulo desde ángulos más grandes.")

    # 1. Análisis de un ángulo específico ingresado por el usuario
    angulo_prueba = leer_flotante("-> Ingresa un ángulo inicial para evaluar (ej. 30): ", 1, 90)

    razon_prueba = calcular_razon_periodo(angulo_prueba)
    error_prueba = (razon_prueba - 1) * 100

    print(f"\n--- Resultado para {angulo_prueba}° ---")
    print(f"Al soltar el péndulo a {angulo_prueba}°, el tiempo real es {razon_prueba:.4f} veces mayor de lo esperado.")
    print(f"El error de usar la fórmula de 'pequeñas oscilaciones' es del {error_prueba:.2f}%.")

    if error_prueba > 1.0:
        print("⚠️ ¡Alerta! El error superó el límite estricto del 1%. La fórmula clásica falló aquí.")
    else:
        print("✅ Todo bien. El error es menor al 1%, la aproximación clásica aún es aceptable.")

    # 2. Tabla resumen de evolución del error
    print("\n--- Evolución del Error según el Ángulo ---")
    print(f"{'Ángulo (°)':<12} | {'Relación T/T0':<15} | {'% Error':<15}")
    print("-" * 46)
    for ang in range(10, 91, 10):
        r = calcular_razon_periodo(ang)
        e = (r - 1) * 100
        print(f"{ang:<12} | {r:<15.4f} | {e:<15.2f}%")

    # 3. Explicación y generación de la gráfica
    print("\n------------------------------------------------------")
    print("[INFO sobre la Gráfica que está a punto de abrirse]:")
    print("- Zona VERDE sombreada: Es el área donde la física clásica funciona (error < 1%).")
    print("- Curva ROJA: Muestra cómo el error se dispara exponencialmente hacia arriba.")
    print("- La FLECHA indicará el ángulo exacto donde la fórmula deja de ser válida.")
    print("-> Cierra la ventana de la gráfica para finalizar el programa.")

    # Generar array de datos finos para una curva suave
    angulos_plot = np.arange(0, 91, 0.5)
    errores_plot = [(calcular_razon_periodo(a) - 1) * 100 for a in angulos_plot]

    plt.figure(figsize=(9, 6))

    # Sombreado de la zona segura (del 0% al 1% de error)
    plt.fill_between(angulos_plot, 0, 1, color='#2ecc71', alpha=0.2, label='Zona de validez (< 1% error)')

    # Curva principal y línea de límite
    plt.plot(angulos_plot, errores_plot, color='#e74c3c', linewidth=3, label='Error real de la fórmula clásica')
    plt.axhline(y=1, color='#34495e', linestyle='--', linewidth=2, label='Límite estricto (1%)')

    # Algoritmo sencillo para encontrar dónde cruza el 1% (Punto Crítico)
    idx_cruce = np.where(np.array(errores_plot) >= 1.0)[0][0]
    angulo_cruce = angulos_plot[idx_cruce]

    # Dibujar un punto y una flecha apuntando al cruce
    plt.scatter([angulo_cruce], [1.0], color='black', zorder=5, s=80)
    plt.annotate(f' Punto de quiebre:\n aprox {angulo_cruce:.1f}°',
                 xy=(angulo_cruce, 1.0), xytext=(angulo_cruce - 20, 3.0),
                 arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=7),
                 fontsize=11, weight='bold', bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))

    # Detalles estéticos de la gráfica
    plt.title('¿En qué ángulo deja de funcionar la fórmula del Péndulo Simple?', fontsize=14, pad=15)
    plt.xlabel('Amplitud inicial θ0 (grados)', fontsize=12)
    plt.ylabel('Error Porcentual (%)', fontsize=12)
    plt.xlim(0, 90)
    plt.ylim(0, max(errores_plot) + 0.5)
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(loc='upper left', fontsize=11)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analizar_pendulo_interactivo()