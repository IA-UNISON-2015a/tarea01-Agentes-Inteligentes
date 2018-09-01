#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
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
__author__ = 'Victor Noriega'

import entornos_o
import doscuartos_o

class SeisCuartos(doscuartos_o.DosCuartos):
    def __init__(self, x0=["A","sucio","sucio",
                            "sucio","sucio", "sucio", "sucio"]):
        """
        El robot empieza en A y todos los cuartos estan sucios.

        """
        self.x = x0[:]
        self.desempeño = 0

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


    def acción_legal(self, percepción):
        lugar, condicion = percepción
        if lugar is "A":
            return acción in ("ir_der", "subir", "nada")
        elif lugar is "B":
            return acción in ("ir_izq", "ir_der","nada")
        elif lugar is "C":
            return acción in ("ir_der", "subir","nada")
        elif lugar is "D":
            return acción in ("ir_izq","nada")
        elif lugar is "E":
            return acción in ("bajar", "ir_izq", "ir_der","nada")
        elif lugar is "F":
            return acción in ("ir_der", "nada")

    def calcular_desempeño(self, acción, cond):
        if acción is "nada" and self.x[0:].find("sucio") is not -1:
            self.desempeño-=2
        if accion is "ir_izq" or acción is "ir_der":
            self.desempeño-=2
        if acción is "subir" or acción is "bajar":
            self.desempeño-=3
        if acción is "nada":
            # Como chingados no voy a poder poner decimales en mis costos??
            self.desempeño-=1.5
        else:
            self.desempeño-=1

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot = self.x[0]
        cond = sel.x[0:]

        self.calcular_desempeño(acción, robot, cond)


        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_izq":
            if robot is "B":
                robot="A"
            elif robot is "C":
                robot="B"
            elif robot is "D":
                robot="E"
            else:
                robot="F"
        elif acción is "ir_der":
            if robot is "B":
                robot="C"
            elif robot is "A":
                robot="B"
            elif robot is "F":
                robot="E"
            else:
                robot="D"
        elif acción is "subir":
            if robot is "A":
                robot = "F"
            else:
                robot = "D"
        else:
            robot = "E"

### Inciso 2: El agente reactivo basado en modelo

class AgenteReactivoModeloSeisCuartos():

    def __init__(self):
        self.x = ["A","sucio","sucio",
                                "sucio","sucio", "sucio", "sucio"]

    """
    La casa se deberia ver asi:


    F  E  D
    A  B  C

    Las casas ABC estan en el primer piso.
    x[1] es A, x[3] es C, x[4] es D y x[6] es F
    """
    def programa(self, percepción):
        robot, situación = percepción

        if situación is "sucio":
            return "limpiar"
        elif robot is "A" and self.x[6] is "sucio" and self.x[2] is "limpio" and self.x[3] is "limpio":
            return "subir"
        elif robot is "C" and self.x[4] is "sucio" and self.x[2] is "limpio" and self.x[1] is "limpio":
            return "subir"
        elif robot is "E" and self.x[6] is "limpio" and self.x[4] is "limpio" and self.x[2] is "sucio":
            return "bajar"
        elif robot is "B" and self.x[3] is "limpio" and self.x[4] is "sucio" :
            return "ir_der"
        elif robot is "B" and self.x[1] is "limpio" and self.x[6] is "sucio" :
            return "ir_izq"
        elif robot is "C" and self.x[2] is "limpio" and self.x[1] is "sucio":
            return "ir_izq"
        elif robot is "E" and self.x[6] is "sucio":
            return "ir_izq"
        elif robot is "E" and self.x[4] is "sucio":
            return "ir_der"
        elif robot is "E" and (self.x[1] is "sucio" or self.x[3] is "sucio"):
            return "bajar"
        elif robot is "A" and self.x[2] is "sucio":
            return "ir_der"
        elif robot is "C" and self.x[2] is "sucio":
            return "ir_izq"
        elif robot is "D" and self.x[5] is "sucio":
            return "ir_izq"
        elif robot is "F" and self.x[5] is "sucio":
            return "ir_der"
        else:
            return "nada"

class AgenteAleatorioSeisCuartos():
    def programa(self, percepcion):
        return choice(SeisCuartos.acción_legal(percepcion()))


class DosCuartosCiego(doscuartos_o.DosCuartos):
    def percepción(self):
        return self.x[0]

class AgenteDosCuartosCiego(doscuartos_o.AgenteReactivoModeloDosCuartos):
    def programa(self, percepción):
        robot = percepción
        # El robot no puede percibir la situacion del cuarto, pero si puede
        # actualizar la situacion de los cuartos con sus acciones
        # por lo que debera recurrir a lo que guarda del entorno y no a sus
        #percepciones
        a, b = self.modelo[1], self.modelo[2]
        if all(cuarto is 'limpio' for cuarto in self.modelo[1:]):
            accion = 'nada'
        elif situacion is 'sucio':
            accion = 'limpiar'
        elif lugar is "A":
            accion = 'ir_der'
        else:
            accion = 'ir_izq'

        self.modelo[0] = robot
        if accion is "limpiar":
            self.modelo[" AB".find(robot)] = "limpio"
        return accion


class DosCuartosEstocástico(doscuartos_o.DosCuartos):
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        # Voy a seguir castigando a mi agente antes de que haga la accion,
        # ya que si tomo una accion pero no la completo, gasto la energia pero
        #no hizo lo que tenia que hacer.
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            num_al = choice(range(1,10))
            if num_al >8:
                self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            num_al = choice(range(1,10))
            if num_al > 9:
                self.x[0] = "A"
        elif acción is "ir_B":
            num_al = choice(range(1,10))
            if num_al >9:
                self.x[0] = "B"




# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
