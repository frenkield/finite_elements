import unittest

import numpy as np
import math

from maillage.ChargeurMaillageGmsh import ChargeurMaillageGmsh
from maillage.MoteurRenduMaillage import MoteurRenduMaillage

np.set_printoptions(threshold = np.inf)
np.set_printoptions(suppress = True, linewidth = np.nan, threshold = np.nan)

class TestChargeurMaillageGmsh(unittest.TestCase):

    def test_charger_maillage1(self):
        chargeur_maillage = ChargeurMaillageGmsh()
        maillage = chargeur_maillage.charger_maillage("../data/maillages/maillage_trou_elliptique.msh")
        self.assertEqual(maillage.get_node_count(), 937)

    def test_charger_maillage2(self):
        chargeur_maillage = ChargeurMaillageGmsh()
        maillage = chargeur_maillage.charger_maillage("../data/maillages/square1.msh")
        self.assertEqual(maillage.get_node_count(), 371)
        self.assertEqual(maillage.get_element_count(), 676)

    def test_charger_maillage3(self):
        chargeur_maillage = ChargeurMaillageGmsh()
        maillage = chargeur_maillage.charger_maillage("../data/maillages/square3.msh")
        # self.assertEqual(maillage.get_node_count(), 371)
        # self.assertEqual(maillage.get_element_count(), 676)

        moteur_rendu = MoteurRenduMaillage()
        # moteur_rendu.rendre_maillage(maillage)

        fonction_coleur1 = lambda node: math.cos(math.pi * node[0]) * math.cos(math.pi * node[1])
        # moteur_rendu.rendre_maillage_fonction(maillage, fonction_coleur1)

        moteur_rendu.rendre_frontiere(maillage)







# fonction_coleur1 = lambda node: math.cos((node[0] - 25) / 25 * math.pi) * math.cos((node[1] - 25) / 25 * math.pi)


# chargeur_maillage = ChargeurMaillage()
# maillage_charge = chargeur_maillage.charger_maillage(GROS_MAILLAGE)
#
# sauvegardeur_maillage = SauvegardeurMaillage()
# sauvegardeur_maillage.sauvegarder_maillage(maillage_genere, "test/test1.msh")

# assert(maillage_genere == maillage_charge)

# print("maillage généré:\n", maillage_genere)
# print("maillage:\n", maillage_charge)

# fonction_coleur1 = lambda node: math.cos((node[0] - 25) / 25 * math.pi) * math.cos((node[1] - 25) / 25 * math.pi)
# fonction_coleur2 = lambda node: math.erf(node[0] / longeur) * math.erf(node[1] / hauteur)
#
#
# MAX_ITERATIONS = 50
#
# def fonction_coleur3(node):
#     z = complex(node[0] / longeur * 2.5 - 2, node[1] / hauteur * 2.5 - 1.25)
#     c = z
#     for n in range(MAX_ITERATIONS):
#         if abs(z) > 2:
#             return n
#         z = z * z + c
#     return MAX_ITERATIONS * -1
#




if __name__ == '__main__':
    unittest.main()
