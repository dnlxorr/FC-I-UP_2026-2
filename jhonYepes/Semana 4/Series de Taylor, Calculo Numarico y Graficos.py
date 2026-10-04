# ==========================================
# JhonAlexanderYepesArias: Series de Taylor Interactivas (Visualización de Error)
# ==========================================
import math
import numpy as np
import matplotlib.pyplot as plt


def taylor_seno(x, terminos):
    """Calcula sen(x) usando serie de Taylor con n términos."""
    aproximacion = 0
    for n in range(terminos):
        aproximacion += ((-1) ** n * x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    return aproximacion


def taylor_exponencial(x, terminos):
    """Calcula e^x usando serie de Taylor con n términos."""
    aproximacion = 0
    for n in range(terminos):
        aproximacion += (x ** n) / math.factorial(n)
    return aproximacion


def leer_entero(mensaje, minimo, maximo):
    """Manejo de errores para entradas de menús y cantidad de términos."""
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            else:
                print(f"Error: Ingrese un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Error crítico: Entrada inválida. Use solo números enteros sin letras.")


def leer_flotante(mensaje):
    """Manejo de errores para el punto de evaluación x."""
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Error crítico: Entrada inválida. Use solo números decimales o enteros.")


def procesar_y_mostrar_tabla(nombre_funcion, funcion_taylor, valor_exacto, x, max_terminos):
    """Genera la tabla en consola y retorna los datos para la gráfica de error."""
    print(f"\n--- Tabla de Error: {nombre_funcion} (x = {x}) ---")
    print(f"{'Términos':<10} | {'Valor Taylor':<15} | {'Valor Exacto':<15} | {'% Error':<15}")
    print("-" * 65)

    lista_terminos = []
    lista_errores = []

    for i in range(1, max_terminos + 1):
        valor_taylor = funcion_taylor(x, i)

        # Evitar división por cero
        if valor_exacto != 0:
            error_porcentual = abs((valor_exacto - valor_taylor) / valor_exacto) * 100
        else:
            error_porcentual = abs(valor_exacto - valor_taylor) * 100

        print(f"{i:<10} | {valor_taylor:<15.6f} | {valor_exacto:<15.6f} | {error_porcentual:<15.6f}%")

        lista_terminos.append(i)
        # Se guarda el error (añadiendo un valor mínimo para evitar error matemático al graficar log(0))
        lista_errores.append(error_porcentual if error_porcentual > 0 else 1e-15)

    return lista_terminos, lista_errores


def analizar_y_graficar_interactivo():
    print("======================================================")
    print("      Análisis Didáctico de Series de Taylor          ")
    print("======================================================")
    print("Este programa compara el valor real de una función")
    print("matemática con una aproximación construida paso a paso.")
    print("======================================================\n")

    print("1. Función Seno, sin(x)")
    print("2. Función Exponencial, e^x")
    print("3. Ambas")
    opcion = leer_entero("Seleccione la función a analizar (1-3): ", 1, 3)

    print("\n------------------------------------------------------")
    print("[INFO sobre la variable 'x']:")
    print("La 'x' es el punto específico donde queremos calcular el valor")
    print("de la función. Por ejemplo, si x=3.14 en el seno, estamos")
    print("calculando cuánto vale el seno de 3.14 radianes.")
    pto_eval = leer_flotante("-> Ingrese el valor numérico de 'x' a evaluar (ej. 3.5): ")

    print("\n------------------------------------------------------")
    print("[INFO sobre los 'términos']:")
    print("Una Serie de Taylor construye la gráfica sumando pequeños")
    print("bloques matemáticos llamados 'términos'.")
    print("- MÁS términos = Mayor precisión, la aproximación se pega más al valor real.")
    print("- MENOS términos = Menor precisión, el cálculo es rápido pero inexacto.")
    max_terminos = leer_entero("-> Ingrese la cantidad máxima de términos a calcular (ej. 5): ", 1, 50)

    x_vals = np.linspace(-2 * np.pi, 2 * np.pi, 100)

    # Configuración dinámica del panel de gráficas
    if opcion == 1:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        ax_func_seno, ax_err_seno = axs[0], axs[1]
    elif opcion == 2:
        fig, axs = plt.subplots(1, 2, figsize=(12, 5))
        ax_func_exp, ax_err_exp = axs[0], axs[1]
    elif opcion == 3:
        fig, axs = plt.subplots(2, 2, figsize=(12, 10))
        ax_func_seno, ax_err_seno = axs[0, 0], axs[0, 1]
        ax_func_exp, ax_err_exp = axs[1, 0], axs[1, 1]

    # --- PROCESAMIENTO DE LA FUNCIÓN SENO ---
    if opcion in [1, 3]:
        seno_real = math.sin(pto_eval)
        term_seno, err_seno = procesar_y_mostrar_tabla("Seno", taylor_seno, seno_real, pto_eval, max_terminos)

        # Gráfica de la Función
        ax_func_seno.plot(x_vals, np.sin(x_vals), label='math.sin(x) (Exacto)', color='black', linewidth=6, alpha=0.2)
        mitad = max(1, max_terminos // 2)
        ax_func_seno.plot(x_vals, [taylor_seno(x, mitad) for x in x_vals], label=f'Taylor ({mitad} terms)',
                          linestyle='--')
        ax_func_seno.plot(x_vals, [taylor_seno(x, max_terminos) for x in x_vals],
                          label=f'Taylor ({max_terminos} terms)', linestyle='--')
        ax_func_seno.set_title("Aproximación de sin(x)")
        ax_func_seno.set_ylim(-2, 2)
        ax_func_seno.legend()
        ax_func_seno.grid(True)

        # Gráfica del Error Porcentual
        ax_err_seno.semilogy(term_seno, err_seno, marker='o', color='red', linestyle='-')
        ax_err_seno.set_title(f"Caída del Error % (x = {pto_eval})")
        ax_err_seno.set_xlabel("Número de Términos (N)")
        ax_err_seno.set_ylabel("Error % (Escala Logarítmica)")
        ax_err_seno.grid(True, which="both", ls="--", alpha=0.5)

    # --- PROCESAMIENTO DE LA FUNCIÓN EXPONENCIAL ---
    if opcion in [2, 3]:
        exp_real = math.exp(pto_eval)
        term_exp, err_exp = procesar_y_mostrar_tabla("Exponencial (Euler)", taylor_exponencial, exp_real, pto_eval,
                                                     max_terminos)

        # Gráfica de la Función
        ax_func_exp.plot(x_vals, np.exp(x_vals), label='math.exp(x) (Exacto)', color='black', linewidth=6, alpha=0.2)
        mitad = max(1, max_terminos // 2)
        ax_func_exp.plot(x_vals, [taylor_exponencial(x, mitad) for x in x_vals], label=f'Taylor ({mitad} terms)',
                         linestyle='--')
        ax_func_exp.plot(x_vals, [taylor_exponencial(x, max_terminos) for x in x_vals],
                         label=f'Taylor ({max_terminos} terms)', linestyle='--')
        ax_func_exp.set_title("Aproximación de e^x")
        ax_func_exp.set_ylim(0, 100)
        ax_func_exp.legend()
        ax_func_exp.grid(True)

        # Gráfica del Error Porcentual
        ax_err_exp.semilogy(term_exp, err_exp, marker='o', color='blue', linestyle='-')
        ax_err_exp.set_title(f"Caída del Error % (x = {pto_eval})")
        ax_err_exp.set_xlabel("Número de Términos (N)")
        ax_err_exp.set_ylabel("Error % (Escala Logarítmica)")
        ax_err_exp.grid(True, which="both", ls="--", alpha=0.5)

    print("\n------------------------------------------------------")
    print("[INFO sobre las Gráficas que están a punto de abrirse]:")
    print("1. GRÁFICAS DE FUNCIÓN (Izquierda):")
    print("   - Camino GRIS de fondo: Es la función matemática real.")
    print("   - Líneas PUNTEADAS: Son las aproximaciones. Notarás que a más")
    print("     términos, la línea punteada sigue mejor el camino gris.")
    print("2. GRÁFICAS DE ERROR (Derecha):")
    print("   - Muestra cómo el porcentaje de error se desploma hacia cero")
    print("     a medida que agregas más términos.")
    print("   - Usa escala logarítmica (los saltos van de 100% a 10%, 1%, etc.)")
    print("-> Cierra la ventana de las gráficas para finalizar el programa.")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    analizar_y_graficar_interactivo()