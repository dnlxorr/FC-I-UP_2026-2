import math
import random

#QuickShort
#BinarySearch

# Índices de cada dato dentro de un registro (tupla):
# registro = (t, x, v, e_cin, e_pot, e_tot)
T, X, V, ECIN, EPOT, ETOT = range(6)


# ---------------------------------------------------------------
# FÍSICA DEL OSCILADOR
# ---------------------------------------------------------------

def calcular_x(t, A, w):
    """Posición x(t) = A cos(wt)."""
    return A * math.cos(w * t)


def calcular_v(t, A, w):
    """Velocidad v(t) = -A w sin(wt)."""
    return -A * w * math.sin(w * t)


def calcular_energia(m, k, x, v):
    """Devuelve (E_cinética, E_potencial, E_total)."""
    e_cin = 0.5 * m * v ** 2
    e_pot = 0.5 * k * x ** 2
    return e_cin, e_pot, e_cin + e_pot


# ---------------------------------------------------------------
# LECTURA DE DATOS
# ---------------------------------------------------------------

def leer_positivo(mensaje):
    """Pide un número real finito y estrictamente positivo; repite hasta que sea válido."""
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Error: ingrese un número válido.")
            continue

        if not math.isfinite(valor) or valor <= 0:
            print("Error: el valor debe ser un número finito estrictamente positivo.")
        else:
            return valor


def leer_real(mensaje):
    """Pide un número real finito (puede ser negativo o cero)."""
    while True:
        try:
            valor = float(input(mensaje))
        except ValueError:
            print("Error: ingrese un número válido.")
            continue

        if not math.isfinite(valor):
            print("Error: el valor debe ser finito.")
        else:
            return valor


# ---------------------------------------------------------------
# ORDENAMIENTO: QUICK SORT
# ---------------------------------------------------------------
# Quick Sort cuesta O(n log n) en promedio, mucho mejor que Bubble,
# Selection o Insertion Sort (O(n²)), que serían muy lentos con miles
# de datos. Funciona así:
#   1. Se elige un pivote.
#   2. Se reparten los datos: menores a un lado, mayores al otro.
#   3. Se repite el proceso en cada lado.
# Nota: los valores de x(t) vienen "casi ordenados" por tramos, por eso
# el pivote se elige al azar (con un pivote fijo el algoritmo sería lento).

def quick_sort(lista, indice):
    """Devuelve una lista NUEVA ordenada (de menor a mayor) según lista[i][indice]."""
    copia = list(lista)  # se ordena una copia para no alterar la original
    _quick_sort(copia, 0, len(copia) - 1, indice)
    return copia


def _quick_sort(a, bajo, alto, indice):
    """Ordena a[bajo..alto] en el mismo lugar."""
    while bajo < alto:
        # Pivote al azar dentro del tramo actual
        pivote = a[random.randint(bajo, alto)][indice]

        # Partición: i avanza desde la izquierda, j desde la derecha
        i, j = bajo, alto
        while i <= j:
            while a[i][indice] < pivote:
                i += 1
            while a[j][indice] > pivote:
                j -= 1
            if i <= j:
                a[i], a[j] = a[j], a[i]
                i += 1
                j -= 1

        # Ahora a[bajo..j] <= pivote y a[i..alto] >= pivote.
        # Se llama recursivamente con el lado MÁS PEQUEÑO y se sigue en bucle
        # con el más grande, así la recursión nunca es demasiado profunda.
        if j - bajo < alto - i:
            _quick_sort(a, bajo, j, indice)
            bajo = i
        else:
            _quick_sort(a, i, alto, indice)
            alto = j


# ---------------------------------------------------------------
# BÚSQUEDA BINARIA
# ---------------------------------------------------------------
# Requiere que la lista esté ORDENADA por el campo que se busca.
# Cada paso descarta la mitad de los datos: O(log n).

def busqueda_binaria(lista, objetivo, indice):
    """
    Devuelve la primera posición pos tal que lista[pos][indice] >= objetivo.
    (Si todos son menores, devuelve len(lista).)
    """
    bajo, alto = 0, len(lista)
    while bajo < alto:
        medio = (bajo + alto) // 2
        if lista[medio][indice] < objetivo:
            bajo = medio + 1
        else:
            alto = medio
    return bajo


