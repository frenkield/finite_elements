import math
import unittest
import numpy as np
import matplotlib.pyplot as plt

from maillage.ChargeurMaillageGmsh import ChargeurMaillageGmsh
from maillage.FormulationVariationnelle import FormulationVariationnelle
from maillage.GenerateurMaillageRectangulaire import GenerateurMaillage
from maillage.MoteurRenduMaillage import MoteurRenduMaillage

np.set_printoptions(threshold = np.inf)
np.set_printoptions(suppress = True, linewidth = np.nan, threshold = np.nan)

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

        # fonction = lambda sommet: math.cos(sommet[0]) * math.cos(sommet[1])
        # fonction = lambda i, j: i + j

        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction)

        # print(second_membre)

        np.testing.assert_allclose(second_membre, [0.25, 0.16666667, 0.16666667, 0.41666667],
                                   rtol = 1e-5, atol = 0)

    def test_solution(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(30, 30, 1, 1)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()
        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()
        matrice = matrice_masse + matrice_rigidite

        constante = 5 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.cos(4 * math.pi * noeud[0]) * math.cos(2 * math.pi * noeud[1])

        #fonction_second_membre = lambda noeud: -1
        # fonction_second_membre = lambda noeud: (3 + noeud[0]) * noeud[1]

        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction_second_membre)
        solution = np.linalg.solve(matrice, second_membre)
        # print(solution)

        # fonction = lambda noeud: math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])
        # vraie_solution = np.array(list(map(fonction, maillage.nodes)))
        # print(vraie_solution)

        moteur_rendu = MoteurRenduMaillage()
        moteur_rendu.rendre_maillage_valeurs_3d(maillage, solution)

        # moteur_rendu.rendre_maillage_valeurs(maillage, vraie_solution)

        # np.testing.assert_allclose(second_membre, [0.25, 0.16666667, 0.16666667, 0.41666667],
        #                            rtol=1e-5, atol=0)

    def test_erreur_solution(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(100, 100, 2, 2)
        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()
        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()
        matrice = matrice_masse + matrice_rigidite

        constante = 2 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])

        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction_second_membre)
        solution = np.linalg.solve(matrice, second_membre)

        fonction_solution = lambda noeud: math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])
        vraie_solution = np.array(list(map(fonction_solution, maillage.noeuds)))
        # print(vraie_solution)

        erreur = vraie_solution - solution

        print(erreur)

        # moteur_rendu = MoteurRenduMaillage()
#        moteur_rendu.rendre_maillage_valeurs_3d(maillage, erreur)

        # moteur_rendu.rendre_maillage_valeurs(maillage, vraie_solution)

        # np.testing.assert_allclose(second_membre, [0.25, 0.16666667, 0.16666667, 0.41666667],
        #                            rtol=1e-5, atol=0)

    def test_appliquer_dirichlet(self):

        # generateur_maillage = GenerateurMaillage()
        # maillage = generateur_maillage.generer_maillage(20, 20, 1, 1)

        chargeur_maillage = ChargeurMaillageGmsh()
        maillage = chargeur_maillage.charger_maillage("../data/maillages/square1.msh")

        formulation_variationnelle = FormulationVariationnelle(maillage)

        matrice_masse = formulation_variationnelle.generer_matrice_masse()
        matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()
        matrice = matrice_masse + matrice_rigidite

        constante = 2 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])
        second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction_second_membre)

        formulation_variationnelle.appliquer_dirichlet_penalisation(matrice, maillage.aretes_du_bord)
        solution = np.linalg.solve(matrice, second_membre)

        fonction_solution = lambda noeud: math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])
        vraie_solution = np.array(list(map(fonction_solution, maillage.noeuds)))

        erreur = vraie_solution - solution

        moteur_rendu = MoteurRenduMaillage()
        moteur_rendu.rendre_maillage_valeurs_3d(maillage, solution)




    def test_erreur_foire(self, dirichlet = False):

        generateur_maillage = GenerateurMaillage()
        h = []
        erreurs_h1_semi = []
        erreurs_l2 = []
        erreurs_h1 = []
        tailles = []

        for taille in range(4, 10, 1):

            tailles.append(taille)
            
            maillage = generateur_maillage.generer_maillage(taille, taille, 1, 1)
            formulation_variationnelle = FormulationVariationnelle(maillage)

            constante = 2 * (math.pi ** 2) + 1
            fonction_second_membre = lambda noeud: constante * math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])

            if dirichlet:
                solution = formulation_variationnelle.resoudre_dirichlet(fonction_second_membre)
            else:
                solution = formulation_variationnelle.resoudre_neumann(fonction_second_membre)

            # ====================================================

            fonction_vraie_solution = lambda noeud: math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])
            vraie_solution = np.array(list(map(fonction_vraie_solution, maillage.noeuds)))

            erreur = vraie_solution - solution

            erreur_h1_semi_carree = formulation_variationnelle.matrice_rigidite.dot(erreur).dot(erreur)
            erreur_h1_semi = math.sqrt(erreur_h1_semi_carree)

            erreur_l2_carree = formulation_variationnelle.matrice_masse.dot(erreur).dot(erreur)
            erreur_l2 = math.sqrt(erreur_l2_carree)

            erreur_h1 = math.sqrt(erreur_l2_carree + erreur_h1_semi_carree)

            # h.append(math.log(1 / (taille - 1)))
            # erreurs_h1_semi.append(math.log(erreur_h1_semi))
            # erreurs_l2.append(math.log(erreur_l2))

            h.append(1 / (taille - 1))
            erreurs_h1_semi.append(erreur_h1_semi)
            erreurs_l2.append(erreur_l2)
            erreurs_h1.append(erreur_h1)

        # print(erreurs_l2)
        # print(erreurs_h1_semi)
        # print(erreurs_h1)

        index_dernier_erreur = len(h) - 1
        pente = (math.log(erreurs_h1[index_dernier_erreur]) - math.log(erreurs_h1[0])) /  \
                (math.log(h[index_dernier_erreur]) - math.log(h[0]))

        fig, ax = plt.subplots()
        
        ax.plot(tailles, erreurs_h1_semi, label="H1 Semi")
        ax.plot(tailles, erreurs_l2, label="L2")
         # ax.plot(h, erreurs_h1, label="H1", color="red")
        
        plt.legend()
