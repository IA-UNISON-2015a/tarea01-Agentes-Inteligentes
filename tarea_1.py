#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea sobre NueveCuartos, NueveCuartosCiego y NueveCuartosEstocástico.

"""
__author__ = 'Daniel Antonio Quihuis Hernandez'

import entornos_f
from random import choice, random

class NueveCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de nueve cuartos en tres pisos.
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.estado = [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def accion_legal(self, estado, accion):
        x, y, z, _ = estado
        if accion in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada"):
            return True
        elif accion == "subir":
            return z < 2 and x == 2
        elif accion == "bajar":
            return z > 0 and x == 0
        return False

    def transicion(self, estado, accion):
        x, y, z, estado_cuartos = estado
        costo = 1

        if accion == "ir_Derecha" and x < 2:
            x += 1
        elif accion == "ir_Izquierda" and x > 0:
            x -= 1
        elif accion == "subir" and self.accion_legal(estado, "subir"):
            z += 1
            costo = 2
        elif accion == "bajar" and self.accion_legal(estado, "bajar"):
            z -= 1
            costo = 2
        elif accion == "limpiar":
            estado_cuartos[z][y][x] = False
            costo = 0.5
        elif accion == "nada":
            costo = 0

        return ((x, y, z, estado_cuartos), costo)

    def percepcion(self, estado):
        x, y, z, estado_cuartos = estado
        return (x, y, z, estado_cuartos[z][y][x])

class NueveCuartosCiego(NueveCuartos):
    """
    Versión de NueveCuartos donde el agente solo conoce su posición.
    """
    def percepcion(self, estado):
        x, y, z, _ = estado
        return (x, y, z)

class NueveCuartosEstocastico(NueveCuartos):
    """
    Versión de NueveCuartos con acciones estocásticas.
    """
    def transicion(self, estado, accion):
        x, y, z, estado_cuartos = estado
        costo = 1

        if random() < 0.1:  # 10% de probabilidad de acción aleatoria
            accion = choice(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"])

        if accion == "ir_Derecha" and x < 2:
            x += 1
        elif accion == "ir_Izquierda" and x > 0:
            x -= 1
        elif accion == "subir" and self.accion_legal(estado, "subir"):
            z += 1
            costo = 2
        elif accion == "bajar" and self.accion_legal(estado, "bajar"):
            z -= 1
            costo = 2
        elif accion == "limpiar":
            if random() < 0.8:  # 80% de probabilidad de limpiar exitosamente
                estado_cuartos[z][y][x] = False
            costo = 0.5
        elif accion == "nada":
            costo = 0

        return ((x, y, z, estado_cuartos), costo)

class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que elige acciones al azar
    """
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    def programa(self, percepcion):
        return choice(self.acciones)