# ---------------------------------------------------------------
# BÚSQUEDAS ESPECÍFICAS DEL OSCILADOR
# ---------------------------------------------------------------

# Columnas por las que se puede ordenar / buscar: (nombre, unidad).
# La energía total no se incluye porque es constante (no hay nada que ordenar).
CAMPOS = {
    X:    ("elongación x", "m"),
    V:    ("velocidad v", "m/s"),
    ECIN: ("energía cinética", "J"),
    EPOT: ("energía potencial", "J"),
}

# Aclaración física que se muestra después de cada búsqueda
NOTAS = {
    X:    "Nota: cada elongación se alcanza dos veces por ciclo; la velocidad tiene la "
          "misma rapidez pero sentido contrario (hacia +x o hacia -x).",
    V:    "Nota: cada velocidad se alcanza dos veces por período, en posiciones x "
          "de signo opuesto (misma distancia al equilibrio).",
    ECIN: "Nota: cada energía cinética se repite 4 veces por período "
          "(a ambos lados del equilibrio y en ambos sentidos de movimiento).",
    EPOT: "Nota: cada energía potencial se repite 4 veces por período "
          "(a ambos lados del equilibrio y en ambos sentidos de movimiento).",
}


def buscar_por_tiempo(registros_por_t, t_objetivo):
    """
    Busca el registro más cercano a un tiempo dado.
    'registros_por_t' ya está ordenado por tiempo (se genera así),
    por lo que NO hace falta ordenar: se aplica búsqueda binaria directa.
    """
    pos = busqueda_binaria(registros_por_t, t_objetivo, T)

    # El más cercano es el de la posición pos o el anterior
    candidatos = []
    if pos > 0:
        candidatos.append(registros_por_t[pos - 1])
    if pos < len(registros_por_t):
        candidatos.append(registros_por_t[pos])

    return min(candidatos, key=lambda r: abs(r[T] - t_objetivo))


def calcular_tolerancia(registros_por_t, indice):
    """
    Mitad del mayor salto que da la columna 'indice' entre dos instantes
    consecutivos. Con esa tolerancia se garantiza que cada vez que la
    magnitud pasa por el valor buscado, al menos un registro cae dentro.
    """
    salto_max = 0.0
    for a, b in zip(registros_por_t, registros_por_t[1:]):
        salto = abs(b[indice] - a[indice])
        if salto > salto_max:
            salto_max = salto
    return salto_max / 2


def buscar_por_valor(registros_ord, indice, objetivo, tolerancia, dt):
    """
    Busca todos los instantes en que la columna 'indice' (x, v, Ecin o Epot)
    pasa por 'objetivo'.

    'registros_ord' debe estar ORDENADO por esa misma columna (quick sort).
    Como el movimiento es periódico, cada valor se repite varias veces,
    por eso se devuelve una lista de "pasos" ordenada por tiempo.
    """
    n = len(registros_ord)

    # 1. Búsqueda binaria: ubica el punto donde 'objetivo' "cabría" en la lista ordenada
    pos = busqueda_binaria(registros_ord, objetivo, indice)

    # 2. Se expande hacia ambos lados recogiendo los registros dentro de la tolerancia
    coincidencias = []

    i = pos - 1
    while i >= 0 and abs(registros_ord[i][indice] - objetivo) <= tolerancia:
        coincidencias.append(registros_ord[i])
        i -= 1

    j = pos
    while j < n and abs(registros_ord[j][indice] - objetivo) <= tolerancia:
        coincidencias.append(registros_ord[j])
        j += 1

    # Si nada cae dentro de la tolerancia, se toman los vecinos inmediatos
    if not coincidencias:
        if pos > 0:
            coincidencias.append(registros_ord[pos - 1])
        if pos < n:
            coincidencias.append(registros_ord[pos])

    # 3. Se ordenan por tiempo para agrupar los registros que pertenecen al mismo paso
    coincidencias = quick_sort(coincidencias, T)

    # 4. Cada grupo de tiempos consecutivos es UN paso por ese valor;
    #    de cada grupo se conserva el registro más cercano al objetivo.
    pasos = []
    grupo = [coincidencias[0]]
    for reg in coincidencias[1:]:
        if reg[T] - grupo[-1][T] > 1.5 * dt:
            pasos.append(min(grupo, key=lambda r: abs(r[indice] - objetivo)))
            grupo = [reg]
        else:
            grupo.append(reg)
    pasos.append(min(grupo, key=lambda r: abs(r[indice] - objetivo)))

    return pasos


