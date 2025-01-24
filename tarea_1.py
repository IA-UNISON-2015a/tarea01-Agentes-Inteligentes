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


class NueveCuartos:
    def __init__(self):
        # Iniciamos el entorno con los nueve cuartos mediante una cuadricula 3x3, cada cuarto con un estado limpio o sucio
        self.rooms = [
            ["sucio", "sucio", "sucio"],    # Primer piso
            ["sucio", "sucio", "sucio"],    # Segundo piso
            ["sucio", "sucio", "sucio"],    # Tercer piso
        ]
        self.agent_position = [0, 0] # [piso, cuarto]
        self.energy_cost = 0  # Registra el costo total de las acciones

        # Definimos el costo de las acciones
        self.action_costs = {
            "limpiar": 1,
            "ir_Derecha": 2,
            "ir_Izquierda": 2,
            "subir": 5,
            "bajar": 5, 
            "nada": 0,
        }
    def perform_actions(self, action):
        floor, room = self.agent_position
        if action == "limpiar":
            if self.rooms[floor][room] == "sucio":
                self.rooms[floor][room] = "limpiar"
                self.energy_cost += self.action_costs["limpiar"]
        elif action == "ir_Derecha" and room < 2:
            self.agent_position[1] += 1
            self.energy_cost += self.action_costs["ir_Derecha"]
        elif action == "ir_Izquierda" and room > 0:
            self.agent_position[1] -= 1
            self.energy_cost += self.action_costs["ir_Izquierda"]
        elif action == "subir" and floor < 2 and room == 2:
            self.agent_position[0] += 1
            self.energy_cost += self.action_costs["subir"]
        elif action == "bajar" and floor > 2 and room == 0:
            self.agent_position[0] -= 1
            self.energy_cost += self.action_costs["bajar"]
        elif action == "nada":
            self.energy_cost += self.action_costs["nada"]
        else:
            print(f"Esta accion '{action}' no es valida en este estado")
    
    def is_clean(self):
        # Revisa que todos los cuartos esten limpios
        return all(room == "limpiar" for floor in self.rooms for room in floor)
    
    def print_environment(self):
        # Imprime el estado actual del entorno
        for i, floor in enumerate(self.rooms):
            print(f"Floor {i + 1}: {floor}")
        print(f"Posicion del agente: {self.agent_position}")
        print(f"Energia gastada: {self.energy_cost}")

class AgenteAleatorio:
    def __init__(self):
        pass

    def choose_action(self, percept):
        """Escoge una accion basada en la percepcion actual"""
        if percept == "sucio":
            return "limpiar"
        else:
            return random.choice(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "nada"])
        
class AgenteBasadoEnModelo:
    def __init__(self):
        self.internal_state = [[None for _ in range(3)] for _ in range(3)] # Representacion interna del entorno
        self.visited_rooms = set() # Mantiene una bitacora de los cuartos visitados

    def update_state(self, position, percept):
        """Actualiza el estado interno basado en la percepcion"""
        floor, room = position
        self.internal_state[floor][room] = percept
        self.visited_rooms.add(tuple(position))

    def choose_action(self, position):
        """Escoge la siguiente accion basado en el estado interno"""
        floor, room = position

        # Prioriza la limpieza de cuartos sucios
        if self.internal_state[floor][room] == "sucio":
            return "limpiar"
        
        # Revisa que cuarto esta mas cerca o que se encuentre sucio
        for f in range(3):
            for r in range(3):
                if self.internal_state[f][r] != "limpiar":
                    if f > floor and room == 2:
                        return "subir"
                    elif f < floor and room == 0:
                        return "bajar"
                    elif r > room:
                        return "ir_Derecha"
                    elif r < room:
                        return "ir_Izquierda"
        
        # Accion por defecto cuando todos los cuartos estan limpios
        return "nada"
    
def simulate(agent, environment, steps=200):
    """Simula al agente en el entorno dado un numero de pasos"""
    for _ in range(steps):
        percept = environment.rooms[environment.agent_position[0]][environment.agent_position[1]]
        if isinstance(agent, AgenteBasadoEnModelo):
            agent.update_state(environment.agent_position, percept)
        action = agent.choose_action(percept if isinstance(agent, AgenteAleatorio) else environment.agent_position)
        environment.perform_actions(action)

        return environment.energy_cost
    
# Se inicializa el entorno con los agentes
environment = NueveCuartos()

# Simulamos el agente aleatorio
simple_agent = AgenteAleatorio()
simple_env = NueveCuartos()
simple_cost = simulate(simple_agent, simple_env)

# Simulamos el agente basado en modelo
model_agent = AgenteBasadoEnModelo()
model_env = NueveCuartos()
model_cost = simulate(model_agent, model_env)

# Imprimimos con los resultados
print("Despues de 200 pasos:")
print("Agente aleatorio:")
simple_env.print_environment()
print("\nAgente basado en modelo:")
model_env.print_environment()

print(f"\nComparacion de costo de energia:\n Agente aleatorio: {simple_cost}\n Agente basado en modelo: {model_cost}")


