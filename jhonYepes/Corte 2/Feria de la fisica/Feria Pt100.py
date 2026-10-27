#1.Librerías y Configuración Visual
import pandas as pd # Maneja tablas de datos estructurados (DataFrames)
import numpy as np # Realiza cálculos matemáticos avanzados y crea arreglos numéricos rápidos
import matplotlib.pyplot as plt # El motor principal para dibujar las gráficas y la ventana
import seaborn as sns # Añade estilos y colores bonitos predeterminados a Matplotlib
from scipy.stats import linregress # Calcula la ecuación de la recta (regresión lineal)
from matplotlib.widgets import TextBox # Trae la caja de texto interactiva para el jurado
import matplotlib.colors as mcolors # Permite crear escalas de colores personalizadas
from matplotlib.collections import LineCollection # Permite dibujar líneas que cambian de color por segmentos

sns.set_theme(style="whitegrid") # Aplica un fondo blanco con cuadrícula gris a la gráfica
plt.rcParams.update({'font.size': 10}) # Ajusta el tamaño de letra general de toda la ventana a 10

#2.Módulo GUM (Cálculo Metrológico)
def modulo_1_calculadora_gum():
    print("--- MÓDULO 1: CÁLCULO GUM COMPLETADO ---")  # Imprime en la consola oculta para debug
    datos_simulados = {  # Crea un diccionario con tus 3 mediciones físicas reales
        'Temperatura_C': [0.0, 17.5, 89.0],
        'Voltaje_Promedio': [0.60, 0.70, 0.85],
        'Desviacion_Std': [0.015, 0.012, 0.018]  # Representa qué tanto varió el multímetro
    }
    df = pd.DataFrame(datos_simulados)  # Convierte el diccionario en una tabla de Pandas
    u_b = 0.01  # Define la incertidumbre de fábrica del multímetro (Tipo B)

    # Aplica la fórmula GUM: Raíz cuadrada de la suma de (Incertidumbre A^2 + Incertidumbre B^2)
    df['Incertidumbre_Combinada'] = np.sqrt((df['Desviacion_Std'] / np.sqrt(5)) ** 2 + (u_b / np.sqrt(3)) ** 2)
    df['Incertidumbre_Expandida'] = df['Incertidumbre_Combinada'] * 2  # Multiplica por factor k=2 (95% de confianza)
    return df  # Devuelve la tabla con los cálculos listos

#3.Preparación del Dashboard y Modelo Matemático
def pipeline_dashboard_feria(df_gum):
    # Extrae la pendiente (slope), el corte (intercept) y la precisión (r_value) de tus datos GUM
    slope, intercept, r_value, _, _ = linregress(df_gum['Temperatura_C'], df_gum['Voltaje_Promedio'])

    # Crea la base de datos de 100,000 puntos para la búsqueda binaria
    array_teorico_temperaturas = np.linspace(-200, 900, 100000)  # Rango de temperaturas (eje X)
    array_teorico_voltajes = (slope * array_teorico_temperaturas) + intercept  # Rango de voltajes (eje Y)
    tolerancia = 0.005  # Margen de error al buscar el voltaje exacto en el arreglo

    fig = plt.figure(figsize=(13, 7))  # Crea la ventana principal de 13x7 pulgadas
    fig.canvas.manager.set_window_title('Dashboard - Pt100 y AD620')  # Le pone título a la ventana de Windows

    # GridSpec divide la ventana en 3 columnas: [4 (Gráfica), 0.2 (Termómetro), 1.5 (Texto)]
    gs = fig.add_gridspec(1, 3, width_ratios=[4, 0.2, 1.5], wspace=0.3)
    plt.subplots_adjust(bottom=0.20, left=0.08, right=0.95,
                        top=0.90)  # Ajusta los márgenes para que quepa la caja de texto

    ax_main = fig.add_subplot(gs[0, 0])  # Asigna la columna 0 a la gráfica principal
    ax_thermo = fig.add_subplot(gs[0, 1])  # Asigna la columna 1 al termómetro
    ax_info = fig.add_subplot(gs[0, 2])  # Asigna la columna 2 a los cálculos

