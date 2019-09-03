import entornos_f
from random import choice


class NueveCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de nueve cuartos,
    donde hay tres cuartos por cada piso,
    tres pisos en total.
    El estado se define como (robot, {cuarto_1, ... , cuarto_n}),
    donde los indices del diccionario representan los nueve cuartos:
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
    y su valor es "limpio" o "sucio".

    Las acciones válidas en el entorno son:
        ("ir_derecha", "ir_izquierda", "subir", "bajar", "limpiar", "nada")
    """

    def accion_legal(self, estado, accion):
        
        robot = estado[0]
        if robot in "A":
            return accion in ("ir_derecha", "limpiar", "nada")
        elif robot in "BEH":
            return accion in ("ir_izquierda", "ir_derecha", "limpiar", "nada")
        elif robot in "CF":
            return accion in ("subir", "ir_izquierda", "limpiar", "nada")
        elif robot in "I":
            return accion in ("ir_izquierda", "limpiar", "nada")
        else:
            return accion in ("bajar", "ir_derecha", "limpiar", "nada")


    def transicion(self, estado, accion):
        robot, cuartos = estado

        if "sucio" not in list(cuartos.values()) and accion is "nada":
            c_local = 0
        
        elif accion is "ir_izquierda" or accion is "ir_derecha":
            c_local = 2

        elif accion is "subir" or accion is "bajar":
            c_local = 3
        
        else:
            c_local = 1

        if accion is "nada":
            return (robot, cuartos, c_local)
        
        elif accion is "ir_derecha":
            if robot in "A":
                return ("B", cuartos, c_local)
            elif robot in "B":
                return ("C", cuartos, c_local)
            elif robot in "D":
                return ("E", cuartos, c_local)
            elif robot in "E":
                return ("F", cuartos, c_local)
            elif robot in "G":
                return ("H", cuartos, c_local)
            elif robot in "H":
                return ("I", cuartos, c_local)
            
        elif accion is "ir_izquierda":
            if robot in "B":
                return ("A", cuartos, c_local)
            elif robot in "C":
                return ("B", cuartos, c_local)
            elif robot in "E":
                return ("D", cuartos, c_local)
            elif robot in "F":
                return ("E", cuartos, c_local)
            elif robot in "H":
                return ("G", cuartos, c_local)
            elif robot in "I":
                return ("H", cuartos, c_local)
        
        elif accion is "limpiar":
            cuartos[robot] = "limpio"
            return (robot, cuartos, c_local)
        
        elif accion is "subir":
            if robot in "C":
                return ("F", cuartos, c_local)
            else:
                return ("I", cuartos, c_local)
        
        elif accion is "bajar":
            if robot in "G":
                return ("D", cuartos, c_local)
            else:
                return ("A", cuartos, c_local)
        
    
    def percepcion(self, estado):
        # regresa en donde se encuentra el robot y si el cuarto esta limpio o sucio
        return estado[0], estado[1][estado[0]]

class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        cuartos = {}
        for char in "ABCDEFGHI":
            cuartos[char] = 'sucio'

        self.modelo = ['A', cuartos]

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[1][robot] = situacion

        # Decide sobre el modelo interno
        if 'sucio' not in list(self.modelo[1].values()):
            return 'nada'
        elif situacion == 'sucio':
            return 'limpiar'

        # despues de limpiar
        elif robot in 'ABE':
            return 'ir_derecha'
        elif robot in 'C':
            return 'subir'
        elif robot in 'F' and self.modelo[1]['E'] == 'sucio':
            return 'ir_izquierda'
        elif robot in 'F' and self.modelo[1]['E'] == 'limpio':
            return 'subir'
        elif robot in 'HI':
            return 'ir_izquierda'
        else:
            return 'bajar'


def prueba_agente(agente):
    cuartos = {}
    for char in 'ABCDEFGHI':
        cuartos[char] = 'sucio'
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            ["A", cuartos.copy()],
            200
        ),
        ["A", cuartos]
    )

class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones
        cuartos = {}
        for char in "ABCDEFGHI":
            cuartos[char] = 'sucio'

        self.modelo = ['A', cuartos]

    def programa(self, percepcion):
        self.modelo[0] = percepcion[0]
        return choice(self.acciones)


def test():
    """
    Prueba del entorno y los agentes
    """

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartos())

    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_izquierda', 'ir_derecha', 'limpiar', 'subir', 'bajar', 'nada']))
    

if __name__ == "__main__":
    test()