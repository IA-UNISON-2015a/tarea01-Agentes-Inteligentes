#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
"""
__author__ = 'Jesus Flores Lacarra'

import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de nueve cuartos.

    El estado se define como (robot, 1A, 1B, 1C, 2A, 2B, 2C, 3A, 3B, 3C)
    donde robot puede tener los valores "1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"
    y pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Solo algunas acciones son posibles en algunos estados, por ejemplo, no se puede subir si el robot está en 3A.
    Solamente se sube por la derecha y se baja por la izquierda.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza.

    """
    
    def __init__(self, x0=["1A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        super().__init__(x0)
        
    def accion_legal(self, accion):
        if accion == "ir_Derecha":
            return self.x[0][1] != "C"
        elif accion == "ir_Izquierda":
            return self.x[0][1] != "A"
        elif accion == "bajar":
            return self.x[0][0] != "1"
        elif accion == "subir":
            return self.x[0][0] != "3"
        return accion in ["limpiar", "nada"]
    
    def transicion(self, accion):
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, cuartos = self.x[0], self.x[1:]
        
        if accion == "nada" and "sucio" in cuartos:
            self.costo += 1
        elif accion == "limpiar":
            self.costo += 1
            self.x[1 - (int(self.x[0][0]))*3 + "ABC".find(self.x[0][1])] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            self.x[0] = self.x[0][0] + "ABC"["ABC".find(self.x[0][1]) + 1]
        elif accion == "ir_Izquierda":
            self.costo += 2
            self.x[0] = self.x[0][0] + "ABC"["ABC".find(self.x[0][1]) - 1]
        elif accion == "bajar":
            self.costo += 3
            self.x[0] = str(int(self.x[0][0]) - 1) + self.x[0][1]
        else:
            self.costo += 3
            self.x[0] = str(int(self.x[0][0]) + 1) + self.x[0][1]
            
    def percepcion(self):
        return self.x[0], self.x[1 - (int(self.x[0][0]))*3 + "ABC".find(self.x[0][1])]

def test():
    """
    Prueba de entorno y los agentes
    """
    
    x0 = ["1A", "sucio", "sucio", "", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"] # Estado inicial
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)
    
    