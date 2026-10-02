import math

# Error por truncamiento: aproximación de e^x mediante Taylor
def exp_taylor(x, n):
    suma = 0.0

    for i in range(n):
        suma += (x ** i) / math.factorial(i)

    return suma


x = 1
n = 5

aproximacion = exp_taylor(x, n)
valor_real = math.exp(x)
error = abs(aproximacion - valor_real)

print("Error de truncamiento")
print(f"Aproximación de Taylor: {aproximacion}")
print(f"Valor real: {valor_real}")
print(f"Error absoluto: {error}")


# Error de redondeo: pérdida de precisión en números grandes
a = 1e16
b = 1e16 + 1

print("\nError de redondeo")
print(f"b - a = {b - a}")