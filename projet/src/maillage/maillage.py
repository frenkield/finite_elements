from matplotlib.tri import Triangulation
import numpy as np
import math


class Maillage:

    def __init__(self, nodes: np.array, elements: np.array):
        self.noeuds = nodes
        self.elements = elements
        self.aretes_du_bord = []
        self.noeuds_du_bord = []
        self.h = 1

    @classmethod
    def vide(cls, nombre_noeuds_horizontal: int, nombre_noeuds_vertical: int):

        assert nombre_noeuds_horizontal > 0
        assert nombre_noeuds_vertical > 0

        nodes = np.zeros((nombre_noeuds_horizontal * nombre_noeuds_vertical, 3),
                         dtype=float)

        elements = np.zeros((2 * (nombre_noeuds_horizontal - 1) *
                             (nombre_noeuds_vertical - 1), 3), dtype=int)

        return cls(nodes, elements)

    def set_node(self, index: int, node: list):
        self.noeuds[index, :] = node

    def set_node_from_values(self, index: int, x: float, y: float, z: float):
        self.noeuds[index, 1] = x
        self.noeuds[index, 2] = y
        self.noeuds[index, 3] = z

    def set_element(self, index: int, element: list):
        self.elements[index] = element

    def get_triangulation(self):
        return Triangulation(self.noeuds[:, 0], self.noeuds[:, 1], self.elements)

    def get_node_count(self):
        return len(self.noeuds)

    def get_element_count(self):
        return len(self.elements)

    def get_noeuds_du_bord(self) -> set:
        return self.noeuds_du_bord

    def get_noeuds_du_bord_indexe(self) -> dict:

        noeuds_du_bord_indexe = {}
        noeuds_du_bord = self.get_noeuds_du_bord()

        index = 0

        for noeud in noeuds_du_bord:
            noeuds_du_bord_indexe[noeud] = index
            index += 1

        return noeuds_du_bord_indexe

    def calcul_determinant_triangle(self, triangle: list):

        triangle_nodes = self.noeuds[triangle]

        arete1 = triangle_nodes[1] - triangle_nodes[0]
        arete2 = triangle_nodes[2] - triangle_nodes[0]

        determinant = arete1[0] * arete2[1] - arete2[0] * arete1[1]
        return determinant

    def calcul_determinant_triangle_inverse(self, triangle: list):
        return 1 / self.calcul_determinant_triangle(triangle)

    def calcul_aire_triangle(self, triangle):
        return math.fabs(self.calcul_determinant_triangle(triangle) / 2)

    def calcul_h_triangle(self, triangle: list):

        triangle_nodes = self.noeuds[triangle]

        arete1 = triangle_nodes[1] - triangle_nodes[0]
        arete2 = triangle_nodes[2] - triangle_nodes[0]
        arete3 = triangle_nodes[2] - triangle_nodes[1]

        longueur1 = math.sqrt(arete1.dot(arete1)) 
        longueur2 = math.sqrt(arete2.dot(arete2)) 
        longueur3 = math.sqrt(arete3.dot(arete3)) 

        return max(longueur1, longueur2, longueur3)

    def calcul_h(self):

        h = 0

        for triangle in self.elements:
            h = max(h, self.calcul_h_triangle(triangle))

        return h

    def point_dans_triangle(self, index_triangle, x, y) -> bool:

        triangle = self.elements[index_triangle]
        triangle_nodes = self.noeuds[triangle]

        node1 = triangle_nodes[0]
        node2 = triangle_nodes[1]
        node3 = triangle_nodes[2]

        x23 = node2[0] - node3[0]
        x31 = node3[0] - node1[0]
        x12 = node1[0] - node2[0]
        y23 = node2[1] - node3[1]
        y31 = node3[1] - node1[1]
        y12 = node1[1] - node2[1]

        inverse_determinant = self.calcul_determinant_triangle_inverse(triangle)

        l1 = inverse_determinant * (y23 * (x - node3[0]) - x23 * (y - node3[1]))
        l2 = inverse_determinant * (y31 * (x - node1[0]) - x31 * (y - node1[1]))
        l3 = inverse_determinant * (y12 * (x - node2[0]) - x12 * (y - node2[1]))

        if l1 >= 0 and l1 <= 1 and l2 >= 0 and l2 <= 1 and l3 >= 0 and l3 <= 1:
            return True

    def calcul_longueur_arete(self, arete: list):
        noeud1 = self.noeuds[arete[0]]
        noeud2 = self.noeuds[arete[1]]
        droite = noeud1 - noeud2
        return math.sqrt(droite.dot(droite))

    def __eq__(self, other):
        if isinstance(other, Maillage):
            return np.array_equal(self.noeuds, other.noeuds) and np.array_equal(self.elements, other.elements)
        return False

    def __str__(self):
        return "noeuds :\n" + np.array_str(self.noeuds) + "\n" + \
               "elements :\n" + np.array_str(self.elements)
