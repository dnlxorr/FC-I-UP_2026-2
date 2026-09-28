from cuadrado import Cuadrado
from circulo import Circulo
from triangulo import Triangulo
from figura_geometrica import FiguraGeometrica


def area_de_figura(figura: FiguraGeometrica) -> float:
    return figura.calcular_area()


def reporte_figuras(figuras):
    print(f"{'Figura':<15}{'Área':<20}")
    total = 0.0
    for f in figuras:
        a = area_de_figura(f)
        total += a
        print(f"{f.nombre():<15}{a:<20.4f}")

if __name__ == "__main__":
    figuras = [Cuadrado(4), Circulo(3), Triangulo(6, 2)]
    reporte_figuras(figuras)