# ============================================================
# ACTIVIDAD 2 - CLASES ABSTRACTAS
# Física Computacional
#
# Tema:
# Clases abstractas y herencia en Python
# ============================================================


# ============================================================
# 1. IMPORTAR LAS HERRAMIENTAS PARA CREAR CLASES ABSTRACTAS
# ============================================================

from abc import ABC, abstractmethod
import math


# ============================================================
# 2. CREAR LA CLASE ABSTRACTA
# ============================================================

class FiguraGeometrica(ABC):

    # --------------------------------------------------------
    # Método abstracto
    # --------------------------------------------------------
    #
    # Todas las figuras geométricas deberán implementar
    # este método.
    #
    # La clase FiguraGeometrica solamente establece la regla,
    # pero no calcula directamente el área.
    # --------------------------------------------------------

    @abstractmethod
    def calcularArea(self):
        pass


# ============================================================
# 3. CREAR LA CLASE CUADRADO
# ============================================================

class Cuadrado(FiguraGeometrica):

    def __init__(self, lado):

        # Guardamos el valor del lado.
        self.lado = lado

    def calcularArea(self):

        # Área del cuadrado:
        #
        # A = lado × lado
        #
        return self.lado * self.lado


# ============================================================
# 4. CREAR LA CLASE TRIANGULO
# ============================================================

class Triangulo(FiguraGeometrica):

    def __init__(self, base, altura):

        # Guardamos la base.
        self.base = base

        # Guardamos la altura.
        self.altura = altura

    def calcularArea(self):

        # Área del triángulo:
        #
        # A = (base × altura) / 2
        #
        return (self.base * self.altura) / 2


# ============================================================
# 5. CREAR LA CLASE CIRCULO
# ============================================================

class Circulo(FiguraGeometrica):

    def __init__(self, radio):

        # Guardamos el radio.
        self.radio = radio

    def calcularArea(self):

        # Área del círculo:
        #
        # A = π × r²
        #
        return math.pi * self.radio ** 2


# ============================================================
# 6. FUNCIÓN GENERAL PARA CALCULAR EL ÁREA
# ============================================================

def calcular_area_figura(figura):

    # La función recibe cualquier objeto que pertenezca
    # a FiguraGeometrica.
    #
    # No necesitamos saber si es:
    #
    # - Cuadrado
    # - Triángulo
    # - Círculo
    #
    # Simplemente llamamos a calcularArea().

    return figura.calcularArea()


# ============================================================
# 7. CREAR LOS OBJETOS
# ============================================================

cuadrado = Cuadrado(5)

triangulo = Triangulo(10, 4)

circulo = Circulo(3)


# ============================================================
# 8. CALCULAR LAS ÁREAS
# ============================================================

area_cuadrado = calcular_area_figura(cuadrado)

area_triangulo = calcular_area_figura(triangulo)

area_circulo = calcular_area_figura(circulo)


# ============================================================
# 9. MOSTRAR LOS RESULTADOS
# ============================================================

print("==============================================")
print("        ÁREAS DE LAS FIGURAS")
print("==============================================")

print("Área del cuadrado:", area_cuadrado)

print("Área del triángulo:", area_triangulo)

print("Área del círculo:", area_circulo)