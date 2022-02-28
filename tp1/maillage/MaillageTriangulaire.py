from matplotlib.tri import Triangulation
import numpy as np


class MaillageTriangulaire:

    def __init__(self, nodes: np.array, elements: np.array):
        self.noeuds = nodes
        self.elements = elements
        self.aretes_du_bord = []

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

    def calcul_determinant_triangle(self, triangle: list):

        triangle_nodes = self.noeuds[triangle]

        arete1 = triangle_nodes[1] - triangle_nodes[0]
        arete2 = triangle_nodes[2] - triangle_nodes[0]

        determinant = arete1[0] * arete2[1] - arete2[0] * arete1[1]
        return determinant

    def calcul_determinant_triangle_inverse(self, triangle: list):
        return 1 / self.calcul_determinant_triangle(triangle)

    def calcul_aire_triangle(self, triangle):
        return self.calcul_determinant_triangle(triangle) / 2

    def point_dans_triangle(self, index_triangle, x, y) -> bool:

        triangle = self.elements[index_triangle];
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

    def __eq__(self, other):
        if isinstance(other, MaillageTriangulaire):
            return np.array_equal(self.noeuds, other.noeuds) and np.array_equal(self.elements, other.elements)
        return False

    def __str__(self):
        return "noeuds :\n" + np.array_str(self.noeuds) + "\n" + \
               "elements :\n" + np.array_str(self.elements)
