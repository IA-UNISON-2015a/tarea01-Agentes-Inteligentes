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
__author__ = 'IvanAlejandroMorenoSoto'

import entornos_o
from random import random
from doscuartos_o import DosCuartos, AgenteReactivoModeloDosCuartos, AgenteAleatorio

##############################################################

# Ejercicio 1.

class SeisCuartos(entornos_o.Entorno):
    """
    Entorno de una casa con seis cuartos: tres en la planta inferior y
    tres en la superior.
    
    Análogamente a DosCuartos, el estado se define como:
    estado := [posición, A, B, C, D, E, F]
    
    D E F
    A B C
    
    Donde A, B, C, son los cuartos inferiores, D, E, F, los superiores,
    y posición puede tomar como valor cualquiera de ellos. Cada cuarto
    puede estar "limpio" o "sucio."
    
    Las acciones válidas son:
    acciones = {"ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"}
    Todas son legales en todos los cuartos excepto por "subir" que únicamente es
    legal en B1 y B3, y "bajar" que sólo se puede realizar en A2.
    
    Los sensores son una tupla que contiene la posición del robot y el estado de
    limpieza del cuarto.
    """
    
    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Define el estado inicial de este entorno.
        De forma predeterminada el robot se encuentra en el cuarto inferior izquierdo
        y toda la casa está sucia.
        
        @param x0: Vector con el estado inicial del entorno de la forma
        [posiciónInicial, limpieza_A, limpieza_B, limpieza_C, limpieza_D, limpieza_E, limpieza_F].
        """
        self.x = x0[:]
        self.desempeño = 0
    
    def acción_legal(self, acción):
        """
        Determina si una acción es legal en el estado actual.
        
        @param acción: Acción que será revisada.
        
        @return True si la acción es legal, False en caso contrario.
        """
        # Se separan los casos en: el robot quiere subir o quiere bajar o quiere hacer
        # cualquier otra cosa.
        if acción is "subir" and (self.x[0] is "A" or self.x[0] is "C"):
            return True
        if acción is "bajar" and self.x[0] is "E":
            return True
        
        return acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")
    
    def transición(self, acción):
        """
        Transforma al entorno según la acción recibida.
        
        @param acción: Acción de entrada al entorno.
        """
        if not self.acción_legal(acción):
            print("La acción no es legal para este estado")
            self.desempeño -= 1
            return
            #raise ValueError("La acción no es legal para este estado")

        posición = self.x[0]
        
        # Se determina el desempeño local.
        if "sucio" in self.x or acción is "limpiar":
            self.desempeño -= 1
        elif acción is "ir_Derecha" or acción is "ir_Izquierda":
            self.desempeño -= 2
        elif acción is "subir" or acción is "bajar":
            self.desempeño -= 3
        
        # Se modifica al entorno.
        if acción is "limpiar":
            self.x[" ABCDEF".find(posición)] = "limpio"
        elif acción is "ir_Derecha":
            if posición is "A":
                self.x[0] = "B"
            elif posición is "B":
                self.x[0] = "C"
            elif posición is "D":
                self.x[0] = "E"
            elif posición is "E":
                self.x[0] = "F"
        elif acción is "ir_Izquierda":
            if posición is "B":
                self.x[0] = "A"
            elif posición is "C":
                self.x[0] = "B"
            elif posición is "E":
                self.x[0] = "D"
            elif posición is "F":
                self.x[0] = "E"
        elif acción is "subir":
            if posición is "A":
                self.x[0] = "D"
            else:
                self.x[0] = "F"
        elif acción is "bajar":
            self.x[0] = "B"
    
    def percepción(self):
        """
        Regresa la percepción del entorno en el estado actual.
        
        @return Una tupla (posición, limpio?)
        """
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

##############################################################

# Ejercicio 2

def hacerPruebaEjercicio1_2(pasos):
    """
    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en SeisCuartos con un agente aleatorio.")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorio(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']), pasos)

    #print("Prueba en SeisCuartos con un agente reactivo basado en modelo.")
    #entornos_o.simulador(SeisCuartos(), AgenteSeisCuartos(), pasos)

##############################################################

# Ejercicio 3.

