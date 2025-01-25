#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
tarea_1.py
----------

"""

import entornos_f
from random import choice, random

__author__ = 'Daniel Antonio Quihuis Hernandez'

"""
Para este caso particular decidi basarme en la forma funcional, es decir basandome en los archivos
entornos_f.py y doscuartos_f.py

NOTA IMPORTANTE: AL MOMENTO DE EJECUTAR EL ARCHIVO tarea_1.py PUEDE QUE SE VERA RARO O PARECIERA QUE MAL
PERO PODER VER BIEN LA EJECUCION SE DEBE REDUCIR EL TAMAÑO DE LA LETRA PARA PODER VERLO COMO DEBE DE SER

NOTA: Nota tuve problemas con el estado al momento de transiciones por lo que puede haber errores en los estados


"""

class NueveCuartos(entornos_f.Entorno):
    """
    Clase para un entorno de nueve cuartos distribuidos en tres pisos.

    El estado se define como (robot, piso_1, piso_2, piso_3)
    donde robot puede tener los valores "1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"
    y piso_1, piso_2, piso_3 son listas con los estados de los cuartos en cada piso.

    Las acciones válidas en el entorno son:
        ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    """
    def __init__(self):
        self.acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    def accion_legal(self, estado, accion):
        robot, piso_1, piso_2, piso_3 = estado
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        if accion == "subir":
            return piso_actual < 3 and cuarto_actual == 'C'
        elif accion == "bajar":
            return piso_actual > 1 and cuarto_actual == 'A'
        else:
            return True

    def transicion(self, estado, accion):
        robot, piso_1, piso_2, piso_3 = estado
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        nuevo_robot = robot
        nuevo_piso_1 = piso_1.copy()
        nuevo_piso_2 = piso_2.copy()
        nuevo_piso_3 = piso_3.copy()

        costo = 1

        if accion == "ir_Derecha":
            if cuarto_actual == 'A':
                nuevo_robot = robot[0] + 'B'
            elif cuarto_actual == 'B':
                nuevo_robot = robot[0] + 'C'
        elif accion == "ir_Izquierda":
            if cuarto_actual == 'C':
                nuevo_robot = robot[0] + 'B'
            elif cuarto_actual == 'B':
                nuevo_robot = robot[0] + 'A'
        elif accion == "subir":
            if piso_actual < 3 and cuarto_actual == 'C':
                nuevo_robot = str(piso_actual + 1) + 'A'
                costo = 2
        elif accion == "bajar":
            if piso_actual > 1 and cuarto_actual == 'A':
                nuevo_robot = str(piso_actual - 1) + 'C'
                costo = 2
        elif accion == "limpiar":
            if piso_actual == 1:
                nuevo_piso_1[ord(cuarto_actual) - ord('A')] = 'limpio'
            elif piso_actual == 2:
                nuevo_piso_2[ord(cuarto_actual) - ord('A')] = 'limpio'
            elif piso_actual == 3:
                nuevo_piso_3[ord(cuarto_actual) - ord('A')] = 'limpio'
            costo = 0.5

        nuevo_estado = (nuevo_robot, nuevo_piso_1, nuevo_piso_2, nuevo_piso_3)
        return nuevo_estado, costo

    def percepcion(self, estado):
        robot, piso_1, piso_2, piso_3 = estado
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        if piso_actual == 1:
            situacion = piso_1[ord(cuarto_actual) - ord('A')]
        elif piso_actual == 2:
            situacion = piso_2[ord(cuarto_actual) - ord('A')]
        elif piso_actual == 3:
            situacion = piso_3[ord(cuarto_actual) - ord('A')]

        return robot, situacion


class AgenteAleatorio(entornos_f.Agente):
    """
    Un agente que solo regresa una acción al azar entre las acciones legales.

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        # Obtener el estado actual del entorno
        robot = percepcion[0]  # El primer elemento de la percepción es el robot
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        # Filtrar acciones legales basadas en el estado actual
        acciones_legales = []
        for accion in self.acciones:
            if accion == "subir":
                if piso_actual < 3 and cuarto_actual == 'C':
                    acciones_legales.append(accion)
            elif accion == "bajar":
                if piso_actual > 1 and cuarto_actual == 'A':
                    acciones_legales.append(accion)
            else:
                acciones_legales.append(accion)

        # Seleccionar una acción aleatoria entre las acciones legales
        return choice(acciones_legales)