# ---------------------------------------------------------------
# IMPRESIÓN
# ---------------------------------------------------------------

def imprimir_encabezado():
    print(
        f"{'t (s)':>8}"
        f"{'x (m)':>10}"
        f"{'v (m/s)':>10}"
        f"{'Ecin (J)':>11}"
        f"{'Epot (J)':>11}"
        f"{'Etot (J)':>11}"
    )


def imprimir_registro(r):
    print(
        f"{r[T]:8.2f}"
        f"{r[X]:10.4f}"
        f"{r[V]:10.4f}"
        f"{r[ECIN]:11.4f}"
        f"{r[EPOT]:11.4f}"
        f"{r[ETOT]:11.4f}"
    )


def imprimir_tabla(registros, filas=20):
    """Imprime aproximadamente 'filas' registros repartidos uniformemente."""
    imprimir_encabezado()
    salto = max(1, len(registros) // filas)
    for j in range(0, len(registros), salto):
        imprimir_registro(registros[j])


# ---------------------------------------------------------------
# ORDENAMIENTOS GUARDADOS (se calculan solo cuando se necesitan)
# ---------------------------------------------------------------

def obtener_ordenado(ordenados, registros_por_t, campo):
    """
    Devuelve los registros ordenados por 'campo'. Si aún no se han ordenado
    así, se ordenan con quick sort y se guardan para no repetir el trabajo.
    """
    if campo not in ordenados:
        nombre = CAMPOS[campo][0]
        print(f"Ordenando los datos por {nombre} (quick sort)...")
        ordenados[campo] = quick_sort(registros_por_t, campo)
    return ordenados[campo]


# ---------------------------------------------------------------
# MENÚ DE CONSULTA
# ---------------------------------------------------------------

def elegir_campo(mensaje):
    """Pregunta por cuál columna trabajar y devuelve su índice (o None si es inválida)."""
    print(mensaje)
    print("  1. Elongación x")
    print("  2. Velocidad v")
    print("  3. Energía cinética")
    print("  4. Energía potencial")
    opciones = {"1": X, "2": V, "3": ECIN, "4": EPOT}
    return opciones.get(input("Elija una opción: ").strip())


def consultar_por_campo(campo, registros_por_t, ordenados, tolerancias, dt, max_mostrar=10):
    """Busca (con búsqueda binaria) los instantes en que 'campo' vale lo que pide el usuario."""
    nombre, unidad = CAMPOS[campo]
    lista = obtener_ordenado(ordenados, registros_por_t, campo)

    if campo not in tolerancias:
        tolerancias[campo] = calcular_tolerancia(registros_por_t, campo)
    tol = tolerancias[campo]

    # Al estar ordenada la lista, el mínimo y el máximo son el primer y último elemento
    minimo, maximo = lista[0][campo], lista[-1][campo]
    objetivo = leer_real(f"{nombre.capitalize()} buscada ({unidad}, entre {minimo:.4f} y {maximo:.4f}): ")

    if objetivo < minimo - tol or objetivo > maximo + tol:
        print("Error: ese valor nunca se alcanza en la simulación.")
        return

    pasos = buscar_por_valor(lista, campo, objetivo, tol, dt)

    print(f"\nLa {nombre} vale ≈ {objetivo:.4f} {unidad} en {len(pasos)} instante(s).")
    print(f"Se muestran los primeros {min(len(pasos), max_mostrar)}:\n")
    imprimir_encabezado()
    for r in pasos[:max_mostrar]:
        imprimir_registro(r)

    r0 = pasos[0]
    print(
        f"\nEn t = {r0[T]:.2f} s: x = {r0[X]:.4f} m | v = {r0[V]:.4f} m/s "
        f"(rapidez = {abs(r0[V]):.4f} m/s)\n"
        f"Ecin = {r0[ECIN]:.4f} J | Epot = {r0[EPOT]:.4f} J | Etot = {r0[ETOT]:.4f} J"
    )
    print(NOTAS[campo])


def menu_busqueda(registros_por_t, ordenados, dt, t_max):
    """Permite al usuario ordenar y consultar datos usando quick sort y búsqueda binaria."""
    tolerancias = {}

    while True:
        print("\n--- Consulta de datos ---")
        print("1. Buscar por elongación x")
        print("2. Buscar por velocidad v")
        print("3. Buscar por energía cinética")
        print("4. Buscar por energía potencial")
        print("5. Buscar por tiempo t")
        print("6. Ver la tabla ordenada por x, v, Ecin o Epot")
        print("7. Salir")
        opcion = input("Elija una opción: ").strip()

        if opcion in ("1", "2", "3", "4"):
            campo = {"1": X, "2": V, "3": ECIN, "4": EPOT}[opcion]
            consultar_por_campo(campo, registros_por_t, ordenados, tolerancias, dt)

        elif opcion == "5":
            t_obj = leer_real(f"Tiempo t buscado (s, entre 0 y {t_max:.2f}): ")

            if t_obj < 0 or t_obj > t_max:
                print("Error: el tiempo está fuera del rango simulado.")
                continue

            r = buscar_por_tiempo(registros_por_t, t_obj)
            print()
            imprimir_encabezado()
            imprimir_registro(r)

        elif opcion == "6":
            campo = elegir_campo("¿Ordenar por cuál magnitud (de menor a mayor)?")
            if campo is None:
                print("Opción no válida.")
                continue
            lista = obtener_ordenado(ordenados, registros_por_t, campo)
            print(f"\n=== Datos ordenados por {CAMPOS[campo][0]} (de menor a mayor) ===\n")
            imprimir_tabla(lista)

        elif opcion == "7":
            print("Fin de la consulta.")
            break

        else:
            print("Opción no válida.")


# ---------------------------------------------------------------
# SIMULACIÓN
# ---------------------------------------------------------------

def simular_oscilador():
    print("--- Simulación de Oscilador Armónico Simple ---")

    # ENTRADA DE DATOS
    m = leer_positivo("Ingrese la masa (kg): ")
    k = leer_positivo("Ingrese la constante elástica (N/m): ")
    A = leer_positivo("Ingrese la amplitud (m): ")
    T_total = leer_positivo("Ingrese el tiempo total de simulación (s): ")

    # PARÁMETROS DEL SISTEMA
    w = math.sqrt(k / m)          # frecuencia angular
    periodo = 2 * math.pi / w     # período
    dt = 0.01                     # intervalo de tiempo entre cálculos
    pasos = round(T_total / dt)

    # LÍMITE DE LA SIMULACIÓN
    if pasos > 1_000_000:
        print("Error: el tiempo total es demasiado grande (máx. 10 000 s).")
        return

    # GENERAR REGISTROS
    # Cada registro es una tupla (t, x, v, e_cin, e_pot, e_tot).
    # Se generan en orden de tiempo, así que la lista ya está ordenada por t.
    registros_por_t = []

    energia_inicial = 0.5 * k * A ** 2
    tolerancia_energia = 0.01 * energia_inicial
    violaciones = 0

    for i in range(pasos + 1):
        t = i * dt
        x = calcular_x(t, A, w)
        v = calcular_v(t, A, w)
        e_cin, e_pot, e_tot = calcular_energia(m, k, x, v)

        registros_por_t.append((t, x, v, e_cin, e_pot, e_tot))

        if abs(e_tot - energia_inicial) > tolerancia_energia:
            violaciones += 1

    # MOSTRAR RESULTADOS (orden cronológico)
    print(f"\nω = {w:.4f} rad/s | Período = {periodo:.4f} s")
    print("\n=== Datos en orden cronológico (ordenados por t) ===\n")
    imprimir_tabla(registros_por_t)

    # ORDENAR POR ELONGACIÓN (las demás columnas se ordenan cuando se piden en el menú)
    ordenados = {}
    registros_por_x = obtener_ordenado(ordenados, registros_por_t, X)

    print("\n=== Datos ordenados por elongación x (de menor a mayor) ===\n")
    imprimir_tabla(registros_por_x)

    # CONCLUSIÓN SOBRE LA ENERGÍA
    if violaciones == 0:
        print(f"\nLa energía total se conserva: {energia_inicial:.4f} J.")
    else:
        print(
            f"\nAdvertencia: la energía se desvió "
            f"de la tolerancia en {violaciones} pasos."
        )

    # CONSULTA INTERACTIVA
    menu_busqueda(registros_por_t, ordenados, dt, pasos * dt)


if __name__ == "__main__":
    simular_oscilador()
