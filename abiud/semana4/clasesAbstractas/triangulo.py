from figura_geometrica import FiguraGeometrica

class Triangulo(FiguraGeometrica):
    def __init__(self, base: float, altura: float):
        if base <= 0 or altura <= 0:
            raise ValueError("Base y altura deben ser positivas.")
        self.base = base
        self.altura = altura

    def calcular_area(self) -> float:
        return 0.5 * self.base * self.altura

    def nombre(self) -> str:
        return "Triángulo"