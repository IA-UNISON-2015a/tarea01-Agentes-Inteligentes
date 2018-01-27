#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
entornos_o.py
------------

Entornos y agentes desde una prespectiva OO

"""

__author__ = 'juliowaissman'

class Entorno:
    """
    Clase abstracta para entornos

    En realidad funciona como un contenedor de funciones

    """

    def __init__(self, x0=[]):
        """
        Inicializa la clase con el estado inicial como una lista

        """
        self.x = x0[:]
        self.desempenio = 0

    def accion_legal(self, accion):
        """
        @param accion: Una accion en el entorno

        @return: True si accion es legal en estado, False en caso contrario

        Por default acepta cualquier accion.

        """
        return True

    def transicion(self, accion):
        """
        @param accion: Uno de los elementos de acciones_legales( estado)

        Modifica self.estado y self.desempenio

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

        @return: accion: Accion seleccionada por el agente.

        """
        pass


def simulador(entorno, agente, pasos=10, verbose=True):
    """Realiza la simulacion de un agente actuando en un entorno de forma generica

    @param entorno: Un objeto de la clase Entorno
    @param agente: Un objeto de la clase Agente
    @param pasos: Un int con el numero de pasos a simular
    @param verbose: Si True, imprime el resultado de la simulacion

    @retrun (historial_estados, historial_acciones,
            historial_desempenio) donde cada una es una lista con los
            estados, acciones y medida de desempenio encontradas a lo
            largo de la simulacion.

    """
    historial_desempenio = [entorno.desempenio]
    historial_estados = [entorno.x[:]]
    historial_acciones = []

    for paso in range(pasos):
        p = entorno.percepcion()
        a = agente.programa(p)
        entorno.transicion(a)

        historial_desempenio.append(entorno.desempenio)
        historial_estados.append(entorno.x[:])
        historial_acciones.append(a)

    historial_acciones.append(None)

    if verbose:
        print(u"\n\nSimulacion de entorno tipo " +
              str(type(entorno)) +
              " con el agente tipo " +
              str(type(agente)) + "\n")

        print('Paso'.center(10) +
              'Estado'.center(40) +
              u'Accion'.center(25) +
              u'Desempenio'.center(15))

        print('_' * (10 + 40 + 25 + 15))

        for i in range(pasos):
            print(str(i).center(10) +
                  str(historial_estados[i]).center(40) +
                  str(historial_acciones[i]).center(25) +
                  str(historial_desempenio[i]).rjust(12))

        print('_' * (10 + 40 + 25 + 15) + '\n\n')

    return historial_estados, historial_acciones, historial_desempenio
