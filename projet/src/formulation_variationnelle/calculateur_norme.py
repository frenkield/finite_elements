import math

class CalculateurNorme:

    def calcul_h1_semi(self, matrice_rigidite, solution):
        h1_semi_carree = matrice_rigidite.dot(solution).dot(solution)
        return math.sqrt(math.fabs(h1_semi_carree))

    def calcul_l2(self, matrice_masse, solution):
        l2_carree = matrice_masse.dot(solution).dot(solution)
        return math.sqrt(math.fabs(l2_carree))

    def calcul_h1(self, matrice_masse, matrice_rigidite, solution):
        h1_semi_carree = matrice_rigidite.dot(solution).dot(solution)
        l2_carree = matrice_masse.dot(solution).dot(solution)
        return math.sqrt(math.fabs(l2_carree + h1_semi_carree))

    def calcul_erreur_h1_semi(self, matrice_rigidite, solution1, solution2):
        erreur = solution1 - solution2
        h1_semi_carree = matrice_rigidite.dot(erreur).dot(erreur)
        return math.sqrt(math.fabs(h1_semi_carree))

    def calcul_erreur_h1(self, matrice_masse, matrice_rigidite, solution1, solution2):
        erreur = solution1 - solution2
        return self.calcul_h1(matrice_masse, matrice_rigidite, erreur)

    def calcul_erreur_h1_relative(self, matrice_masse, matrice_rigidite, solution1, solution2):
        erreur = solution1 - solution2
        erreur_h1 = self.calcul_h1(matrice_masse, matrice_rigidite, erreur)
        solution2_h1 = self.calcul_h1(matrice_masse, matrice_rigidite, solution2)
        return erreur_h1 / solution2_h1

    def calcul_erreur_l2(self, matrice_masse, solution1, solution2):
        erreur = solution1 - solution2
        return self.calcul_l2(matrice_masse, erreur)

