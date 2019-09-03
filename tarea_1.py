#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_f.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Mario Cesar Enriquez Rodriguez'

from entornos_f import Entorno, Agente, simulador, imprime_simulación
from doscuartos_f import DosCuartos
from random import choice, random
import math
class SeisCuartos(DosCuartos):
    """
    Clase para un entorno de 6 cuartos (3 en cada piso, 2 pisos).
    Muy sencilla solo regrupa métodos.

    El estado se define como (robot, a1, b1, c1, a2, b2, c2)
    donde robot puede tener los valores  "A_1", "B_1", "C_1", "A_2", "B_2" y "C_2"
    A_1", "B_1", "C_1", "A_2", "B_2" y "C_2" pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son
        (""ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").

    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """

    def acción_legal(self, acción):
        return acción in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def transición(self, estado, acción):
        robot, a1, b1, c1, a2, b2, c2,  = estado

        c_local = 0 if a1 == b1 == c1 == a2 == b2 == c2 == "limpio" and acción is "nada" else 1

        return ((estado, c_local) if a1 is "nada" else
                (("A_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "B_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "B_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "A_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "C_1" else

                (("A_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "B_2" else
                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "B_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "A_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "C_2" else

                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "subir" and robot == "C_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "bajar" and robot == "C_2" else
                ((robot, "limpio", b1, c1, a2, b2, c2), c_local) if robot is "A_1" else
                ((robot, a1, "limpio", c1, a2, b2, c2), c_local) if robot is "B_1" else
                ((robot, a1, b1, "limpio", a2, b2, c2), c_local) if robot is "C_1" else
                ((robot, a1, b1, c1, "limpio", b2, c2), c_local) if robot is "A_2" else
                ((robot, a1, b1, c1, a2, "limpio", c2), c_local) if robot is "B_2" else
                ((robot, a1, b1, c1, a2, b2, "limpio"), c_local))


    def percepción(self, estado):
        return estado[0], estado[math.ceil(" A_1B_1C_1A_2B_2C_2".find(estado[0])/3)]

class SeisCuartosCiego(SeisCuartos):
    """
    Clase para un entorno ciego de 6 cuartos (3 en cada piso, 2 pisos).
    Muy sencilla solo regrupa métodos.

    El estado se define como (robot, a1, b1, c1, a2, b2, c2)
    donde robot puede tener los valores  "A_1", "B_1", "C_1", "A_2", "B_2" y "C_2"
    A_1", "B_1", "C_1", "A_2", "B_2" y "C_2" pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son
        (""ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").

    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio o sucio)  (No importa el vvalor del estado en este entorno
    con la ubicación del robot y el estado de limpieza

    """

    def transición(self, estado, acción):
        robot, a1, b1, c1, a2, b2, c2,  = estado

        c_local = 0

        return ((estado, c_local) if a1 is "nada" else
                (("A_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "B_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "B_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "A_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "C_1" else

                (("A_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "B_2" else
                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "B_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Derecha" and robot == "A_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "ir_Izquierda" and robot == "C_2" else

                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is "subir" and robot == "C_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is "bajar" and robot == "C_2" else
                ((robot, "limpio", b1, c1, a2, b2, c2), c_local) if robot is "A_1" else
                ((robot, a1, "limpio", c1, a2, b2, c2), c_local) if robot is "B_1" else
                ((robot, a1, b1, "limpio", a2, b2, c2), c_local) if robot is "C_1" else
                ((robot, a1, b1, c1, "limpio", b2, c2), c_local) if robot is "A_2" else
                ((robot, a1, b1, c1, a2, "limpio", c2), c_local) if robot is "B_2" else
                ((robot, a1, b1, c1, a2, b2, "limpio"), c_local))

        def percepción(self, estado):
            return estado[0], "sucio"

class SeisCuartosEstocastico(SeisCuartos):
    """
    Clase para un entorno estocastico de 6 cuartos (3 en cada piso, 2 pisos).
    Muy sencilla solo regrupa métodos.

    El estado se define como (robot, a1, b1, c1, a2, b2, c2)
    donde robot puede tener los valores  "A_1", "B_1", "C_1", "A_2", "B_2" y "C_2"
    A_1", "B_1", "C_1", "A_2", "B_2" y "C_2" pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son
        (""ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
        El agente toma el movimiento de cuarto correcto solo el 80% de las veces

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
        El agente limpia correctamente solo el 90% de las veces

    """

    def transición(self, estado, acción):
        robot, a1, b1, c1, a2, b2, c2,  = estado

        c_local = 0 if a1 == b1 == c1 == a2 == b2 == c2 == "limpio" and acción is "nada" else 1

        return ((estado, c_local) if a1 is "nada" else
                (("A_1", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Izquierda" if random() <= 0.9 else "ir_Derecha") and robot == "B_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Derecha" if random() <= 0.9 else "ir_Izquierda") and robot == "B_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Derecha" if random() <= 0.9 else "ir_Izquierda") and robot == "A_1" else
                (("B_1", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Izquierda" if random() <= 0.9 else "ir_Derecha") and robot == "C_1" else

                (("A_2", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Izquierda" if random() <= 0.9 else "ir_Derecha") and robot == "B_2" else
                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Derecha" if random() <= 0.9 else "ir_Izquierda") and robot == "B_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Derecha" if random() <= 0.9 else "ir_Izquierda") and robot == "A_2" else
                (("B_2", a1, b1, c1, a2, b2, c2), c_local) if acción is ("ir_Izquierda" if random() <= 0.9 else "ir_Derecha") and robot == "C_2" else

                (("C_2", a1, b1, c1, a2, b2, c2), c_local) if acción is ("subir" if random() <= 0.9 else "ir_Izquierda") and robot == "C_1" else
                (("C_1", a1, b1, c1, a2, b2, c2), c_local) if acción is ("bajar" if random() <= 0.9 else "ir_Derecha") and robot == "C_2" else
                (estado, c_local) if a1 == b1 == c1 == a2 == b2 == c2 == "limpio" else # Aqui tenia error
                ((robot, "limpio" if random() <= 0.8 else "sucio", b1, c1, a2, b2, c2), c_local) if robot is "A_1" else
                ((robot, a1, "limpio" if random() <= 0.8 else "sucio", c1, a2, b2, c2), c_local) if robot is "B_1" else
                ((robot, a1, b1, "limpio" if random() <= 0.8 else "sucio", a2, b2, c2), c_local) if robot is "C_1" else
                ((robot, a1, b1, c1, "limpio" if random() <= 0.8 else "sucio", b2, c2), c_local) if robot is "A_2" else
                ((robot, a1, b1, c1, a2, "limpio" if random() <= 0.8 else "sucio", c2), c_local) if robot is "B_2" else
                ((robot, a1, b1, c1, a2, b2, "limpio" if random() <= 0.8 else "sucio"), c_local))

class AgenteAleatorio(Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, _):
        return choice(self.acciones)

class AgenteReactivoModeloSeisCuartos(Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A_1', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[math.ceil(" A_1B_1C_1A_2B_2C_2".find(robot) / 3)] = situación

        # Decide sobre el modelo interno
        a1, b1, c1, a2, b2, c2 = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        return ('nada' if a1 == a2 == b1 == b2 == c1 == c2 == 'limpio' else
                'limpiar' if situación == 'sucio' else
                "ir_Izquierda" if robot == "B_1" and a1 == 'sucio' else
                "ir_Derecha" if robot == "B_1" and a1 == 'limpio' else
                "ir_Derecha" if robot == "A_1" else
                "ir_Izquierda" if robot == "C_1" and (a1 == 'sucio' or b1 == 'sucio') else

                "ir_Izquierda" if robot == "B_2" and a2 == 'sucio' else
                "ir_Derecha" if robot == "B_2" and a2 == 'limpio' else
                "ir_Derecha" if robot == "A_2" else
                "ir_Izquierda" if robot == "C_2" and (a2 == 'sucio' or b2 == 'sucio') else

                "subir" if robot == "C_1" else
                "bajar")

def prueba_agente(agente):
    imprime_simulación(
        simulador(
            SeisCuartos(),
            agente,
            ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"],
            100
        ),
        ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    )

def prueba_agente_ciego(agente):
    imprime_simulación(
        simulador(
            SeisCuartosCiego(),
            agente,
            ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"],
            100
        ),
        ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    )


def prueba_agente_estocastico(agente):
    imprime_simulación(
        simulador(
            SeisCuartosEstocastico(),
            agente,
            ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"],
            100
        ),
        ["A_1", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    )

def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    prueba_agente(AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]))
    print("Prueba del entorno con un agente reactivo")
    prueba_agente(AgenteReactivoModeloSeisCuartos())

    print("Prueba del entorno ciego con un agente aleatorio")
    prueba_agente_ciego(AgenteReactivoModeloSeisCuartos())
    print("Prueba del entorno ciego  con un agente reactivo con modelo")
    prueba_agente_ciego(AgenteReactivoModeloSeisCuartos())

    print("Prueba del entorno estocastico con un agente aleatorio")
    prueba_agente_estocastico(AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]))
    print("Prueba del entorno estocastico con un agente reactivo con modelo")
    prueba_agente_estocastico(AgenteReactivoModeloSeisCuartos())


if __name__ == "__main__":
    test()

# Requiere el modulo entornos_f.py
# Usa el modulo doscuartos_f.py para reutilizar código
# Agrega los modulos que requieras de python
