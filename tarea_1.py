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
import random
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
            if cuarto_actual is "E": self.x[0] = "B"

    def percepcion(self):
        """
        Se encuentra el cuarto segun su posicion en la lista de estados de los cuartos
        por eso el espacio en blanco inical

        @return La posicion de nuestro agente en el entorno, y el estado de esa posicion (cuarto)
        """
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

# **********************************************************************************************
#       Ejercio 2
class AgenteReactivo_Modelo_SeisCuartos(entornos_o.Agente):
    """
    Agente Reactivo para el entorno SeisCuartos
    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos, todos los cuartos sucios
        Utilizamos un diccionario pues porque se me hizo mas facil para ubicar los cuartos a traves de
        su llave
        """
        self.modelo = {"robot":"A", "A":"sucio", "B":"sucio", "C":"sucio", "D":"sucio", "E":"sucio", "F":"sucio"}
        #self.modelo =  ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]

    def programa(self,percepcion):
        """
        Reaccion si el cuarto esta sucio, regresa la accion 'limpiar'
        Si el cuarto esta limpio revisa hacia donde moverse y regresa la dirreccion a cual moverse

        """
        cuarto_actual, estado_actual = percepcion

        # Actualizamos
        self.modelo["robot"] = cuarto_actual
        self.modelo[cuarto_actual] = estado_actual

        # Dado que el cuarto esta sucio decimos que lo limpie
        if estado_actual is "sucio":
            return "limpiar"

        #Si ningun piso esta sucio regresa nada
        if not "sucio" in [self.modelo[i] for i in "ABCDEF"]: return "nada"
        #Decidimos la accion a realizar dado el estados de los cuartos y la posicion
        # El cuarto esta limpio llegados a este punto
        if cuarto_actual in "ABC":
            #Estmos en el primer piso
            if cuarto_actual in 'AC' and ("sucio" in [self.modelo[i] for i in "ABC"]):
                #self.modelo['A'] == "limpio" and self.modelo['B'] == "limpio" and self.modelo['C'] == "limpio": primer aproximacion
                # Revisamos el estado del piso en el modelo y si podemos subir, subimos
                return "subir"
            elif cuarto_actual is not 'C':
                #Recorremos hacia derecha o izquierda hasta el tope, entonces cuando en el
                # modelo, los cuartos inferiores esten limpios sube
                return "ir_Derecha"
            elif cuarto_actual is not 'A':
                return "ir_Izquierda"
        else: #cuarto in "DEF"
            #Estmos en el segundo piso
            if cuarto_actual is 'E' and "sucio" in [self.modelo[i] for i in "DEF"]:
                #self.modelo['D'] == "limpio" and self.modelo['E'] == "limpio" and self.modelo['F'] == "limpio":
                # Revisamos el estado del piso en el modelo y si podemos subir, subimos
                return "bajar"
            elif cuarto_actual is not 'F':
                #Recorremos hacia derecha o izquierda hasta el tope, entonces cuando en el
                # modelo, los cuartos inferiores esten limpios sube
                return "ir_Derecha"
            elif cuarto_actual is not 'D':
                return "ir_Izquierda"
        #En caso extraordinario, dile que haga nada
        return "nada"

class AgenteAleatorio_SeisCuartos(entornos_o.Agente):
    """
    Dependiendo del cuarto tenemos derecho a ciertos movimientos,
    define eso dado la percepcion.
    """
    def __init__(self,acciones):
        """
        Recibimos todos las acciones del agentes
        """
        self.acciones = acciones

    def programa(self, percepcion):
        cuarto_actual = percepcion[0]

        # De la lista de acciones posibles, copiamos y no modificamos la lista del agente
        acciones = self.acciones[:]

        if cuarto_actual in "ABC":
            acciones.remove("bajar")
            if cuarto_actual is "B":    acciones.remove("subir")
            elif cuarto_actual is "A":  acciones.remove("ir_Izquierda")
            elif cuarto_actual is "C":  acciones.remove("ir_Derecha")
        elif cuarto_actual in "DEF":
            acciones.remove("subir")
            if cuarto_actual in "DF":   acciones.remove("bajar")
            if cuarto_actual is "D":  acciones.remove("ir_Izquierda")
            if cuarto_actual is "F":  acciones.remove("ir_Derecha")

        return random.choice(acciones)

def test1(pasos = 100):
    """
    Simulacion del entorno seis caurtos
    """

    print("Prueba en SeisCuartos con un agente aleatorio.")
    entornos_o.simulador(SeisCuartos(), AgenteAleatorio_SeisCuartos(['ir_Derecha', 'ir_Izquierda', 'subir', 'bajar', 'limpiar', 'nada']), pasos)

    print("Prueba en SeisCuartos con un agente reactivo basado en modelo.")
    entornos_o.simulador(SeisCuartos(), AgenteReactivo_Modelo_SeisCuartos(), pasos)

# **********************************************************************************************
#       Ejercicio 3
class DosCuartosCiego(entornos_o.Entorno):
    """
    Entorno ciego, el robot no puede saber que estado tiene el cuarto
    por lo cual siempre entrara a limpiar.
    El robot tiene memoria "sabiendo" que cuarto fue limpiado, asume todo esta sucio
    por default

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_A", "ir_B", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if accion is not "nada" or a is "sucio" or b is "sucio":
            self.desempeno -= 1

        if accion is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif accion is "ir_A":
            self.x[0] = "A"
        elif accion is "ir_B":
            self.x[0] = "B"

        print("Accion en transicion:" +accion)
    def percepcion(self):
                        #no puedes saber si esta limpio
        return self.x[0] #, self.x[" AB".find(self.x[0])]

class AgenteReactivo_Modelo_DosCuartosCiego(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot = percepcion #ubicacion robot

        # Actualiza el modelo interno
        self.modelo[0] = robot
        # No sabes la situacion
        situacion = self.modelo[' AB'.find(robot)]

        if situacion is "sucio":
            # le decimos a nuestro robot que esta limpio dado que no tenemos vision del entorno
            self.modelo[' AB'.find(robot)] = "limpio"
            return "limpiar"
        if self.modelo[1] == self.modelo[2] == "limpio": return "nada"
        if robot == "A": return "ir_B"
        else: return "ir_A"


def test2():
    print("Prueba del entorno DosCuartosCiego con un agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(),
                         doscuartos_o.AgenteAleatorio(['ir_A', 'ir_B', 'limpiar', 'nada']),
                         100)

    print("Prueba del entorno DosCuartosCiegocon un agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivo_Modelo_DosCuartosCiego(), 100)

# **********************************************************************************************
#       Ejercicio 4

# **********************************************************************************************
if __name__ == "__main__":
    print("Probando Ejercicio 1 y 2")
    # revisar agente reactivo ciclado, nunca entra a cuarto F
    #test1() #testeando Ejercio 1 y 2
    test2() # testeando Ejercicio 3
    print("Hecho por Gilberto Espinoza")

# **********************************************************************************************
