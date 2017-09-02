#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

En esta tarea realiza las siguiente acciones:

1.- Desarrolla un entorno similar al de los dos cuartos (el cual se encuentra
    en el módulo doscuartos_o.py), pero con tres cuartos en el primer piso,
    y tres cuartos en el segundo piso.

    El entorno se llamará SeisCuartos

    Las acciones totales serán

    ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]

    La acción de "subir" solo es legal en el piso de abajo (cualquier cuarto),
    y la acción de "bajar" solo es legal en el piso de arriba.

    Las acciones de subir y bajar son mas costosas en término de energía
    que ir a la derecha y a la izquierda, por lo que la función de desempeño
    debe de ser de tener limpios todos los cuartos, con el menor numero de
    acciones posibles, y minimozando subir y bajar en relación a ir a los
    lados.

2.- Diseña un Agente reactivo basado en modelo para este entorno y compara
    su desempeño con un agente aleatorio despues de 100 pasos de simulación.

3.- Al ejemplo original de los dos cuartos, modificalo de manera que el agente
    solo pueda saber en que cuarto se encuentra pero no sabe si está limpio
    o sucio.

    A este nuevo entorno llamalo DosCuartosCiego

    Diseña un agente racional para este problema, pruebalo y comparalo
    con el agente aleatorio.

4.- Reconsidera el problema original de los dos cuartos, pero ahora modificalo
    para que cuando el agente decida aspirar, el 80% de las veces limpie pero
    el 20% (aleatorio) deje sucio el cuarto. Diseña un agente racional
    para este problema, pruebalo y comparalo con el agente aleatorio.

    A este entorno llamalo DosCuartosEstocástico

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Patricia Quiroz'

class Entorno:
    """
    Clase abstracta para entornos

    En realidad funciona como un contenedor de funciones

    """

    def __init__(self, x0=[]):
        # Inicializa la clase con el estado inicial como una lista
        self.x = x0[:]


        self.desempeno = 0

    def accion_legal(self, accion):
        """
        @param acción: Una accion en el entorno

        @return: True si accion es legal en estado, False en caso contrario

        Por default acepta cualquier acción.

        """
        return True

    def transicion(self, accion):
        """
        @param accion: Uno de los elementos de acciones_legales( estado)

        Modifica self.estado y self.desempeño

        """
        pass

    def percepcion(self):
        """
        @return: Tupla con los valores que se perciben del entorno por
                 default el estado completo

        """
        return self.x


class Agente(object):
    """
    Clase abstracta para un agente que interactua con un
    entorno discreto determinista observable.

    """

    def programa(self, percepcion):
        """
        @param percepcion: Lista con los valores que se perciben de un entorno

        @return: accion: Acción seleccionada por el agente.

        """
        pass


def simulador(entorno, agente, pasos=10, verbose=True):
    """Realiza la simulación de un agente actuando en un entorno de forma genérica

    @param entorno: Un objeto de la clase Entorno
    @param agente: Un objeto de la clase Agente
    @param pasos: Un int con el número de pasos a simular
    @param verbose: Si True, imprime el resultado de la simulación

    @retrun (historial_estados, historial_acciones,
            historial_desempeño) donde cada una es una lista con los
            estados, acciones y medida de desempeño encontradas a lo
            largo de la simulación.

    """
    historial_desempeno = [entorno.desempeno]
    historial_estados = [entorno.x[:]]
    historial_acciones = []

    for paso in range(pasos):
        p = entorno.percepcion()
        a = agente.programa(p)
        entorno.transicion(a)

        historial_desempeno.append(entorno.desempeno)
        historial_estados.append(entorno.x[:])
        historial_acciones.append(a)

    historial_acciones.append(None)

    if verbose:
        print(u"\n\nSimulación de entorno tipo " +
              str(type(entorno)) +
              " con el agente tipo " +
              str(type(agente)) + "\n")

        print('Paso'.center(10) +
              'Estado'.center(40) +
              u'Acción'.center(25) +
              u'Desempeño'.center(15))

        print('_' * (10 + 40 + 25 + 15))

        for i in range(pasos):
            print(str(i).center(10) +
                  str(historial_estados[i]).center(40) +
                  str(historial_acciones[i]).center(25) +
                  str(historial_desempeno[i]).rjust(12))

        print('_' * (10 + 40 + 25 + 15) + '\n\n')

    return historial_estados, historial_acciones, historial_desempeno