#4. Construcción Visual: Línea de Gradiente y Datos
    # Define la paleta de colores del termómetro: Azul, Cian, Amarillo, Rojo
    cmap = mcolors.LinearSegmentedColormap.from_list("therm", ["#0000ff", "#00ffff", "#ffff00", "#ff0000"])
    norm = plt.Normalize(-50, 150)  # Le dice al color que -50 es azul profundo y 150 es rojo profundo

    temp_rango_completo = np.linspace(-200, 900, 2000)  # Crea los puntos para dibujar la línea visual
    voltajes_modelo_completo = (slope * temp_rango_completo) + intercept  # Calcula el voltaje de esa línea

    # Esta matemática compleja transforma los puntos XY individuales en "segmentos" conectables
    puntos = np.array([temp_rango_completo, voltajes_modelo_completo]).T.reshape(-1, 1, 2)
    segmentos = np.concatenate([puntos[:-1], puntos[1:]], axis=1)

    # Aplica la paleta de colores a los segmentos y los dibuja como una línea punteada semitransparente
    linea_gradiente = LineCollection(segmentos, cmap=cmap, norm=norm, linestyle='--', alpha=0.6)
    linea_gradiente.set_array(temp_rango_completo)  # Mapea la temperatura al color correspondiente
    ax_main.add_collection(linea_gradiente)  # Pega la línea multicolor en la gráfica

    # Dibuja los 3 puntos rojos experimentales y sus barras de error negras usando la tabla GUM
    ax_main.errorbar(df_gum['Temperatura_C'], df_gum['Voltaje_Promedio'],
                     yerr=df_gum['Incertidumbre_Expandida'], fmt='o', color='red',
                     ecolor='black', elinewidth=2, capsize=5, label='Datos Experimentales (GUM)', zorder=5)

    #5. Configuración de Paneles y Textos
    ax_main.set_title('Curva de Calibración Interactiva', fontweight='bold')  # Título de la gráfica
    ax_main.set_xlabel('Temperatura (°C)', fontweight='bold')  # Nombre eje X
    ax_main.set_ylabel('Voltaje (V)', fontweight='bold')  # Nombre eje Y
    ax_main.set_xlim(-20, 120)  # Fija la cámara inicial de X
    ax_main.set_ylim(0.55, 0.95)  # Fija la cámara inicial de Y
    ax_main.legend(loc='lower right')  # Pone el cuadro de leyendas en la esquina inferior derecha

    historial_temp, historial_volt = [], []  # Listas vacías donde se guardarán los números ingresados
    lista_textos_historial = []  # Lista vacía donde se guardará el texto visual del historial

    # Crea un objeto gráfico para las estrellas negras interactivo, pero inicia vacío ([], [])
    puntos_dinamicos, = ax_main.plot([], [], marker='*', color='black', markersize=16, linestyle='None', zorder=10)

    # Dibuja el cuadro de notificaciones (arriba a la izquierda)
    cuadro_resultado = ax_main.text(0.02, 0.92, 'Ingresa un voltaje abajo...', transform=ax_main.transAxes,
                                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

    # Dibuja el cuadro del registro histórico (un poco más abajo)
    cuadro_historial = ax_main.text(0.02, 0.70, 'Registro Histórico:\n(Vacío)', transform=ax_main.transAxes,
                                    va='top', fontsize=9, bbox=dict(facecolor='#f0f8ff', alpha=0.8, edgecolor='blue'))

    # Dibuja el termómetro lateral con su escala de color
    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax_thermo)
    ax_thermo.set_title('Rango', fontsize=9, fontweight='bold', pad=10)  # Título del termómetro

    ax_info.axis('off')  # Borra los ejes del tercer panel porque solo queremos texto flotante, no una gráfica
    texto_matematico = (
        "ANÁLISIS METROLÓGICO\n------------------------------------\n\n"
        f"$V(T) = {slope:.5f} \\cdot T + {intercept:.4f}$\n\n"
        f"Sensibilidad: {(slope * 1000):.2f} mV/°C\n\n"
        f"$R^2 = {r_value ** 2:.4f}$\n\n"
        f"Incertidumbre (k=2): $\\pm {df_gum['Incertidumbre_Expandida'].mean():.4f}$ V\n\n"
        "Resolución: Búsqueda O(log n)"
    )  # (Este bloque de texto ya lo conoces, arma el resumen de ecuaciones con format strings)
    # Pega el resumen matemático en el tercer panel
    ax_info.text(0, 0.5, texto_matematico, va='center', ha='left', fontsize=11,
                 bbox=dict(facecolor='#f8f9fa', edgecolor='#dee2e6', boxstyle='round,pad=1'))

   #6. El Corazón Interactivo (Widget y Búsqueda Binaria)
    axbox = plt.axes([0.15, 0.05, 0.25, 0.06])  # Dibuja un rectángulo en la parte baja de la ventana
    text_box = TextBox(axbox, 'Multímetro (V): ', initial='')  # Mete el widget de texto en ese rectángulo

    def procesar_medicion(texto_ingresado):  # Función que se dispara al dar "Enter" en la caja
        if not texto_ingresado.strip(): return  # Si está vacío o son espacios, aborta sin hacer nada

        try:
            voltaje_medido = float(texto_ingresado.replace(',', '.'))  # Intenta convertir el texto a número decimal
        except ValueError:  # Si meten letras o símbolos raros, el programa cae aquí
            cuadro_resultado.set_text(f"Error: '{texto_ingresado}' no es válido.")  # Muestra el error
            cuadro_resultado.get_bbox_patch().set_edgecolor('red')  # Pinta el borde de rojo
            text_box.set_val('')  # Borra la caja
            fig.canvas.draw_idle()  # Refresca la pantalla
            return  # Aborta la función

        # Inicia algoritmo de Búsqueda Binaria O(log n)
        low, high, indice_encontrado = 0, len(array_teorico_voltajes) - 1, -1

        while low <= high:  # Mientras el límite inferior no cruce al superior
            mid = (low + high) // 2  # Encuentra la mitad del arreglo
            voltaje_mid = array_teorico_voltajes[mid]  # Mira qué voltaje hay en esa mitad
            if abs(voltaje_mid - voltaje_medido) <= tolerancia:  # Si es igual a lo que ingresó el jurado
                indice_encontrado = mid  # ¡Lo encontró! Guarda el índice
                break  # Rompe el ciclo while
            elif voltaje_mid < voltaje_medido:
                low = mid + 1  # Si el voltaje buscado es mayor, descarta la mitad de abajo
            else:
                high = mid - 1  # Si es menor, descarta la mitad de arriba

