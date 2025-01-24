import entornos_f
from random import choice

class TresCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de tres cuartos.
    
    El estado se define como (robot, cuartos)
    donde robot indica la posición del robot (índice de la lista)
    y cuartos es una lista donde cada elemento puede ser "limpio" o "sucio".

    Las acciones válidas en el entorno son
        ("izq", "der", "limpiar", "nada").

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza del cuarto en el que se encuentra
    """
    def accion_legal(self, estado, accion):
        return accion in ("izq", "der", "subir", "bajar", "limpiar", "nada")

    def transicion(self, estado, accion):
        robot, cuartos = estado
        cuartos = cuartos[:]  # Crear una copia de la lista para evitar efectos colaterales

        if accion == "nada":
            return (estado, 0 if all(c == "limpio" for c in cuartos) else 1)
        elif accion == "limpiar":
            cuartos[robot] = "limpio"
            return ((robot, cuartos), 1)
        elif accion == "izq":
            if robot > 0:
                return ((robot - 1, cuartos), 1)
            return (estado, 1)
        elif accion == "der":
            if robot < len(cuartos) - 1:
                return ((robot + 1, cuartos), 1)
            return (estado, 1)

    def percepcion(self, estado):
        robot, cuartos = estado
        return (robot, cuartos[robot])
    

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
        return ('limpiar' if situacion == 'sucio' else  # Limpia si el cuarto donde se encuentra está sucio
                choice(["izq", "der"]) if robot == 1 else # Se mueve si el cuantro donde se encuentra está 
                "izq" if robot == 2 else
                'der')

class AgenteReactivoModeloTresCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo para tres cuartos
    """
    def __init__(self, n_cuartos):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = [0] + ['sucio'] * n_cuartos  # [robot, cuartos]

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[1 + robot] = situacion

        # Decide sobre el modelo interno
        cuartos = self.modelo[1:]
        return ('nada' if all(c == 'limpio' for c in cuartos) else # No hace nada si todo está limpio
                'limpiar' if situacion == 'sucio' else  # Limpia si el cuarto donde se encuentra está sucio
                choice(["izq", "der"]) if robot == 1 else # Se mueve si el cuantro donde se encuentra está 
                "izq" if robot == 2 else
                'der')
    
def prueba_agente(agente):
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            TresCuartos(),
            agente,
            (0, ["sucio", "sucio", "sucio"]),  # Estado inicial
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
    prueba_agente(AgenteReactivoModeloTresCuartos(3))

if __name__ == "__main__":
    test()