class AgenteReactivoModeloNueveCuartos(entornos_f.Agente):
    """
    Un agente reactivo basado en modelo para el entorno de NueveCuartos.

    """
    def __init__(self):
        self.modelo = ['1A', ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio']]

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]
        if piso_actual == 1:
            self.modelo[1][ord(cuarto_actual) - ord('A')] = situacion
        elif piso_actual == 2:
            self.modelo[2][ord(cuarto_actual) - ord('A')] = situacion
        elif piso_actual == 3:
            self.modelo[3][ord(cuarto_actual) - ord('A')] = situacion

        # Decide sobre el modelo interno
        if situacion == 'sucio':
            return 'limpiar'
        else:
            if piso_actual == 1:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
            elif piso_actual == 2:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
            elif piso_actual == 3:
                if cuarto_actual == 'A':
                    # Verificar si la acción "bajar" es legal
                    if piso_actual > 1:
                        return 'bajar'
                    else:
                        return 'ir_Derecha'  # Si no puede bajar, moverse a la derecha
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    return 'ir_Izquierda'


class NueveCuartosCiego(NueveCuartos):
    """
    Variante de NueveCuartos donde el agente no puede percibir el estado de limpieza.

    """
    def percepcion(self, estado):
        robot, piso_1, piso_2, piso_3 = estado
        return robot


