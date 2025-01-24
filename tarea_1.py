#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'Luis Mario Sainz'

import entornos_f
import entornos_o
import random

class NineRooms:
    def __init__(self):
        self.rooms = [["dirty"] * 3 for _ in range(3)] # Los tres pisos con tres cuartos (todos sucios por defecto)
        self.agent_position = [0, 0] # [piso, cuarto] inicializados en 0
        self.energy_cost = 0
    
    def perform_action(self, action):
        floor, room = self.agent_position

        if action == "clean":
            self.rooms[floor][room] = "clean"
            self.energy_cost += 1 # Limpiar el cuarto es la segunda opcion economica
        elif action == "go_Right" and room < 2:
            self.agent_position[1] += 1
            self.energy_cost += 2
        elif action == "go_Left" and room > 0:
            self.agent_position[1] -= 1
            self.energy_cost += 2
        elif action == "go_Upstairs" and floor < 2 and room == 2:
            self.agent_position[0] += 1
            self.energy_cost += 5 # Subir las escaleras es una accion costosa
        elif action == "go_Downstairs" and floor >2 and room == 0:
            self.agent_position[0] -= 1
            self.energy_cost += 5 # Bajar las escaleras es una accion costosa
        elif action == "do_Nothing":
            self.energy_cost += 0 # Hacer nada es la opcion mas economica

    def all_rooms_clean(self):
        return all(all(room == "clean" for room in floor) for floor in self.rooms)

    def print_environment(self):
        for floor in reversed(range(3)):
            print(f"Floor {floor + 1}: {self.rooms[floor]}")
            print(f"Agent Position: Floor {self.agent_position[0] + 1}, Room {self.agent_position[1] + 1}")
            print("-" * 30)

class SimpleReflexAgent:
    def __init__(self):
        pass

    def choose_action(self, percept):
        """Choose action based on the current percept"""
        if percept == "dirty":
            return "clean"
        else:
            return random.choice(["go_Right", "go_Left", "go_Upstairs", "go_Downstairs", "do_Nothing"])

class ModelBasedReflexAgent:
    def __init__(self):
        self.internal_state = [[None for _ in range(3)] for _ in range(3)] # Su representacion interna del entorno
        self.visited_rooms = set() # Manteniendo un registro de los cuartos visitados

    def update_state(self, position, percept):
        """Update the internal state based on the percept"""
        floor, room = position
        self.internal_state[floor][room] = percept
        self.visited_rooms.add(tuple(position))
    
    def choose_action(self, position):
        """Choose the next action based on the internal state"""
        floor, room = position

        # Priorizamos limpiar los cuartos sucios
        if self.internal_state[floor][room] == "dirty":
            return "clean"
        
        # Busca el cuarto mas cercano o un cuarto sucio
        for f in range(3):
            for r in range(3):
                if self.internal_state[f][r] != "clean":
                    if f > floor and room == 2:
                        return "go_Upstairs"
                    elif f < floor and room == 0:
                        return "go_Downstairs"
                    elif r > room:
                        return "go_Right"
                    elif r < room:
                        return "go_Left"
        
        # Accion por defecto cuando todos los cuartos se encuentren limpios
        return "do_Nothing"

def simulate(agent, environment, steps=200):
    for step in range(steps):
        if environment.all_rooms_clean():
            print(f"All rooms are clean! Simulation stopped after {step} steps.")
            break
        
        percept = environment.rooms[environment.agent_position[0]][environment.agent_position[1]]

        # Actualiza el estado si el agente es basado en modelo
        if hasattr(agent, 'update_state'):
            agent.update_state(environment.agent_position, percept)
        
        # Decidir una accion
        action = agent.choose_action(
            percept if not hasattr(agent, 'update_state') else environment.agent_position
        )

        # Realizar la accion en el entorno
        environment.perform_action(action)

        # Imprime el entorno despues de cada paso
        print(f"Step {step + 1}: Agent chosen action '{action}'")
        environment.print_environment()
    
    return environment.energy_cost

# Se realiza la comparacion
simple_agent = SimpleReflexAgent()
simple_env = NineRooms()
print("Simple Reflex Agent Simulation:")
simple_cost = simulate(simple_agent, simple_env)

model_agent = ModelBasedReflexAgent()
model_env = NineRooms()
print("\nModel-based Reflex Agent Simulation:")
model_cost = simulate(model_agent, model_env)

# Resultados
print(f"\nEnergy Cost Comparison:\n- Simple Reflex Agent: {simple_cost}\n- Model-based Reflex Agent: {model_cost}")
