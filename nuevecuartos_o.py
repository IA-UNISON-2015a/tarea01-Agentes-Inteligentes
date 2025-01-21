import entornos_o
from random import choice


__author__ = 'alantorres'

class NueveCuartos(entornos_o.Entorno):

    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]):
        self.x = x0
        self.costo = 0



    def accion_legal(self, action):
        if (action == "go_right" and self.x[0] in ("C", "F", "I")):
            return False
        elif (action == "go_left" and self.x[0] in ("A", "D", "G")):
            return False
        elif (action == "go_up" and self.x[0] in ("A", "B", "C")):
            return False
        elif (action == "go_down" and self.x[0] in ("G", "H", "I")):
            return False
        else:
            return action in ("go_right", "go_left", "go_up", "go_down", "clean", "nothing")

    def transicion(self, action):
        if not self.accion_legal(action):
            raise ValueError("La acción no es legal para este estado")
        
        cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        robot, a, b, c, d, e, f, g, h, i = self.x

        def buscar_indice(matriz, elemento):
            for i, fila in enumerate(matriz):
                if elemento in fila:
                    return i, fila.index(elemento)
            return None  # Si no se encuentra el elemento
    
        index = buscar_indice(cuartos, self.x[0])

        if action != "nothing" or a == "sucio" or b == "sucio" or c == "sucio" or d == "sucio" or e == "sucio" or f == "sucio" or g == "sucio" or h == "sucio" or i == "sucio":
            self.costo += 1
        if action == "clean":
            self.x[" ABCDEFGHI".find(self.x[0])] = "limpio"
        elif action == "go_right":
            self.x[0] = cuartos[index[0]][index[1] + 1]
        elif action == "go_left":
            self.x[0] = cuartos[index[0]+1][index[1] - 1]

        elif action == "go_up":
            self.x[0] == cuartos[index[0] + 1][index[1]]
        elif action == "go_down":
            self.x[0] == cuartos[index[0] - 1][index[1]]
    
    def percepcion(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


class AgenteAleatorio(entornos_o.Agente):
    def __init__(self, actions):
        self.actions = actions

    def programa(self, _):
        return choice(self.actions)

def test():
    x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"]
    entornos_o.simulador(NueveCuartos(x0), AgenteAleatorio(["go_up","go_down", "go_right", "go_left", "clean", "nothing"]), 100)

if __name__ == "__main__":
    test()