#        plt.xscale('log')
#        plt.yscale('log')
        
        #ax.text(0.252, 0.8, 'pente = %f' % pente, fontsize=15)
        
        #ax.axis('tight')
        
        #plt.annotate('pente = %f' % pente, xy=(0.5, 0.5), xycoords='axes fraction')
        
        plt.show()













    def test_erreur(self):

        constante = 2 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])
        fonction_solution_exacte = lambda noeud: math.sin(math.pi * noeud[0]) * math.sin(math.pi * noeud[1])

        chargeur_maillage = ChargeurMaillageGmsh()
        h = []
        erreurs_h1_semi = []
        erreurs_l2 = []

        fichiers_maillage = ["data/maillages/square1.msh", "data/maillages/square2.msh", "data/maillages/square3.msh"]

        for fichier_maillage in fichiers_maillage:

            maillage = chargeur_maillage.charger_maillage(fichier_maillage)
            
            taille = math.sqrt(maillage.get_node_count())
            print("taille", taille)

            h.append(1 / (taille - 1))

            formulation_variationnelle = FormulationVariationnelle(maillage)

            solution = formulation_variationnelle.resoudre_dirichlet(fonction_second_membre)
            vraie_solution = np.array(list(map(fonction_solution_exacte, maillage.noeuds)))
            erreur = vraie_solution - solution

            # moteur_rendu = MoteurRenduMaillage()
            # moteur_rendu.rendre_maillage_valeurs_3d(maillage, erreur)

            erreur_h1_semi_carree = formulation_variationnelle.matrice_rigidite.dot(erreur).dot(erreur)
            erreur_h1_semi = math.sqrt(erreur_h1_semi_carree)
            erreurs_h1_semi.append(erreur_h1_semi)

            erreur_l2_carree = formulation_variationnelle.matrice_masse.dot(erreur).dot(erreur)
            erreur_l2 = math.sqrt(erreur_l2_carree)
            erreurs_l2.append(erreur_l2)


        index_dernier_erreur = len(h) - 1
        pente = (math.log(erreurs_h1_semi[index_dernier_erreur]) - math.log(erreurs_h1_semi[0])) /  \
                (math.log(h[index_dernier_erreur]) - math.log(h[0]))
        print(pente)

#        fig, ax = plt.subplots()

        plt.plot(h, erreurs_h1_semi, label="H1 Semi")
        plt.plot(h, erreurs_l2, label="L2")

        plt.legend()

#        ax.axis('tight')
#        plt.xscale('log')
#        plt.yscale('log')

#        plt.gca().set_xlim(0.0, 0.05)
#        plt.gca().set_ylim(0.0, 0.05)

#        plt.annotate('pente = %f' % pente, xy=(0.2, 0.4), xycoords='axes fraction')

        plt.show()










    def test_erreur_dirichlet(self):
        self.test_erreur(True)


if __name__ == '__main__':
    unittest.main()
