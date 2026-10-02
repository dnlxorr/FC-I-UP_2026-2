"""
Clase abstracta FiguraGeometrica y polimorfismo.

En este programa se crea una clase abstracta llamada
FiguraGeometrica y varias clases hijas que representan
diferentes figuras geométricas.

También se utiliza el polimorfismo, ya que todas las figuras
pueden utilizar el mismo método calcularArea(), aunque cada
una lo implementa de una manera diferente.
"""


# math permite utilizar constantes y funciones matemáticas,
# por ejemplo:
# - math.pi
# - math.sqrt()
import math

# ABC y abstractmethod permiten crear clases abstractas
# y métodos abstractos.
from abc import ABC, abstractmethod



# ===============================================================
# CLASE ABSTRACTA
# ===============================================================

class FiguraGeometrica(ABC):
    """
    Clase abstracta que funciona como estructura común
    para todas las figuras geométricas.

    Toda figura que herede de esta clase debe implementar
    el método calcularArea().
    """

    # Constructor de la clase.
    def __init__(self, nombre):

        # Guarda el nombre de la figura.
        self.nombre = nombre


    # -----------------------------------------------------------
    # MÉTODO ABSTRACTO
    # -----------------------------------------------------------

    @abstractmethod
    def calcularArea(self):
        """
        Método abstracto.

        Toda subclase debe implementar este método para
        poder ser utilizada como FiguraGeometrica.

        Aquí no se escribe una fórmula porque cada figura
        tiene una fórmula de área diferente.
        """

    # -----------------------------------------------------------
    # MÉTODO CONCRETO
    # -----------------------------------------------------------

    def __str__(self):
        """
        Define cómo se mostrará el objeto cuando se convierta
        a texto.

        Se utiliza el nombre de la figura y su área.
        """

        # self.calcularArea() llama al método correspondiente
        # de la subclase.
        #
        # :.4f significa que el área se muestra con 4 decimales.
        return f"{self.nombre} (area = {self.calcularArea():.4f})"



# ===============================================================
# SUBCLASES CONCRETAS
# ===============================================================

# ---------------------------------------------------------------
# CUADRADO
# ---------------------------------------------------------------

class Cuadrado(FiguraGeometrica):

    def __init__(self, lado):

        # Llama al constructor de FiguraGeometrica
        # y establece el nombre "Cuadrado".
        super().__init__("Cuadrado")

        # Guarda el valor del lado.
        self.lado = lado


    def calcularArea(self):
        """
        Calcula el área del cuadrado.

        A = lado²
        """

        return self.lado ** 2



# ---------------------------------------------------------------
# RECTÁNGULO
# ---------------------------------------------------------------

class Rectangulo(FiguraGeometrica):

    def __init__(self, base, altura):

        # Llama al constructor de la clase padre.
        # Guarda "Rectangulo" como nombre.
        super().__init__("Rectangulo")

        # Guarda la base y la altura.
        self.base = base
        self.altura = altura


    def calcularArea(self):
        """
        Calcula el área del rectángulo.

        A = base × altura
        """

        return self.base * self.altura



# ---------------------------------------------------------------
# TRIÁNGULO
# ---------------------------------------------------------------

class Triangulo(FiguraGeometrica):

    def __init__(self, base, altura):

        # Establece el nombre de la figura.
        super().__init__("Triangulo")

        # Guarda base y altura.
        self.base = base
        self.altura = altura


    def calcularArea(self):
        """
        Calcula el área del triángulo.

        A = base × altura / 2
        """

        return self.base * self.altura / 2



# ---------------------------------------------------------------
# CÍRCULO
# ---------------------------------------------------------------

class Circulo(FiguraGeometrica):

    def __init__(self, radio):

        # Establece el nombre.
        super().__init__("Circulo")

        # Guarda el radio.
        self.radio = radio


    def calcularArea(self):
        """
        Calcula el área del círculo.

        A = πr²
        """

        return math.pi * self.radio ** 2



# ---------------------------------------------------------------
# TRAPECIO
# ---------------------------------------------------------------

class Trapecio(FiguraGeometrica):

    def __init__(self, base_mayor, base_menor, altura):

        # Establece el nombre.
        super().__init__("Trapecio")

        # Guarda las dos bases y la altura.
        self.base_mayor = base_mayor
        self.base_menor = base_menor
        self.altura = altura


    def calcularArea(self):
        """
        Calcula el área del trapecio.

        A = ((B + b) × h) / 2
        """

        return (
            (self.base_mayor + self.base_menor)
            * self.altura
            / 2
        )



# ===============================================================
# FUNCIÓN GENERAL: OBTENER ÁREA
# ===============================================================

def obtener_area(figura: FiguraGeometrica) -> float:
    """
    Recibe cualquier objeto que sea FiguraGeometrica
    y devuelve su área.

    El tipo se comprueba antes de calcular el área.
    """

    # isinstance() comprueba si el objeto pertenece a la clase
    # FiguraGeometrica o a alguna de sus subclases.

    # Por ejemplo:
    #
    # isinstance(Cuadrado(4), FiguraGeometrica)
    #
    # devuelve True.

    if not isinstance(figura, FiguraGeometrica):

        # Si el objeto no es una figura geométrica,
        # se genera un error TypeError.
        raise TypeError(
            "Se esperaba un objeto FiguraGeometrica"
        )

    # Si el objeto es válido, se llama a calcularArea().
    #
    # Aquí aparece el POLIMORFISMO.
    #
    # Si figura es un Cuadrado:
    #     llama a Cuadrado.calcularArea()
    #
    # Si figura es un Circulo:
    #     llama a Circulo.calcularArea()
    #
    # etc.
    return figura.calcularArea()



