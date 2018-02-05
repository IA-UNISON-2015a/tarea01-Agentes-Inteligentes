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
__author__ = 'Raúl Pérez'

from doscuartos_o import DosCuartos, AgenteReactivoModeloDosCuartos, AgenteAleatorio
from entornos_o import simulador
from random import choice, random

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python

"""
Ejercicio 1
"""
class SeisCuartos(DosCuartos):
    """
    Clase para un entorno de seis cuartos.

    El estado se define como (robot, A, B, C, D, E, F)
    donde A, B y C son los pisos de abajo y D, E, y F son los de arriba,
    robot puede tener los valores de "A", "B", "C", "D", "E", "F"
    A, B, C, D, E y F pueden tener los valores "limpio" y "sucio"

    Las acciones válidas en el entorno son ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada").
    La acción de "subir" solo es legal en el piso de abajo, en los cuartos de los extremos, 
    mientras que la acción de "bajar" solo es legal en el piso de arriba y en el cuarto de el 
    centro (dos escaleras para subir, una escalera para bajar).

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza
    """  
    def __init__(self, x0=["F", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en B y todos los cuartos
        están sucios
        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        robot = self.x[0]

        return (True if acción is "subir" and robot in ("A", "C") 
            or acción is "bajar" and robot is "E"
            or acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")
            else False)

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x

        if acción is "subir":
            self.desempeño -= 2
            self.x[0] = "D" if robot is "A" else "F"
        elif acción is "bajar":
            self.desempeño -= 2
            self.x[0] = "B"
        elif "sucio" in (a, b, c, d, e, f):
            self.desempeño -= 1
        
        if acción is "limpiar":
            self.desempeño -= .5
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha":
            self.x[0] = ("B" if robot is "A"
                   else "C" if robot is "B"
                   else "E" if robot is "D"
                   else "F" if robot is "E"
                   else robot)
        elif acción is "ir_Izquierda":
            self.x[0] = ("A" if robot is "B"
                   else "B" if robot is "C"
                   else "D" if robot is "E"
                   else "E" if robot is "F"
                   else robot)

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

"""
Ejercicio 2
"""

class AgenteReactivoModeloSeisCuartos():
    """
    Un agente reactivo basado en modelo para el entorno seis cuartos
    """
    def __init__(self, modelo=['F', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = modelo[:]    
            
    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        _ ,a, b, c, d, e, f = self.modelo

        return ('nada' if (a == b == c == d == e == f == 'limpio') 
            else 'limpiar' if (situación == 'sucio')
            else 'ir_Derecha' if (robot is "A") and ('sucio' in (b, c))
            else 'ir_Derecha' if (robot is "B") and ((c is 'sucio') and (a is 'limpio'))
            else 'ir_Izquierda' if (robot is "C") and ('sucio' in (a, b))
            else 'ir_Izquierda' if (robot is "B") and ((a is 'sucio') and (c is 'limpio'))
            else choice(['ir_Derecha', 'ir_Izquierda']) if (robot is "B") and ((a == c == 'sucio') or ('sucio' in (d, e, f)))
            else 'subir' if (robot in ("A", "C")) and ('sucio' in (d, e, f))
            else 'ir_Derecha' if (robot is "D") and (('sucio' in (e, f)) or ('sucio' in (a, b, c)))
            else 'ir_Derecha' if (robot is "E") and ((f is 'sucio') and (d is 'limpio'))
            else 'ir_Izquierda' if (robot is "F") and (('sucio' in (d, e)) or ('sucio' in (a, b, c)))
            else 'ir_Izquierda' if (robot is "E") and ((d is 'sucio') and (f is 'limpio'))
            else choice(['ir_Derecha', 'ir_Izquierda']) if (robot is "E") and (d == f == 'sucio')
            else 'bajar' if (robot is "E") and ('sucio' in (a, b, c))
            else 'nada')

"""
Ejercicio 3
"""

class DosCuartosCiego(DosCuartos):
    """
    Clase para un entorno de dos cuartos ciego.

    """
    def percepción(self):
        """
        Solo percibe en que cuarto esta
        """
        return self.x[0]

class AgenteReactivoModeloDosCuartosCiego():
    """
        Un agente reactivo basado en modelo para el entorno dos cuartos ciego
    """
    def __init__(self, modelo=['A', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = modelo[:]

    def programa(self, percepción):
        robot = percepción
        # Actualiza el modelo interno
        self.modelo[0] = robot
        # obtiene la situacion desde el modelo
        situación = self.modelo[' AB'.find(robot)]
        # Decide sobre el modelo interno
        _, a, b = self.modelo
        # si el cuarto en el que esta el robot esta 'sucio', entonces lo pone en 'limpio' sino lo deja en 'sucio'
        self.modelo[' AB'.find(robot)] = 'limpio' if situación is 'sucio' else situación
    
        return ('nada' if (a == b == 'limpio') 
                else 'limpiar' if (situación is 'sucio') 
                else 'ir_A' if (robot is 'B') 
                else 'ir_B')

"""
Ejercicio 4
"""

class DosCuartosEstocástico(DosCuartos):
    """
    Clase Entorno dos cuartos estocastico

    El 80% de las veces limpia pero el otro 20% deja sucio el cuarto. 
    Igualmente, cuando el agente decida cambiar de cuarto, se cambie correctamente 
    de cuarto el 90% de la veces y el 10% se queda en su lugar.

    """

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        _ , a, b = self.x
        
        if (acción is not "nada") or ((a is "sucio") or (b is "sucio")):
            self.desempeño -= 1

        if (acción is "limpiar") and random() <= 0.8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif (acción is "ir_A") and random() <= 0.9:
            self.x[0] = "A"
        elif (acción is "ir_B") and random() <= 0.9:
            self.x[0] = "B"
        else:
            raise Exception("Siempre no...")

class AgenteReactivoModeloDosCuartosEstocastico(AgenteReactivoModeloDosCuartos):
    
    def __init__(self, modelo=['A', 'sucio', 'sucio']):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = modelo[:]

"""
Pruebas
"""

def test_seis_cuartos(cuarto_inicial='B'):
    """
    Prueba para el entorno seis cuartos

    """
    
    estados = [cuarto_inicial, "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    acciones = ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
    entorno = SeisCuartos(estados[:])
    agente_modelo = AgenteReactivoModeloSeisCuartos(entorno.x)
    
    print("Prueba del entorno seis cuartos con un agente basado en modelo")
    simulador(entorno, agente_modelo, 100)

    entorno = SeisCuartos(estados[:])
    agente_aleatorio = AgenteAleatorio(acciones[:])

    print("Prueba del entorno seis cuartos con un agente aleatorio")
    simulador(entorno, agente_aleatorio, 100)

def test_dos_cuartos_ciego(cuarto_inicial='A'):
    """
    Prueba entorno dos cuartos ciego

    """
    estados = [cuarto_inicial, "sucio", "sucio"]
    acciones = ["ir_A", "ir_B", "limpiar", "nada"]
    entorno  = DosCuartosCiego(estados[:])
    agente_modelo = AgenteReactivoModeloDosCuartosCiego(entorno.x)

    print("Prueba del entorno dos cuartos ciego con un agente basado en modelo")
    simulador(entorno, agente_modelo, 100)

    entorno = DosCuartosCiego(estados[:])
    agente_aleatorio = AgenteAleatorio(acciones[:])

    print("Prueba del entorno dos cuartos ciego con un agente aleatorio")
    simulador(entorno, agente_aleatorio, 100)

def test_dos_cuartos_estocastico(cuarto_inicial='A'):
    """
    Prueba entorno dos cuartos ciego
    
    """

    estados = [cuarto_inicial, "sucio", "sucio"]
    acciones = ["ir_A", "ir_B", "limpiar", "nada"]
    entorno = DosCuartosEstocástico(estados[:])
    agente_modelo = AgenteReactivoModeloDosCuartosEstocastico(entorno.x)

    print("Prueba del entorno dos cuartos estocastico con un agente basado en modelo")
    simulador(entorno, agente_modelo, 100)

    entorno  = DosCuartosEstocástico(estados[:])
    agente_aleatorio = AgenteAleatorio(acciones[:])

    print("Prueba del entorno dos cuartos estocastico con un agente aleatorio")
    simulador(entorno, agente_aleatorio, 100)    

def test():
    """
    Prueba del entorno y los agentes

    """
    for cuarto in ('A', 'B', 'C', 'D', 'E', 'F'):
        test_seis_cuartos(cuarto)
    
    for cuarto in ('A', 'B'):    
        test_dos_cuartos_ciego(cuarto)
    
    for cuarto in ('A', 'B'):
        test_dos_cuartos_estocastico(cuarto)

if __name__ == "__main__":
    test()

"""
Observaciones

Para el entorno de seis cuartos la diferencia es muy grande, esto se debe a que el
agente basado en modelo decide que hacer dependiendo de lo que conoce y el otro es
a lo que caiga.

Cuarto inicial  | Agente basado en modelo  | Agente aleatorio
        A       |         -15              |       -78.5
        B       |         -16              |       -89.5
        C       |         -15              |       -81.0
        D       |         -17              |       -85.5  
        E       |         -18              |       -90.5
        F       |         -17              |       -77.0

Para el entorno de dos cuartos ciego la diferencia es igual de grande,
esto se debe igual a que el agente basado en modelo decide que hacer dependiendo de lo que conoce 
y el otro es a lo que caiga.

Cuarto inicial  | Agente basado en modelo  | Agente aleatorio
        A       |          -3              |       -82.0
        B       |          -3              |       -72.0

Para el entorno de dos cuartos estocastico la diferencia es igual de grande...

Cuarto inicial  | Agente basado en modelo  | Agente aleatorio
        A       |          -8              |       -81.0
        B       |          -4              |       -84.0

"""
        