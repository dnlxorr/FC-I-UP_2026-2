"""Guía de laboratorio: Integración numérica aplicada al péndulo.
Requisitos: pip install numpy scipy matplotlib
Ejecución: python guia_integracion_numerica_completa.py
Genera: tres imágenes PNG y una tabla CSV en carpeta resultados_integracion.
"""
from pathlib import Path
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# PARÁMETROS DE LA GUÍA
L, g = 1.0, 9.81
theta_0 = np.deg2rad(60.0)
k = np.sin(theta_0 / 2.0)
a, b = 0.0, np.pi / 2.0
M2, M4 = 0.75, 3.5
SALIDA = Path(__file__).resolve().parent / 'resultados_integracion'
SALIDA.mkdir(exist_ok=True)


def integrando(phi):
    """Integrando del período exacto del péndulo."""
    return 1.0 / np.sqrt(1.0 - k**2 * np.sin(phi)**2)


def trapecio_compuesto(f, a, b, n):
    if not isinstance(n, (int, np.integer)) or n <= 0:
        raise ValueError('n debe ser entero positivo')
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    return (h / 2.0) * (y[0] + 2.0 * np.sum(y[1:-1]) + y[-1])


def simpson_13_compuesto(f, a, b, n):
    if not isinstance(n, (int, np.integer)) or n < 2 or n % 2:
        raise ValueError('Para Simpson, n debe ser entero par >= 2')
    h = (b - a) / n
    x = np.linspace(a, b, n + 1)
    y = f(x)
    suma_impares = np.sum(y[1:-1:2])
    suma_pares = np.sum(y[2:-1:2])
    return (h / 3.0) * (y[0] + 4.0 * suma_impares + 2.0 * suma_pares + y[-1])


def periodo(I):
    return 4.0 * np.sqrt(L / g) * I


def minimo_teorico(tolerancia):
    n_trap = math.floor(math.sqrt((b-a)**3 * M2 / (12*tolerancia))) + 1
    umbral_simp = ((b-a)**5 * M4 / (180*tolerancia))**.25
    n_simp = 2 * (math.floor(umbral_simp / 2) + 1)
    return n_trap, n_simp


def primera_particion_empirica(metodo, I_ref, tol=1e-8):
    # La búsqueda se realiza en n pares para comparar ambos métodos en igualdad.
    for n in range(2, 1002, 2):
        if abs(metodo(integrando, a, b, n)-I_ref) < tol:
            return n
    return None


def main():
    T0 = 2*np.pi*np.sqrt(L/g)
    I_ref, _ = quad(integrando, a, b, epsabs=1e-13, epsrel=1e-13)
    T_ref = periodo(I_ref)
    n_vals = np.array([2,4,8,16,32,64,128,256])
    datos = []
    for n in n_vals:
        it = trapecio_compuesto(integrando, a, b, int(n))
        iss = simpson_13_compuesto(integrando, a, b, int(n))
        datos.append((int(n), it, iss, abs(it-I_ref), abs(iss-I_ref)))

    print('=== GUÍA: INTEGRACIÓN NUMÉRICA ===')
    print(f'k = {k:.8f} | T0 = {T0:.12f} s | I_ref = {I_ref:.12f}')
    print(' n    I_trapecio      I_Simpson       Error_trapecio     Error_Simpson')
    for n, it, iss, et, es in datos:
        print(f'{n:3d}  {it:.12f}  {iss:.12f}  {et:.6e}   {es:.6e}')
    it100 = trapecio_compuesto(integrando,a,b,100)
    is100 = simpson_13_compuesto(integrando,a,b,100)
    print('\n=== RESULTADOS DEL PUNTO 6 (n=100) ===')
    print(f'Integral trapecio: {it100:.12f}')
    print(f'Integral Simpson:  {is100:.12f}')
    print(f'Período real de referencia: {T_ref:.12f} s')
    print(f'Período calculado Simpson:  {periodo(is100):.12f} s')
    print(f'Subestimación respecto al período real: {(T_ref-T0)/T_ref*100:.6f}%')
    for tol in (1e-4,1e-8):
        nt, ns = minimo_teorico(tol)
        print(f'Cotas para error integral < {tol:g}: Trapecio n >= {nt}; Simpson n >= {ns}')
    print('Primer n par experimental con error < 1e-8:')
    print('Trapecio:',primera_particion_empirica(trapecio_compuesto,I_ref))
    print('Simpson: ',primera_particion_empirica(simpson_13_compuesto,I_ref))
    print('Nota: errores en ~1e-15 están limitados por precisión de punto flotante.')

    with (SALIDA/'tabla_convergencia.csv').open('w', newline='',encoding='utf-8-sig') as fp:
        wr=csv.writer(fp)
        wr.writerow(['n','I_trapecio','I_Simpson','error_absoluto_trapecio','error_absoluto_Simpson'])
        wr.writerows(datos)

    # FIGURA 1: integrando del péndulo.
    phi=np.linspace(a,b,600)
    fig,ax=plt.subplots(figsize=(8,4.8))
    ax.plot(phi,integrando(phi),linewidth=2)
    ax.fill_between(phi,integrando(phi),alpha=.16)
    ax.set(xlabel='Ángulo de integración φ (rad)',ylabel='f(φ)',
           title='Función integrando del péndulo (amplitud inicial 60°)')
    ax.grid(alpha=.3)
    fig.tight_layout()
    fig.savefig(SALIDA/'01_funcion_integrando.png',dpi=200)
    plt.close(fig)

    # FIGURA 2: gráfica Log-Log solicitada por la guía.
    fig,ax=plt.subplots(figsize=(8.6,5.4))
    for j,simbolo,etiqueta in [(3,'o','Trapecio compuesto'),(4,'s','Simpson 1/3 compuesto')]:
        error=np.asarray([v[j] for v in datos])
        mask=error>0
        ax.loglog(n_vals[mask],error[mask],marker=simbolo,linewidth=1.8,label=etiqueta)
    ax.axhline(np.finfo(float).eps,linestyle=':',color='gray',label='Épsilon de máquina (referencia)')
    ax.set(xlabel='Número de subintervalos n',ylabel='Error absoluto |I_num - I_ref|',
           title='Convergencia numérica: Trapecio vs. Simpson')
    ax.grid(True,which='both',alpha=.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(SALIDA/'02_convergencia_loglog.png',dpi=200)
    plt.close(fig)

    # FIGURA 3: comparación física de períodos.
    fig,ax=plt.subplots(figsize=(7.6,4.7))
    etiquetas=['Modelo lineal T₀','Péndulo real T(60°)']
    valores=[T0,T_ref]
    barras=ax.bar(etiquetas,valores,width=.56)
    ax.set(ylabel='Período (s)',title='Influencia de la amplitud en el período del péndulo',ylim=(0,2.5))
    for barra, valor in zip(barras,valores):
        ax.text(barra.get_x()+barra.get_width()/2,valor+.035,f'{valor:.6f} s',ha='center',fontsize=10)
    ax.grid(axis='y',alpha=.25)
    fig.tight_layout()
    fig.savefig(SALIDA/'03_comparacion_periodos.png',dpi=200)
    plt.close(fig)
    print('\nArchivos generados en:', SALIDA)

if __name__=='__main__':
    main()
