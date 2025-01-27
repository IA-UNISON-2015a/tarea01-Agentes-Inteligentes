#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'alantorres'

import entornos_f
import entornos_o
from random import choice, random
# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_o.Entorno):

    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0
        self.costo = 0


    cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]

    def accion_legal(self, action):
        if (action == "ir_Derecha" and (self.x[0] in [fila[2] for fila in self.cuartos])):
            return False
        elif (action == "ir_Izquierda" and (self.x[0] in [fila[0] for fila in self.cuartos])):
            return False
        elif (action == "bajar" and ((self.x[0] in self.cuartos[0]) or not (self.x[0] in [fila[0] for fila in self.cuartos] ))):
            return False
        elif (action == "subir" and ((self.x[0] in self.cuartos[2]) or not (self.x[0] in [fila[2] for fila in self.cuartos]))):
            return False
        else:
            return action in ("ir_Derecha", "ir_Izquierda", "bajar", "subir", "limpiar", "nada")

    def transicion(self, action):
        if not self.accion_legal(action):
            return


        robot, a, b, c, d, e, f, g, h, i = self.x

        def buscar_indice(matriz, elemento):
            for i, fila in enumerate(matriz):
                if elemento in fila:
                    return i, fila.index(elemento)
            return None  
    
        index = buscar_indice(self.cuartos, self.x[0])
        if (index == None):
            return
        if action != "nada" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio" or g == "sucio" or h == "sucio" or i == "sucio":
            self.costo += 1
        if action == "limpiar":
            self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
        elif action == "ir_Derecha":
            self.costo += 1
            self.x[0] = self.cuartos[index[0]][index[1] + 1]
        elif action == "ir_Izquierda":
            self.costo += 1
            self.x[0] = self.cuartos[index[0]][index[1] - 1]

        elif action == "bajar":
            self.costo += 2
            self.x[0] = self.cuartos[index[0] - 1][index[1]]
        elif action == "subir":
            self.costo += 2
            self.x[0] = self.cuartos[index[0] + 1][index[1]]
    
    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, actions, entorno):
        self.actions = actions
        self.entorno = entorno

    def programa(self, _): 
        acciones_legales = [action for action in self.actions if self.entorno.accion_legal(action)]
        if not acciones_legales:
            raise ValueError("No hay acciones legales disponibles.")
        return choice(acciones_legales)

class AgenteReactivoNueveCuartos(entornos_o.Agente):
    
    def __init__ (self, entorno):
        self.entorno = entorno

    def programa(self, percepcion):
         robot, situacion = percepcion
         if situacion == "sucio":
             return "limpiar"
         else:
             acciones_legales = []
             actions = ["bajar", "subir", "ir_Derecha", "ir_Izquierda"]
             for action in actions:
                 if(self.entorno.accion_legal(action)):
                     acciones_legales.append(action)
             if acciones_legales:
                return choice(acciones_legales)
             return "nada"
         

class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self, entorno):
       self.modelo = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"] 
       self.entorno = entorno
    
    def programa(self, percepcion):
        
        robot, situacion = percepcion
        self.modelo[0] = robot
        self.modelo[' ABCDEFGHI'.find(robot)] = situacion
        a, b, c, d, e, f, g, h, i = self.modelo[1:10] 
        if all(var == "limpio" for var in [a, b, c, d, e, f, g, h, i]):
           return "nada"
        elif (situacion == "sucio"):
           return "limpiar"
        else:
             
            def buscar_indice(matriz, elemento):
                for i, fila in enumerate(matriz):
                    if elemento in fila:
                        return i, fila.index(elemento)
                return None  
            index = buscar_indice(self.entorno.cuartos,robot)
            if(robot == 'A'):
                return "ir_Derecha"
            if(index[0] == 0):
                if(index[1] == 2):
                    return "subir"
                return "ir_Derecha"
            if(index[0] == 1):
                if(index[1] == 2 and all(var == "limpio" for var in [d,e,f])):
                    return "subir"
                if(all(var == "limpio" for var in [d,e,f])) :
                    return "ir_Derecha"
                return "ir_Izquierda"
            if(index[0] == 2):
                return "ir_Izquierda"

        
class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
         return self.x[0]


