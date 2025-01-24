import entornos_f
from random import choice

class TresCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de tres cuartos.
    
    El estado se define como (robot, A, B, C)
    donde robot puede tener los valores "A", "B", "C"
    A, B y C pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son
        ("izq", "der", "limpiar", "nada").

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza del cuarto en el que se encuentra
    """
    def accion_legal(self, estado, accion):
        return accion in ("izq", "der", "subir", "bajar", "limpiar", "nada")

    def transicion(self, estado, accion):
        robot, a, b, c = estado

        if accion == "nada":
            return (estado, 0 if a == b == c == "limpio" else 1)
        elif accion == "limpiar":
            if robot == "A":
                return (("A", "limpio", b, c), 1)
            elif robot == "B":
                return (("B", a, "limpio", c), 1)
            elif robot == "C":
                return (("C", a, b, "limpio"), 1)
        elif accion == "izq":
            if robot == "A":
                return (("A", a, b, c), 1)
            elif robot == "B":
                return (("A", a, b, c), 1)
            elif robot == "C":
                return (("B", a, b, c), 1)
        elif accion == "der":
            if robot == "A":
                return (("B", a, b, c), 1)
            elif robot == "B":
                return (("C", a, b, c), 1)
            elif robot == "C":
                return (("C", a, b, c), 1)

    def percepcion(self, estado):
        robot, a, b, c = estado
        if robot == "A":
            return (robot, a)
        elif robot == "B":
            return (robot, b)
        elif robot == "C":
            return (robot, c)

class AgenteAleatorioTresCuartos(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoTresCuartos(entornos_f.Agente):
    """
    Un agente reactivo simple para tres cuartos
    """
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'izq' if robot == 'B' else
                'izq' if robot == 'C' else
                'der')

class AgenteReactivoModeloTresCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo para tres cuartos
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABC'.find(robot)] = situacion

        # Decide sobre el modelo interno
        a, b, c = self.modelo[1], self.modelo[2], self.modelo[3]
        return ('nada' if a == b == c == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'izq' if robot == 'B' else
                'izq' if robot == 'C' else
                'der')

def prueba_agente(agente):
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            TresCuartos(),
            agente,
            ["A", "sucio", "sucio", "sucio"],
            100
        ),
        ["A", "sucio", "sucio", "sucio"]
    )

def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorioTresCuartos(['izq', 'der', 'limpiar', 'nada']))

    print("Prueba del entorno con un agente reactivo")
    prueba_agente(AgenteReactivoTresCuartos())

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloTresCuartos())

if __name__ == "__main__":
    test()
