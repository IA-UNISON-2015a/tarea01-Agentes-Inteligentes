#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

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
__author__ = 'Rafael Alejandro Castillo Lopez'

import random
from collections import namedtuple

class Environment:
    '''
    Clase abstracta para ambientes, implementa cosas utiles
    '''
    def __init__(self, x0):
        self._state = x0
        self.performance = 0

    def transition(self, action):
        if not self.legal_action(action):
            raise ValueError("Accion ilegal")
        return self._transition(action)

    def legal_action(self, action):
        raise NotImplementedError

    def _transition(self, action):
        raise NotImplementedError

    @property
    def state(self):
        return self._state

    @property
    def percerpts(self):
        return self.state

    def __repr__(self):
        class_name = self.__class__.__name__
        return "{}(estado={}, desempeño={})".format(class_name,
                                                    self._state,
                                                    self.performance)


HouseState = namedtuple('HouseState', ['position', 'rooms'])

class HouseEnvironment(Environment):
    '''
    Modelo del ambiente de una casa de seis cuartos, para que una
    aspiradora robotica haga lo suyo
    '''
    actions = {'left', 'right', 'up', 'down', 'clean', 'noop'}

    def __init__(self, x0=HouseState(0, ['dirty' for _ in range(6)])):
        super().__init__(x0)

    def legal_action(self, action):
        pos = self._state.position
        return (action in self.actions and not
                (action == 'up' and  pos > 2) or
                (action == 'down' and pos < 3))

    def _transition(self, action):
        position, rooms = self._state

        if action == 'left':
            self.performance -= 1
            new_position = position - 1  if position % 3 \
                           else position
            self._state = HouseState(new_position, rooms)
        elif action == 'right':
            self.performance -= 1
            print((position + 1) % 3)
            new_position = position + 1 if (position + 1) % 3 \
                           else position
            self._state = HouseState(new_position, rooms)
        elif action == 'up':
            self.performance -= 2
            self._state = HouseState(position + 3, rooms)
        elif action == 'down':
            self.performance -= 2
            self._state = HouseState(position - 3, rooms)
        elif action == 'clean':
            self.performance -= 1
            rooms[position] = 'clean'

    @property
    def state(self):
        current = self._state
        return HouseState(current.position, current.rooms[:])

    @property
    def percepts(self):
        position, rooms = self._state
        return position, rooms[position]


class ReactiveHouseAgent:
    '''
    Clase que implementa un agente reactivo para el entorno de la
    aspiradora en la casa. Funciona haciendo un recorrido fijo y
    deteniendose a limpiar si encuentra un cuarto sucio, y
    deteniendose por completo cuando da una vuelta por toda la casa
    '''
    movement_sequence = ['right', 'right', 'up',
                         'down', 'left', 'left']
    route = [1, 2, 5, 0, 3, 4]
    def __init__(self):
        self.starting_position = None

    def program(self, percerpts):
        position, room_state = percerpts

        next_room = self.route[position]

        if self.starting_position is None:
            self.starting_position = position

        if room_state == 'dirty':
            return 'clean'
        elif self.starting_position == next_room:
            return 'noop'
        else:
            return self.movement_sequence[position]


def simulate(environment, agent, steps=20):
    for step in range(steps):
        p = environment.percepts
        print(p)
        a = agent.program(p)
        environment.transition(a)

        yield step, environment.state, a, environment.performance

environment = HouseEnvironment()
agent = ReactiveHouseAgent()

for step, state, action, performance in simulate(environment, agent):
    print(state, action)

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
