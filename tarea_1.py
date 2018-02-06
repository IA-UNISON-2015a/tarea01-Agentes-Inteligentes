#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Rolando Velez'

from random import choice

class Environment:
    def __init__(self, x0=[]):
        self.x = x0[:]
        self.performance = 0

    def legal_action(self, action):
        return True

    def transition(self, action):
        pass
    
    def percepts(self):
        return self.x

class Agent(object):
    def program(self, percepts):
        pass
    
def simulator(env, agent, steps=10, verbose=True):
    performance_history = [env.performance]
    state_history = [env.x[:]]
    action_history = []

    for step in range(steps):
        p = env.percepts()
        a = agent.program(p)
        env.transition(a)

        performance_history.append(env.performance)
        state_history.append(env.x[:])
        action_history.append(a)

    action_history.append(None)

    if verbose:
        print(u"\n\nEnvironment Simulation of type " +
                str(type(env)) +
                " with an Agent of type " +
                str(type(agent)) + "\n")

        print('Step'.center(10) +
                'State'.center(60) +
                u'Action'.center(25) +
                u'Performance'.center(15))

        print('_' * (10 + 60 + 25 + 15))

        for i in range(steps):
            print(str(i).center(10) +
                    str(state_history[i]).center(60) +
                    str(action_history[i]).center(25) +
                    str(performance_history[i]).rjust(12))

        print('_' * (10 + 60 + 25 + 15) + '\n\n')

    return state_history, action_history, performance_history

