import math

# ============================================================
# RESPUESTA TEMPORAL DE UN CIRCUITO RC SERIE
# ============================================================

print("==========================================")
print("     SIMULACIÓN DE UN CIRCUITO RC")
print("==========================================")
print("1. Carga del capacitor")
print("2. Descarga del capacitor")
print()


# ------------------------------------------------------------
# 1. ENTRADA DE DATOS
# ------------------------------------------------------------

R = float(input("Ingrese la resistencia R [ohm]: "))
C = float(input("Ingrese la capacitancia C [F]: "))
V0 = float(input("Ingrese el voltaje V0 [V]: "))
modo = int(input("Seleccione el modo (1 = Carga, 2 = Descarga): "))


# ------------------------------------------------------------
# 2. VALIDACIÓN DE DATOS
# ------------------------------------------------------------

if R <= 0:
    print("Error: la resistencia debe ser mayor que cero.")

elif C <= 0:
    print("Error: la capacitancia debe ser mayor que cero.")

elif V0 < 0:
    print("Error: el voltaje no puede ser negativo.")

elif modo != 1 and modo != 2:
    print("Error: el modo debe ser 1 (Carga) o 2 (Descarga).")

else:

    # --------------------------------------------------------
    # 3. CONSTANTE DE TIEMPO
    # --------------------------------------------------------

    tau = R * C
    tiempo_final = 5 * tau

    # Se utilizarán 100 pasos de tiempo
    numero_pasos = 100
    dt = tiempo_final / numero_pasos


    # --------------------------------------------------------
    # 4. FUNCIONES PERSONALIZADAS
    # --------------------------------------------------------

    def voltaje_capacitor(t, R, C, V0, modo):
        """
        Calcula el voltaje del capacitor en el instante t.
        """

        tau = R * C

        if modo == 1:
            # Carga
            Vc = V0 * (1 - math.exp(-t / tau))

        elif modo == 2:
            # Descarga
            Vc = V0 * math.exp(-t / tau)

        return Vc


    def corriente(t, R, C, V0, modo):
        """
        Calcula la corriente del circuito en el instante t.
        """

        tau = R * C

        if modo == 1:
            # Carga
            I = (V0 / R) * math.exp(-t / tau)

        elif modo == 2:
            # Descarga
            I = -(V0 / R) * math.exp(-t / tau)

        return I


    # --------------------------------------------------------
    # 5. LISTAS PARA ALMACENAR LOS RESULTADOS
    # --------------------------------------------------------

    tiempos = []
    voltajes = []
    corrientes = []


    # --------------------------------------------------------
    # 6. SIMULACIÓN TEMPORAL MEDIANTE UN LAZO FOR
    # --------------------------------------------------------

    evento_99 = False

    for n in range(numero_pasos + 1):

        t = n * dt

        Vc = voltaje_capacitor(t, R, C, V0, modo)
        I = corriente(t, R, C, V0, modo)

        tiempos.append(t)
        voltajes.append(Vc)
        corrientes.append(I)

        # ----------------------------------------------------
        # Detección del 99 %
        # ----------------------------------------------------

        if modo == 1:

            # En carga, el capacitor alcanza el 99 %
            # cuando Vc >= 0.99*V0

            if Vc >= 0.99 * V0 and evento_99 == False:
                print(
                    f"\nADVERTENCIA: El capacitor ha alcanzado "
                    f"más del 99 % de su carga en t = {t:.6f} s."
                )
                evento_99 = True

        elif modo == 2:

            # En descarga consideramos completado más del 99 %
            # cuando queda como máximo el 1 % del voltaje inicial

            if Vc <= 0.01 * V0 and evento_99 == False:
                print(
                    f"\nADVERTENCIA: El capacitor ha completado "
                    f"más del 99 % de su descarga en t = {t:.6f} s."
                )
                evento_99 = True


    # --------------------------------------------------------
    # 7. RESUMEN DE LA SIMULACIÓN
    # --------------------------------------------------------

    print("\n==========================================")
    print("       RESUMEN DE LA SIMULACIÓN")
    print("==========================================")

    print(f"Resistencia R       = {R:.4f} ohm")
    print(f"Capacitancia C      = {C:.6e} F")
    print(f"Voltaje V0          = {V0:.4f} V")
    print(f"Constante de tiempo = {tau:.6f} s")
    print(f"Tiempo simulado     = {tiempo_final:.6f} s")
    print(f"Paso temporal       = {dt:.6f} s")

    if modo == 1:
        print("Modo                 = CARGA")

    elif modo == 2:
        print("Modo                 = DESCARGA")


    # --------------------------------------------------------
    # 8. TABLA DE EVOLUCIÓN TEMPORAL
    # --------------------------------------------------------

    print("\n================================================")
    print(" Tiempo [s]       Vc [V]          I [A]")
    print("================================================")

    for i in range(len(tiempos)):

        print(
            f"{tiempos[i]:10.6f}    "
            f"{voltajes[i]:10.6f}    "
            f"{corrientes[i]:12.6e}"
        )

    print("================================================")