#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------
wawa
Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Alexis Martinez'

import entornos_o
from random import choice,random

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
import doscuartos_o
from doscuartos_o import AgenteReactivoModeloDosCuartos


class DosCuartosCiego(doscuartos_o.DosCuartos):

    def percepción(self):
        return self.x[0]


class DosCuartosEstocastico(doscuartos_o.DosCuartos):

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            if random() <= .80:
                self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"
# Agrega los modulos que requieras de python


class SeisCuartos(entornos_o.Entorno):

    def __init__(self,x0=["A","sucio","sucio","sucio","sucio","sucio","sucio"]):
        """
        Inicializamos en el cuarto A planta baja y todo esta sucio

        acomodo de los cuartos:
            D | E | F
            A | B | C


        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self,accion,robot):
        if robot == "E" and accion in ("bajar","ir_izquierda","ir_derecha","nada","limpiar"):
            return accion
        elif robot == "B" and accion in ("subir","ir_izquierda","ir_derecha","nada","limpiar"):
            return accion
        elif robot == "D" and accion in ("bajar","ir_derecha","nada","limpiar"):
            return accion
        elif robot == "A" and accion in ("subir","ir_derecha","nada","limpiar"):
            return accion
        elif robot == "F" and accion in ("bajar","ir_izquierda","nada","limpiar"):
            return accion
        elif robot == "C" and accion in ("subir","ir_izquierda","nada","limpiar"):
            return accion
        else:
            return False

    def transición(self, acción):
        robot,a,b,c,d,e,f = self.x
      #  print("robot:{} accion:{} \n".format(robot,acción))

        if not self.acción_legal(acción,robot):
            raise ValueError("La acción no es legal para este estado")

        if acción is not "nada" or "sucio" in (a,b,c,d,e,f):
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[(" ABCDEF".find(self.x[0]))] = "limpio"
        elif acción is "ir_izquierda":
            if robot == "C":
                self.x[0] = "B"
            elif robot == "F":
                self.x[0] = "E"
            elif robot == "B":
                self.x[0] = "A"
            elif robot == "E":
                self.x[0] = "D"
        elif acción is "ir_derecha":
            if robot == "A":
                self.x[0] = "B"
            elif robot == "D":
                self.x[0] = "E"
            elif robot == "B":
                self.x[0] = "C"
            elif robot == "E":
                self.x[0] = "F"
        elif acción is "subir":
            self.desempeño -= 1
            if robot == "A":
                self.x[0] = "D"
            elif robot == "B":
                self.x[0] = "E"
            elif robot == "C":
                self.x[0] = "F"
        elif acción is "bajar":
            self.desempeño -= 1
            if robot == "D":
                self.x[0] = "A"
            elif robot == "E":
                self.x[0] = "B"
            elif robot == "F":
                self.x[0] = "C"


    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        robot = percepcion[0]

        if robot == "E":
            self.acciones = ("bajar","ir_izquierda","ir_derecha","nada","limpiar")
        elif robot == "B":
            self.acciones = ("subir","ir_izquierda","ir_derecha","nada","limpiar")
        elif robot == "D":
            self.acciones = ("bajar","ir_derecha","nada","limpiar")
        elif robot == "A":
            self.acciones = ("subir","ir_derecha","nada","limpiar")
        elif robot == "F":
            self.acciones = ("bajar","ir_izquierda","nada","limpiar")
        elif robot == "C":
            self.acciones = ("subir","ir_izquierda","nada","limpiar")

        return choice(self.acciones)


class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ["A","sucio","sucio","sucio","sucio","sucio","sucio"]

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a,b,c,d,e,f = self.modelo[1:]

        if a==b==c==d==e==f == "limpio":
            return 'nada'
        else:
            if situación == 'sucio':
                return 'limpiar'
            else:
                if robot == 'A':
                    return ('ir_derecha' if 'sucio' in [b,c] else
                            'subir')
                elif robot == 'B':
                    return('ir_derecha' if c =='sucio' else
                           'ir_izquiera' if a == 'sucio' else 'subir')
                elif robot == 'C':
                    return ('ir_izquierda' if 'sucio' in [a,b] else
                            'subir')
                elif robot == 'D':
                    return ('ir_derecha' if 'sucio' in [e,f] else
                            'bajar')
                elif robot == 'E':
                    return('ir_derecha' if f =='sucio' else
                           'ir_izquierda' if d == 'sucio' else 'bajar')
                elif robot == 'F':
                    return ('ir_izquierda' if 'sucio' in [d,e] else
                            'bajar')

class AgenteRacionalDosCuartos(entornos_o.Agente):

    def __init__(self):

        self.cont = 0



    def programa(self,percepcion):
        robot = percepcion
        self.cont += 1

        if self.cont == 1 or self.cont == 3:
            return "limpiar"
        elif self.cont == 2 :
            return ('ir_B' if robot =='A' else 'ir_A')
        else:
            return 'nada'









print("Prueba del entorno con un agente aleatorio Seis Cuartos")
entornos_o.simulador(SeisCuartos(),
                     AgenteAleatorio(['ir_izquierda', 'ir_derecha','subir','bajar','limpiar', 'nada']),
                         100)
print("Prueba del entorno con un agente Reactivo Seis Cuartps")
entornos_o.simulador(SeisCuartos(),
                     AgenteReactivoModeloSeisCuartos(),
                     100)
"""
    Para el modelo de seis cuartos el agente Reactivo basado en modelo lo limpia todo
    para el paso 12 con un desempeño de -12
    y para el aleatorio los resultados dieron a partir de la pasada 70 con un
    desempeño mayor a -90 en alguna de mis corridas fue la menor


"""

print("Prueba del entorno con un agente racional Modelo Ciego")
entornos_o.simulador(DosCuartosCiego(), AgenteRacionalDosCuartos(),
                     50)

print("Prueba del entorno con un agente aleatorio Modelo Ciego")
entornos_o.simulador(DosCuartosCiego(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                     50)
"""
    Para el modelo dos cuartos Ciego siempre para el paso 4 ya tenia todo limpia con
    un desempeño de -3
    y con el aleatorio por el paso 20 con un desempeño de -19 fue la menor de las
    pasadas hechas
"""

print("Prueba del entorno con un agente racional Modelo Estocastico")
entornos_o.simulador(DosCuartosEstocastico(),doscuartos_o.AgenteReactivoModeloDosCuartos(),
                     50)

print("Prueba del entorno con un agente aleatorio Modelo Estocastico")
entornos_o.simulador(DosCuartosEstocastico(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                     50)
"""
    Con el Agente racional obtuve un minimo de -3 en desempeño y un maximo de -6 en las pasadas obtenidas
    y el aleatorio se limpio todo para la pasada 16 con un desempeño de -16

"""
