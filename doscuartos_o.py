#!/usr/bin/env python
# -*- coding: utf-8 -*-

#*******************************Observaciones(Punto 2)**************************
#despues de hacer el entorno ciego, lo primero que se puede observar es que el
#agente aleatorio se comporta de igual manera ya que no le importa mucho que
#percepción recibe, en cambio de el agente reactivo debe de ser diferente ya que
#como es basado en modelo, debe de actualizar el modelo antes de que se realice
#la acción, suponiendo que el cuarto siempre es limpiado. El comportamiento del
#agente reactivo es basicamente igual, ya que el robot siempre limpia. Se puede
#observar que el reactivo basado en modelo tiene mas rendimiento, ya que ya no
#hace nada cuando tiene ambos cuartos sucios.

#*******************************Observaciones(Punto 2)**************************
#en el ambiente estocastico el agente aleatorio y el reactivo simple no cambió
#mucho el comportamiento, lo único que cambia es que el reactivo a veces tarda
#un poco mas en tener todos los cuartos limpios. En cambio el agente con modelo
#cambia un poco mas, ya que a veces tarda un poco más en cumplir con el modelo.

"""
doscuartos.py.py
------------

Ejemplo de un entorno muy simple y agentes idem

"""

import entornos_o
from random import choice


__author__ = 'juliowaissman'

class DosCuartosEstocastico(object):
    """docstring forDosCuartosEstocastico."""
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
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
            n = choice(list(range(10)))
            if n in list(range(8)):
                self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class DosCuartosCiego(object):
    """Clase de los dos cuartos ciego"""
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
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
        return self.x[0]

class AgenteRacionalModeloCiego(object):
    """Clase de agente racional pero que no puede saber su el cuarto está sucio"""
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        situación = self.modelo[' AB'.find(robot)]

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        if a == b == 'limpio':
            return 'nada'
        elif situación == 'sucio':
            self.modelo[' AB'.find(robot)] = 'limpio'
            return 'limpiar'
        elif robot == 'B':
            return 'ir_A'
        else:
            return 'ir_B'

class DosCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
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


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoDoscuartos(entornos_o.Agente):
    """
    Un agente reactivo simple

    """
    def programa(self, percepción):
        robot, situación = percepción
        return ('limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(DosCuartosEstocastico(),
                         AgenteReactivoDoscuartos(),
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocastico(),
                         AgenteReactivoModeloDosCuartos(),
                         100)

if __name__ == "__main__":
    test()