# ===============================================================
# FUNCIÓN PARA CALCULAR EL ÁREA TOTAL
# ===============================================================

def area_total(figuras) -> float:
    """
    Suma las áreas de una lista de figuras.

    Las figuras pueden ser de diferentes tipos.
    """

    # Recorre todas las figuras de la lista.
    #
    # Para cada figura:
    # 1. obtener_area() calcula su área.
    # 2. math.fsum() suma todos los resultados.
    #
    # math.fsum() realiza una suma de números de punto flotante
    # con mayor precisión que sum() en algunos casos.
    return math.fsum(
        obtener_area(f)
        for f in figuras
    )



# ===============================================================
# DEMOSTRACIÓN
# ===============================================================

# Esta condición comprueba que el archivo se esté ejecutando
# directamente.
#
# Si se importa desde otro archivo, este bloque no se ejecuta.
if __name__ == "__main__":


    # ===========================================================
    # 1. INTENTAR CREAR LA CLASE ABSTRACTA
    # ===========================================================

    # Una clase abstracta no puede ser instanciada directamente.
    #
    # Por eso se utiliza try/except para capturar el error.
    try:

        # Se intenta crear un objeto de FiguraGeometrica.
        FiguraGeometrica("Generica")

    except TypeError as e:

        # Python genera TypeError porque la clase tiene
        # un método abstracto sin implementar.
        print("1. Instanciar la clase abstracta falla:")
        print(f"   TypeError: {e}\n")


    # ===========================================================
    # 2. SUBCLASE INCOMPLETA
    # ===========================================================

    # Se crea una clase que hereda de FiguraGeometrica,
    # pero no implementa calcularArea().
    class Incompleta(FiguraGeometrica):
        pass


    # Se intenta crear un objeto de Incompleta.
    try:
        Incompleta("Rota")

    except TypeError as e:

        # También ocurre TypeError porque Incompleta
        # sigue teniendo el método calcularArea() sin implementar.
        print("2. Subclase sin calcularArea falla:")
        print(f"   TypeError: {e}\n")


    # ===========================================================
    # 3. POLIMORFISMO
    # ===========================================================

    # Se crea una lista con diferentes tipos de figuras.
    #
    # Todas heredan de FiguraGeometrica,
    # pero cada una tiene una implementación diferente
    # de calcularArea().
    figuras = [
        Cuadrado(4),
        Rectangulo(3, 5),
        Triangulo(6, 2.5),
        Circulo(2),
        Trapecio(8, 4, 3),
    ]


    # Muestra el área de cada figura.
    print("3. Area de cada figura con obtener_area():")

    # Recorre la lista de figuras.
    for f in figuras:

        # f.nombre obtiene el nombre de la figura.
        #
        # obtener_area(f) llama al método calcularArea()
        # correspondiente a cada objeto.
        #
        # :<11 significa que el nombre se alinea a la izquierda
        # ocupando 11 espacios.
        print(
            f"   {f.nombre:<11} -> "
            f"{obtener_area(f):.4f}"
        )


    # ===========================================================
    # 4. ÁREA TOTAL
    # ===========================================================

    # area_total() recorre todas las figuras,
    # obtiene sus áreas y las suma.
    print(
        f"\n4. Area total de todas las figuras: "
        f"{area_total(figuras):.4f}"
    )


    # ===========================================================
    # 5. OBJETO QUE NO ES UNA FIGURA
    # ===========================================================

    # Se intenta enviar un texto a obtener_area().
    try:
        obtener_area("no soy una figura")

    except TypeError as e:

        # Como el objeto no pertenece a FiguraGeometrica,
        # isinstance() devuelve False y se genera el error.
        print(
            f"\n5. Objeto invalido rechazado: {e}"
        )


    # ===========================================================
    # 6. EXTENSIBILIDAD: ROMBO
    # ===========================================================

    # Se crea una nueva figura heredando de FiguraGeometrica.
    class Rombo(FiguraGeometrica):

        def __init__(self, diagonal_mayor, diagonal_menor):

            # Establece el nombre.
            super().__init__("Rombo")

            # Guarda las diagonales.
            self.d1 = diagonal_mayor
            self.d2 = diagonal_menor


        def calcularArea(self):
            """
            Calcula el área del rombo.

            A = (D × d) / 2
            """

            return self.d1 * self.d2 / 2


    # Se utiliza la nueva clase directamente
    # con la función obtener_area().
    #
    # No fue necesario modificar obtener_area().
    print(
        f"\n6. Nueva figura sin modificar obtener_area: "
        f"{obtener_area(Rombo(6, 4)):.4f}"
    )


    # ===========================================================
    # 7. EXTENSIBILIDAD: HEXÁGONO
    # ===========================================================

    # Se crea otra nueva figura.
    class Hexagono(FiguraGeometrica):

        def __init__(self, lado):

            # Establece el nombre.
            super().__init__("Hexagono")

            # Guarda el lado.
            self.lado = lado


        def calcularArea(self):
            """
            Calcula el área de un hexágono regular.

            A = (3√3 / 2) × lado²
            """

            return (
                (3 * math.sqrt(3) / 2)
                * self.lado ** 2
            )


    # Al igual que con el rombo, obtener_area()
    # funciona sin modificar su código.
    print(
        f"\n6. Nueva figura sin modificar obtener_area: "
        f"{obtener_area(Hexagono(6)):.4f}"
    )