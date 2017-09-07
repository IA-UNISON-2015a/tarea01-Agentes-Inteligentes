import entornos_o
from random import choice

__author__ = 'AthenaVianney'


class DosCuartosEstocastico(entornos_o.Entorno):

    def __init__(self, x0=["A", "sucio", "sucio"]):
        # Por default inicialmente el robot está en A y los dos cuartos están sucios
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        proba = choice(range(100))
        robot, a, b = self.x

        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar" and proba > 80:
            self.x[" AB".find(self.x[0])] = "limpio" 
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    # Un agente que solo regresa una accion al azar entre las acciones legales
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteRacionalDosCuartosEstocastico(entornos_o.Agente):
    # Un agente Racional simple
    def __init__(self):
    # Inicializa el modelo interno en el peor de los casos
      self.modelo = ['A', 'sucio', 'sucio']
    
    def programa(self, percepción):
        robot, situación = percepción

        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


def test():
    # Prueba del entorno y los agentes
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)

    print("Prueba del entorno con un agente Racional")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteRacionalDosCuartosEstocastico(), 100)
 

if __name__ == "__main__":
    test()