class AgenteRacionalNueveCuartosCiego(entornos_f.Agente):
    """
    Un agente racional para el entorno de NueveCuartosCiego.

    """
    def __init__(self):
        self.modelo = ['1A', ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio']]

    def programa(self, percepcion):
        robot = percepcion
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        # Decide sobre el modelo interno
        if piso_actual == 1:
            if self.modelo[1][ord(cuarto_actual) - ord('A')] == 'sucio':
                return 'limpiar'
            else:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
        elif piso_actual == 2:
            if self.modelo[2][ord(cuarto_actual) - ord('A')] == 'sucio':
                return 'limpiar'
            else:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
        elif piso_actual == 3:
            if self.modelo[3][ord(cuarto_actual) - ord('A')] == 'sucio':
                return 'limpiar'
            else:
                if cuarto_actual == 'A':
                    # Verificar si la acción "bajar" es legal
                    if piso_actual > 1:
                        return 'bajar'
                    else:
                        return 'ir_Derecha'  # Si no puede bajar, moverse a la derecha
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    return 'ir_Izquierda'


class NueveCuartosEstocástico(NueveCuartos):
    """
    Variante de NueveCuartos con acciones estocásticas.

    """
    def transicion(self, estado, accion):
        robot, piso_1, piso_2, piso_3 = estado
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        nuevo_robot = robot
        nuevo_piso_1 = piso_1.copy()
        nuevo_piso_2 = piso_2.copy()
        nuevo_piso_3 = piso_3.copy()

        costo = 1

        if accion == "limpiar":
            if random() < 0.8:
                if piso_actual == 1:
                    nuevo_piso_1[ord(cuarto_actual) - ord('A')] = 'limpio'
                elif piso_actual == 2:
                    nuevo_piso_2[ord(cuarto_actual) - ord('A')] = 'limpio'
                elif piso_actual == 3:
                    nuevo_piso_3[ord(cuarto_actual) - ord('A')] = 'limpio'
            costo = 0.5
        elif accion in ["ir_Derecha", "ir_Izquierda", "subir", "bajar"]:
            if random() < 0.8:
                if accion == "ir_Derecha":
                    if cuarto_actual == 'A':
                        nuevo_robot = robot[0] + 'B'
                    elif cuarto_actual == 'B':
                        nuevo_robot = robot[0] + 'C'
                elif accion == "ir_Izquierda":
                    if cuarto_actual == 'C':
                        nuevo_robot = robot[0] + 'B'
                    elif cuarto_actual == 'B':
                        nuevo_robot = robot[0] + 'A'
                elif accion == "subir":
                    if piso_actual < 3 and cuarto_actual == 'C':
                        nuevo_robot = str(piso_actual + 1) + 'A'
                        costo = 2
                elif accion == "bajar":
                    if piso_actual > 1 and cuarto_actual == 'A':
                        nuevo_robot = str(piso_actual - 1) + 'C'
                        costo = 2
            elif random() < 0.1:
                # Se queda en su lugar
                pass
            else:
                # Realiza una acción legal aleatoria
                acciones_legales = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
                accion = choice(acciones_legales)
                return self.transicion(estado, accion)

        nuevo_estado = (nuevo_robot, nuevo_piso_1, nuevo_piso_2, nuevo_piso_3)
        return nuevo_estado, costo


class AgenteRacionalNueveCuartosEstocástico(entornos_f.Agente):
    """
    Un agente racional para el entorno de NueveCuartosEstocástico.

    """
    def __init__(self):
        self.modelo = ['1A', ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio']]

    def programa(self, percepcion):
        robot, situacion = percepcion
        piso_actual = int(robot[0])
        cuarto_actual = robot[1]

        # Actualiza el modelo interno
        if piso_actual == 1:
            self.modelo[1][ord(cuarto_actual) - ord('A')] = situacion
        elif piso_actual == 2:
            self.modelo[2][ord(cuarto_actual) - ord('A')] = situacion
        elif piso_actual == 3:
            self.modelo[3][ord(cuarto_actual) - ord('A')] = situacion

        # Decide sobre el modelo interno
        if situacion == 'sucio':
            return 'limpiar'
        else:
            if piso_actual == 1:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
            elif piso_actual == 2:
                if cuarto_actual == 'A':
                    return 'ir_Derecha'
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    # Verificar si la acción "subir" es legal
                    if piso_actual < 3:
                        return 'subir'
                    else:
                        return 'ir_Izquierda'  # Si no puede subir, moverse a la izquierda
            elif piso_actual == 3:
                if cuarto_actual == 'A':
                    # Verificar si la acción "bajar" es legal
                    if piso_actual > 1:
                        return 'bajar'
                    else:
                        return 'ir_Derecha'  # Si no puede bajar, moverse a la derecha
                elif cuarto_actual == 'B':
                    return 'ir_Derecha'
                elif cuarto_actual == 'C':
                    return 'ir_Izquierda'


def prueba_agente(entorno, agente, estado_inicial, pasos=200):
    historial = entornos_f.simulador(
        entorno(),
        agente,
        estado_inicial,
        pasos
    )
    entornos_f.imprime_simulacion(historial, estado_inicial)


def test():
    """
    Prueba del entorno y los agentes

    """
    estado_inicial = ('1A', ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio'], ['sucio', 'sucio', 'sucio'])

    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(NueveCuartos, AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']),
                  estado_inicial)

    print("Prueba del entorno con un agente reactivo basado en modelo")
    prueba_agente(NueveCuartos, AgenteReactivoModeloNueveCuartos(),
                  estado_inicial)

    print("Prueba del entorno NueveCuartosCiego con un agente racional")
    prueba_agente(NueveCuartosCiego, AgenteRacionalNueveCuartosCiego(),
                  estado_inicial)

    print("Prueba del entorno NueveCuartosEstocástico con un agente racional")
    prueba_agente(NueveCuartosEstocástico, AgenteRacionalNueveCuartosEstocástico(),
                  estado_inicial)


if __name__ == "__main__":
    test()