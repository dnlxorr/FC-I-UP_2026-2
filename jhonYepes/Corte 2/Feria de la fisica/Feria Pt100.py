import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import linregress
from matplotlib.widgets import TextBox
import matplotlib.colors as mcolors
from matplotlib.collections import LineCollection

sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10})


def modulo_1_calculadora_gum():
    print("--- MÓDULO 1: CÁLCULO GUM COMPLETADO ---")
    datos_simulados = {
        'Temperatura_C': [0.0, 17.5, 89.0],
        'Voltaje_Promedio': [0.60, 0.70, 0.85],
        'Desviacion_Std': [0.015, 0.012, 0.018]
    }
    df = pd.DataFrame(datos_simulados)
    u_b = 0.01

    df['Incertidumbre_Combinada'] = np.sqrt((df['Desviacion_Std'] / np.sqrt(5)) ** 2 + (u_b / np.sqrt(3)) ** 2)
    df['Incertidumbre_Expandida'] = df['Incertidumbre_Combinada'] * 2
    return df


def pipeline_dashboard_feria(df_gum):
    slope, intercept, r_value, _, _ = linregress(df_gum['Temperatura_C'], df_gum['Voltaje_Promedio'])

    array_teorico_temperaturas = np.linspace(-200, 900, 100000)
    array_teorico_voltajes = (slope * array_teorico_temperaturas) + intercept
    tolerancia = 0.005

    fig = plt.figure(figsize=(13, 7))
    fig.canvas.manager.set_window_title('Dashboard - Pt100 y AD620')

    gs = fig.add_gridspec(1, 3, width_ratios=[4, 0.2, 1.5], wspace=0.3)
    plt.subplots_adjust(bottom=0.20, left=0.08, right=0.95, top=0.90)

    ax_main = fig.add_subplot(gs[0, 0])
    ax_thermo = fig.add_subplot(gs[0, 1])
    ax_info = fig.add_subplot(gs[0, 2])

    cmap = mcolors.LinearSegmentedColormap.from_list("therm", ["#0000ff", "#00ffff", "#ffff00", "#ff0000"])
    norm = plt.Normalize(-50, 150)

    temp_rango_completo = np.linspace(-200, 900, 2000)
    voltajes_modelo_completo = (slope * temp_rango_completo) + intercept

    puntos = np.array([temp_rango_completo, voltajes_modelo_completo]).T.reshape(-1, 1, 2)
    segmentos = np.concatenate([puntos[:-1], puntos[1:]], axis=1)

    linea_gradiente = LineCollection(segmentos, cmap=cmap, norm=norm, linestyle='--', alpha=0.6)
    linea_gradiente.set_array(temp_rango_completo)
    ax_main.add_collection(linea_gradiente)

    ax_main.errorbar(df_gum['Temperatura_C'], df_gum['Voltaje_Promedio'],
                     yerr=df_gum['Incertidumbre_Expandida'], fmt='o', color='red',
                     ecolor='black', elinewidth=2, capsize=5, label='Datos Experimentales (GUM)', zorder=5)

    ax_main.set_title('Curva de Calibración Interactiva', fontweight='bold')
    ax_main.set_xlabel('Temperatura (°C)', fontweight='bold')
    ax_main.set_ylabel('Voltaje (V)', fontweight='bold')
    ax_main.set_xlim(-20, 120)
    ax_main.set_ylim(0.55, 0.95)
    ax_main.legend(loc='lower right')

    historial_temp, historial_volt = [], []
    lista_textos_historial = []

    puntos_dinamicos, = ax_main.plot([], [], marker='*', color='black', markersize=16, linestyle='None', zorder=10)

    cuadro_resultado = ax_main.text(0.02, 0.92, 'Ingresa un voltaje abajo...', transform=ax_main.transAxes,
                                    bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))

    cuadro_historial = ax_main.text(0.02, 0.70, 'Registro Histórico:\n(Vacío)', transform=ax_main.transAxes,
                                    va='top', fontsize=9, bbox=dict(facecolor='#f0f8ff', alpha=0.8, edgecolor='blue'))

    cb = fig.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), cax=ax_thermo)
    ax_thermo.set_title('Rango', fontsize=9, fontweight='bold', pad=10)

    ax_info.axis('off')
    texto_matematico = (
        "ANÁLISIS METROLÓGICO\n------------------------------------\n\n"
        f"$V(T) = {slope:.5f} \\cdot T + {intercept:.4f}$\n\n"
        f"Sensibilidad: {(slope * 1000):.2f} mV/°C\n\n"
        f"$R^2 = {r_value ** 2:.4f}$\n\n"
        f"Incertidumbre (k=2): $\\pm {df_gum['Incertidumbre_Expandida'].mean():.4f}$ V\n\n"
        "Resolución: Búsqueda O(log n)"
    )
    ax_info.text(0, 0.5, texto_matematico, va='center', ha='left', fontsize=11,
                 bbox=dict(facecolor='#f8f9fa', edgecolor='#dee2e6', boxstyle='round,pad=1'))

    axbox = plt.axes([0.15, 0.05, 0.25, 0.06])
    text_box = TextBox(axbox, 'Multímetro (V): ', initial='')

    def procesar_medicion(texto_ingresado):
        if not texto_ingresado.strip(): return

        try:
            voltaje_medido = float(texto_ingresado.replace(',', '.'))
        except ValueError:
            cuadro_resultado.set_text(f"Error: '{texto_ingresado}' no es válido.")
            cuadro_resultado.get_bbox_patch().set_edgecolor('red')
            text_box.set_val('')
            fig.canvas.draw_idle()
            return

        low, high, indice_encontrado = 0, len(array_teorico_voltajes) - 1, -1

        while low <= high:
            mid = (low + high) // 2
            voltaje_mid = array_teorico_voltajes[mid]
            if abs(voltaje_mid - voltaje_medido) <= tolerancia:
                indice_encontrado = mid
                break
            elif voltaje_mid < voltaje_medido:
                low = mid + 1
            else:
                high = mid - 1

        if indice_encontrado != -1:
            temp_calculada = array_teorico_temperaturas[indice_encontrado]
            cuadro_resultado.set_text(f"Éxito: {voltaje_medido} V ➜ {temp_calculada:.2f} °C")
            cuadro_resultado.get_bbox_patch().set_edgecolor('green')

            historial_temp.append(temp_calculada)
            historial_volt.append(voltaje_medido)
            puntos_dinamicos.set_data(historial_temp, historial_volt)

            ax_thermo.axhline(y=temp_calculada, color='black', linewidth=2, alpha=0.8)

            lista_textos_historial.insert(0, f"• {voltaje_medido} V = {temp_calculada:.1f} °C")
            if len(lista_textos_historial) > 10: lista_textos_historial.pop()
            cuadro_historial.set_text("Registro Histórico:\n" + "\n".join(lista_textos_historial))

            lim_x_inf, lim_x_sup = ax_main.get_xlim()
            lim_y_inf, lim_y_sup = ax_main.get_ylim()
            if temp_calculada < lim_x_inf: lim_x_inf = temp_calculada - 15
            if temp_calculada > lim_x_sup: lim_x_sup = temp_calculada + 15
            if voltaje_medido < lim_y_inf: lim_y_inf = voltaje_medido - 0.05
            if voltaje_medido > lim_y_sup: lim_y_sup = voltaje_medido + 0.05
            ax_main.set_xlim(lim_x_inf, lim_x_sup)
            ax_main.set_ylim(lim_y_inf, lim_y_sup)

        else:
            temp_teorica = (voltaje_medido - intercept) / slope
            if temp_teorica > 850:
                motivo = f"Sensor Pt100 derretido (>850°C)"
            elif temp_teorica < -200:
                motivo = f"Sensor Pt100 congelado (<-200°C)"
            else:
                motivo = f"Anomalía electrónica detectada"

            cuadro_resultado.set_text(
                f"Física Inviable: {voltaje_medido} V equivale a ~{temp_teorica:.0f} °C\n({motivo})")
            cuadro_resultado.get_bbox_patch().set_edgecolor('orange')

        text_box.set_val('')
        fig.canvas.draw_idle()

    text_box.on_submit(procesar_medicion)
    plt.show()


if __name__ == "__main__":
    df_resultados = modulo_1_calculadora_gum()
    pipeline_dashboard_feria(df_resultados)