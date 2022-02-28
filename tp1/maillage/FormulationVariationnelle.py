import sys

import numpy as np

from maillage.MaillageTriangulaire import MaillageTriangulaire


class FormulationVariationnelle:

    def __init__(self, maillage: MaillageTriangulaire):
        self.maillage = maillage

    # TODO - pas super efficace si on crée une nouvelle (petite) matrice à chaque fois
    def generer_matrice_masse_elementaire(self, triangle):
        determinant = self.maillage.calcul_determinant_triangle(triangle)
        matrice = np.array([[2, 1, 1], [1, 2, 1], [1, 1, 2]], dtype=float)
        matrice = matrice * determinant / 24
        return matrice

    def generer_matrice_masse(self):

        matrice = np.zeros((self.maillage.get_node_count(), self.maillage.get_node_count()), dtype=float)

        for triangle in self.maillage.elements:

            matrice_elementaire = self.generer_matrice_masse_elementaire(triangle)

            for i in range(0, 3):

                noeud_i = triangle[i]
                matrice[noeud_i][noeud_i] += matrice_elementaire[i][i]

                for j in range(i + 1, 3):
                    noeud_j = triangle[j]
                    matrice[noeud_i][noeud_j] += matrice_elementaire[i][j]
                    matrice[noeud_j][noeud_i] += matrice_elementaire[j][i]

        return matrice

    # TODO - pas super efficace si on crée une nouvelle (petite) matrice à chaque fois
    def generer_matrice_rigidite_elementaire(self, triangle):

        matrice = np.zeros((3, 3), dtype=float)
        noeuds_triangle = self.maillage.noeuds[triangle]

        noeud1 = noeuds_triangle[0]
        noeud2 = noeuds_triangle[1]
        noeud3 = noeuds_triangle[2]

        matrice[0][0] = (noeud2 - noeud3).dot(noeud2 - noeud3)
        matrice[1][1] = (noeud3 - noeud1).dot(noeud3 - noeud1)
        matrice[2][2] = (noeud1 - noeud2).dot(noeud1 - noeud2)

        matrice[0][1] = matrice[1][0] = (noeud2 - noeud3).dot(noeud3 - noeud1)
        matrice[0][2] = matrice[2][0] = (noeud2 - noeud3).dot(noeud1 - noeud2)
        matrice[1][2] = matrice[2][1] = (noeud3 - noeud1).dot(noeud1 - noeud2)

        matrice /= (2 * self.maillage.calcul_determinant_triangle(triangle))

        return matrice

    def generer_matrice_rigidite(self):

        matrice = np.zeros((self.maillage.get_node_count(), self.maillage.get_node_count()), dtype=float)

        for triangle in self.maillage.elements:

            elementaire = self.generer_matrice_rigidite_elementaire(triangle)

            for i in range(0, 3):
                matrice[triangle[i]][triangle[i]] += elementaire[i][i]

                for j in range(i + 1, 3):
                    matrice[triangle[i]][triangle[j]] += elementaire[i][j]
                    matrice[triangle[j]][triangle[i]] = matrice[triangle[i]][triangle[j]]

        return matrice

    def generer_second_membre(self, matrice_masse, fonction):

        second_membre = np.array(list(map(fonction, self.maillage.noeuds)))
        second_membre = matrice_masse.dot(second_membre)

        return second_membre

    def resoudre_neumann(self, fonction_second_membre):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()
        matrice = self.matrice_masse + self.matrice_rigidite

        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)
        return np.linalg.solve(matrice, second_membre)

    def appliquer_dirichlet_elimination(self, matrice, second_membre, noeuds_bord):
        
        for noeud in noeuds_bord:
            
            for i in range(0, matrice.shape[0]):
                matrice[noeud][i] = 0
                matrice[i][noeud] = 0

            matrice[noeud][noeud] = 1
            second_membre[noeud] = 0
        

    def appliquer_dirichlet_penalisation(self, matrice, aretes_du_bord):
        
        for arete in aretes_du_bord:
            matrice[arete[0]][arete[0]] = 10**30 # sys.float_info.max
            matrice[arete[1]][arete[1]] = 10**30 # sys.float_info.max

    def resoudre_dirichlet(self, fonction_second_membre):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()
        matrice = self.matrice_masse + self.matrice_rigidite

        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)

        self.appliquer_dirichlet_penalisation(matrice, self.maillage.aretes_du_bord)
        return np.linalg.solve(matrice, second_membre)
