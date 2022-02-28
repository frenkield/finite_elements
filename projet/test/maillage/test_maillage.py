import unittest
import numpy as np

from src.maillage.generateur_maillage import GenerateurMaillage

# np.set_printoptions(threshold = np.inf)
# np.set_printoptions(suppress = True, linewidth = np.nan, threshold = np.nan)

class TestMaillage(unittest.TestCase):

    def test_generer_maillage(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        triangle = maillage.elements[0]
        self.assertEqual(maillage.calcul_determinant_triangle(triangle), 1)

    def test_calcul_determinant_triangle(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(4, 4, 18, 18)
        triangle = maillage.elements[0]
        self.assertEqual(maillage.calcul_determinant_triangle(triangle), 36)

    def test_calcul_determinant_triangle_enfer(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        self.assertEqual(maillage.calcul_determinant_triangle(np.array([0, 1, 2])), 1)
        self.assertEqual(maillage.calcul_determinant_triangle(np.array([2, 0, 1])), 1)
        self.assertEqual(maillage.calcul_determinant_triangle(np.array([1, 2, 0])), 1)
        self.assertEqual(maillage.calcul_determinant_triangle(np.array([0, 2, 1])), -1)

    def test_aretes_du_bord(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)
        aretes = maillage.aretes_du_bord
        aretes_corrects = [[0, 1], [0, 3], [1, 2], [2, 5], [3, 6], [6, 7], [5, 8], [7, 8]]
        self.assertEqual(aretes, aretes_corrects)

    def test_calcul_longueur_arete(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(9, 9, 1, 1)
        aretes = maillage.aretes_du_bord

        longueur = maillage.calcul_longueur_arete(aretes[0])
        self.assertEqual(longueur, 0.125)

    def test_get_noeuds_bord(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)
        noeuds = maillage.get_noeuds_du_bord()

        noeuds_corrects = {0, 1, 2, 3, 5, 6, 7, 8}
        self.assertEqual(noeuds, noeuds_corrects)

    def test_get_noeuds_bord_indexe(self):
        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(3, 3, 1, 1)
        noeuds = maillage.get_noeuds_du_bord_indexe()

        noeuds_corrects = {0: 0, 1: 1, 2: 2, 3: 3, 5: 4, 6: 5, 7: 6, 8: 7}
        self.assertEqual(noeuds, noeuds_corrects)

if __name__ == '__main__':
    unittest.main()
