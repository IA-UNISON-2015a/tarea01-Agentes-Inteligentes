#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán: ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.
"""
__author__ = 'Patricia Quiroz'

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from random import choice
import entornos_o


class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de Seis cuartos.
    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B", "C", "D", "E", "F", que pueden tener los valores "limpio", "sucio".

    Las acciones válidas en el entorno son ("ir_Der", "ir_Izq", "subir", "bajar", "limpiar", "nada")
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?), con la ubicación del robot y el estado de limpieza (donde se encuentra el robot).
    """

    def __init__(self, x0=["A", "sucio", "limpio", "sucio", "sucio", "limpio", "sucio"]):
        """ El robot empieza en el cuarto A y todos los cuartos estan sucios // x=[robot,A,B,C,D,E,F]
            Cuartos: D,E,F
                     A,B,C"""
        self.x = x0[:]
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_Der", "ir_Izq", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x #Se asigna el lugar donde empezara el robot y las situaciones (sucio/limpio) de cada cuarto.

        if accion != "nada" or a is "sucio" or b is "sucio" or c is"sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            if accion is "subir" or accion is "bajar":
                self.desempeno -= 2
            else:
                self.desempeno -= 1

        if accion is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"

        #Posibles formas en que el robot se puede mover dependiendo de el cuarto en donde se encuentre.
        elif accion is "ir_Izq" and self.x[0] is "B" or accion is "bajar" and self.x[0] is "F":
            self.x[0] = "A"
        elif accion is "ir_Der" and self.x[0] is "A" or accion is "bajar" and self.x[0] is "E" or accion is "ir_Izq" and self.x[0] is "C":
            self.x[0] = "B"
        elif accion is "ir_Der" and self.x[0] is "B" or accion is "bajar" and self.x[0] is "D":
            self.x[0] = "C"
        elif accion is "subir" and self.x[0] is "C" or accion is "ir_Der" and self.x[0] is "E":
            self.x[0] = "D"
        elif accion is "subir" and self.x[0] is "B" or accion is "ir_Izq" and self.x[0] is "D" or accion is "ir_Der" and self.x[0] is "F":
            self.x[0] = "E"
        elif accion is "subir" and self.x[0] is "A" or accion is "ir_Izq" and self.x[0] is "E":
            self.x[0] = "F"

    def percepcion(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
        Un agente reactivo basado en modelo
        El modelo empieza desde A y sigue la siguiente forma:
            F <- E <- D
            A -> B -> C ↑
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situacion #Sutuacion donde se encuentra el robot actualmente.

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]

        if a==b==c==d==e==f=='limpio': #Cuando todos los cuartos esten limpios se deja de castigar.
            aux='nada'
        elif situacion is 'sucio': #Si el cuarto en que se encuentra el robot esta sucio, este lo limpia.
            aux='limpiar'
        elif robot == 'A' or robot == 'B' or robot == 'F':
            aux='ir_Der'
        elif robot == 'D' or robot == 'E':
            aux = 'ir_Izq'
        elif robot == 'C':
            aux='subir'

        return (aux)

def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatori-o")
    simulador(SeisCuartos(), AgenteAleatorio(('ir_Der', 'ir_Izq', 'subir', 'bajar', 'limpiar', 'nada')), 100)

    print("Prueba del entorno con un agente reactivo con modelo")
    simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)


if __name__ == "__main__":
    test()
    e = SeisCuartos()