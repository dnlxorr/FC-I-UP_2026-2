"""
Guía de Laboratorio: Integración Numérica
Física Computacional I - Regla del Trapecio y Simpson 1/3 (compuestas)
Período exacto del péndulo simple: T = 4*sqrt(L/g) * K(k),  k = sin(theta_0/2)

Contenido:
  Parte 1  : parámetros y n mínimo (cotas teóricas)
  Parte 2  : algoritmos de integración (vectorizados con NumPy)
  Parte 3  : convergencia del error + gráfica log-log (rojo = Trapecio, azul = Simpson)
  Parte 6  : resultados con n = 100
  Pregunta 2: n necesario para tolerancia 1e-8
  Extra    : verificación de los órdenes O(h^2) y O(h^4) con una integral NO periódica
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# ======================================================================
# --- Parámetros Físicos y constantes ---
# ======================================================================
L = 1.0
g = 9.81
theta_0 = np.radians(60)
k = np.sin(theta_0 / 2.0)               # k = sin(30°) = 0.5
T0 = 2 * np.pi * np.sqrt(L / g)         # período de pequeñas oscilaciones

A, B = 0.0, np.pi / 2                    # límites de la integral elíptica
M2, M4 = 0.75, 3.5                       # cotas de las derivadas (dadas en la guía)

N_VALORES = np.array([2, 4, 8, 16, 32, 64, 128, 256])
EPS = np.finfo(float).eps                # épsilon de máquina (≈ 2.2e-16)

ROJO = '#E41A1C'                         # Trapecio
AZUL = '#1F4FD8'                         # Simpson 1/3
GRIS = '0.45'

MOSTRAR_GRAFICA = True                   # False -> solo guarda la imagen


def integrando(phi):
    """Función f(phi) para la integral elíptica del péndulo."""
    return 1.0 / np.sqrt(1.0 - (k**2) * (np.sin(phi)**2))


# ======================================================================
# PARTE 2: Algoritmos de integración (vectorizados con NumPy)
# ======================================================================
def trapecio_compuesto(f, a, b, n):
    """Calcula la integral usando la Regla del Trapecio Compuesto."""
    if n < 1:
        raise ValueError("El número de subintervalos n debe ser >= 1.")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    # T = (h/2) * [f0 + 2*(f1 + ... + f_{n-1}) + fn]
    return (h / 2.0) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])


def simpson_13_compuesto(f, a, b, n):
    """Calcula la integral usando Simpson 1/3 (n debe ser par)."""
    if n < 2 or n % 2 != 0:
        raise ValueError("El número de subintervalos n debe ser PAR (n >= 2).")
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    # Índices impares (1, 3, ..., n-1) -> peso 4
    # Índices pares interiores (2, 4, ..., n-2) -> peso 2
    suma_impares = np.sum(y[1:-1:2])
    suma_pares = np.sum(y[2:-2:2])
    return (h / 3.0) * (y[0] + 4 * suma_impares + 2 * suma_pares + y[-1])


# ======================================================================
# PARTE 1: n mínimo según las cotas teóricas de error
# ======================================================================
def n_minimo_trapecio(tol, a=A, b=B, M2=M2):
    """|E_T| <= (b-a)^3 / (12 n^2) * M2 < tol  ->  n > sqrt((b-a)^3 M2 / (12 tol))."""
    return int(np.ceil(np.sqrt((b - a)**3 * M2 / (12 * tol))))


def n_minimo_simpson(tol, a=A, b=B, M4=M4):
    """|E_S| <= (b-a)^5 / (180 n^4) * M4 < tol  ->  n > ((b-a)^5 M4 / (180 tol))^(1/4).
    Simpson exige n par, así que se sube al siguiente par si hace falta."""
    n = int(np.ceil(((b - a)**5 * M4 / (180 * tol))**0.25))
    return n + (n % 2)


def parte1():
    print("=" * 62)
    print(" PARTE 1: PARÁMETROS Y n MÍNIMO (error < 1e-4)")
    print("=" * 62)
    print(f"k = sin(30°)                   = {k:.4f}")
    print(f"T0 = 2*pi*sqrt(L/g)            = {T0:.4f} s")
    print(f"n mínimo Trapecio  (cota)      = {n_minimo_trapecio(1e-4)}")
    print(f"n mínimo Simpson   (cota, par) = {n_minimo_simpson(1e-4)}")


# ======================================================================
# PARTE 3: Análisis de convergencia del error
# ======================================================================
def errores_convergencia(f, a, b, n_valores, I_exacto):
    """Errores absolutos de Trapecio y Simpson para cada n."""
    err_trap = np.array([abs(trapecio_compuesto(f, a, b, n) - I_exacto) for n in n_valores])
    err_simp = np.array([abs(simpson_13_compuesto(f, a, b, n) - I_exacto) for n in n_valores])
    return err_trap, err_simp


def pendiente_ajustada(n_valores, err, piso=1e-14):
    """Pendiente log-log (ajuste lineal) usando solo los puntos que están
    por encima del piso del redondeo de punto flotante. Devuelve NaN si
    quedan menos de 2 puntos."""
    mascara = err > piso
    if mascara.sum() < 2:
        return np.nan
    return np.polyfit(np.log(n_valores[mascara]), np.log(err[mascara]), 1)[0]


def tabla_errores(titulo, n_valores, err_trap, err_simp):
    print(f"\n{titulo}")
    print(f"{'n':>5} {'Error Trapecio':>18} {'Error Simpson':>18}")
    for n, et, es in zip(n_valores, err_trap, err_simp):
        print(f"{n:>5} {et:>18.3e} {es:>18.3e}")
    print(f"Pendiente log-log (puntos con error > 1e-14): "
          f"Trapecio = {pendiente_ajustada(n_valores, err_trap):.2f} | "
          f"Simpson = {pendiente_ajustada(n_valores, err_simp):.2f}")


def dibujar_convergencia(ax, n_valores, err_trap, err_simp, titulo):
    """Gráfica log-log: Trapecio en rojo, Simpson en azul."""
    ax.loglog(n_valores, np.maximum(err_trap, 1e-17), 'o-', color=ROJO, lw=2, ms=7,
              label=r'Trapecio  $O(h^2)$')
    ax.loglog(n_valores, np.maximum(err_simp, 1e-17), 's-', color=AZUL, lw=2, ms=7,
              label=r'Simpson 1/3  $O(h^4)$')
    # Rectas de referencia (desplazadas x4 respecto al primer punto para que
    # no queden tapadas por las curvas cuando éstas siguen la pendiente teórica)
    ax.loglog(n_valores, 4 * err_trap[0] * (n_valores / n_valores[0])**-2.0,
              '--', color=ROJO, alpha=0.45, lw=1.3, label='pendiente −2')
    ax.loglog(n_valores, 4 * err_simp[0] * (n_valores / n_valores[0])**-4.0,
              '--', color=AZUL, alpha=0.45, lw=1.3, label='pendiente −4')
    # Piso del redondeo de punto flotante (IEEE 754, doble precisión)
    ax.axhline(EPS, color=GRIS, ls='-.', lw=1.1, label=f'ε de máquina ({EPS:.1e})')
    ax.set_ylim(1e-18, 1e1)
    ax.set_xlabel('n (subintervalos)')
    ax.set_ylabel('Error absoluto')
    ax.set_title(titulo, fontsize=11)
    ax.grid(True, which='both', alpha=0.3)


# ======================================================================
# PARTE 6: Resultados con n = 100 subintervalos
# ======================================================================
def parte6(n=100):
    I_trap = trapecio_compuesto(integrando, A, B, n)
    I_simp = simpson_13_compuesto(integrando, A, B, n)
    T_real = 4 * np.sqrt(L / g) * I_simp               # T(60°) = 4*sqrt(L/g)*I
    err_rel_T = (T_real - T0) / T_real * 100           # % de subestimación del modelo lineal
    err_rel_T0 = (T_real - T0) / T0 * 100              # convención alternativa

    print("\n" + "=" * 62)
    print(f" PARTE 6: RESULTADOS NUMÉRICOS (n = {n})")
    print("=" * 62)
    print(f"{'Concepto':<34} | {'Valor calculado':>20}")
    print("-" * 58)
    print(f"{'Integral I (Trapecio)':<34} | {I_trap:>20.10f}")
    print(f"{'Integral I (Simpson 1/3)':<34} | {I_simp:>20.10f}")
    print(f"{'Período real T(60°) [s]':<34} | {T_real:>20.4f}")
    print(f"{'Error relativo vs T0 (sobre T) %':<34} | {err_rel_T:>20.2f}")
    print(f"{'Error relativo (sobre T0) %':<34} | {err_rel_T0:>20.2f}")


# ======================================================================
# PREGUNTA 2: n necesario para tolerancia 1e-8 (cotas teóricas)
# ======================================================================
def pregunta2(tol=1e-8):
    n_t, n_s = n_minimo_trapecio(tol), n_minimo_simpson(tol)
    print("\n" + "=" * 62)
    print(f" PREGUNTA 2: TOLERANCIA {tol:.0e} (según cotas teóricas)")
    print("=" * 62)
    print(f"Trapecio: n ≈ {n_t}")
    print(f"Simpson : n ≈ {n_s}   (≈ {n_t / n_s:.0f} veces menos subintervalos)")


# ======================================================================
# PROGRAMA PRINCIPAL
# ======================================================================
def main():
    parte1()

    # --- Parte 3: péndulo (integrando periódica) ---
    I_exacto, _ = quad(integrando, A, B)               # valor de referencia
    err_trap, err_simp = errores_convergencia(integrando, A, B, N_VALORES, I_exacto)
    print("\n" + "=" * 62)
    print(" PARTE 3: CONVERGENCIA DEL ERROR")
    print("=" * 62)
    print(f"I_exacto (quad) = {I_exacto:.16f}")
    tabla_errores("Péndulo simple (integrando periódica):", N_VALORES, err_trap, err_simp)

    # --- Extra: integral NO periódica, donde sí se ven las pendientes -2 y -4 ---
    I_exp = np.e - 1.0                                  # ∫0^1 e^x dx (exacta)
    err_trap_e, err_simp_e = errores_convergencia(np.exp, 0.0, 1.0, N_VALORES, I_exp)
    tabla_errores("Verificación con  ∫0^1 e^x dx  (no periódica):",
                  N_VALORES, err_trap_e, err_simp_e)

    parte6()
    pregunta2()

    # --- Gráfica (se muestra al final para que no bloquee las salidas anteriores) ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
    dibujar_convergencia(ax1, N_VALORES, err_trap, err_simp,
                         r'Péndulo simple ($\theta_0 = 60°$): integrando periódica')
    dibujar_convergencia(ax2, N_VALORES, err_trap_e, err_simp_e,
                         r'Verificación: $\int_0^1 e^x\,dx$ (no periódica)')
    fig.suptitle('Convergencia del error numérico (escala log-log)',
                 fontsize=13, fontweight='bold')
    handles, etiquetas = ax1.get_legend_handles_labels()
    fig.legend(handles, etiquetas, loc='lower center', ncol=5, fontsize=9.5, frameon=False)
    fig.tight_layout(rect=[0, 0.07, 1, 0.95])
    fig.savefig('convergencia_loglog.png', dpi=150)
    print("\n[INFO] Gráfica guardada en 'convergencia_loglog.png'")
    if MOSTRAR_GRAFICA:
        plt.show()


if __name__ == '__main__':
    main()
