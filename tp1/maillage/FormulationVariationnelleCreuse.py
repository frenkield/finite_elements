import sys
import time
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse import linalg

from maillage.MaillageTriangulaire import MaillageTriangulaire
from maillage.FormulationVariationnelle import FormulationVariationnelle


class FormulationVariationnelleCreuse(FormulationVariationnelle):

    def resoudre_neumann(self, fonction_second_membre):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()
        matrice = self.matrice_masse + self.matrice_rigidite

        matrice_csr = csr_matrix(matrice) 
        
        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)
        return linalg.spsolve(matrice_csr, second_membre)

    def evaluer_performance_neumann(self, fonction_second_membre):

        self.matrice_masse = self.generer_matrice_masse()
        self.matrice_rigidite = self.generer_matrice_rigidite()

        matrice = self.matrice_masse + self.matrice_rigidite
        matrice_csr = csr_matrix(matrice) 
        

        second_membre = self.generer_second_membre(self.matrice_masse, fonction_second_membre)


        start_time = time.time()
        solution = np.linalg.solve(matrice, second_membre)
        temps = time.time() - start_time

        start_time = time.time()
        solution_csr = linalg.spsolve(matrice_csr, second_membre)
        temps_csr = time.time() - start_time




        print(temps - temps_csr)