# Ex. 1
class SixRooms(Environment):
    """
        Six Rooms.                                  _____________
        2 Floors, 3 rooms each floor.               | D | E | F |
        Can only go up on room "A" or "C".          | A | B | C |
        Can only go down on room "E".               -------------
        Actions to perform can only be ["go_right", "go_left", "go_up", "go_down", "suck", "noop"]
    """
    def __init__(self, x0=["A", "dirty", "dirty", "dirty", "dirty", "dirty", "dirty"]):
        
        self.x = x0[:]
        self.performance = 0

    def legal_action(self, action):
       """
            Check if the action the robot wants to perform is legal in the current state.
       """
       if self.x[0] == "A":
           return action in ("go_right", 'go_up', "suck", "noop")
       elif self.x[0] == "B":
           return action in ("go_right", "go_left", "suck", "noop")
       elif self.x[0] == "C":
           return action in ("go_left", "go_up", "suck", "noop")
       elif self.x[0] == "D":
           return action in ("go_right", "suck", "noop")
       elif self.x[0] == "E":
           return action in ("go_right", "go_left", "go_down", "suck", "noop")
       else:
           return action in ("go_left", "suck", "noop")
    
    def transition(self, action):
        """
            First it checks if the action that we want to perform is legal in it's current state.
            Instructions say that the action of "suck" is the cheapest action there is, compared to all others.
            So following that rule, we set the performance value to 0.5 if the robot decides to clean.
            Since the action of going up/down is more costly than all the other actions we set it's performance value at 2.
            Finally I set the performance value of going right/left to 1. (Cheaper than going up/down but higher than cleaning).
            After that there's a lot of if's statements to check where the robot is going next after performing the given action.
        """
        
        if not self.legal_action(action):
            raise ValueError("Action is illegal in the current state. ", str(self.x[0]), str(action))
        
        robot, a, b, c, d, e, f = self.x
        if (action is not "noop" or a is "dirty" or b is "dirty" or c is "dirty" or
                d is "dirty" or e is "dirty" or f is "dirty"):
            if action is "go_up" or action is "go_down":
                self.performance -= 2
            elif action is "suck":
                self.performance -= 0.5
            else:
                self.performance -= 1
        if action is "suck":
            self.x[" ABCDEF".find(self.x[0])] = "clean"
        elif action is "go_right":
            if self.x[0] == "A":
                self.x[0] = "B"
            elif self.x[0] == "B":
                self.x[0] = "C"
            elif self.x[0] == "D":
                self.x[0] = "E"
            elif self.x[0] == "E":
                self.x[0] = "F"
        elif action is "go_left":
            if self.x[0] == "F":
                self.x[0] = "E"
            elif self.x[0] == "E":
                self.x[0] = "D"
            elif self.x[0] == "C":
                self.x[0] = "B"
            elif self.x[0] == "B":
                self.x[0] = "A"
        elif action == "go_up":
            if self.x[0] == "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        elif action == "go_down":
            self.x[0] = "B"
    
    def percepts(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


# Ex. 2

class SixRoomsRandomAgent(Agent):
    
    def __init__(self, actions):
        self.actions = actions
    
    def program(self, percepts):
        if percepts[0] == "A":
            return choice(["go_right", "go_up", "suck", "noop"])
        elif percepts[0] == "B":
            return choice(["go_right", "go_left", "suck", "noop"])
        elif percepts[0] == "C":
            return choice(["go_left", "go_up", "suck", "noop"])
        elif percepts[0] == "D":
            return choice(["go_right", "suck", "noop"])
        elif percepts[0] == "E":
            return choice(["go_right", "go_left", "go_down", "suck", "noop"])
        else:
            return choice(["go_left", "suck", "noop"])

class SixRoomsModelBasedReflexAgent(Agent):

    def __init__(self):
        self.model = ['A', 'dirty', 'dirty', 'dirty', 'dirty', 'dirty', 'dirty']

    def program(self, percepts):
        robot_pos, status = percepts

        self.model[0] = robot_pos
        self.model[' ABCDEF'.find(robot_pos)] = status

        a, b, c, d, e, f = self.model[1], self.model[2], self.model[3], \
                self.model[4], self.model[5], self.model[6]

        if a == b == c == d == e == f == "clean":
            return "noop"
        elif status == "dirty":
            return "suck"
        elif robot_pos == "A":
            if b == "dirty" or c == "dirty":
                return "go_right"
            else:
                return "go_up"
        elif robot_pos == "B":
            if a == "dirty":
                return "go_left"
            else:
                return "go_right"
        elif robot_pos == "C":
            if a == "dirty" or b == "dirty":
                return "go_left"
            else:
                return "go_up"
        elif robot_pos == "D":
            if a == "dirty" or b == "dirty" or c == "dirty" or e == "dirty" or f == "dirty":
                return "go_right"
        elif robot_pos == "E":
            if d == "dirty":
                return "go_left"
            elif f == "dirty":
                return "go_right"
            else:
                return "go_down"
        else:
            if a == "dirty" or b == "dirty" or c == "dirty" or d == "dirty" or e == "dirty":
                return "go_left"


# Ex. 3
class TwoRoomsEnvironment(Environment):

    def __init__(self, x0=["A", "dirty", "dirty"]):
        self.x = x0[:]
        self.performance = 0

    def legal_action(self, action):
        return action in ("go_A", "go_B", "suck", "noop")

    def transition(self, action):
        if not self.legal_action(action):
            raise ValueError("Action is illegal in the current state.", str(self.x[0]), str(action))

        robot, a, b = self.x
        if action is not "noop" or a is "dirty" or b is "dirty":
            self.performance -= 1
        if action is "suck":
            self.x[" AB".find(self.x[0])] = "clean"
        elif action is "go_A":
            self.x[0] = "A"
        elif action is "go_B":
            self.x[0] = "B"
    
    def percepts(self):
        return self.x[0], self.x[" AB".find(self.x[0])]

class BlindTwoRoomsEnvironment(TwoRoomsEnvironment):
    """
    Robot only knows the room he's in but not if it's clean or dirty.
    """
    def percepts(self):
        return self.x[0]

class TwoRoomsReflexAgent(Agent):
    def program(self, percepts):
        robot, status = percepts
        return ("suck" if status == "dirty" else
                "go_A" if robot == "B" else "go_B")

def sre_test():
    print("Random Agent on the Six Rooms Environment")
    simulator(SixRooms(),
            SixRoomsRandomAgent(["go_right", "go_left", "go_up", "go_down", "suck", "noop"]),
            100) 
    
    print("Model-Based Reflex Agent on the Six Rooms Environment")
    simulator(SixRooms(),
            SixRoomsModelBasedReflexAgent(),
            100)

if __name__ == "__main__":
    sre_test()
