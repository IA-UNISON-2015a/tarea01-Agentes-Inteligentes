import entornos_o
from random import choice

__author__ = 'AthenaVianney'

class DosCuartosCiego(entornos_o.Entorno):
    def __init__(self, x0=["A", "sucio", "sucio"]):
        # Por default inicialmente el robot está en A y los dos cuartos están sucios
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteRacionalDoscuartos(entornos_o.Agente):
    # Un agente Racional simple
    def __init__(self):
        self.modelo = ["A", "sucio", "sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        if not "sucio" in self.modelo:
            return "nada"

        situación = self.modelo[" AB".find(robot)]
        self.modelo[" AB".find(robot)] = "limpio"

        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


def test():
    # Prueba del entorno y los agentes
    print ("Prueba ciegas")
    entornos_o.simulador(DosCuartosCiego(), AgenteRacionalDoscuartos(), 100)

if __name__ == "__main__":
    test()
