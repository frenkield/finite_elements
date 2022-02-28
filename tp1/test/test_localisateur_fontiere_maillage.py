import unittest

import numpy as np

from maillage.GenerateurMaillageRectangulaire import GenerateurMaillage
from maillage.LocalisateurFrontiereMaillage import LocalisateurFrontiereMaillage

np.set_printoptions(threshold = np.inf)
np.set_printoptions(suppress = True, linewidth = np.nan, threshold = np.nan)

class TestLocalisateurFrontiereMaillage(unittest.TestCase):

    def test_trouver_aretes(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)

        localisateur = LocalisateurFrontiereMaillage(maillage)
        aretes = localisateur.trouver_aretes()

        print(aretes)

        aretes_corrects = [[0, 1], [0, 4], [1, 4], [0, 3], [0, 4], [3, 4], [1, 2], [1, 5],
                           [2, 5], [1, 4], [1, 5], [4, 5], [3, 4], [3, 7], [4, 7], [3, 6],
                           [3, 7], [6, 7], [4, 5], [4, 8], [5, 8], [4, 7], [4, 8], [7, 8]]

        self.assertEqual(aretes, aretes_corrects)

    def test_trouver_aretes_avec_type(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)

        localisateur = LocalisateurFrontiereMaillage(maillage)
        aretes = localisateur.trouver_aretes_avec_type()


        print(aretes)

        aretes_corrects = [[0, 1, False], [0, 3, False], [1, 2, False], [0, 4, False], [0, 4, True],
                           [3, 4, False], [1, 4, False], [1, 4, True], [2, 5, False], [1, 5, False],
                           [1, 5, True], [4, 5, False], [3, 4, True], [3, 6, False], [4, 5, True],
                           [3, 7, False], [3, 7, True], [6, 7, False], [4, 7, False], [4, 7, True],
                           [5, 8, False], [4, 8, False], [4, 8, True], [7, 8, False]]

        # self.assertEqual(aretes, aretes_corrects)


    def test_trouver_aretes_du_bord(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)

        # m = MoteurRenduMaillage()
        # m.rendre_maillage(maillage)

        localisateur = LocalisateurFrontiereMaillage(maillage)
        aretes = localisateur.trouver_aretes_du_bord()

        aretes_corrects = [[0, 1], [0, 3], [1, 2], [2, 5], [3, 6], [6, 7], [5, 8], [7, 8]]
        self.assertEqual(aretes, aretes_corrects)


if __name__ == '__main__':
    unittest.main()
