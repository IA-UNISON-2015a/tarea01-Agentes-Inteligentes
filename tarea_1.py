import entornos_f
from random import choice

class NueveCuartos(entornos_f.Entorno):
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
            if robot in [1, 2, 4, 5, 7, 8]:
                return ((robot - 1, cuartos), 2)
            return (estado, 1)
        elif accion == "der":
            if robot in [0, 1, 3, 4, 6, 7]:
                return ((robot + 1, cuartos), 2)
            return (estado, 1)
        elif accion == "bajar":
            if robot in [3, 6]:
                return ((robot - 3, cuartos), 3)
            return (estado, 1)
        elif accion == "subir":
            if robot in [2, 5]:
                return ((robot + 3, cuartos), 3)
            return (estado, 1)

    def percepcion(self, estado):
        robot, cuartos = estado
        return (robot, cuartos[robot])
    
class NueveCuartosCiego(NueveCuartos):
    """
    Entorno de nueve cuartos donde el agente solo percibe su ubicación,
    pero no sabe si el cuarto está limpio o sucio.
    """
    def percepcion(self, estado):
        robot, _ = estado
        return robot  # Solo devuelve la posición del robot
    


class AgenteAleatorioNueveCuartos(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoNueveCuartos(entornos_f.Agente):
    """
    Un agente reactivo simple para tres cuartos
    """
    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else  # Limpia si el cuarto donde se encuentra está sucio
                choice(["izq", "der"]) if robot in [1, 4, 7] else # Se mueve si el cuarto donde se encuentra está limpio
                choice(["izq", "subir"]) if robot in [2, 5] else
                choice(["der", "bajar"]) if robot in [3, 6] else
                "izq" if robot == 8 else
                'der')

class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
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
                choice(["izq", "der"]) if robot in [1, 4, 7] else # Se mueve si el cuarto donde se encuentra está limpio
                choice(["izq", "subir"]) if robot in [2, 5] else
                choice(["der", "bajar"]) if robot in [3, 6] else
                "izq" if robot == 8 else
                'der')
    
class AgenteReactivoModeloNueveCuartosCiego(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo para el entorno NueveCuartosCiego.
    Mantiene un modelo interno para rastrear el estado de los cuartos.
    """
    def __init__(self, n_cuartos):
        self.modelo = [0] + ["sucio"] * n_cuartos  # [robot, cuartos]

    def programa(self, percepcion):
        robot = percepcion
        self.modelo[0] = robot

        cuartos = self.modelo[1:]
        if all(c == "limpio" for c in cuartos):
            return "nada"
        if self.modelo[1 + robot] == "sucio":
            self.modelo[1 + robot] = "limpio"
            return "limpiar"
        if robot in [1, 4, 7]: return choice(["izq", "der"])
        elif robot in [2, 5]: return choice(["izq", "subir"])
        elif robot in [3, 6]: return choice(["der", "bajar"])
        elif robot == 8: return "izq"
        return 'der'
    
    
def prueba_agente(agente, entorno_class):
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            entorno_class(),
            agente,
            (0, ["sucio"] * 9),  # Estado inicial
            200
        ),
        [0, ["sucio"] * 9]
    )

def test():
    """
    Prueba del entorno de nueve cuartos y los agentes
    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorioNueveCuartos(['izq', 'der', "subir", "bajar", 'limpiar', 'nada']), NueveCuartos)

    print("Prueba del entorno con un agente reactivo")
    prueba_agente(AgenteReactivoNueveCuartos(), NueveCuartos)

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartos(9), NueveCuartos)

def test_ciego():
    """
    Prueba del entorno de nueve cuartos ciego y los agentes
    """
    print("Prueba del entorno NueveCuartosCiego con un agente aleatorio")
    prueba_agente(AgenteAleatorioNueveCuartos(), NueveCuartosCiego)

    print("Prueba del entorno NueveCuartosCiego con un agente reactivo basado en modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartosCiego(9), NueveCuartosCiego)

if __name__ == "__main__":
    test()
    # test_ciego()