"""

Ejemplo de un entorno muy simple y agentes idem

"""


class DosCuartos(Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza (donde se encuentra el robot).

    """

    def __init__(self, x0=["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """ El robot esta en el cuarto A y todos los cuartos estan sucios
            x=[robot,A,B,C,D,E,F]
            cuartos: D,E,F
                    A,B,C

        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeno = 0

    def accion_legal(self, accion):
        return accion in ("ir_Der", "ir_Izq", "subir", "bajar", "limpiar", "nada")

    def transicion(self, accion):
        if not self.accion_legal(accion):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x
        if accion is "subir" or accion is "bajar":
            self.desempeno -= 1

        if accion is not "nada" or a is "sucio" or b is "sucio" or c is"sucio" or d is "sucio" or e is "sucio" or f is "sucio":
            self.desempeno -= 1

        if accion is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        # MOVERTE EN CUARTOS DE LA PARTE DE ABAJO
        elif accion is "ir_Der" and self.x[0] is "A":
            self.x[0] = "B"
        elif accion is "subir" and self.x[0] is "A":
            self.x[0] = "D"
        elif accion is "ir_Der" and self.x[0] is "B":
            self.x[0] = "C"
        elif accion is "ir_Izq" and self.x[0] is "B":
            self.x[0] = "A"
        elif accion is "subir" and self.x[0] is "B":
            self.x[0] = "E"
        elif accion is "ir_Izq" and self.x[0] is "C":
            self.x[0] = "B"
        elif accion is "subir" and self.x[0] is "C":
            self.x[0] = "F"
        # MOVERTE EN LOS CUARTOS DE ARRIBA
        elif accion is "ir_Der" and self.x[0] is "D":
            self.x[0] = "E"
        elif accion is "bajar" and self.x[0] is "D":
            self.x[0] = "A"
        elif accion is "ir_Der" and self.x[0] is "E":
            self.x[0] = "F"
        elif accion is "ir_Izq" and self.x[0] is "E":
            self.x[0] = "D"
        elif accion is "bajar" and self.x[0] is "E":
            self.x[0] = "B"
        elif accion is "ir_Izq" and self.x[0] is "F":
            self.x[0] = "E"
        elif accion is "bajar" and self.x[0] is "F":
            self.x[0] = "C"
            # MOVERTE DE UN CUARTO DE ABAJO HACIA ARRIBA

    def percepcion(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]


class AgenteAleatorio(Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """

    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteReactivoModeloDosCuartos(Agente):
    """
    Un agente reactivo basado en modelo

    """

    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio']

    def programa(self, percepcion):
        robot, situacion = percepcion

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situacion

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        # Cambia dependiendo de situacion
        if a==b==c==d==e==f=='limpio':
            aux='nada'
        elif situacion is 'sucio':
            aux='limpiar'
        elif robot == 'A' or robot == 'B':
            aux='ir_Der'
        elif robot == 'C':
            aux='subir'
        elif robot == 'F' or robot == 'E':
            aux='ir_Izq'
        elif robot == 'D':
            aux='bajar'

        return (aux)


def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatori-o")
    simulador(DosCuartos(),
              AgenteAleatorio(('ir_Der', 'ir_Izq', 'subir', 'bajar', 'limpiar', 'nada')),
             100)

    print("Prueba del entorno con un agente reactivo con modelo")
    simulador(DosCuartos(), AgenteReactivoModeloDosCuartos(), 100)


if __name__ == "__main__":
    test()
    e = DosCuartos()
    # e = DosCuartos()
    # print(e.x)

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
