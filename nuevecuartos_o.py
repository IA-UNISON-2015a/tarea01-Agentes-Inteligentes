import entornos_o
from random import choice


__author__ = 'alantorres'

class NineRooms(entornos_o.Entorno):

    def __init__(self, x0 = ["A", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio", "sucio"])

    def legal_action(self, action):
        if (action == "go_right" and self.x[0] in ("C", "F", "I")):
            return false
        elif (action == "go_left" and self.x[0] in ("A", "D", "G")):
            return false
        elif (action == "go_up" and self.x[0] in ("A", "B", "C")):
            return false
        elif (action == "go_down" and self.x[0] in ("G", "H", "I")):
            return false
        else:
            return action in ("go_right", "go_left", "go_up", "go_down", "clean", "nothing")

    def transition(self, action):
        if not self.legal_action(action):
            raise ValueError("La acción no es legal para este estado")
        
        cuartos = [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        robot, a, b ,c, d, e, f, g, h, i = self.x

        def buscar_indice(matriz, elemento):
            for i, fila in enumerate(matriz):
                if elemento in fila:
                    return i, fila.index(elemento)
            return None  # Si no se encuentra el elemento
    
        index = buscar_indice(cuartos, self.x[0])

        if action != "nothing" or a == "sucio", b == "sucio", c == "sucio", d == "sucio", e == "sucio", f == "sucio", g == "sucio", h == "sucio", i == "sucio":
            self.costo += 1
        if action == "clean":
            self.x[" ABCDEFGHI".find(self.x[0])] == "limpio"
        elif action == "go_right":
             self.x[0] = cuartos[index[0]][index[1] + 1]
        elif action == "go_left":
             self.x[0] = cuartos[index[0]+1][index[1] - 1]

        elif action == "go_up":
            self.x[0] == cuartos[index[0] + 1][index[]]
        elif action == "go_down":
            self.x[0] == cuartos[index[0] - 1][index[]]
    
    def perception(self):
        return self.x[0], self.x[" ABCDEFGHI".find(self.x[0])]


class RandomAgent(entornos_o.Agente):



