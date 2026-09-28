import math

# Error de truncamiento: aproximar e^x con serie de Taylor
def exp_taylor(x, n):
    suma = 0.0
    for i in range(n):
        suma += (x ** i) / math.factorial(i)
    return suma

print(exp_taylor(1, 5))   # Aproximación con 5 términos
print(math.exp(1))         # Valor real
print(abs(exp_taylor(1, 5) - math.exp(1)))  # Error

# Error de redondeo: restar números muy cercanos
a = 1e16
b = 1e16 + 1
print(b - a)  # Debería ser 1, pero probablemente dé 0.0