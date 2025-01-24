#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'georginasalcido'

import entornos_o
from random import choice

class NueveCuartos(entornos_o.Entorno):
    # Lista de listas para acomodar los cuartos y ponerlos todos sucios
    def __init__(self, x0=[0, 0, [["sucio"] * 3 for _ in range(3)]]):
        self.x = x0[:]
        self.costo = 0

    def accion_legal(self, accion):
        return accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")
    
    def transicion(self, accion):
        if not self.acción_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        piso, cuarto, estado = self.x

        # VER COMO HACER MÁS BONITO Y OPTIMIZADO
        if accion == "limpiar":
            self.costo += 1
            estado[piso][cuarto] = "limpio"
        elif accion == "ir_Derecha":
            self.costo += 2
            if cuarto < 2:
                self.x[1] += 1
        elif accion == "ir_Izquierda":
            self.costo += 2
            if cuarto > 0:
                self.x[1] += 1
        elif accion == "subir":
            self.costo += 3
            if cuarto == 2 and piso < 2:
                self.x[0] += 1
        elif accion == "bajar":
            self.costo += 3
            if cuarto == 0 and piso > 0:
                self.x[0] -= 1
        elif accion == "nada":
            if estado[piso][cuarto] == "sucio":
                self.costo += 1

    def percepcion(self):
        piso, cuarto, estado = self.x
        return piso, cuarto, estado[piso][cuarto]
    
class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

"""
class AgenteReactivoNuevecuartos(entornos_o.Agente):
    def programa(self, percepcion):
        piso, cuarto, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_Derecha' if cuarto < 2 else 
                'subir' if cuarto == 2 and piso < 2 else
                'ir_Izquierda' if cuarto > 0 else
                'bajar' if cuarto == 0 and piso > 0 else
                'nada' )
"""
    
class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    def __init__(self):
        self.modelo = [0, 0, [["sucio"] * 3 for _ in range(3)]]

    def programa(self, percepcion):
        piso, cuarto, situacion = percepcion

        self.modelo[0] = piso
        self.modelo[1] = cuarto
        self.modelo[2][piso][cuarto] = situacion

        return ('limpiar' if situacion == 'sucio' else
                'ir_Derecha' if cuarto < 2 and 'sucio' in self.modelo[2][piso][cuarto+1:] else
                'subir' if cuarto == 2 and piso < 2 and 'sucio' in self.modelo[2][piso+1] else
                'ir_Izquierda' if cuarto > 0 and 'sucio' in self.modelo[2][piso][:cuarto] else
                'bajar' if cuarto == 0 and piso > 0 and 'sucio' in self.modelo[2][:piso] else
                'nada')
 
class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
        return self.x[0], self.x[1]
    
class AgenteRacionalNueveCuartosCiego(entornos_o.Agente):
    def __init__(self):
        self.modelo = [0, 0, [["sucio"] * 3 for _ in range(3)]]

    def programa(self, percepcion):
        piso, cuarto = percepcion

        self.modelo[0] = piso
        self.modelo[1] = cuarto
        self.modelo[2][piso][cuarto] = "limpio"

        return ('limpiar' if situacion == 'sucio' else
                'ir_Derecha' if cuarto < 2 and 'sucio' in self.modelo[2][piso][cuarto+1:] else
                'subir' if cuarto == 2 and piso < 2 and 'sucio' in self.modelo[2][piso+1] else
                'ir_Izquierda' if cuarto > 0 and 'sucio' in self.modelo[2][piso][:cuarto] else
                'bajar' if cuarto == 0 and piso > 0 and 'sucio' in self.modelo[2][:piso] else
                'nada')