class AgenteReactivoModeloNueveCuartosCiego(entornos_o.Agente):
     def __init__(self, entorno):
         self.modelo = ["?", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
         self.entorno = entorno
         self.hashmap = {}
     def programa(self, percepcion):
         robot = percepcion
         if(len(self.hashmap) == 9):
             return "nada"
         if not (percepcion in self.hashmap):
             self.hashmap[percepcion] = percepcion
             return "limpiar"
             
         acciones_legales = []
         actions = ["bajar", "subir", "ir_Derecha", "ir_Izquierda"]
         for action in actions:
             if(self.entorno.accion_legal(action)):
                 acciones_legales.append(action)
         
         if acciones_legales:
            return choice(acciones_legales)


class NueveCuartosEstocastico(entornos_o.Entorno):

    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0
        self.costo = 0


    cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]

    def accion_legal(self, action):
        if (action == "ir_Derecha" and (self.x[0] in [fila[2] for fila in self.cuartos])):
            return False
        elif (action == "ir_Izquierda" and (self.x[0] in [fila[0] for fila in self.cuartos])):
            return False
        elif (action == "bajar" and ((self.x[0] in self.cuartos[0]) or not (self.x[0] in [fila[0] for fila in self.cuartos] ))):
            return False
        elif (action == "subir" and ((self.x[0] in self.cuartos[2]) or not (self.x[0] in [fila[2] for fila in self.cuartos]))):
            return False
        else:
            return action in ("ir_Derecha", "ir_Izquierda", "bajar", "subir", "limpiar", "nada")

    def transicion(self, action):
        if not self.accion_legal(action):
            return


        robot, a, b, c, d, e, f, g, h, i = self.x

        def buscar_indice(matriz, elemento):
            for i, fila in enumerate(matriz):
                if elemento in fila:
                    return i, fila.index(elemento)
            return None  
    
        index = buscar_indice(self.cuartos, self.x[0])
        if (index == None):
            return
        if action != "nada" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio" or g == "sucio" or h == "sucio" or i == "sucio":
            self.costo += 1
        if action == "limpiar":
            if (random() < 0.8):
                self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
            else:
                return 
        elif action == "ir_Derecha":
            if (random() < 0.8):
                self.costo += 1
                
                self.x[0] = self.cuartos[index[0]][index[1] + 1]
            elif (random() <0.9):
                return 
            elif (random() <1.0):
                acciones_legales = [action for action in ["ir_Derecha", "ir_Izquierda", "bajar", "subir", "limpiar", "nada"] if self.accion_legal(action)] 
                self.transicion(choice(acciones_legales))
        elif action == "ir_Izquierda":
            if (random() < 0.8):
                self.costo += 1    
                self.x[0] = self.cuartos[index[0]][index[1] - 1]
            elif (random() <0.9):
                return 
            elif (random() <1.0):
                acciones_legales = [action for action in ["ir_Derecha", "ir_Izquierda", "bajar", "subir", "limpiar", "nada"] if self.accion_legal(action)] 
                self.transicion(choice(acciones_legales))

        elif action == "bajar":
            if (random() < 0.8):
                self.costo += 2
                self.x[0] = self.cuartos[index[0] - 1][index[1]]
            elif (random() <0.9):
                return 
            elif (random() <1.0):
                acciones_legales = [action for action in ["ir_derecha", "ir_izquierda", "bajar", "subir", "limpiar", "nada"] if self.accion_legal(action)] 
                self.transicion(choice(acciones_legales))
        elif action == "subir":
            if (random() < 0.8):
                self.costo += 2
                self.x[0] = self.cuartos[index[0] + 1][index[1]]
            elif (random() <0.9):
                return 
            elif (random() <1.0):
                acciones_legales = [action for action in ["ir_derecha", "ir_izquierda", "bajar", "subir", "limpiar", "nada"] if self.accion_legal(action)] 
                self.transicion(choice(acciones_legales))
    
    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


    
def test():
    x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(x0), AgenteAleatorio(["bajar", "subir", "ir_Derecha", "ir_Izquierda", "limpiar", "nada"], NueveCuartos(x0)), 200)

    print("Prueba del entorno con un agente reactivo")
    x1 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartos(x1), AgenteReactivoNueveCuartos(NueveCuartos(x1)), 200)

    print("Prueba del entorno con un agente reactivo con modelo")
    x2 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartos(x2), AgenteReactivoModeloNueveCuartos(NueveCuartos(x2)), 200)

    print("Prueba del entorno ciego con un agente reactivo con modelo")
    x3 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartosCiego(x3), AgenteReactivoModeloNueveCuartosCiego(NueveCuartosCiego(x3)), 200)

    print("Prueba del entorno estocástico con un agente aleatorio")
    x4 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartosEstocastico(x4), AgenteAleatorio(["bajar", "subir", "ir_Derecha", "ir_Izquierda", "limpiar", "nada"], NueveCuartosEstocastico(x4)), 200)

    print("Prueba del entorno estocástico con un agente reactivo con modelo")
    x5 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartosEstocastico(x5), AgenteReactivoModeloNueveCuartos(NueveCuartosEstocastico(x5)), 200)
if __name__ == "__main__":
    test()
