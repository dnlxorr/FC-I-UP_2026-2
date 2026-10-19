# ====================================================================
# JhonAlexanderYepesArias: Integración Numérica (Péndulo No Lineal)
# ====================================================================
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# --- PARÁMETROS FÍSICOS GLOBALES ---
L = 1.0
g = 9.81
theta_0 = np.radians(60)
k = np.sin(theta_0 / 2.0)
T0 = 2 * np.pi * np.sqrt(L / g)


def integrando(phi):
    """Función f(phi) para la integral elíptica del péndulo."""
    return 1.0 / np.sqrt(1.0 - (k ** 2) * (np.sin(phi) ** 2))


def trapecio_compuesto(f, a, b, n):
    """Calcula la integral usando la Regla del Trapecio Compuesto."""
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    # Fórmula: (h/2) * [f(x0) + 2*sum(f(xi)) + f(xn)]
    integral = (h / 2.0) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral


def simpson_13_compuesto(f, a, b, n):
    """Calcula la integral usando Simpson 1/3 (n debe ser par)."""
    if n % 2 != 0:
        raise ValueError("El número de subintervalos n debe ser PAR.")

    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)

    # Suma de índices impares (1, 3, 5...) y pares (2, 4, 6...)
    suma_impares = np.sum(y[1:-1:2])
    suma_pares = np.sum(y[2:-2:2])

    # Fórmula: (h/3) * [f(x0) + 4*sum(impares) + 2*sum(pares) + f(xn)]
    integral = (h / 3.0) * (y[0] + 4 * suma_impares + 2 * suma_pares + y[-1])
    return integral


def leer_entero(mensaje, minimo, maximo):
    """Manejo de errores para menús interactivos."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Error: Ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Error crítico: Entrada inválida. Use solo números enteros.")


def mostrar_resultados_n100():
    """Resuelve la Parte 6 de la Guía: Resultados para n=100."""
    print("\n" + "=" * 60)
    print(" PARTE 6: RESULTADOS NUMÉRICOS OBTENIDOS (n = 100)")
    print("=" * 60)

    n = 100
    a, b = 0, np.pi / 2

    # Cálculos de las integrales
    I_trap = trapecio_compuesto(integrando, a, b, n)
    I_simp = simpson_13_compuesto(integrando, a, b, n)

    # Cálculo del período real usando el valor de Simpson (el más preciso)
    T_real = 4 * np.sqrt(L / g) * I_simp

    # Error relativo respecto a la aproximación de pequeñas oscilaciones (T0)
    error_relativo = abs((T_real - T0) / T_real) * 100

    print(f"{'Concepto':<35} | {'Valor Calculado':<15}")
    print("-" * 55)
    print(f"{'Integral I (Trapecio, n=100)':<35} | {I_trap:.9f}")
    print(f"{'Integral I (Simpson 1/3, n=100)':<35} | {I_simp:.9f}")
    print(f"{'Período Real T(60°)':<35} | {T_real:.6f} s")
    print(f"{'Error Relativo vs T0':<35} | {error_relativo:.4f} %")
    print("-" * 55)
    print(f"[INFO] T0 (Aproximación lineal) era: {T0:.6f} s")


def graficar_convergencia():
    """Resuelve la Parte 5 de la Guía: Gráfica Log-Log del Error."""
    print("\n[INFO] Calculando errores y generando gráfica Log-Log...")

    # Valor de referencia exacto usando scipy
    I_exacto, _ = quad(integrando, 0, np.pi / 2)

    n_valores = np.array([2, 4, 8, 16, 32, 64, 128, 256])
    err_trap = []
    err_simp = []

    for n in n_valores:
        I_t = trapecio_compuesto(integrando, 0, np.pi / 2, n)
        I_S = simpson_13_compuesto(integrando, 0, np.pi / 2, n)

        # Guardar errores absolutos (sumando 1e-16 para evitar log(0) por seguridad)
        err_trap.append(abs(I_t - I_exacto) + 1e-16)
        err_simp.append(abs(I_S - I_exacto) + 1e-16)

    # Configuración didáctica de la gráfica
    plt.figure(figsize=(9, 6))

    # Escala Log-Log para ambos ejes
    plt.loglog(n_valores, err_trap, marker='o', color='#e74c3c', linewidth=2, markersize=8,
               label='Trapecio Compuesto O(h²)')
    plt.loglog(n_valores, err_simp, marker='s', color='#2980b9', linewidth=2, markersize=8, label='Simpson 1/3 O(h⁴)')

    plt.title('Convergencia del Error Numérico (Escala Log-Log)', fontsize=14, fontweight='bold', pad=15)
    plt.xlabel('Número de subintervalos (n)', fontsize=12)
    plt.ylabel('Error Absoluto |I_num - I_exacto|', fontsize=12)

    plt.grid(True, which="both", ls="--", alpha=0.6)
    plt.legend(fontsize=11)

    # Anotaciones didácticas en la gráfica para explicar las pendientes
    plt.annotate('Caída lenta (Pendiente -2)', xy=(16, err_trap[3]), xytext=(32, err_trap[3] * 10),
                 arrowprops=dict(facecolor='#e74c3c', shrink=0.05, width=1.5, headwidth=6))

    plt.annotate('Caída drástica (Pendiente -4)', xy=(16, err_simp[3]), xytext=(32, err_simp[3] * 1000),
                 arrowprops=dict(facecolor='#2980b9', shrink=0.05, width=1.5, headwidth=6))

    plt.tight_layout()
    plt.show()


def menu_principal():
    print("======================================================")
    print("   Laboratorio: Integración Numérica (Trapecio y Simpson)")
    print("======================================================")
    print("1. Ver Tabla de Resultados Físicos (n = 100)")
    print("2. Generar Gráfica Log-Log de Convergencia del Error")
    print("3. Ejecutar todo")
    print("======================================================")

    opcion = leer_entero("Seleccione una opción (1-3): ", 1, 3)

    if opcion in [1, 3]:
        mostrar_resultados_n100()
    if opcion in [2, 3]:
        graficar_convergencia()


if __name__ == '__main__':
    menu_principal()