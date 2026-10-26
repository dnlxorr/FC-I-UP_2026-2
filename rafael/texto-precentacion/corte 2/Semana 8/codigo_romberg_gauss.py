
import numpy as np

# Datos físicos
m = 2.5
T1 = 20.0
T2 = 200.0
tolerancia = 1e-6

def calor_especifico(T):
    return (
        400
        + 0.25*T
        + 30*np.exp(-T/150.0)*np.sin(T/40.0)
    )

def trapecio_compuesto(f, a, b, n):
    h = (b-a)/n
    suma = 0.5*(f(a) + f(b))
    for i in range(1, n):
        x = a + i*h
        suma += f(x)
    return h*suma

def romberg(f, a, b, tolerancia=1e-6, max_nivel=15):
    R = np.zeros((max_nivel, max_nivel))
    R[0, 0] = trapecio_compuesto(f, a, b, 1)

    for i in range(1, max_nivel):
        n = 2**i
        R[i, 0] = trapecio_compuesto(f, a, b, n)

        for j in range(1, i+1):
            R[i, j] = (
                R[i, j-1]
                + (R[i, j-1] - R[i-1, j-1])/(4**j - 1)
            )

        error = abs(R[i, i] - R[i-1, i-1])

        if error < tolerancia:
            return R[i, i], n, error

    return R[max_nivel-1, max_nivel-1], 2**(max_nivel-1), error

def gauss_legendre(f, a, b, n):
    nodos, pesos = np.polynomial.legendre.leggauss(n)
    integral = 0.0

    for i in range(n):
        x = (b-a)/2*nodos[i] + (a+b)/2
        integral += pesos[i]*f(x)

    return (b-a)/2*integral

def gauss_adaptativo(f, a, b, tolerancia=1e-6, n_inicial=2, n_max=128):
    n = n_inicial
    I_anterior = gauss_legendre(f, a, b, n)

    while n < n_max:
        n *= 2
        I_actual = gauss_legendre(f, a, b, n)
        error = abs(I_actual - I_anterior)

        if error < tolerancia:
            return I_actual, n, error

        I_anterior = I_actual

    return I_actual, n, error

# Romberg
I_R, n_R, error_R = romberg(
    calor_especifico,
    T1,
    T2,
    tolerancia
)

Q_R = m*I_R

# Gauss-Legendre
I_G, n_G, error_G = gauss_adaptativo(
    calor_especifico,
    T1,
    T2,
    tolerancia
)

Q_G = m*I_G

print("ROMBERG")
print("Integral =", I_R)
print("n =", n_R)
print("Error =", error_R)
print("Q =", Q_R, "J")

print("\nGAUSS-LEGENDRE")
print("Integral =", I_G)
print("n =", n_G)
print("Error =", error_G)
print("Q =", Q_G, "J")

print("\nDiferencia:")
print(abs(Q_R-Q_G), "J")
