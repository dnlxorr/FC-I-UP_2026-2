from figura_geometrica import FiguraGeometrica

class Cuadrado(FiguraGeometrica):
    def __init__(self, lado: float):
        if lado <= 0:
            raise ValueError("El lado debe ser mayor que cero.")
        self.lado = lado

    def calcular_area(self) -> float:
        return self.lado ** 2

    def nombre(self) -> str:
        return "Cuadrado"