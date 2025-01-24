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

    El estado se define como (robot, [["sucio", ...], ["sucio", ...]...])
    donde robot puede tener los valores (0,0), ..., (2, 2)
    y pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"].
    Solo algunas acciones son posibles en algunos estados, por ejemplo, no se puede subir si el robot está en (2,2).
    Solamente se sube por la derecha y se baja por la izquierda.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza.

    """
    
    def __init__(self, x0 = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]]):
        super().__init__(x0)
        
    def accion_legal(self, accion):
        print("Entrando a accion_legal")
        print("El estado es: ", self.x)
        print("La acción es: ", accion)
        
        piso, cuarto = self.x[0]
        if accion == "ir_Derecha":
            return cuarto != 2
        elif accion == "ir_Izquierda":
            return cuarto != 0
        elif accion == "bajar":
            return piso != 0 and cuarto == 0 # Solo bajar por la izquierda
        elif accion == "subir":
            return piso != 2 and cuarto == 2 # Solo subir por la derecha
        else:
            return accion in ["limpiar", "nada"]
    
    def transicion(self, accion):
        if not self.acción_legal(accion):
            print("accion ilegal")
            raise ValueError("La acción no es legal para este estado")  
        
        robot, cuartos = self.x[0], self.x[1]

        if accion == "nada" and "sucio" in cuartos:
            self.costo += 1
        elif accion == "limpiar":
            self.costo += 1
            cuartos[robot[0]][robot[1]] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            self.x[0] = (robot[0], robot[1] + 1)
        elif accion == "ir_Izquierda":
            self.costo += 2
            self.x[0] = (robot[0], robot[1] - 1)
        elif accion == "bajar":
            self.costo += 3
            self.x[0] = (robot[0] - 1, robot[1])
        else:  # accion == "subir"
            self.costo += 3
            self.x[0] = (robot[0] + 1, robot[1])
            
    def percepcion(self):
        robot = self.x[0]
        print("robot: ", robot)
        return robot, self.x[1][robot[0]][robot[1]]
    

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales.

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        accion = choice(self.acciones)
        while not NueveCuartos().acción_legal(accion):
            print("accion ilegal")
            accion = choice(self.acciones)
        return accion

def test():
    """
    Prueba de entorno y los agentes
    """
    
    x0 = [(0,0), [["sucio" for _ in range(3)] for _ in range(3)]] # Estado inicial
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    
    print("Prueba del entorno con un agente aleatorio")
    
    agente = AgenteAleatorio(acciones)
    entorno = NueveCuartos(x0)
    
    
    #for i in range(100):
    #    print("Estado: ", entorno.percepcion())
    #    accion = agente.programa(entorno.percepcion())
    #    print("Acción: ", accion)
    #    entorno.transicion(accion)
    #    print("Costo: ", entorno.costo)
    #    print()
    
    entornos_o.simulador(NueveCuartos(x0),
                         AgenteAleatorio(acciones),
                         100)
    
if __name__ == "__main__":
    test()
    
    