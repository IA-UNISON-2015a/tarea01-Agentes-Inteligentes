#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

    Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra en el módulo doscuartos_o.py),
    pero con tres cuartos en el primer piso, tres cuartos en el segundo piso y tres cuartos en el 3er piso.

    El entorno se llamará NueveCuartos.

    Las acciones totales serán ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    La acción de "subir" solo es legal en los primeros dos pisos, en los cuartos de la derecha,
    mientras que la acción de "bajar" solo es legal en los dos pisos de arriba de arriba y en el cuarto de la izquierda.

    Las acciones de subir y bajar son mas costosas en término de energía que ir a la derecha y a la
    izquierda, por lo que la función de desempeño debe de ser de tener limpios todos los cuartos, con
    el menor numero de acciones posibles, y minimizando subir y bajar en relación a ir a los lados.
    El costo de limpiar es menor a los costos   de cualquier acción.

    Diseña un Agente reactivo basado en modelo para este entorno y compara su desempeño con un agente
    aleatorio despues de 200 pasos de simulación.

    A este modelo de NueveCuartos, modificalo de manera que el agente solo pueda saber en que cuarto se
    encuentra pero no sabe si está limpio o sucio. Utiliza la herencia entre clases para no escribir código redundante.

    A este nuevo entorno llamalo NueveCuartosCiego.

    Diseña un agente racional para este problema, pruebalo y comparalo con el agente aleatorio.

    Al modelo original de NueveCuartos modificalo para que cuando el agente decida aspirar, el 80% de
    las veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, cuando el agente decida
    cambiar de cuarto, se cambie correctamente de cuarto el 80% de la veces, el 10% de la veces se queda
    en su lugar y el 10% de las veces realiza una acción legal aleatoria. Diseña un agente racional para
    este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llámalo NueveCuartosEstocástico.

    Todos los incisos tienen un valor de 25 puntos sobre la calificación de
    la tarea.

"""
__author__ = 'Garcia Celeste'

import entornos_f
from random import choice, sample

# Requiere el modulo entornos_f.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python
class NueveCuartos(entornos_f.Entorno):
    def acción_legal(self, estado, acción):
        if estado[0] == "A":
            return acción in ("ir_Der", "limpiar", "nada")
        elif estado[0] == "B" or estado[0] == "E" or estado[0] == "H":
            return acción in ("ir_Der", "ir_Izq", "limpiar", "nada")
        elif estado[0] == "C" or estado[0] == "F":
            return acción in ("ir_Izq", "subir", "limpiar", "nada")
        elif estado[0] == "D" or estado[0] == "G":
            return acción in ("ir_Der", "bajar", "limpiar", "nada")
        elif estado[0] == "I":
            return acción in ("ir_Izq", "limpiar", "nada")

    def transición(self, estado, acción):
        robot, cuartos = estado[0], estado[1][:]

        def todos_limpios():
            return all([x == 'limpio' for x in cuartos])

        def modificar_estado(robot, cuartos, acción):
            if acción is "ir_Der":
                if estado[0] is "A":
                    robot = "B"
                elif estado[0] is "B":
                    robot = "C"
                elif estado[0] is "D":
                    robot = "E"
                elif estado[0] is "E":
                    robot = "F"
                elif estado[0] is "G":
                    robot = "H"
                elif estado[0] is "H":
                    robot = "I"
                c_local = 2
            elif acción is "ir_Izq":
                if estado[0] is "B":
                    robot = "A"
                elif estado[0] is "C":
                    robot = "B"
                elif estado[0] is "E":
                    robot = "D"
                elif estado[0] is "F":
                    robot = "E"
                elif estado[0] is "H":
                    robot = "G"
                elif estado[0] is "I":
                    robot = "H"
                c_local = 2
            elif acción is "bajar":
                if estado[0] is "D":
                    robot = "A"
                elif estado[0] is "G":
                    robot = "D"
                c_local = 3
            elif acción is "subir":
                if estado[0] is "C":
                    robot = "F"
                elif estado[0] is "F":
                    robot = "I"
                c_local = 3
            elif acción is "limpiar":
                cuartos["ABCDEFGHI".find(estado[0])] = "limpio"
                c_local = 1
            else:
                if todos_limpios():
                    c_local = 0
                else:
                    c_local = 4
            return robot, cuartos, c_local

        #cl = costo_local(acción)
        r, c , cl= modificar_estado(robot, cuartos, acción)
        return ((r, c), cl)

    def percepción(self, estado):
        return estado[0], estado[1]["ABCDEFGHI".find(estado[0])]

class AgenteReactivoModeloNuevecuartos(entornos_f.Agente):
        """ Un agente reactivo basado en el modelo """
        def __init__(self):
            """ Inicializa el modelo interno en el peor de los casos """
            cuartos = ["sucio"] * 9
            self.modelo = ['A', cuartos]

        def programa(self, percepción):
             robot, situación = percepción

             # Actualiza el modelo interno
             self.modelo[0] = robot
             self.modelo[1]['ABCDEFGHI'.find(robot)] = situación

             def calcular_acción(percepción):
                if situación is "sucio":
                    return "limpiar"
                else:
                    if all([x == "limpio" for x in self.modelo[1]]):
                        return "nada"
                    elif robot == "A" or robot == "B" or robot == "E":
                        return "ir_Der"
                    elif robot == "H" and self.modelo[1][8] is "sucio":
                        return "ir_Der"
                    elif robot == "H" and self.modelo[1][8] is "limpio":
                        return "ir_Izq"
                    elif robot == "B" or robot == "E" or robot == "I":
                        return "ir_Izq"
                    elif robot == "D" and self.modelo[1][4] is "sucio":
                        return "ir_Der"
                    elif robot == "C" or robot == "F":
                        return "subir"
                    elif robot == "G":
                        return "bajar"
                    elif robot == "D" and  self.modelo[1][4] is "limpio":
                        return "bajar"

            # Decide sobre el modelo interno
             return (calcular_acción(percepción))

class AgenteAleatorio(entornos_f.Agente):
        def __init__(self, acciones):
            self.acciones = acciones
            cuartos = ["sucio"] * 9
            self.modelo = ['A', cuartos]

        def programa(self, percepción):
            self.modelo[0] = percepción[0]
            for a in sample(self.acciones, len(self.acciones)):
                if NueveCuartos().acción_legal(self.modelo[0], a):
                    return a

def prueba_agente(agente):
    entornos_f.imprime_simulación(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            ["A", ["sucio"] * 9],200),
            ["A", ["sucio"]* 9])

class NueveCuartosCiego(NueveCuartos):
    def percepción(self, estado)Ñ
    return estado[0]

def test():
    """
    Prueba del entorno y los agentes
    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_Der', 'ir_Izq', 'subir', 'bajar', 'limpiar', 'nada']))

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNuevecuartos())

if __name__ == "__main__":
    test()
