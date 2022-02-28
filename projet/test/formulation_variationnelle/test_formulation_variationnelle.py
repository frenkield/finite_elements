import math
import unittest
import numpy as np

from src.formulation_variationnelle.formulation_variationnelle import FormulationVariationnelle
from src.maillage.generateur_maillage import GenerateurMaillage

class TestFormulationVariationnelle(unittest.TestCase):

    def test_generer_matrice_masse_elementaire1(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        triangle = np.array([0, 1, 2])

        matrice_masse_elementaire = formulation_variationnelle.generer_matrice_masse_elementaire(triangle)

        reference = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]])
        reference = reference / 24

        self.assertEqual(matrice_masse_elementaire.tolist(),
                         reference.tolist())

        vecteur_test = np.ones(3)
        aire_totale = vecteur_test.dot(matrice_masse_elementaire.dot(vecteur_test))
        self.assertEqual(aire_totale, 0.5)

    def test_generer_matrice_masse_elementaire2(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(4, 4, 18, 18)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        triangle = maillage.elements[0]

        matrice_masse = formulation_variationnelle.generer_matrice_masse_elementaire(triangle)

        reference = np.array([[3, 1.5, 1.5], [1.5, 3, 1.5], [1.5, 1.5, 3]])
        self.assertEqual(matrice_masse.tolist(), reference.tolist())

        vecteur_test = np.ones(3)
        aire_totale = vecteur_test.dot(matrice_masse.dot(vecteur_test))
        self.assertEqual(aire_totale, 18)

    def test_generer_matrice_masse1(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)
        matrice_masse = formulation_variationnelle.generer_matrice_masse()

        vecteur_test = np.array([1, 1, 1, 1])
        aire_totale = vecteur_test.dot(matrice_masse.dot(vecteur_test))
        self.assertEqual(aire_totale, 1)

    def test_generer_matrice_masse2(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(4, 4, 18, 18)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()

        vecteur_test = np.ones(16)
        aire_totale = vecteur_test.dot(matrice_masse.dot(vecteur_test))
        self.assertEqual(aire_totale, 324)

    def test_generer_matrice_rigidite_elementaire1(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        triangle = np.array([0, 1, 2])

        matrice_rigidite_elementaire = formulation_variationnelle.generer_matrice_rigidite_elementaire(triangle)

        solution = np.array([[2, -1, -1], [-1, 1, 0], [-1, 0, 1]]) / 2
        self.assertEqual(solution.tolist(), matrice_rigidite_elementaire.tolist())

        vecteur_test = np.ones(3)
        produit_matrice_vecteur = matrice_rigidite_elementaire.dot(vecteur_test)
        self.assertEqual(produit_matrice_vecteur.dot(produit_matrice_vecteur), 0)

    def test_generer_matrice_rigidite_elementaire2(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        triangle = maillage.elements[0]
        matrice_rigidite_elementaire = formulation_variationnelle.generer_matrice_rigidite_elementaire(triangle)
        vecteur_test = np.ones(3)
        produit_matrice_vecteur = matrice_rigidite_elementaire.dot(vecteur_test)
        self.assertEqual(produit_matrice_vecteur.dot(produit_matrice_vecteur), 0)

        triangle = maillage.elements[1]
        matrice_rigidite_elementaire = formulation_variationnelle.generer_matrice_rigidite_elementaire(triangle)
        vecteur_test = np.ones(3)
        produit_matrice_vecteur = matrice_rigidite_elementaire.dot(vecteur_test)
        self.assertEqual(produit_matrice_vecteur.dot(produit_matrice_vecteur), 0)

    def test_generer_matrice_rigidite1(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()

        vecteur_test = np.ones(4)
        produit_matrice_vecteur = matrice_rigidite.dot(vecteur_test)
        self.assertEqual(produit_matrice_vecteur.dot(produit_matrice_vecteur), 0)

    def test_generer_matrice_rigidite2(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(8, 11, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()

        vecteur_test = np.ones(8 * 11)
        produit_matrice_vecteur = matrice_rigidite.dot(vecteur_test)
        self.assertAlmostEqual(produit_matrice_vecteur.dot(produit_matrice_vecteur), 0)

    def test_generer_second_membre(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(2, 2, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()

        fonction = lambda noeud: noeud[0] + noeud[1]
        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction)

        np.testing.assert_allclose(second_membre, [0.25, 0.16666667, 0.16666667, 0.41666667],
                                   rtol = 1e-5, atol = 0)

    def test_solution(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(20, 20, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()
        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()
        matrice = matrice_masse + matrice_rigidite

        constante = 2* (math.pi ** 2) + 1
        fonction_second_membre =\
            lambda noeud: constante * math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])

        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction_second_membre)
        solution = np.linalg.solve(matrice, second_membre)

        fonction = lambda noeud: math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])
        vraie_solution = np.array(list(map(fonction, maillage.noeuds)))

        erreur = vraie_solution - solution
        assert(erreur.dot(erreur) < 0.15)

if __name__ == '__main__':
    unittest.main()
