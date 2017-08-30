#*******************************Observaciones***********************************
#Al comparar el agente aleatorio con el basado en modelo, se puede observar que
#el agente basado en modelo tiene más desempeño, esto se debe a que este agente
#deja de hacer acciones cuando su modelo es cumplido, y ya que todos los cuartos
#quedan limpios deja de perder rendimiento el agente. El agente aleatorio no se
#preocupa por si los cuartos están limpios o están sucios, simplemente hace una
#acción aleatoria sin importar como esté el estado.
__author__ = "Roberto Salazar"

import entornos_o
import doscuartos_o

class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """Clase para el agente reactivo basado en modelo con seis cuartos"""
    def __init__(self):
        self.modelo = ['A', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio', 'sucio'] #se inicializa el modelo

    def programa(self, percepción):
        robot, situación = percepción

        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        return ('nada' if not 'sucio' in self.modelo[1:] else
                'limpiar' if situación == 'sucio' else
                'ir_Derecha' if robot == 'A' or robot == 'B' else
                'bajar' if robot == 'C' else
                'ir_Izquierda')

class SeisCuartos(entornos_o.Entorno):
    """Clase de los seis cuartos. Tres cuartos arriba y tres abajo."""
    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        """Basicamente el mismo constructor que la clase DosCuartos."""
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x
        if acción is "nada" and "sucio" in self.x[1:] or acción in ("ir_Derecha","ir_Izquierda", "limpiar"):
            self.desempeño -= 1
        elif acción in ("subir", "bajar"):
            self.desempeño -= 2
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha":
            if robot is "A":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "C"
            elif robot is "D":
                self.x[0] = "E"
            elif robot is "E":
                self.x[0] = "F"
        elif acción is "ir_Izquierda":
            if robot is "C":
                self.x[0] = "B"
            elif robot is "B":
                self.x[0] = "A"
            elif robot is "F":
                self.x[0] = "E"
            elif robot is "E":
                self.x[0] = "D"
        elif acción is "subir":
            if robot is "D":
                self.x[0] = "A"
            elif robot is "E":
                self.x[0] = "B"
            elif robot is "F":
                self.x[0] = "C"
        elif acción is "bajar":
            if robot is "A":
                self.x[0] = "D"
            elif robot is "B":
                self.x[0] = "E"
            elif robot is "C":
                self.x[0] = "F"

    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]

if __name__ == "__main__":
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         doscuartos_o.AgenteAleatorio(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]),
                         100)

    print("Prueba del entorno con un reactivo basado en modelo")
    entornos_o.simulador(SeisCuartos(),
                         AgenteReactivoModeloSeisCuartos(),
                         100)
