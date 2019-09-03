from nuevecuartos_f import *
from random import randint, choice

class NueveCuartosEstocastico(NueveCuartos):
    
    def accion_legal_aleatoria(self, estado):
        robot = estado[0]
        print("El robot esta en", robot)
        if robot in "A":
            return choice(["ir_derecha", "limpiar"])
        elif robot in "BEH":
            return choice(["ir_izquierda", "ir_derecha", "limpiar"])
        elif robot in "CF":
            return choice(["subir", "ir_izquierda", "limpiar"])
        elif robot in "I":
            return choice(["ir_izquierda", "limpiar"])
        else:
            return choice(["bajar", "ir_derecha", "limpiar"])
        
    def transicion(self, estado, accion):
        robot, cuartos = estado

        probabilidad = randint(1,10)

        # cuando el agente decide cambiar de cuarto, se cambia correctamente de cuarto el 80% de la veces, 
        # el 10% de la veces se queda en su lugar y el 10% de las veces realiza una acción legal aleatoria
        if accion in ['ir_izquierda', 'ir_derecha', 'subir', 'bajar']:
            if probabilidad == 1:
                accion = self.accion_legal_aleatoria(estado)
                print('la accion de movimiento se cambio a', accion)
            elif probabilidad == 10:
                print('la accion se cambio a nada')
                accion = 'nada'
            

        if "sucio" not in list(cuartos.values()) and accion is "nada":
            c_local = 0
        
        elif accion is "ir_izquierda" or accion is "ir_derecha":
            c_local = 2

        elif accion is "subir" or accion is "bajar":
            c_local = 3
        
        else:
            c_local = 1

        if accion is "nada":
            return (robot, cuartos, c_local)

        
        elif accion is "ir_derecha":
        
            if robot in "A":
                return ("B", cuartos, c_local)
            elif robot in "B":
                return ("C", cuartos, c_local)
            elif robot in "D":
                return ("E", cuartos, c_local)
            elif robot in "E":
                return ("F", cuartos, c_local)
            elif robot in "G":
                return ("H", cuartos, c_local)
            elif robot in "H":
                return ("I", cuartos, c_local)
            
        elif accion is "ir_izquierda":
            if robot in "B":
                return ("A", cuartos, c_local)
            elif robot in "C":
                return ("B", cuartos, c_local)
            elif robot in "E":
                return ("D", cuartos, c_local)
            elif robot in "F":
                return ("E", cuartos, c_local)
            elif robot in "H":
                return ("G", cuartos, c_local)
            elif robot in "I":
                return ("H", cuartos, c_local)
        
        elif accion is "limpiar":
            
            if randint(1,10) <= 8:
                cuartos[robot] = "limpio"
            else:
                print("intento limpiar pero no pudo")
            return (robot, cuartos, c_local)
        
        elif accion is "subir":
            if robot in "C":
                return ("F", cuartos, c_local)
            else:
                return ("I", cuartos, c_local)
        
        elif accion is "bajar":
            if robot in "G":
                return ("D", cuartos, c_local)
            else:
                return ("A", cuartos, c_local)


def prueba_agente_estocastica(agente):
    cuartos = {}
    for char in 'ABCDEFGHI':
        cuartos[char] = 'sucio'
    entornos_f.imprime_simulacion(
        entornos_f.simulador(
            NueveCuartosEstocastico(),
            agente,
            ["A", cuartos.copy()],
            200
        ),
        ["A", cuartos]
    )

def test_estocastico():
    """
    Prueba del entorno y los agentes
    """

    print("Prueba del entorno con un agente reactivo con modelo")
    prueba_agente_estocastica(AgenteReactivoModeloNueveCuartos())

    # print("Prueba del entorno con un agente aleatorio")
    # prueba_agente(AgenteAleatorio(['ir_izquierda', 'ir_derecha', 'limpiar', 'subir', 'bajar', 'nada']))

if __name__ == "__main__":
    test_estocastico()