class DosCuartosCiego(DosCuartos):
    """
    Entorno basado en DosCuartos donde el robot solo tiene
    acceso a su posición actual.
    """

    def percepción(self):
        """
        @return Únicamente la posición actual del robot.
        """
        return self.x[0]

class AgenteDosCuartosCiego(AgenteReactivoModeloDosCuartos):
    """
    Agente para el entorno DosCuartosCiego.
    """

    def programa(self, percepción):
        """
        Aquí, el robot decide que acción realizará según su memoria de la
        situación del cuarto donde está.

        @param percepción Percepción del entorno en el estado actual.
        
        @return Una de cuatro acciones de ['ir_A', 'ir_B', 'limpiar', 'nada'].
        """

        # Se actualiza el lugar actual del robot.
        self.modelo[0] = percepción

        # Revisa lo que recuerda sobre el cuarto en el que se encuentra.
        situación = self.modelo[' AB'.find(percepción)]

        a, b = self.modelo[1], self.modelo[2]

        if a == b == 'limpio':
            return 'nada'
        elif situación == 'sucio':
            # Antes de regresar la acción, se actualiza la memoria sobre
            # el cuarto actual.
            self.modelo[' AB'.find(percepción)] = 'limpio'
            return 'limpiar'
        elif percepción == 'B':
            return 'ir_A'
        else:
            return 'ir_B'

def hacerPruebaEjercicio3(pasos):
    """
    Prueba el AgenteDosCuartosCiego y el AgenteAleatorio (de doscuartos_o)
    en el entorno DosCuartosCiego.

    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en DosCuartosCiego con un agente aleatorio.")
    entornos_o.simulador(DosCuartosCiego(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), pasos)

    print("Prueba en DosCuartosCiego con un agente racional.")
    entornos_o.simulador(DosCuartosCiego(), AgenteDosCuartosCiego(), pasos)

##############################################################

# Ejercicio 4.

class DosCuartosEstocástico(DosCuartos):
    """
    Entorno en el cual el agente tiene un 80% de éxito al limpiar un
    cuarto y un 90% al cambiarse de cuarto.
    """

    def transición(self, acción):
        """
        Implementa una transición estocástica del entorno.

        @param acción Acción del agente.
        """
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado.")

        robot, a, b = self.x

        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1

        if acción is "limpiar" and random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A" and random() <= 0.9:
            self.x[0] = "A"
        elif acción is "ir_B" and random() <= 0.9:
            self.x[0] = "B"

class AgenteDosCuartosEstocástico(AgenteReactivoModeloDosCuartos):
    """
    Agente racional para el entorno DosCuartosEstocástico. Está
    basado en un modelo.
    """
    
    def programa(self, percepción):
        """
        Funciona igual que el agente reactivo basado en modelo usado
        en DosCuartos, pero al momento de escoger una acción tiene en
        cuenta que puede fallar.
        
        @param percepción: Percepción de DosCuartosEstocástico.
        """
        posición, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = posición
        self.modelo[' AB'.find(posición)] = situación

        # Decide sobre el modelo interno y la posibilidad de fallo.
        a, b = self.modelo[1], self.modelo[2]
        éxito = random()
        
        # Si el robot 'siente' que puede fallar, mejor hace nada.
        if (a == b == 'limpio') or éxito < 0.1:
            return 'nada'
        elif situación is 'sucio' and éxito >= 0.2:
            return 'limpiar'
        elif posición is 'A' and self.modelo[2] == 'sucio':
            return 'ir_B'
        elif posición is 'B' and self.modelo[1] == 'sucio':
            return 'ir_A'

def hacerPruebaEjercicio4(pasos):
    """
    @param pasos: Número de pasos de la simulación.
    """

    print("Prueba en DosCuartosEstocástico con un agente aleatorio.")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']), pasos)

    print("Prueba en DosCuartosEstocástico con un agente racional.")
    entornos_o.simulador(DosCuartosEstocástico(), AgenteDosCuartosEstocástico(), pasos)

##############################################################

if __name__ == "__main__":
    #hacerPruebaEjercicio1_2(100)
    #hacerPruebaEjercicio3(100)
    hacerPruebaEjercicio4(100)
