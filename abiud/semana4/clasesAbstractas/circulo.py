import math
from figura_geometrica import FiguraGeometrica

class Circulo(FiguraGeometrica):
    def __init__(self, radio: float):
        if radio <= 0:
            raise ValueError("El radio debe ser mayor que cero.")
        self.radio = radio

    def calcular_area(self) -> float:
        return math.pi * self.radio ** 2

    def nombre(self) -> str:
        return "Círculo"