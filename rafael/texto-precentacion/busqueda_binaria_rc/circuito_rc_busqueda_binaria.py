"""Simulación de carga/descarga RC y búsqueda binaria de voltajes."""
import math


def leer_float(mensaje, minimo=0, inclusivo=False):
    while True:
        try:
            valor = float(input(mensaje))
            if not math.isfinite(valor) or (valor < minimo if inclusivo else valor <= minimo):
                print(f"Error: ingrese un número {'mayor o igual' if inclusivo else 'mayor'} que {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: debe ingresar un valor numérico.")


def leer_modo():
    while True:
        opcion = input("Seleccione el modo (1 = Carga, 2 = Descarga): ").strip()
        if opcion in ("1", "2"):
            return int(opcion)
        print("Error: seleccione 1 o 2.")


def voltaje_capacitor(t, R, C, V0, modo):
    tau = R * C
    if modo == 1:
        return V0 * (-math.expm1(-t / tau))
    return V0 * math.exp(-t / tau)


def corriente(t, R, C, V0, modo):
    magnitud = (V0 / R) * math.exp(-t / (R * C))
    return magnitud if modo == 1 else -magnitud


def buscar_voltaje(vol_objetivo, voltajes, tiempos, corrientes, modo):
    """Búsqueda binaria O(log n) del punto muestreado más cercano.

    Voltajes ascendentes en carga y descendentes en descarga.
    Retorna (tiempo, voltaje, corriente) o None si está fuera del rango simulado.
    """
    if not voltajes:
        return None
    minimo, maximo = min(voltajes[0], voltajes[-1]), max(voltajes[0], voltajes[-1])
    if not minimo <= vol_objetivo <= maximo:
        return None
    izquierda, derecha = 0, len(voltajes) - 1
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        if voltajes[medio] == vol_objetivo:
            return tiempos[medio], voltajes[medio], corrientes[medio]
        if (voltajes[medio] < vol_objetivo) == (modo == 1):
            izquierda = medio + 1
        else:
            derecha = medio - 1
    candidatos = [i for i in (izquierda, derecha) if 0 <= i < len(voltajes)]
    indice = min(candidatos, key=lambda i: abs(voltajes[i] - vol_objetivo))
    return tiempos[indice], voltajes[indice], corrientes[indice]


def main():
    print("=" * 48)
    print("       SIMULACIÓN DE UN CIRCUITO RC")
    print("=" * 48)
    print("1. Carga del capacitor")
    print("2. Descarga del capacitor")
    R = leer_float("Ingrese la resistencia R [ohm]: ")
    C = leer_float("Ingrese la capacitancia C [F]: ")
    V0 = leer_float("Ingrese el voltaje V0 [V]: ", inclusivo=True)
    modo = leer_modo()

    tau = R * C
    tiempo_final = 5 * tau
    numero_pasos = 100
    dt = tiempo_final / numero_pasos
    tiempos, voltajes, corrientes = [], [], []
    evento_99 = False

    for n in range(numero_pasos + 1):
        t = n * dt
        Vc = voltaje_capacitor(t, R, C, V0, modo)
        I = corriente(t, R, C, V0, modo)
        tiempos.append(t)
        voltajes.append(Vc)
        corrientes.append(I)
        if V0 > 0 and not evento_99:
            if modo == 1 and Vc >= 0.99 * V0:
                print(f"\nAVISO: el capacitor alcanzó al menos el 99 % de su carga en t = {t:.6f} s.")
                evento_99 = True
            elif modo == 2 and Vc <= 0.01 * V0:
                print(f"\nAVISO: el capacitor completó al menos el 99 % de su descarga en t = {t:.6f} s.")
                evento_99 = True

    print("\n" + "=" * 48)
    print("           RESUMEN DE LA SIMULACIÓN")
    print("=" * 48)
    print(f"Resistencia R       = {R:.4f} ohm")
    print(f"Capacitancia C      = {C:.6e} F")
    print(f"Voltaje V0          = {V0:.4f} V")
    print(f"Constante de tiempo = {tau:.6f} s")
    print(f"Tiempo simulado     = {tiempo_final:.6f} s")
    print(f"Paso temporal       = {dt:.6f} s")
    print(f"Modo                = {'CARGA' if modo == 1 else 'DESCARGA'}")
    print("\n" + "=" * 58)
    print(f"{'Tiempo [s]':>14} {'Vc [V]':>18} {'I [A]':>18}")
    print("=" * 58)
    for t, Vc, I in zip(tiempos, voltajes, corrientes):
        print(f"{t:14.6f} {Vc:18.6f} {I:18.6e}")
    print("=" * 58)

    print("\nBÚSQUEDA BINARIA DE DATOS FÍSICOS")
    print("Busque un voltaje para conocer el tiempo y la corriente correspondientes.")
    print(f"Rango simulado de voltajes: {min(voltajes[0], voltajes[-1]):.6f} a {max(voltajes[0], voltajes[-1]):.6f} V")
    while True:
        entrada = input("\nVoltaje a buscar [V] (Enter para terminar): ").strip()
        if not entrada:
            break
        try:
            buscado = float(entrada)
            if not math.isfinite(buscado):
                raise ValueError
        except ValueError:
            print("Error: escriba un voltaje numérico válido.")
            continue
        resultado = buscar_voltaje(buscado, voltajes, tiempos, corrientes, modo)
        if resultado is None:
            print("Ese voltaje está fuera del rango de la simulación de 0 a 5τ.")
            continue
        t, Vc, I = resultado
        print(f"Voltaje solicitado  = {buscado:.6f} V")
        print(f"Voltaje más cercano = {Vc:.6f} V")
        print(f"Tiempo             = {t:.6f} s")
        print(f"Corriente          = {I:.6e} A")
        print(f"Error de voltaje   = {abs(Vc - buscado):.6e} V")
        print("Nota: el resultado corresponde al punto muestreado más cercano.")
    print("Fin del programa.")


if __name__ == "__main__":
    main()
