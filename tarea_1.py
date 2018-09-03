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
from random import choice


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

    def acción_legal(self, acción ):
        percepción = self.percepción()
        lugar, condicion = percepción[0], percepción[1]
        if lugar is "A":
            return acción in ("ir_der", "subir", "nada", "limpiar")
        elif lugar is "B":
            return acción in ("ir_izq", "ir_der","nada", "limpiar")
        elif lugar is "C":
            return acción in ("ir_izq", "subir","nada", "limpiar")
        elif lugar is "D":
            return acción in ("ir_izq","nada", "limpiar")
        elif lugar is "E":
            return acción in ("bajar", "ir_izq", "ir_der","nada", "limpiar")
        elif lugar is "F":
            return acción in ("ir_der", "nada", "limpiar")

    def calcular_desempeño(self, acción, cond):
        #Tentativo cambio a takewhile() si los tiempos siguen bien
        #si alguien leyo esto le pido una disculpa, la construccion no terminó
        alguno_cochino = False
        for a in self.x[1:]:
            if a is "sucio":
                alguno_cochino = True
                break
        #takewhile(lambda x: x is "sucio", self.x[1:])

        if acción is "nada" and alguno_cochino:
            self.desempeño-=2
        elif acción is "ir_izq" or acción is "ir_der":
            self.desempeño-=2
        elif acción is "subir" or acción is "bajar":
            self.desempeño-=3
        elif acción is "nada":
            # Como chingados no voy a poder poner decimales en mis costos??
            self.desempeño-=1.5
        else:
            self.desempeño-=1

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot = self.x[0]
        cond = self.x[1:]

        self.calcular_desempeño(acción, cond)


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
        elif acción is "bajar":
            robot = "B"
        self.x[0] = robot

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
        robot,situación = percepción[0], percepción[1]
        if situación is "sucio":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
            return "limpiar"
        elif robot is "A" and (self.x[2] is "sucio" or self.x[3] is "sucio" or self.x[4] is "sucio"):
            self.x[0] = "B"
            return "ir_der"
        elif robot is "A" and (self.x[6] is "sucio" or self.x[5] is "sucio"):
            self.x[0] = "F"
            return "subir"
        elif robot is "B" and (self.x[3] is "sucio" or self.x[4] is "sucio"):
            self.x[0] = "C"
            return "ir_der"
        elif robot is "B":
            self.x[0] = "A"
            return "ir_izq"
        elif robot is "C" and (self.x[2] is "sucio" or self.x[1] is "sucio" ):
            self.x[0] = "B"
            return "ir_izq"
        elif robot is "C" and (self.x[4] is "sucio" or self.x[5] is "sucio"):
            self.x[0] = "D"
            return "subir"
        elif robot is "D":
            self.x[0] = "E"
            return "ir_izq"
        elif robot is "E" and (self.x[4] is "sucio"):
            self.x[0] = "D"
            return "ir_der"
        elif robot is "E" and (self.x[6] is "sucio"):
            self.x[0] = "F"
            return "ir_izq"
        elif robot is "E":
            self.x[0] = "B"
            return "bajar"
        elif robot is "F":
            self.x[0] = "E"
            return "ir_der"
        else:
            return "nada"
            """
            Cual es el modelo de este agente ?

            Bueno, yo podria llamarle "A fijo", pues las condicionales que
            he usado hacen que dentro del primer piso, si los alrededores del
            lugar en el que esta parecen limpios, lo regresen al cuarto A
            y si estan en el segundo piso, lo lleven a D mas facilmente, y
            estando en D y los cuartos de arriba limpios, bajar a B y
            al estar en B regresarte a A, y si todos estan limpios, se detiene
            """

class AgenteAleatorioSeisCuartos():
    def programa(self, percepcion):
        robot, situación = percepcion[0], percepcion[1]
        if robot is "A":
            return choice(["nada","limpiar", "subir", "ir_der"])
        elif robot is "B":
            return choice(["nada","limpiar",  "ir_der", "ir_izq"])
        elif robot is "E":
            return choice(["nada","limpiar",  "ir_der", "ir_izq", "bajar"])
        elif robot is "C":
            return choice(["nada","limpiar", "subir", "ir_izq"])
        elif robot is "D":
            return choice(["nada","limpiar", "ir_izq"])
        elif robot is "F":
            return choice(["nada","limpiar", "ir_der"])


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


        # Es posible que el estado inicial ya haya estado limpio y aun asi
        #limpie, por eso configuro al agente para el peor de los casos
        #Esto deberia ameritar mas costo inicial, considerando el peor de los
        #casos
        situacion = self.modelo[" AB".find(robot)]
        if all(cuarto is 'limpio' for cuarto in self.modelo[1:]):
            accion = 'nada'
        elif situacion is 'sucio':
            accion = 'limpiar'
        elif robot is "A":
            accion = 'ir_B'
        else:
            accion = 'ir_A'

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
            num_al = choice(range(1,11))
            if num_al > 2:
                self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            num_al = choice(range(1,11))
            if num_al > 1:
                self.x[0] = "A"
        elif acción is "ir_B":
            num_al = choice(range(1,11))
            if num_al > 1:
                self.x[0] = "B"
class AgenteDosCuartosEstocastico(doscuartos_o.AgenteReactivoModeloDosCuartos):
    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')



def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno SeisCuartos con un Agente Reactivo Basado en modelo")
    entornos_o.simulador(SeisCuartos(),
                         AgenteReactivoModeloSeisCuartos(), 100)

    print("Prueba del entorno SeisCuartos con un Agente Aleatorio: ")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorioSeisCuartos(), 100)

    print("Prueba del entorno DosCuartosCiego con un Agente Racional")
    entornos_o.simulador(DosCuartosCiego(), AgenteDosCuartosCiego(), 100)

    print("Prueba del entorno DosCuartosEstocástico con Agente Racional")
    entornos_o.simulador(DosCuartosEstocástico(),
                        AgenteDosCuartosEstocastico(), 100)
    print("Prueba del entorno DosCuartos con Agente Aleatorio")
    entornos_o.simulador(doscuartos_o.DosCuartos(),
                        doscuartos_o.AgenteAleatorio(["ir_A",
                        "ir_B", "limpiar", "nada"]), 100)


if __name__ == "__main__":
    test()

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
