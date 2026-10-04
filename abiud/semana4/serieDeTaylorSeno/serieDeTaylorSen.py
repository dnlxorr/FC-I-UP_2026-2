import math

print("Serie de Taylor del seno")
print("------------------------")

x = float(input("Ingrese x: "))

# Valor de referencia
valor_referencia = math.sin(x)

print("\nVALOR DE REFERENCIA")
print(f"sin({x}) = {valor_referencia:.10f}")


# Aproximaciones de Taylor
print("\nAPROXIMACIONES DE TAYLOR")
print("Termino     Aproximacion")

suma = 0
aproximaciones = []

for n in range(10):
    termino = ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    suma += termino

    aproximaciones.append(suma)

    print(f"{n + 1:<11}{suma:.10f}")


# Error de aproximacion
print("\nERROR DE APROXIMACION")
print("Termino     Error")

errores_aproximacion = []

for n in range(10):
    error = abs(valor_referencia - aproximaciones[n])
    errores_aproximacion.append(error)

    print(f"{n + 1:<11}{error:.15e}")


# Error de redondeo
print("\nERROR DE REDONDEO")
print("Termino     Aproximacion redondeada     Error de redondeo")

errores_redondeo = []

for n in range(10):
    aproximacion_redondeada = round(aproximaciones[n], 10)

    error_redondeo = abs(aproximaciones[n] - aproximacion_redondeada)
    errores_redondeo.append(error_redondeo)

    print(f"{n + 1:<11}{aproximacion_redondeada:<27.10f}{error_redondeo:.15e}")


# Error de truncamiento
print("\nERROR DE TRUNCAMIENTO")
print("Termino     Error de truncamiento")

errores_truncamiento = []

for n in range(10):
    error_truncamiento = abs(valor_referencia - aproximaciones[n])
    errores_truncamiento.append(error_truncamiento)

    print(f"{n + 1:<11}{error_truncamiento:.15e}")


# Selection Sort
print("\nSELECTION SORT")

datos = []

for n in range(10):
    datos.append((n + 1, errores_aproximacion[n]))

for i in range(len(datos) - 1):
    posicion_menor = i

    for j in range(i + 1, len(datos)):
        if datos[j][1] < datos[posicion_menor][1]:
            posicion_menor = j

    if posicion_menor != i:
        print(f"Swap: termino {datos[i][0]} <-> termino {datos[posicion_menor][0]}")
        datos[i], datos[posicion_menor] = datos[posicion_menor], datos[i]

print("\nERRORES ORDENADOS")
print("Termino     Error")

for termino, error in datos:
    print(f"{termino:<11}{error:.15e}")