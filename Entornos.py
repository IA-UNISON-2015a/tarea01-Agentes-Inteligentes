#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'juanmanuel'

"""

Entornos
------------

Clase abstracta para entornos

"""

class Entorno(object):

    def Sensores(self,estado):
      """

       @param estado: Tupla con un estado válido para el entorno

       @return: Tupla con los valores que se perciben de un entorno

      """     
    pass

    def Accion_Legal(self,estado,accion):
      """

        @param estado: Tupla con un estado válido para el entorno

        @param accion: Uno de los elementos de acciones_legales(estado)

        @return: Booleano True si la accion es legal en el estado, False en caso contrario

        Por default acepta cualquier acción.

      """
      return True 

    def Transicion(self,estado,accion):
      """

         @param estado: Tupla con un estado válido para el entorno

         @param accion: Uno de los elementos de acciones_legales( estado)

         @return: el estado a donde transita el entorno cuando el
                  agente aplica la acción o una tupla de pares ordenados
                  con el posible estado nuevo y su probabilidad.

      """
    pass

    def Desempeno_Local(self,estado,accion):
      """

        @param estado: Lista con un estado válido para el entorno

        @param accion: Uno de los elementos de acciones_legales( estado)

        @return: un número flotante con el desempeño de aplicar la accion en el estado

      """
    pass

"""

  Clase abstracta para un agente que interactua con un
  entorno discreto determinista observable.

"""

class Agente(object):

    def Programa(self,percepcion):
      """

        @param percepcion: Lista con los valores que se perciben de un entorno

        @return: accion: Acción seleccionada por el agente, utilizando su programa de agente.

      """
    pass

"""

  Realiza la simulación de un agente actuando en un entorno de forma genérica

"""

def Simulador(entorno,agente,estado_inicial,pasos=10,verbose=True):

    estado = estado_inicial
    performance = 0
    performances = [performance]
    estados = [estado]
    acciones = [None]

    for paso in range(pasos):

        percepcion = entorno.Sensores(estado)
        accion = agente.Programa(percepcion)
        estado_n = entorno.Transicion(estado,accion)
        performance += entorno.Desempeno_Local(estado,accion)

        performances.append(performance)
        estados.append(estado_n)
        acciones.append(accion)
        estado = estado_n

    if verbose:
        print "\n\nSimulacion de entorno tipo " + \
              str(type(entorno)) + \
              " con el agente tipo " + \
              str(type(agente)) + "\n"

        print 'Paso'.center(10) + \
              'Estado'.center(40) + \
              'Accion'.center(25) + \
              u'Desempeño'.center(15)

        print '_' * (10 + 40 + 25 + 15)

        for i in range(pasos):
            print (str(i).center(10) +
                   str(estados[i]).center(40) +
                   str(acciones[i]).center(25) +
                   str(performances[i]).rjust(12))

        print '_' * (10 + 40 + 25 + 15) + '\n\n'

    return estados,acciones,performances


