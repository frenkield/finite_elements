import math
import unittest
import time
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import linalg
import matplotlib
import matplotlib.pyplot as plt

from maillage.FormulationVariationnelleCreuse import FormulationVariationnelleCreuse
from maillage.FormulationVariationnelle import FormulationVariationnelle
from maillage.GenerateurMaillageRectangulaire import GenerateurMaillage

from maillage.MoteurRenduMaillage import MoteurRenduMaillage

np.set_printoptions(threshold = np.inf)
np.set_printoptions(suppress = True, linewidth = np.nan, threshold = np.nan)

class TestFormulationVariationnelleCreuse(unittest.TestCase):

    def test_solution(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(30, 30, 1, 1)
        formulation_variationnelle_creuse = FormulationVariationnelleCreuse(maillage)

        constante = 5 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.cos(4 * math.pi * noeud[0]) * math.cos(2 * math.pi * noeud[1])

        solution = formulation_variationnelle_creuse.resoudre_neumann(fonction_second_membre)
        print(solution)



        # fonction = lambda noeud: math.cos(math.pi * noeud[0]) * math.cos(math.pi * noeud[1])
        # vraie_solution = np.array(list(map(fonction, maillage.nodes)))
        # print(vraie_solution)

        moteur_rendu = MoteurRenduMaillage()
        moteur_rendu.rendre_maillage_valeurs(maillage, solution)

        # moteur_rendu.rendre_maillage_valeurs(maillage, vraie_solution)

        # np.testing.assert_allclose(second_membre, [0.25, 0.16666667, 0.16666667, 0.41666667],
        #                            rtol=1e-5, atol=0)

    def test_solution_compare(self):

        generateur_maillage = GenerateurMaillage()
        maillage = generateur_maillage.generer_maillage(30, 30, 1, 1)

        constante = 5 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.cos(4 * math.pi * noeud[0]) * math.cos(2 * math.pi * noeud[1])

        formulation_variationnelle_creuse = FormulationVariationnelleCreuse(maillage)
        solution = formulation_variationnelle_creuse.resoudre_neumann(fonction_second_membre)

        formulation_variationnelle = FormulationVariationnelle(maillage)
        solution_dense = formulation_variationnelle.resoudre_neumann(fonction_second_membre)

        np.testing.assert_allclose(solution, solution_dense, rtol = 1e-10, atol = 0)


    def test_temps_solution(self, dirichlet = False):

        constante = 5 * (math.pi ** 2) + 1
        fonction_second_membre = lambda noeud: constante * math.cos(4 * math.pi * noeud[0]) * math.cos(2 * math.pi * noeud[1])
        generateur_maillage = GenerateurMaillage()

        taille = []
        temps = []

        for i in range(50, 90, 5):
        
            taille.append(i)
            
            maillage = generateur_maillage.generer_maillage(i, i, 1, 1)
            formulation_variationnelle = FormulationVariationnelle(maillage)

            matrice_masse = formulation_variationnelle.generer_matrice_masse()
            matrice_rigidite = formulation_variationnelle.generer_matrice_rigidite()
            matrice_dense = matrice_masse + matrice_rigidite
            second_membre = formulation_variationnelle.generer_second_membre(matrice_masse, fonction_second_membre)

            if dirichlet:
                formulation_variationnelle.appliquer_dirichlet_penalisation(matrice_dense, maillage.aretes_du_bord)

            matrice_csr = csr_matrix(matrice_dense)

            # ==================================================================

            start_time = time.time()
            np.linalg.solve(matrice_dense, second_membre)
            temps_dense_directe = time.time() - start_time

            # ==================================================================

            start_time = time.time()
            linalg.cg(matrice_dense, second_membre) #, atol=0.001)
            temps_dense_iterative = time.time() - start_time

            # ==================================================================

            start_time = time.time()
            linalg.spsolve(matrice_csr, second_membre)
            temps_creuse_directe = time.time() - start_time

            # ==================================================================

            start_time = time.time()
            linalg.cg(matrice_csr, second_membre) #, atol=0.001)
            temps_creuse_iterative = time.time() - start_time

            # ==================================================================

            temps.append([temps_dense_directe, temps_dense_iterative, temps_creuse_directe, temps_creuse_iterative])

            print("terminé iteration", len(taille))

        temps_np = np.array(temps)

        plt.plot(taille, temps_np[:, 0], label="Dense Directe")
        plt.plot(taille, temps_np[:, 1], label="Dense Iterative")
        plt.plot(taille, temps_np[:, 2], label="Creuse Directe")
        plt.plot(taille, temps_np[:, 3], label="Creuse Iterative")

        plt.legend()

        if dirichlet:
            plt.title("Temps Execution - Dirichlet")
        else:
            plt.title("Temps Execution - Neumann")

        # plt.xscale('log')
        # plt.yscale('log')
        
        plt.show()

    def test_temps_solution_dirichlet(self):
        self.test_temps_solution(True)

if __name__ == '__main__':
    unittest.main()
