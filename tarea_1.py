#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------
"""
__author__ = 'Lenika Elizabeth Montoya Valencia'

from entornos_f import Entorno

import random
from random import choice



class NueveCuartos(Entorno):
    def __init__(self):
        self.estado = {
            'aspiradora': (1,1),
            'cuartos': {(p , c): choice(['sucio', 'limpio']) for p in range (1,4) for c in range (1,4)},
    }

    def percepcion(self, s):
        piso, cuarto = self.estado ['aspiradora']
        return self.estado ['aspiradora'], self.estado ['cuartos'][(piso, cuarto)]

    def accion_legal(self, accion):
        piso, cuarto = self.estado['aspiradora']
        if accion == 'ir_Derecha':
            return cuarto < 3
        if accion == 'ir_Izquierda':
            return cuarto > 1
        if accion == 'subir':
            return piso < 3 and cuarto ==3
        if accion == 'bajar':
            return piso > 1 and cuarto ==1
        return accion in ["limpiar", "nada"]

    def movimiento(self, accion):
        piso, cuarto = self.estado['aspiradora']
        nuevo_estado = self.estado.copy()
        costo = 1

        if accion == "ir_Derecha" and cuarto == 3:
            nuevo_estado['aspiradora']= (piso, cuarto + 1)
        elif accion == "ir_Izquierda" and cuarto > 1:
            nuevo_estado['aspiradora']= (piso, cuarto - 1)
        elif accion == "subir" and piso < 3 and cuarto ==3:
            nuevo_estado['cuartos'] = (piso + 1, cuarto)
            costo = 2
        elif accion == "bajar" and piso > 1 and cuarto == 1:
            nuevo_estado['cuartos'] = (piso - 1, cuarto)
            costo = 2
        elif accion == "limpiar":
            nuevo_estado['cuartos'][(piso, cuarto)] = 'limpio'
            costo = 0.5
        return nuevo_estado, costo

class NueveCuartosCiego(NueveCuartos):
    def __init__(self):
        super().__init__()

    def percepcion(self):
        piso, cuarto = self.estado['aspiradora']
        return self.estado['aspiradora'], 'desconocido'

class NueveCuartosEstocastico(NueveCuartos):
    def __init__(self):
        super().__init__()

    def transicion(self, accion):
        piso, cuarto = self.estado['aspiradora']
        nuevo_estado = self.estado.copy()
        costo = 1
        if accion == "ir_Derecha" and cuarto < 3:
            if random.random() > 0.2:
                nuevo_estado['aspiradora'] = (piso, cuarto + 1)
            else:
                nuevo_estado['aspiradora'] = (piso, cuarto)
        elif accion == "ir_Izquierda" and cuarto > 1:
            if random.random() > 0.2:
                nuevo_estado['aspiradora'] = (piso, cuarto - 1)
            else:
                nuevo_estado['aspiradora'] = (piso, cuarto)
        elif accion == "limpiar":
            if random.random() > 0.2:
                nuevo_estado['cuartos'][(piso, cuarto)] = 'limpio'
            costo = 0.5
        return nuevo_estado, costo

class AgenteReactivoNueveCuartos:
    def __init__(self):
        pass

    def actuacion(self, percepcion, modelo):
        (piso, cuarto), estado_cuarto = percepcion
        modelo['aspiradora'] = (piso, cuarto)
        modelo['cuartos'][(piso, cuarto)] = estado_cuarto

        if estado_cuarto == 'sucio':
            return "limpiar"

        for p in range(1, 4):
            for c in range(1, 4):
                if modelo['cuartos'][(p, c)] == 'sucio':
                    if p == piso:
                        return "ir_Derecha" if c > cuarto else "ir_Izquierda"
                    return "subir" if p > piso else "bajar"

        return "nada"

class AgenteReactivoCiego:
    def __init__(self):
        pass

    def actuacion(self, percepcion, modelo):
        (piso, cuarto), _ = percepcion
        modelo['aspiradora'] = (piso, cuarto)

        return "limpiar" if piso != 3 else "ir_Izquierda"

class AgenteRacionalEstocastico:
    def __init__(self):
        pass

    def actuacion(self, percepcion, modelo):
        (piso, cuarto), estado_cuarto = percepcion
        modelo['aspiradora'] = (piso, cuarto)
        modelo['cuartos'][(piso, cuarto)] = estado_cuarto

        if estado_cuarto == 'sucio':
            return "limpiar"

        for p in range(1, 4):
            for c in range(1, 4):
                if modelo['cuartos'][(p, c)] == 'sucio':
                    if p == piso:
                        return "ir_Derecha" if c > cuarto else "ir_Izquierda"
                    return "subir" if p > piso else "bajar"

        return "nada"


def simulador(entorno, agente, pasos):
    estado = entorno.estado
    modelo = {'aspiradora': estado['aspiradora'], 'cuartos': estado['cuartos'].copy()}
    desempeno = 0

    for _ in range(pasos):
        percep = entorno.percepcion()
        accion = agente.actuacion(percep, modelo)
        if entorno.accion_legal(accion):
            estado, costo = entorno.movimiento(accion)
            desempeno -= costo

    return desempeno, estado

def prueba_agentes():
    entorno_nueve_cuartos = NueveCuartos()
    agente_reactivo = AgenteReactivoNueveCuartos()
    agente_random = AgenteReactivoCiego()
    agente_racional = AgenteRacionalEstocastico()

    desempeno_reactivo, _ = simulador(entorno_nueve_cuartos, agente_reactivo, 200)
    desempeno_random, _ = simulador(entorno_nueve_cuartos, agente_random, 200)
    desempeno_racional, _ = simulador(entorno_nueve_cuartos, agente_racional, 200)

    print(f"Desempeño Agente Reactivo: {desempeno_reactivo}")
    print(f"Desempeño Agente Aleatorio: {desempeno_random}")
    print(f"Desempeño Agente Racional: {desempeno_racional}")

if __name__ == "__main__":
    prueba_agentes()
