from random import choice
import random
class DosCuartosEstocastico:

    def __init__(self, x0=["A", "sucio", "sucio"]):

        self.x = x0[:]
        self.desempenio = 0

    def accion_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempenio -= 1
        if accion is "limpiar" and random.random() < 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            self.x[0] = "A"
        elif accion is "ir_B":
            self.x[0] = "B"

    def percepcion(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteAleatorio:
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteReactivoModeloDosCuartos:
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situacion

        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situacion == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')

def simulador(entorno, agente, pasos=10, verbose=True):

    historial_desempenio = [entorno.desempenio]
    historial_estados = [entorno.x[:]]
    historial_acciones = []

    for paso in range(pasos):
        p = entorno.percepcion()
        a = agente.programa(p)
        entorno.transicion(a)

        historial_desempenio.append(entorno.desempenio)
        historial_estados.append(entorno.x[:])
        historial_acciones.append(a)

    historial_acciones.append(None)

    if verbose:
        print(u"\n\nSimulación de entorno tipo " +
              str(type(entorno)) +
              " con el agente tipo " +
              str(type(agente)) + "\n")

        print('Paso'.center(10) +
              'Estado'.center(40) +
              u'Acción'.center(25) +
              u'Desempeño'.center(15))

        print('_' * (10 + 40 + 25 + 15))

        for i in range(pasos):
            print(str(i).center(10) +
                  str(historial_estados[i]).center(40) +
                  str(historial_acciones[i]).center(25) +
                  str(historial_desempenio[i]).rjust(12))

        print('_' * (10 + 40 + 25 + 15) + '\n\n')

    return historial_estados, historial_acciones, historial_desempenio

def test():
    print("Prueba del entorno con un agente aleatorio")
    simulador(DosCuartosEstocastico(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    simulador(DosCuartosEstocastico(), AgenteReactivoModeloDosCuartos(), 100)


if __name__ == "__main__":
    test()