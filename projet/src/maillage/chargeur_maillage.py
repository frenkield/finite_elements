import logging

import numpy

from .maillage import Maillage
from .localisateur_frontiere_maillage import LocalisateurFrontiereMaillage


NODE_COUNT_LINE = "#Nombre de noeuds"
NODES_START_LINE = "#Coordonnees des noeuds"
TRIANGLE_COUNT_LINE = "#Nombre de triangles"
TRIANGLES_START_LINE = "#Numeros des sommets de chaque triangle"

class ChargeurMaillage:

    def advance_to_line(self, file, line_text: str) -> bool:

        while True:

            line = file.readline().strip()

            if not line:
                continue

            if line == line_text:
                return True

        return False

    def read_nodes(self, file, node_count) -> numpy.array:

        logging.debug("node count = %d", node_count)

        nodes = numpy.zeros((node_count, 3), dtype=float)
        index = 0

        while index < node_count:

            node_text = file.readline().strip()

            if not node_text:
                continue

            node_data = node_text.split()

            x = float(node_data[0])
            y = float(node_data[1])
            z = float(node_data[2])

            nodes[index, 0] = x
            nodes[index, 1] = y
            nodes[index, 2] = z

            index += 1

        return nodes

    def read_elements(self, file, triangle_count) -> numpy.array:

        logging.debug("element count = %d", triangle_count)

        elements = numpy.zeros((triangle_count, 3), dtype=int)
        index = 0

        while index < triangle_count:

            element_text = file.readline().strip()

            if not element_text:
                continue

            element_data = element_text.split()

            node1 = int(element_data[0])
            node2 = int(element_data[1])
            node3 = int(element_data[2])

            elements[index, 0] = node1
            elements[index, 1] = node2
            elements[index, 2] = node3

            index += 1

        return elements

    def extraire_neouds_du_bord(self, aretes_du_bord) -> set:

        noeuds_du_bord = set()

        for arete in aretes_du_bord:
            noeuds_du_bord.add(arete[0])
            noeuds_du_bord.add(arete[1])

        return noeuds_du_bord

    def charger_maillage(self, filename, extraire_aretes_du_bord = False) -> Maillage:

        with open(filename) as donneesMaillage:

            found_node_count = self.advance_to_line(donneesMaillage, NODE_COUNT_LINE)
            assert found_node_count, "compte des neouds pas trouver dans %s" % (filename)
            node_count = int(donneesMaillage.readline())

            self.advance_to_line(donneesMaillage, NODES_START_LINE)
            nodes = self.read_nodes(donneesMaillage, node_count)

            self.advance_to_line(donneesMaillage, TRIANGLE_COUNT_LINE)
            triangle_count = int(donneesMaillage.readline())

            self.advance_to_line(donneesMaillage, TRIANGLES_START_LINE)
            triangles = self.read_elements(donneesMaillage, triangle_count)

            maillage = Maillage(nodes, triangles)

            if extraire_aretes_du_bord:
                localisateur = LocalisateurFrontiereMaillage(maillage)
                aretes_du_bord = localisateur.trouver_aretes_du_bord()
                maillage.aretes_du_bord = aretes_du_bord
                maillage.noeuds_du_bord = self.extraire_neouds_du_bord(maillage.aretes_du_bord)

            return maillage
