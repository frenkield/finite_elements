import unittest
import numpy as np

from src.formulation_variationnelle.formulation_variationnelle_bloc import FormulationVariationnelleBloc
from src.maillage.generateur_maillage import GenerateurMaillage
from src.maillage.chargeur_maillage import ChargeurMaillage

from src.formulation_variationnelle.formulation_variationnelle_poisson import FormulationVariationnellePoisson

class TestFormulationVariationnelleBloc(unittest.TestCase):

    def test_generer_matrice_bord(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(5, 5, 1, 1)
        formulation_variationnelle = FormulationVariationnelleBloc(maillage)

        matrice_bord = formulation_variationnelle.generer_matrice_bord()
        assert(matrice_bord.shape == (25, 16))

        self.assertAlmostEqual(matrice_bord[0][0], 0.166, delta = 0.001)
        self.assertAlmostEqual(matrice_bord[10][9], 0.041, delta = 0.001)

    def test_generer_second_membre_bord(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(5, 5, 1, 1)
        formulation_variationnelle = FormulationVariationnelleBloc(maillage)

        matrice_bord = formulation_variationnelle.generer_matrice_bord()
        noeuds_bord = maillage.get_noeuds_du_bord()

        fonction = lambda noeud: noeud[0] + noeud[1]

        second_membre_bord =\
            formulation_variationnelle.generer_second_membre_bord(matrice_bord, noeuds_bord, fonction)

        second_membre_bord_correcte = [0.02083333, 0.0625, 0.125, 0.1875, 0.25, 0.0625, 0.3125,
                                       0.125, 0.375, 0.1875, 0.4375, 0.25, 0.3125, 0.375,
                                       0.4375, 0.47916667]

        np.testing.assert_allclose(second_membre_bord, second_membre_bord_correcte, rtol = 1e-5, atol = 0)

    def test_generer_second_membre_bord_bloc(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(5, 5, 1, 1)
        formulation_variationnelle = FormulationVariationnelleBloc(maillage)

        matrice_bord = formulation_variationnelle.generer_matrice_bord()

        fonction = lambda noeud: noeud[0] + noeud[1]

        second_membre_bord_bloc =\
            formulation_variationnelle.generer_second_membre_bord_bloc(matrice_bord, fonction)

        second_membre_bord_correcte = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                                       0, 0, 0, 0, 0, 0, 0,
                                       0.02083333, 0.0625, 0.125, 0.1875, 0.25, 0.0625, 0.3125,
                                       0.125, 0.375, 0.1875, 0.4375, 0.25, 0.3125, 0.375,
                                       0.4375, 0.47916667]

        np.testing.assert_allclose(second_membre_bord_bloc, second_membre_bord_correcte, rtol = 1e-5, atol = 0)

    def test_generer_matrice_bloc(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(4, 4, 1, 1)
        formulation_variationnelle = FormulationVariationnelleBloc(maillage)

        matrice_bord = formulation_variationnelle.generer_matrice_bord()
        matrice_bloc_rigidite_bord = formulation_variationnelle.generer_matrice_bloc(matrice_bord)

        assert(matrice_bloc_rigidite_bord.shape == (28, 28))

        self.assertAlmostEqual(matrice_bloc_rigidite_bord[0][0], 1, delta = 0.001)
        self.assertAlmostEqual(matrice_bloc_rigidite_bord[0][16], 0.222, delta = 0.001)
        self.assertAlmostEqual(matrice_bloc_rigidite_bord[21][11], 0.055, delta = 0.001)

    def test_resoudre_bloc(self):

        # filename = "data/maillages/test/maillage_tipi.txt"
        filename = "data/maillages/maillage3_2.txt"
        chargeur_maillage = ChargeurMaillage()
        maillage = chargeur_maillage.charger_maillage(filename, True)

        fonction_g = lambda sommet: (sommet[0] ** 2 + sommet[1] ** 2) / 2
        fonction_laplacien_g = lambda sommet: 2

        # =================================================================

        formulation_variationnelle = FormulationVariationnellePoisson(maillage)
        u_tilde = formulation_variationnelle.resoudre_dirichlet(fonction_laplacien_g)
        g = np.array(list(map(fonction_g, maillage.noeuds)))
        u = u_tilde + g

        # moteur_rendu = MoteurRenduMaillage()
        # moteur_rendu.rendre_maillage_valeurs_3d(maillage, u)

        # ==============================================================

        formulation_variationnelle_bloc = FormulationVariationnelleBloc(maillage)
        solution_bloc = formulation_variationnelle_bloc.resoudre_bloc(fonction_g)

        # moteur_rendu = MoteurRenduMaillage()
        # moteur_rendu.rendre_maillage_valeurs_3d(maillage, solution_bloc)

        np.testing.assert_allclose(solution_bloc, u, rtol = 0.01, atol = 0)

if __name__ == '__main__':
    unittest.main()
