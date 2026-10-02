from abc import ABC, abstractmethod

class FiguraGeometrica(ABC):
    @abstractmethod
    def calcular_area(self) -> float:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass