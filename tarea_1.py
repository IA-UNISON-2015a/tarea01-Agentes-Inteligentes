#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------
Tarea de desarrollo de entornos y agentes
==========================================
En esta tarea realiza las siguiente acciones:
1.- Desarrolla un entorno similar al de los dos cuartos,
    pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.
    Las acciones totales serán
    A = {"irDerecha", "irIzquierda", "subir", "bajar", "limpiar" y "noOp"}
    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.
    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.
2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.
3.- Al ejemplo original de los dos cuardos, modificalo de manera que el agente
    sabe en que cuarto se encuentra pero no sabe si está limpio o sucio.
    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.
4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.
Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.
"""
__author__ = 'Jorge_Carvajal'

import entornos
import math
import copy
import random
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

from random import choice

 
class SeisCuartos(entornos.Entorno):
    """
    Clase para un entorno de 6 cuartos en un total de 2 pisos.
    El estado se define como 
                (robot, D1,D2,D3,U1,U2,U3) 
    donde robot puede tener los valores "D1", ..., "U3"
   "D1", .. "U3" pueden tener los valores "limpio", "sucio"
    Las acciones válidas en el entorno son 
            "subir", "subir", "irDerecha", "irIzquierda", "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.
    Los sensores es una tupla 
                (robot, limpio?) 
    con la ubicación del robot y el estado de limpieza
    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, D1,D2,D3,U1,U2,U3 = estado
        if accion  == 'noOp': 
            return (robot,D1,D2,D3,U1,U2,U3)
        if accion == 'limpiar':
            if robot == 'D1':
                return (robot,'limpio',D2,D3,U1,U2,U3)
            elif robot == 'D2':
                return (robot,D1,'limpio',D3,U1,U2,U3)
            elif robot == 'D3':
                return (robot,D1,D2,'limpio',U1,U2,U3)
            elif robot == 'U1':
                return (robot,D1,D2,D3,'limpio',U2,U3)
            elif robot == 'U2':
                return (robot,D1,D2,D3,U1,'limpio',U3)
            elif robot == 'U3':
                return (robot,D1,D2,D3,U1,U2,'limpio')
        cuarto = 'U1'
        if accion == 'irDerecha':
            cuarto = robot[0] + str((int(robot[1]) + 1))
        elif accion == 'irIzquierda':
            cuarto = robot[0] + str((int(robot[1]) - 1))
        elif accion == 'subir':
            cuarto = 'U' + robot[1]
        elif accion == 'bajar':
            cuarto = 'D' + robot[1]
        return (cuarto,D1,D2,D3,U1,U2,U3)

    def sensores(self, estado):
        robot, D1,D2,D3,U1,U2,U3 = estado
        if robot == 'D1':
            return robot,D1
        if robot == 'D2':
            return robot,D2
        if robot == 'D3':
            return robot,D3
        if robot == 'U1':
            return robot,U1
        if robot == 'U2':
            return robot,U2
        if robot == 'U3':
            return robot,U3

    def accion_legal(self, estado, accion):
        robot, D1,D2,D3,U1,U2,U3 = estado
        if not(
            accion == 'subir' and (robot[0] == 'U' or robot[1] == '2') or
            accion == 'bajar' and (robot[0] == 'D' or robot[1] == '2') or 
            accion == 'irDerecha' and robot[1] == '3' or
            accion == 'irIzquierda' and robot[1] == '1'
            ):
            return accion in ('irDerecha','irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, U1,U2,U3,D1,D2,D3 = estado
        if accion == 'noOp' and U1 == U2 == U3 == D1 == D2 == D3 == 'limpio':
            return 0
        if accion == 'noOp':
            return -1
        if accion == 'subir' or accion == 'bajar': 
            return -4 # -4 cubre el peor de los casos, tener que limpiar todos los cuartos de un piso estando en el cuarto de enmedio
        return -1

class AgenteAleatorioSeisCuartos(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        accionesLegales = copy.copy(self.acciones)
        robot, cuarto = percepcion
        if(robot[0] == 'U' or robot[1] == '2'):
            accionesLegales.remove('subir')
        if(robot[0] == 'D' or robot[1] == '2'):
            accionesLegales.remove('bajar')
        if(robot[1] == '1'):
            accionesLegales.remove('irIzquierda')
        if(robot[1] == '3'):
            accionesLegales.remove('irDerecha')
        return choice(accionesLegales) 


class AgenteReactivoSeisCuartos(entornos.Agente):
    """
    Un agente reactivo simple
    U1 == 'sucio' or U2 == 'sucio' or U3 == 'sucio' or D1 == 'sucio' or D2 == 'sucio' or D3 == 'sucio'
    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irDerecha' if robot[0] == 'D' and robot[1] != '3' else
                'subir' if robot[1] == '3' and robot[0] == 'D' else
                'irIzquierda' if robot[1] != '1' else
                'bajar')


class AgenteReactivoModeloSeisCuartos(entornos.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['D2', 'sucio', 'sucio','sucio','sucio','sucio','sucio']
        self.lugar = {'D1': 1, 'D2': 2,'D3': 3, 'U1': 4,'U2': 5, 'U3': 6 }

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[self.lugar[robot]] = situacion

        # Decide sobre el modelo interno
        D1,D2,D3,U1,U2,U3 = self.modelo[1], self.modelo[2],self.modelo[3],self.modelo[4],self.modelo[5],self.modelo[6]
        return ('noOp' if D1 == D2 == D3 == U1 == U2 == U3 =='limpio' else
                'limpiar' if situacion == 'sucio' else
                # checa si el cuarto de la derecha ya lo limpiaste antes de ir a la derecha
                'irDerecha' if robot[1] != '3' and self.modelo[self.lugar[robot]+1] == 'sucio' else
                'irIzquierda' if robot[1] != '1' and (self.modelo[self.lugar[robot]-1] == 'sucio' or (self.modelo[self.lugar[robot]-2] == 'sucio')) else
                'subir' if robot[0] == 'D' and (robot[1] == '1' or robot[1] == '3') and D1 == D2 == D3 == 'limpio' else
                'bajar' )

"""
incisos 3 y 4 de tarea.....
"""
class DosCuartosCiego(entornos.Entorno):
    """
    Clase para un entorno de dos cuartos sin sensor de limpieza.
    El estado se define como 
                (robot, A, B) 
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"
    Las acciones válidas en el entorno son 
            "irA", "irB", "limpiar" y "noOp". 
    Todas las acciones son válidas en todos los estados.
    Los sensores devuelven un valor
                (robot)
    con la ubicación del robot
    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B = estado

        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', 'limpio', B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, 'limpio'))

    def sensores(self, estado):
        robot = estado[0]
        return robot

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class AgenteAleatorioDosCuartos(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales
    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteReactivoModeloDosCuartosCiego(entornos.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos
        """
        self.modelo = ['A', 'sucio', 'sucio']
        self.lugar = {'A': 1, 'B': 2}

    def programa(self, percepcion):
        robot = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        if (self.modelo[1] == self.modelo[2] == 'limpio'):
            return 'noOp'
        if(self.modelo[self.lugar[self.modelo[0]]] == 'sucio' ):
            self.modelo[self.lugar[self.modelo[0]]] = 'limpio'
            return 'limpiar'
        if(self.modelo[0] == 'A'):
            return 'irB'
        return 'irA'

class DosCuartosAleatorio(entornos.Entorno):

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B = estado

        estadoLimpieza = None
        if (accion == 'limpiar'):
            rand = random.random()
            if(rand < 0.8):
                estadoLimpieza = 'limpio'
            else:
                estadoLimpieza = 'sucio'
        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', estadoLimpieza, B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, estadoLimpieza))

    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1

class AgenteReactivoDosCuartos(entornos.Agente):
    """
    Un agente reactivo simple
    """

    def programa(self, percepcion):
        robot, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'irA' if robot == 'B' else
                'irB')
def test():
    """
    Prueba del entorno y los agentes
    """
    print "Prueba del entorno de seis cuartos con un agente aleatorio"
    entornos.simulador(SeisCuartos(),
                       AgenteAleatorioSeisCuartos(['irDerecha','irIzquierda', 'subir', 'bajar', 'limpiar', 'noOp']),
                       ('D1', 'sucio', 'sucio','sucio','sucio','sucio','sucio'), 100)

    print "Prueba del entorno de seis cuartos con un agente reactivo"
    entornos.simulador(SeisCuartos(),
                       AgenteReactivoSeisCuartos(),
                       ('D1', 'sucio', 'sucio','sucio','sucio','sucio','sucio'), 100)

    print "Prueba del entorno de seis cuartos con un agente reactivo basado en modelo"
    entornos.simulador(SeisCuartos(),
                       AgenteReactivoModeloSeisCuartos(),
                       ('U1', 'sucio', 'sucio','sucio','sucio','sucio','sucio'), 100)
    print "Prueba del entorno de dos cuartos a ciegas con un agente aleatorio"
    entornos.simulador(DosCuartosCiego(),
                       AgenteAleatorioDosCuartos(['irA','irB','limpiar','noOp']),
                       ('A', 'sucio', 'sucio'), 100)
    print "Prueba del entorno de dos cuartos a ciegas con un agente reactivo basado en modelo"
    entornos.simulador(DosCuartosCiego(),
                       AgenteReactivoModeloDosCuartosCiego(),
                       ('A', 'sucio', 'sucio'), 100)
    print "Prueba del entorno de dos cuartos con falla aleatoria con un agente aleatorio"
    entornos.simulador(DosCuartosAleatorio(),
                       AgenteAleatorioDosCuartos(['irA','irB','limpiar','noOp']),
                       ('A', 'sucio', 'sucio'), 100)
    print "Prueba del entorno de dos cuartos con falla aleatoria con un agente reactivo"
    entornos.simulador(DosCuartosAleatorio(),
                       AgenteReactivoDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)


if __name__ == '__main__':
    test()