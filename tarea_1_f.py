#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Revisa el archivo README.md con las instrucciones de la tarea.

"""
__author__ = 'georginasalcido'

import entornos_f
from doscuartos_f import AgenteAleatorio

# Requiere el modulo entornos_f.py o entornos_o.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python

class NueveCuartos(entornos_f.Entorno):

    def accion_legal(self, _, accion):
        return accion in ("ir_Izquierda", "ir_Derecha", "subir", "bajar", "limpiar", "nada")
    
    def transicion(self, estado, accion):
        robot, piso, cuartos = estado

        # El robot puede estar en uno de los 3 cuartos --> robot puede ser 0, 1 o 2
        # El robot puede estar en uno de los 3 pisos --> piso puede ser 0, 1 o 2
        # cuartos sería un arreglo con el estado de cada cuarto del piso --> cada cuarto puede ser "limpio" o "sucio"

        c_local = 0 if cuartos[piso][robot] == "limpio" and accion == "nada" else 1
        # CAMBIAR COSTOS
        return ((estado, c_local) if accion == "nada" else
                ((robot - 1, piso, cuartos), c_local) if accion == "ir_Izquierda" and robot > 0 else
                ((robot + 1, piso, cuartos), c_local) if accion == "ir_Derecha" and robot < 2 else
                ((robot, piso + 1, cuartos), c_local) if robot == "subir" and robot == 2 and piso < 3 else
                ((robot, piso - 1, cuartos), c_local) if robot == "bajar" and robot == 0 and piso > 0 else
                ((robot, piso, "limpio"), c_local) if robot == "limpiar" else # VER COMO ACCEDER AL CUARTO ESPECIFICO
                (estado, c_local) 
                )
    
    def percepcion(self, estado):
        robot, piso, cuartos = estado
        return cuartos, piso, cuartos[piso][robot]

class AgenteReactivo(entornos_f.Agente):
    def programa(self, percepcion):
        cuartos, piso, situacion = percepcion
        return ('limpiar' if situacion == 'sucio' else
                'ir_Izquierda' if robot < 0 else 
                'bajar' if robot == 0 else
                'ir_Derecha' if robot > 2 else
                'subir'
                )
    
class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    def __init__(self):
        self.modelo = [0, 0, [['sucio'] * 3 for _ in range(3)]]

    def programa(self, percepcion):
        # robot, situación = percepción
        cuartos, piso, situacion = percepcion

        self.modelo[0] = cuartos
        self.modelo[1] = piso
        self.modelo[2][piso][cuartos] = situacion

        cuarto, piso = self.modelo[0], self.modelo[1]
        return ('nada' if piso == 2 and cuarto == 2 and all(
                    estado == 'limpio' for piso in self.modelo[2] for estado in piso) else
                'limpiar' if situacion == 'sucio' else
                'ir_Derecha' if cuarto < 2 else
                'ir_Izquierda' if cuarto > 0 else
                'subir' if cuarto == 2 and piso < 2 else
                'bajar' if cuarto == 0 and piso > 0 else
                'nada' # VER COMO ARREGLAR ESTO
                )
    
def prueba_agente(agente):
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartos(),
            agente,
            [0, 0, [['sucio'] * 3 for _ in range(3)]],
            100
        ),
        [0, 0, [['sucio'] * 3 for _ in range(3)]])

def test():
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(['ir_Izquierda', 'ir_Derecha', 'subir', 'bajar', 'limpiar', 'nada']))

    print("Prueba del entorno con un agente reactivo")
    prueba_agente(AgenteReactivo())

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente(AgenteReactivoModeloNueveCuartos())
    

if __name__ == "__main__":
    test()