#7. Respuesta Visual y Auto-Zoom
        if indice_encontrado != -1:  # Si el índice cambió, significa que encontró el voltaje
            temp_calculada = array_teorico_temperaturas[indice_encontrado]  # Saca la temperatura equivalente
            cuadro_resultado.set_text(
                f"Éxito: {voltaje_medido} V ➜ {temp_calculada:.2f} °C")  # Muestra mensaje de éxito
            cuadro_resultado.get_bbox_patch().set_edgecolor('green')  # Pinta el borde de verde

            historial_temp.append(temp_calculada)  # Guarda la temperatura en la memoria RAM
            historial_volt.append(voltaje_medido)  # Guarda el voltaje
            puntos_dinamicos.set_data(historial_temp, historial_volt)  # Dibuja TODAS las estrellas acumuladas

            # Pinta una raya negra permanente en el termómetro indicando el nivel térmico
            ax_thermo.axhline(y=temp_calculada, color='black', linewidth=2, alpha=0.8)

            # Mete el texto a la lista del historial visual (ej. • 0.5 V = -40 °C)
            lista_textos_historial.insert(0, f"• {voltaje_medido} V = {temp_calculada:.1f} °C")
            if len(lista_textos_historial) > 10: lista_textos_historial.pop()  # Si hay más de 10, borra el más viejo
            cuadro_historial.set_text("Registro Histórico:\n" + "\n".join(lista_textos_historial))  # Actualiza la caja

            # --- Auto-Zoom Dinámico ---
            lim_x_inf, lim_x_sup = ax_main.get_xlim()  # Pide los límites actuales de la cámara X
            lim_y_inf, lim_y_sup = ax_main.get_ylim()  # Pide los límites actuales de la cámara Y

            # Si el nuevo punto se sale de la cámara actual, empuja el límite 15 grados / 0.05 voltios más allá
            if temp_calculada < lim_x_inf: lim_x_inf = temp_calculada - 15
            if temp_calculada > lim_x_sup: lim_x_sup = temp_calculada + 15
            if voltaje_medido < lim_y_inf: lim_y_inf = voltaje_medido - 0.05
            if voltaje_medido > lim_y_sup: lim_y_sup = voltaje_medido + 0.05

            ax_main.set_xlim(lim_x_inf, lim_x_sup)  # Aplica la nueva cámara X (Zoom out)
            ax_main.set_ylim(lim_y_inf, lim_y_sup)  # Aplica la nueva cámara Y

#8. Lógica Física Inviable y Ejecución
        else:  # Si el While loop terminó sin encontrar nada, cayó fuera de los límites del Pt100
            temp_teorica = (voltaje_medido - intercept) / slope  # Aplica y=mx+b invertida para saber qué temp sería
            if temp_teorica > 850:
                motivo = f"Sensor Pt100 derretido (>850°C)"  # Si supera 850, el platino muere
            elif temp_teorica < -200:
                motivo = f"Sensor Pt100 congelado (<-200°C)"  # Si baja de -200, límite criogénico
            else:
                motivo = f"Anomalía electrónica detectada"  # Fallo del amplificador AD620

            cuadro_resultado.set_text(
                f"Física Inviable: {voltaje_medido} V equivale a ~{temp_teorica:.0f} °C\n({motivo})")
            cuadro_resultado.get_bbox_patch().set_edgecolor('orange')  # Pinta el borde naranja

        text_box.set_val('')  # Limpia la caja interactiva para que el jurado escriba rápido el siguiente
        fig.canvas.draw_idle()  # Refuerza a Windows que redibuje toda la pantalla

    text_box.on_submit(procesar_medicion)  # Conecta la tecla "Enter" de la caja con la función de arriba
    plt.show()  # Inicia el motor gráfico de Matplotlib y despliega la ventana


if __name__ == "__main__":  # Esta línea le dice a Python: "Si alguien ejecuta este archivo directamente..."
    df_resultados = modulo_1_calculadora_gum()  # Llama al Módulo 1 (genera los datos)
    pipeline_dashboard_feria(df_resultados)  # Le entrega los datos al Dashboard interactivo