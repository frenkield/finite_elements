import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import linalg
from .formulation_variationnelle import FormulationVariationnelle


class FormulationVariationnellePoisson(FormulationVariationnelle):

    def resoudre_neumann(self, fonction_second_membre):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()

        # juste rigidté pour poisson
        matrice = self.matrice_rigidite

        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)

        matrice_csr = csr_matrix(matrice)
        return linalg.spsolve(matrice_csr, second_membre)

    def resoudre_dirichlet(self, fonction_second_membre, avec_penalisation = False):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()

        # juste rigidté pour poisson
        matrice = self.matrice_rigidite

        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)

        if avec_penalisation:
            self.appliquer_dirichlet_penalisation(matrice, self.maillage.aretes_du_bord)

        else:
            self.appliquer_dirichlet_elimination(matrice, second_membre, self.maillage.aretes_du_bord)

        matrice_csr = csr_matrix(matrice)
        return linalg.spsolve(matrice_csr, second_membre)

    def resoudre_disque_dirichlet_exacte(self):

        fonction_solution = lambda sommet: (1 - sommet[0]**2 - sommet[1]**2) / 4
        solution_exacte = np.array(list(map(fonction_solution, self.maillage.noeuds)))

        return solution_exacte
