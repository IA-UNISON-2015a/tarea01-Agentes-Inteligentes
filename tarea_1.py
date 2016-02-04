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
__author__ = 'Nan'

import entornos, random
# Requiere el modulo entornos.py
# El modulo doscuartos.py puede ser de utilidad para reutilizar código
# Agrega los modulos que requieras de python

class SeisCuartos(entornos.Entorno):
    """
    distribucion de los cuartos:
    | D | E | F |
    | A | B | C |
    """
    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no se puede realizar en este estado")

        nuevo = list(estado)
        modelo = ('robot', 'A', 'B', 'C', 'D', 'E', 'F')

        if accion == 'limpiar':
            nuevo[modelo.index(nuevo[0])] = 'limpio'
        elif accion == 'subir':
            nuevo[0] = modelo[modelo.index(nuevo[0]) + 3]
        elif accion == 'bajar':
            nuevo[0] = modelo[modelo.index(nuevo[0]) - 3]
        elif accion == 'irDerecha':
            nuevo[0] = modelo[modelo.index(nuevo[0]) + 1]
        elif accion == 'irIzquierda':
            nuevo[0] = modelo[modelo.index(nuevo[0]) - 1]

        return tuple(nuevo)

    def sensores(self, estado):
        modelo = ('robot', 'A', 'B', 'C', 'D', 'E', 'F')
        return (estado[0], estado[modelo.index(estado[0])])

    def accion_legal(self, estado, accion):
        if (estado[0] == 'A' or estado[0] == 'D') and accion == 'irIzquierda':
            return False
        if (estado[0] == 'C' or estado[0] == 'F') and accion == 'irDerecha':
            return False
        if estado[0] < 'D' and accion == 'bajar':
            return False
        if estado[0] > 'C' and accion == 'subir':
            return False
        return True

    def desempeno_local(self, estado, accion):
        if accion == 'subir' or accion == 'bajar':
            return -2
        if accion == 'noOp' and not 'sucio' in estado:
            return 0
        return -1

class DosCuartosACiegas(entornos.Entorno):
    """
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
        robot, A, B = estado
        return robot

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class DosCuartosSemiLimpio(entornos.Entorno):
    """
    """

    def transicion(self, estado, accion):
        if not self.accion_legal(estado, accion):
            raise ValueError("La accion no es legal para este estado")

        robot, A, B = estado

        return (('A', A, B) if accion == 'irA' else
                ('B', A, B) if accion == 'irB' else
                (robot, A, B) if accion == 'noOp' else
                ('A', ('limpio' if random.random() <= 0.8 else 'sucio'), B) if accion == 'limpiar' and robot == 'A' else
                ('B', A, ('limpio' if random.random() <= 0.8 else 'sucio')))

    def sensores(self, estado):
        robot, A, B = estado
        return robot, A if robot == 'A' else B

    def accion_legal(self, estado, accion):
        return accion in ('irA', 'irB', 'limpiar', 'noOp')

    def desempeno_local(self, estado, accion):
        robot, A, B = estado
        return 0 if accion == 'noOp' and A == B == 'limpio' else -1


class AgenteAleatorioDosCuartos(entornos.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self):
        self.acciones = ('irA', 'irB', 'limpiar', 'noOp')

    def programa(self, percepcion):
        return random.choice(self.acciones)


class AgenteReactivoSeisCuartos(entornos.Agente):
    """docstring for AgenteReactivoSeisCuartos"""

    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        self.modelo[0], situacion = percepcion
        self.modelo[' ABCDEF'.index(self.modelo[0])] = situacion

        if not 'sucio' in self.modelo:
            return 'noOp'

        return ('limpiar' if situacion == 'sucio' else
            'irDerecha' if self.modelo[0] < 'C' else
            'subir' if self.modelo[0] == 'C' else
            'irIzquierda' if self.modelo[0] > 'D' else
            'bajar')

class AgenteAleatorioSeisCuartos(entornos.Agente):
    """docstring for AgenteAleatorioSeisCuartos"""
    
    def __init__(self):
        self.acciones = {
            'A': ('irDerecha', 'subir', 'limpiar', 'noOp'),
            'B': ('irIzquierda', 'irDerecha', 'subir', 'limpiar', 'noOp'),
            'C': ('irIzquierda', 'subir', 'limpiar', 'noOp'),
            'D': ('irDerecha', 'bajar', 'limpiar', 'noOp'),
            'E': ('irIzquierda', 'irDerecha', 'bajar', 'limpiar', 'noOp'),
            'F': ('irIzquierda', 'bajar', 'limpiar', 'noOp')
        }

    def programa(self, percepcion):
        robot, _ = percepcion
        return random.choice(self.acciones[robot])
        
class AgenteReactivoCiegoDosCuartos(entornos.Agente):
    """docstring for AgenteReactivoCiegoDosCuartos"""

    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']
    
    def programa(self, percepcion):
        self.modelo[0] = percepcion

        if not 'sucio' in self.modelo:
            return 'noOp'

        situacion = self.modelo[' AB'.index(self.modelo[0])]
        self.modelo[' AB'.index(self.modelo[0])] = 'limpio'


        return ('limpiar' if situacion == 'sucio' else
                'irA' if self.modelo[0] == 'B' else
                'irB')
        
class AgenteReactivoDosCuartosSemilimpio(entornos.Agente):
    """docstring for AgenteReactivoDosCuartosSemilimpio"""
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        self.modelo[0], situacion = percepcion
        self.modelo[' AB'.index(self.modelo[0])] = situacion

        if not 'sucio' in self.modelo:
            return 'noOp'

        return ('limpiar' if situacion == 'sucio' else
                'irA' if self.modelo[0] == 'B' else
                'irB')
        

def test():
    """
    Prueba del entorno y los agentes

    """

    print "Prueba del entorno de seis cuartos con un agente reactivo"
    entornos.simulador(SeisCuartos(),
                       AgenteReactivoSeisCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de seis cuartos con un agente aleatorio"
    entornos.simulador(SeisCuartos(),
                       AgenteAleatorioSeisCuartos(),
                       ('A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo ciego"
    entornos.simulador(DosCuartosACiegas(),
                       AgenteReactivoCiegoDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartosACiegas(),
                       AgenteAleatorioDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente reactivo ciego"
    entornos.simulador(DosCuartosSemiLimpio(),
                       AgenteReactivoDosCuartosSemilimpio(),
                       ('A', 'sucio', 'sucio'), 100)

    print "Prueba del entorno de dos cuartos con un agente aleatorio"
    entornos.simulador(DosCuartosSemiLimpio(),
                       AgenteAleatorioDosCuartos(),
                       ('A', 'sucio', 'sucio'), 100)

if __name__ == '__main__':
    test()

        