class AgenteReactivoModelo(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo para NueveCuartos
    """
    def __init__(self):
        self.modelo = [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]

    def programa(self, percepcion):
        x, y, z, sucio = percepcion
        self.modelo[z][y][x] = sucio

        if sucio:
            return "limpiar"

        # Buscar el cuarto sucio más cercano
        for dx, dy, dz, accion in [(1,0,0,"ir_Derecha"), (-1,0,0,"ir_Izquierda"), (0,0,1,"subir"), (0,0,-1,"bajar")]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < 3 and 0 <= ny < 3 and 0 <= nz < 3:
                if self.modelo[nz][ny][nx]:
                    if accion == "subir" and x != 2:
                        return "ir_Derecha"
                    elif accion == "bajar" and x != 0:
                        return "ir_Izquierda"
                    return accion

        return "nada"

class AgenteRacionalCiego(entornos_f.Agente):
    """
    Un agente racional para NueveCuartosCiego
    """
    def __init__(self):
        self.modelo = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.ultimo_movimiento = None

    def programa(self, percepcion):
        x, y, z = percepcion

        if self.modelo[z][y][x] is None:
            self.modelo[z][y][x] = False
            return "limpiar"

        # Buscar el cuarto no visitado más cercano
        for dx, dy, dz, accion in [(1,0,0,"ir_Derecha"), (-1,0,0,"ir_Izquierda"), (0,0,1,"subir"), (0,0,-1,"bajar")]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < 3 and 0 <= ny < 3 and 0 <= nz < 3:
                if self.modelo[nz][ny][nx] is None:
                    if accion == "subir" and x != 2:
                        return "ir_Derecha"
                    elif accion == "bajar" and x != 0:
                        return "ir_Izquierda"
                    self.ultimo_movimiento = accion
                    return accion

        # Si todos los cuartos han sido visitados, volver a limpiar
        self.modelo = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        return "limpiar"

class AgenteRacionalEstocastico(entornos_f.Agente):
    """
    Un agente racional para NueveCuartosEstocastico
    """
    def __init__(self):
        self.modelo = [[[1.0 for _ in range(3)] for _ in range(3)] for _ in range(3)]
        self.ultimo_movimiento = None

    def programa(self, percepcion):
        x, y, z, sucio = percepcion
        self.modelo[z][y][x] = 0.2 if not sucio else min(1.0, self.modelo[z][y][x] + 0.1)

        if sucio:
            return "limpiar"

        # Buscar el cuarto con mayor probabilidad de estar sucio
        max_prob = 0
        mejor_accion = "nada"
        for dx, dy, dz, accion in [(1,0,0,"ir_Derecha"), (-1,0,0,"ir_Izquierda"), (0,0,1,"subir"), (0,0,-1,"bajar")]:
            nx, ny, nz = x + dx, y + dy, z + dz
            if 0 <= nx < 3 and 0 <= ny < 3 and 0 <= nz < 3:
                if self.modelo[nz][ny][nx] > max_prob:
                    max_prob = self.modelo[nz][ny][nx]
                    mejor_accion = accion

        if mejor_accion == "subir" and x != 2:
            return "ir_Derecha"
        elif mejor_accion == "bajar" and x != 0:
            return "ir_Izquierda"

        self.ultimo_movimiento = mejor_accion
        return mejor_accion

def estado_a_str(estado):
    x, y, z, estado_cuartos = estado
    pisos = []
    for piso in estado_cuartos:
        piso_str = ''.join('limpio' if not cuarto else 'sucio' for cuarto in piso[0])
        pisos.append(piso_str)
    return f"({x}, {y}, {z}, {', '.join(pisos)})"

def imprime_simulacion(historial, s_0):
    print("\n\nSimulación, iniciando en el estado " + estado_a_str(s_0) + "\n")
    print('Paso'.center(10) + 'Acción'.center(40) + 'Siguiente estado'.center(50) + 'Costo'.center(15))
    print('_' * (10 + 40 + 50 + 15))

    for i, (a_i, s_i, c_i) in enumerate(historial):
        print(str(i).center(10) + str(a_i).center(40) + estado_a_str(s_i).center(50) + str(c_i).rjust(12))
    print('_' * (10 + 40 + 50 + 15) + '\n\n')

def prueba_agente(entorno, agente, pasos=100):
    estado = (0, 0, 0, [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)])
    costo_total = 0
    historial = []

    for _ in range(pasos):
        percepcion = entorno.percepcion(estado)
        accion = agente.programa(percepcion)
        estado, costo = entorno.transicion(estado, accion)
        costo_total += costo
        historial.append((accion, estado, costo_total))

    return historial

def test():
    """
    Prueba de los entornos y agentes
    """
    print("Prueba de NueveCuartos con un agente aleatorio")
    entorno = NueveCuartos()
    agente_aleatorio = AgenteAleatorio()
    historial_aleatorio = prueba_agente(entorno, agente_aleatorio)
    imprime_simulacion(historial_aleatorio, (0, 0, 0, [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]))

    print("\nPrueba de NueveCuartos con un agente reactivo con modelo")
    entorno = NueveCuartos()
    agente_reactivo_modelo = AgenteReactivoModelo()
    historial_reactivo_modelo = prueba_agente(entorno, agente_reactivo_modelo)
    imprime_simulacion(historial_reactivo_modelo, (0, 0, 0, [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]))

    print("\nPrueba de NueveCuartosCiego con un agente racional")
    entorno = NueveCuartosCiego()
    agente_racional_ciego = AgenteRacionalCiego()
    historial_racional_ciego = prueba_agente(entorno, agente_racional_ciego)
    imprime_simulacion(historial_racional_ciego, (0, 0, 0, [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]))

    print("\nPrueba de NueveCuartosEstocastico con un agente racional")
    entorno = NueveCuartosEstocastico()
    agente_racional_estocastico = AgenteRacionalEstocastico()
    historial_racional_estocastico = prueba_agente(entorno, agente_racional_estocastico)
    imprime_simulacion(historial_racional_estocastico, (0, 0, 0, [[[True for _ in range(3)] for _ in range(3)] for _ in range(3)]))

if __name__ == "__main__":
    test()