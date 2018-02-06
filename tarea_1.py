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

   Las acciónes totales serán

   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ```

   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos,
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciónes de subir y bajar son mas costosas en término de
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
__author__ = 'Adrian Emilio Vazquez Icedo'

import entornos_o
import doscuartos_o
import random

#########################################################################################
"""
    #inciso 1
    Desarrollo entorno 6 cuartos
"""
class SeisCuartos(entornos_o.Entorno):
    """
    Clase entorno 6 SeisCuartos
    """
    def __init__(self, x0=["A", "sucio", "sucio","sucio", "sucio", "sucio", "sucio"]):
        """
        Por default esta en A(abajo izquierda) y los 6 cuartos estan sucios
        """
        self.x = x0[:]
        self.desempeño = 0

    """
    Se definen las acciones permitidas dependiendo la posicion en la que se
    encuentra el robot.
    """
    def acción_legal(self, acción):
        if acción == "nada" or "limpiar":
            return True
        if self.x[0] == "A" and acción in ("ir_Derecha", "subir"):
           return True
        if self.x[0] == "B" and acción in ("ir_Derecha", "ir_Izquierda"):
           return True
        if self.x[0] == "C" and acción in ("ir_Izquierda", "subir"):
           return True
        if self.x[0] == "D" and acción == "ir_Derecha":
           return True
        if self.x[0] == "E" and acción in ("ir_Derecha", "ir_Izquierda", "bajar"):
           return True
        if self.x[0] == "F" and acción == "ir_Izquierda":
          return True

    """
    Se revisa si el movimiento es legal y en caso de no serlo se envia un mensaje.
    """
    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("Esta acción no es legal en el estado actual.")

        robot, a,b,c,d,e,f = self.x
        """
        Se revisa si todavia no se termina de limpiar los cuartos o si se realizara una accion, en caso de realizarse
        la accion reducir el desempeño dependiendo lo que realize el robot.
        DEspues se actualiza el estatus del cuarto y la ubicacion del robot de ser necesario.
        """
        if acción is not "nada" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio":
            if acción == "limpiar": 
                self.desempeño -= 1
            elif acción in ("ir_Derecha", "ir_Izquierda"):
                self.desempeño -= 2
            elif acción in ("subir", "bajar"):
                self.desempeño -=3

        if acción == "limpiar":
            self.x[" ABCDEF".find(robot)] = "limpio"
        elif acción == "ir_Derecha":
            if robot == "A":
                self.x[0] = "B"
            elif robot == "B":
                self.x[0] = "C"
            elif robot == "D":
                self.x[0] = "E"
            else:
                self.x[0] = "F"
        elif acción == "ir_Izquierda":
            if robot == "C":
                self.x[0] = "B"
            elif robot == "B":
                self.x[0] = "A"
            elif robot == "F":
                self.x[0] = "E"
            else:
                self.x[0] = "D"
        elif acción == "subir":
            if robot == "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        elif acción == "bajar":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

#########################################################################################
"""
    #inciso 2
    Desarrollo agente reactivo basado en modelo para el entorno de 6 cuartos
"""
class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']
    """
    Proceso por el cual el robot interactua en el entorno.
    """
    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]

        #Revisa si hay un cuarto sucio en el entorno
        if not "sucio" in self.modelo:
            return "nada"
        #Si el cuarto actual se encuentra sucio, se limpia.
        if situación == "sucio":
            return "limpiar"

        #se revisa si el robot se encuentra en el piso de abajo
        if robot in ("A", "B", "C"):
            #Se revisa si al menos un cuarto de abajo se encuentra sucio
            if not "sucio" in (a,b,c):
                #Si ningun cuarto de abajo se encuentra sucio y el robot esta en b, se revisa la opcion mas optima para subir al segundo piso
                if robot == "B":
                    #Revisar si es mas optimo subir por la izquierda o la derecha
                    return ("ir_Izquierda" if d == "sucio" else "ir_Derecha")
                #Se sube al segundo piso si se esta en A o C
                else:
                    return "subir"
            #Se revisa a donde se debe mover el robot si hay cuartos sucios en el primer piso.
            else:
                return ("ir_Derecha" if robot == "A" or (robot == "B" and a == "limpio") else "ir_Izquierda")
        #El robot se encuentra en el piso de abajo
        else:
            if not "sucio" in (d, e, f):
                return ("ir_Derecha" if robot == "D" else "ir_Izquierda" if robot == "F" else "bajar")
            else:
                return ("ir_Derecha" if robot == "D" or (robot == "E" and d == "limpio") else "ir_Izquierda")
"""
    Agente que toma decisiones aleatorias apartir de su ubicacion en los 6 cuartos.
"""
class AgenteAleatorioSeisCuartos(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales dependiendo su
    ubicacion en la casa.
    """
    def __init__(self, acciones):
        self.acciones = acciones

    #Este robot selecciona al azar una accion dependiendo su ubicacion
    def programa(self, percepción):
        robot = percepción[0]
        if robot == "A":
                return random.choice(["ir_Derecha", "subir", "nada", "limpiar"])
        if robot == "B":
                return random.choice(["ir_Derecha", "ir_Izquierda", "nada", "limpiar"])
        if robot == "C":
                return random.choice(["ir_Izquierda", "subir", "nada", "limpiar"])
        if robot == "D":
                return random.choice(["ir_Derecha", "nada", "limpiar"])
        if robot == "E":
                return random.choice(["ir_Derecha", "ir_Izquierda", "bajar", "nada", "limpiar"])

        return random.choice(["ir_Izquierda", "nada", "limpiar"])

#########################################################################################
"""
    #inciso 3
    Desarrollo DosCuartosCiego donde el agente solo puede saber en que cuarto esta.
"""

"""
    En este entorno el robot solo puede saber en donde se encuentra pero no tiene informacion de la limpieza de los cuartos.
"""
class DosCuartosCiego(doscuartos_o.DosCuartos):
    #Regresa la informacion de donde se encuentra el robot.
    def percepción(self):
        return self.x[0]

class AgenteReactivoDosCuartosCiego(entornos_o.Agente):

     def __init__(self):
         """
         Inicializa el modelo interno en el peor de los casos
         """
         self.modelo = ['A', 'sucio', 'sucio']

     def programa(self, percepcion):
         robot = percepcion #ubicacion robot

         # Actualiza el modelo interno
         self.modelo[0] = robot

         status = self.modelo[' AB'.find(robot)]

         a, b, = self.modelo[1], self.modelo[2]

         #Se utiliza el conocimiento que tiene el robot, ya que no puede revisar como estan los cuartos
         #Si nunca a limpiado el robot va a limpiar ese cuarto aunque este limpio.
         if status == "sucio":
             #actualiza su conocimiento
             self.modelo[' AB'.find(robot)] = "limpio"
             return "limpiar"
        #Si ya limpio los dos cuartos se detiene
         if a == b == "limpio":
             return "nada"
        #Se cambia de habitación
         if robot == "A":
             return "ir_B"
         else:
             return "ir_A"

#########################################################################################
"""
    #inciso 4
    Desarrollo DosCuartosEstocasticos donde se tiene una posibilidad de que no se realize la accion deseada.
"""
class DosCuartosEstocástico(doscuartos_o.DosCuartos):

    def transición(self, acción):
        #Se revisa si la accion es valida
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x

        #Si la accion es diferente de "nada" o todavia no se termina de limpar los cuartos se disminulle el desempeño
        if acción is not "nada" or a == "sucio" or b == "sucio":
            self.desempeño -= 1
        #Si el robot va a limpiar hay un 80% de que se limpie  y un 20% de que se quede igual.
        if acción == "limpiar" and random.random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        #Si el robot va a moverse hay un 90% de que se mueva  y un 10% de que se quede donde está.
        elif random.random() <= 0.9:
            if acción == "ir_A":
                self.x[0] = "A"
            else:
                self.x[0] = "B"

class AgenteReactivoModeloDosCuartosEstocástico(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

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
"""
Test de los entornos y agentes.
"""
def test2():
    print("Inciso 2 agente reactivo vs agente aleatorio en SeisCuartos\n\n")
    #inciso 2
    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 100)

    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorioSeisCuartos(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 100)
    
def test3():    
    print("Inciso 3 agente racional ciego vs agente aleatorio en DosCuartosCiego\n\n")
    #inciso 3
    print("Prueba del entorno dos cuatos con agente racional ciego")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoDosCuartosCiego(), 100)

    print("Prueba del entorno dos cuatos con agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)
def test4(): 
    print("Inciso 4 agente reactivo vs agente aleatorio en DosCuartosEstocastico\n\n")
    #inciso 4
    print("Prueba del entorno estocástico con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteReactivoModeloDosCuartosEstocástico(), 100)

    print("Prueba del entorno estocástico con un agente aleatorio")
    entornos_o.simulador(DosCuartosEstocástico(), doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), 100)

if __name__ == "__main__":
    test4()


# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
