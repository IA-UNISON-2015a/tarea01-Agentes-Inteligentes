#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
nuevecuartos.py
----------------

Entorno con tres pisos y tres cuartos por piso.
Basado en entornos_o.py.

"""

import entornos_o
from random import choice


__author__ = 'Miguel Cruz Duarte'


class NueveCuartos(entornos_o.Entorno):
    def __init__(self, x0=None):
        """
        Inicializa el entorno con un estado inicial dado, o por defecto todos los cuartos sucios y el agente en 1A.
        """
        if x0 is None:
            x0 = {
                "robot": "1A", 
                "estado_cuartos": {
                    f"{piso}{cuarto}": "sucio"
                    for piso in range(1, 4)
                    for cuarto in "ABC"
                }
            }
        self.x = x0  # Ahora es un diccionario, no una lista
        self.costo = 0

    def accion_legal(self, accion):
        """
        Verifica si una acción es legal en el estado actual.
        """
        robot = self.x["robot"]
        piso, cuarto = int(robot[0]), robot[1]

        if accion == "ir_Derecha":
            return cuarto != "C"
        elif accion == "ir_Izquierda":
            return cuarto != "A"
        elif accion == "subir":
            return piso < 3 and cuarto == "C"
        elif accion == "bajar":
            return piso > 1 and cuarto == "A"
        elif accion in ["limpiar", "nada"]:
            return True
        return False

    def transicion(self, accion):
        """
        Cambia el estado del entorno según la acción.
        """
        if not self.accion_legal(accion):
            raise ValueError(f"La acción '{accion}' no es legal para este estado.")

        robot = self.x["robot"]
        piso, cuarto = int(robot[0]), robot[1]
        estado_cuartos = self.x["estado_cuartos"]

        if accion == "ir_Derecha":
            self.x["robot"] = f"{piso}{chr(ord(cuarto) + 1)}"
            self.costo += 2
        elif accion == "ir_Izquierda":
            self.x["robot"] = f"{piso}{chr(ord(cuarto) - 1)}"
            self.costo += 2
        elif accion == "subir":
            self.x["robot"] = f"{piso + 1}A"
            self.costo += 5
        elif accion == "bajar":
            self.x["robot"] = f"{piso - 1}C"
            self.costo += 5
        elif accion == "limpiar":
            estado_cuartos[robot] = "limpio"
            self.costo += 1
        elif accion == "nada":
            self.costo += 0

    def percepcion(self):
        """
        Devuelve la percepción del agente: posición y estado del cuarto actual.
        """
        robot = self.x["robot"]
        return robot, self.x["estado_cuartos"][robot]


class AgenteAleatorioNueveCuartos(entornos_o.Agente):
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    def programa(self, percepcion):
        entorno = percepcion[0]  # Aquí estamos obteniendo el objeto completo del entorno
        # Filtra las acciones legales según el entorno completo
        acciones_legales = [
            accion for accion in self.acciones if entorno.accion_legal(accion)
        ]
        return choice(acciones_legales) if acciones_legales else "nada"


class AgenteReactivoNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo simple para el entorno de nueve cuartos.
    """
    def programa(self, percepcion):
        print("Percepción:", percepcion)
        # Desempaquetar la percepción correctamente
        robot, situacion = percepcion  # Percepción solo contiene robot y estado de cuarto

        # Implementar la lógica de acción dependiendo del estado percibido
        if situacion == "sucio":
            return "limpiar"
        elif robot.endswith("C") and int(robot[0]) < 3:
            return "subir"
        elif robot.endswith("A") and int(robot[0]) > 1:
            return "bajar"
        elif robot.endswith("A"):
            return "ir_Derecha"
        elif robot.endswith("B"):
            return "ir_Derecha"
        elif robot.endswith("C"):
            return "ir_Izquierda"
        return "nada"


class AgenteReactivoModeloNueveCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo para el entorno de nueve cuartos.
    """
    def __init__(self):
        """
        Inicializa el modelo interno.
        """
        self.modelo = {"robot": "1A", 
                       "estado_cuartos": {f"{piso}{cuarto}": "sucio"
                                          for piso in range(1, 4)
                                          for cuarto in "ABC"}}

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo["robot"] = robot
        self.modelo["estado_cuartos"][robot] = situacion

        # Decide en base al modelo
        estado_cuartos = self.modelo["estado_cuartos"]
        if all(estado == "limpio" for estado in estado_cuartos.values()):
            return "nada"
        elif situacion == "sucio":
            return "limpiar"
        elif robot.endswith("C") and int(robot[0]) < 3:
            return "subir"
        elif robot.endswith("A") and int(robot[0]) > 1:
            return "bajar"
        elif robot.endswith("A"):
            return "ir_Derecha"
        elif robot.endswith("B"):
            return "ir_Derecha"
        elif robot.endswith("C"):
            return "ir_Izquierda"
        return "nada"


def test():
    """
    Prueba del entorno y los agentes.
    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(NueveCuartos(),
                         AgenteAleatorioNueveCuartos(),
                         100)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(NueveCuartos(), 
                         AgenteReactivoNueveCuartos(), 
                         100)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(NueveCuartos(), 
                         AgenteReactivoModeloNueveCuartos(), 
                         100)

if __name__ == "__main__":
    test()