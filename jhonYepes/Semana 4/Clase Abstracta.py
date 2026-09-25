# ==========================================
# 2. Clases Abstractas: Figuras Geométricas
# ==========================================
from abc import ABC, abstractmethod
import math

# 1. Creamos la clase abstracta (la plantilla)
class FiguraGeometrica(ABC):
    @abstractmethod
    def calcularArea(self):
        """Este método DEBE ser implementado por cualquier clase hija"""
        pass

# 2. Clases que heredan y aplican su propia fórmula
class Cuadrado(FiguraGeometrica):
    def __init__(self, lado):
        self.lado = lado

    def calcularArea(self):
        return self.lado ** 2

class Triangulo(FiguraGeometrica):
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def calcularArea(self):
        return (self.base * self.altura) / 2

class Circulo(FiguraGeometrica):
    def __init__(self, radio):
        self.radio = radio

    def calcularArea(self):
        return math.pi * (self.radio ** 2)

# 3. Función independiente que recibe la clase abstracta
def obtener_area_figura(figura: FiguraGeometrica):
    """Recibe cualquier objeto que sea una FiguraGeometrica y calcula su área"""
    return figura.calcularArea()

# --- Prueba del código ---
if __name__ == "__main__":
    mi_cuadrado = Cuadrado(4)
    mi_triangulo = Triangulo(5, 10)
    mi_circulo = Circulo(3)

    print(f"Área del Cuadrado: {obtener_area_figura(mi_cuadrado)}")
    print(f"Área del Triángulo: {obtener_area_figura(mi_triangulo)}")
    print(f"Área del Círculo: {obtener_area_figura(mi_circulo):.4f}")