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
__author__ = 'gilbertoespinoza'

""" Importaciones generales """
import entornos_o
# Requiere el modulo entornos_o.py

# Usa el modulo doscuartos_o.py para reutilizar código
import doscuartos_o
# Agrega los modulos que requieras de python

# **********************************************************************************************
##      Ejercicio 1
class SeisCuartos(entornos_o.Entorno):
    """
        Clase para un entorno de seis cuartos, distribuidos
        D E F
        A B C
        Para subir al piso de arriba se debe estar en D o F
        Para bajar en el cuarto B

        Las acciones válidas en el entorno son:
            ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    """
    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default empezamos en A y todos los cuartos estan sucios
        """
        self.x = x0[:]
        # Hemos hecho un costo cero
        self.desempeno = 0

    def accion_legal(self, accion):
        if accion in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"):
            #Validado que la accion este dentro de las acciones posibles
            if accion is "ir_Derecha":
                #Para que esta accion sea legal debes estar en el A B D o E
                return self.x[0] in ("A", "B", "D", "E")
            elif accion is "ir_Izquierda":
                #Para que esta accion sea legal debes estar en el B C E F
                return self.x[0] in ("B", "C", "E", "F")
            elif accion is "subir":
                #Para que esta accion sea legal debes estar en el A y C
                return self.x[0] in ("A", "C")
            elif accion is "bajar":
                #Para que esta accion sea legal debes estar en el B
                return self.x[0] is "E"
            else:
                #Limpiar y nada son las acciones restantes, entonces siempre son legales
                return True
        else:
            # La accion que quieren realizar no es parte del conjunto de acciones legales
            return False

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        #Asiganando el lugar de nuestro agente (robot), y el estado de los cuartos
        cuarto_actual = self.x[0]

        """ Intentando una aproximacion con diccionarios... deprecated
        etiq = ["A", "B", "C", "D", "E", "F"] #etiquetas de los cuartos
        # ubicamos los cuartos por su etiqueta y estado definido en __init__
        cuartos = {etiq[i]:self.x[i+1] for i in range(len(etiq))}
        """

        # Costos para el desempeno del agente
        COSTO_LIMPIAR = 1
        COSTO_MOVER = 2
        COSTO_SUBIR_BAJAR = 3

        if accion is "limpiar":
            self.desempeno -= COSTO_LIMPIAR
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        if accion is "ir_Derecha":
            self.desempeno -= COSTO_MOVER
            if cuarto_actual is "A": self.x[0] = "B"
            if cuarto_actual is "B": self.x[0] = "C"
            if cuarto_actual is "D": self.x[0] = "E"
            if cuarto_actual is "E": self.x[0] = "F"
        if accion is "ir_Izquierda":
            self.desempeno -= COSTO_MOVER
            if cuarto_actual is "B": self.x[0] = "A"
            if cuarto_actual is "C": self.x[0] = "B"
            if cuarto_actual is "E": self.x[0] = "D"
            if cuarto_actual is "F": self.x[0] = "E"
        if accion is "subir":
            self.desempeno -= COSTO_SUBIR_BAJAR
            if cuarto_actual is "A": self.x[0] = "D"
            if cuarto_actual is "C": self.x[0] = "F"
        if accion is "bajar":
            self.desempeno -= COSTO_SUBIR_BAJAR
            if cuarto_actual is "A": self.x[0] = "B"

    def percepcion(self):
        """
        Se encuentra el cuarto segun su posicion en la lista de estados de los cuartos
        por eso el espacio en blanco inical

        @return La posicion de nuestro agente en el entorno, y el estado de esa posicion (cuarto)
        """
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]





# **********************************************************************************************

# **********************************************************************************************


# **********************************************************************************************



# **********************************************************************************************


# **********************************************************************************************
