import logging

from maillage.MaillageTriangulaire import MaillageTriangulaire

NODES_LINE = "$Noeuds"
NODES_END_LINE = "$FinNoeuds"
ELEMENTS_LINE = "$Elements"
ELEMENTS_END_LINE = "$FinElements"


class SauvegardeurMaillage:

    def sauvegarder_maillage(self, maillage: MaillageTriangulaire, filename: str):

        logging.debug("sauvegarder maillage dans %s", filename)

        with open(filename, "w") as fichier_maillage:

            fichier_maillage.write(NODES_LINE + "\n")
            fichier_maillage.write("{}\n".format((maillage.get_node_count())))

            for index, node in enumerate(maillage.noeuds):
                fichier_maillage.write("{} {} {} {}\n".format(index, node[0], node[1], node[2]))

            fichier_maillage.write(NODES_END_LINE + "\n")

            fichier_maillage.write(ELEMENTS_LINE + "\n")
            fichier_maillage.write("{}\n".format((maillage.get_element_count())))

            for index, element in enumerate(maillage.elements):
                fichier_maillage.write("{} {} {} {}\n".format(index, element[0], element[1], element[2]))

            fichier_maillage.write(ELEMENTS_END_LINE + "\n")
