import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import linalg
from .formulation_variationnelle import FormulationVariationnelle


class FormulationVariationnelleBloc(FormulationVariationnelle):

    def generer_matrice_bord(self):

        noeuds_du_bord_indexe = self.maillage.get_noeuds_du_bord_indexe()
        matrice = np.zeros((self.maillage.get_node_count(), len(noeuds_du_bord_indexe)), dtype=float)

        for arete in self.maillage.aretes_du_bord:

            longueur = self.maillage.calcul_longueur_arete(arete)
            longueur_sur_3 = longueur / 3
            longueur_sur_6 = longueur / 6
            noeud1 = arete[0]
            noeud2 = arete[1]

            noeud1_index = noeuds_du_bord_indexe[noeud1]
            noeud2_index = noeuds_du_bord_indexe[noeud2]

            matrice[noeud1][noeud1_index] += longueur_sur_3
            matrice[noeud2][noeud2_index] += longueur_sur_3

            matrice[noeud1][noeud2_index] = longueur_sur_6
            matrice[noeud2][noeud1_index] = longueur_sur_6

        return matrice

    def generer_second_membre_bord(self, matrice_bord, noeuds_bord: set, fonction_bord):

        second_membre = np.zeros(len(self.maillage.noeuds), dtype=float)

        # TODO - meilleure quadrature ?

        for index_noeud in noeuds_bord:
            noeud = self.maillage.noeuds[index_noeud]
            second_membre[index_noeud] = fonction_bord(noeud)

        # ca nous donne un vecteur de la bonne taille...
        second_membre = np.transpose(matrice_bord).dot(second_membre)

        return second_membre

    def generer_second_membre_bord_bloc(self, matrice_bord, fonction_bord):

        noeuds_bord = self.maillage.get_noeuds_du_bord()

        second_membre_bord =\
            self.generer_second_membre_bord(matrice_bord, noeuds_bord, fonction_bord)

        second_membre_bloc_bord = np.zeros(matrice_bord.shape[0] + second_membre_bord.shape[0])
        second_membre_bloc_bord[matrice_bord.shape[0]:] = second_membre_bord

        return second_membre_bloc_bord

    def generer_matrice_bloc(self, matrice_bord):

        matrice_rigidite = self.generer_matrice_rigidite()
        taille_matrice_rigidite = matrice_rigidite.shape[0]
        taille_matrice_bloc = matrice_rigidite.shape[0] +  matrice_bord.shape[1]

        matrice_rigidite_bloc_bord = np.zeros((taille_matrice_bloc, taille_matrice_bloc))

        matrice_rigidite_bloc_bord[0:taille_matrice_rigidite, 0:taille_matrice_rigidite] = matrice_rigidite
        matrice_rigidite_bloc_bord[0:matrice_bord.shape[0], taille_matrice_rigidite:] = matrice_bord
        matrice_rigidite_bloc_bord[taille_matrice_rigidite:, 0:matrice_bord.shape[0]] = matrice_bord.transpose()

        return matrice_rigidite_bloc_bord

    def resoudre_bloc(self, fonction_bord):

        matrice_bord = self.generer_matrice_bord()
        matrice_bloc = self.generer_matrice_bloc(matrice_bord)
        matrice_bloc_csr = csr_matrix(matrice_bloc)

        second_membre_bord_bloc = self.generer_second_membre_bord_bloc(matrice_bord, fonction_bord)

        solution = linalg.spsolve(matrice_bloc_csr, second_membre_bord_bloc)
        solution = solution[:self.maillage.get_node_count()]

        return solution

