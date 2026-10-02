import math
import matplotlib.pyplot as plt

print("Graficas de la serie de Taylor del seno")
print("---------------------------------------")

x = float(input("Ingrese x: "))

# Valor de referencia
valor_referencia = math.sin(x)

# Calculo de las aproximaciones de Taylor
aproximaciones = []

suma = 0

for n in range(10):
    termino = ((-1) ** n) * (x ** (2 * n + 1)) / math.factorial(2 * n + 1)
    suma += termino
    aproximaciones.append(suma)


# Calculo de los errores
errores_aproximacion = []
errores_redondeo = []
errores_truncamiento = []

for n in range(10):

    # Error de aproximacion
    error_aproximacion = abs(valor_referencia - aproximaciones[n])
    errores_aproximacion.append(error_aproximacion)

    # Error de redondeo
    aproximacion_redondeada = round(aproximaciones[n], 10)
    error_redondeo = abs(aproximaciones[n] - aproximacion_redondeada)
    errores_redondeo.append(error_redondeo)

    # Error de truncamiento
    error_truncamiento = abs(valor_referencia - aproximaciones[n])
    errores_truncamiento.append(error_truncamiento)


terminos = list(range(1, 11))


# Grafica 1: aproximacion de Taylor
plt.figure()

plt.plot(terminos, aproximaciones, marker="o", label="Taylor")
plt.axhline(valor_referencia, linestyle="--", label="Valor de referencia")

plt.xlabel("Numero de terminos")
plt.ylabel("Valor")
plt.title("Aproximacion de Taylor del seno")
plt.legend()
plt.grid()

plt.show()


# Grafica 2: error de aproximacion
plt.figure()

plt.plot(terminos, errores_aproximacion, marker="o")

plt.xlabel("Numero de terminos")
plt.ylabel("Error")
plt.title("Error de aproximacion")
plt.yscale("log")
plt.grid()

plt.show()


# Grafica 3: error de redondeo
plt.figure()

plt.plot(terminos, errores_redondeo, marker="o")

plt.xlabel("Numero de terminos")
plt.ylabel("Error")
plt.title("Error de redondeo")
plt.yscale("log")
plt.grid()

plt.show()


# Grafica 4: error de truncamiento
plt.figure()

plt.plot(terminos, errores_truncamiento, marker="o")

plt.xlabel("Numero de terminos")
plt.ylabel("Error")
plt.title("Error de truncamiento")
plt.yscale("log")
plt.grid()

plt.show()


# Grafica 5: comparacion de errores
plt.figure()

plt.plot(terminos, errores_aproximacion, marker="o",
         label="Error de aproximacion")

plt.plot(terminos, errores_redondeo, marker="o",
         label="Error de redondeo")

plt.plot(terminos, errores_truncamiento, marker="o",
         label="Error de truncamiento")

plt.xlabel("Numero de terminos")
plt.ylabel("Error")
plt.title("Comparacion de errores")
plt.yscale("log")
plt.legend()
plt.grid()

plt.show()