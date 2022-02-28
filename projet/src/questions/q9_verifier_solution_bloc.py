import numpy as np
from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage
from formulation_variationnelle.moteur_rendu_erreur import MoteurRenduErreur
from formulation_variationnelle.formulation_variationnelle_poisson import FormulationVariationnellePoisson
from formulation_variationnelle.formulation_variationnelle_bloc import FormulationVariationnelleBloc
from formulation_variationnelle.calculateur_norme import CalculateurNorme


chargeur_maillage = ChargeurMaillage()
moteur_rendu_erreur = MoteurRenduErreur()
calculateur_norme = CalculateurNorme()

fichiers_maillage_1 = [
    "data/maillages/maillage1_1.txt",
    "data/maillages/maillage1_2.txt",
    "data/maillages/maillage1_3.txt",
    "data/maillages/maillage1_4.txt",
    "data/maillages/maillage1_5.txt"
]

fichiers_maillage_2 = [
    "data/maillages/maillage2_1.txt",
    "data/maillages/maillage2_2.txt",
    "data/maillages/maillage2_3.txt",
    "data/maillages/maillage2_4.txt",
    "data/maillages/maillage2_5.txt"
]

def fonction_g(sommet): return (sommet[0] ** 2 + sommet[1] ** 2) / 2
def fonction_laplacien_g(sommet): return 2

def calcul_erreur(fichiers_maillage):

    erreurs = []
    h = []

    for fichier in fichiers_maillage:

        print("calcul de l'erreur avec le maillage", extraire_petit_filename(fichier))

        maillage = chargeur_maillage.charger_maillage(fichier, True)
        h.append(maillage.calcul_h())

        # =============================================================================

        formulation_variationnelle = FormulationVariationnellePoisson(maillage)
        u_tilde = formulation_variationnelle.resoudre_dirichlet(fonction_laplacien_g)
        g = np.array(list(map(fonction_g, maillage.noeuds)))
        solution_type_1 = u_tilde + g

        # =============================================================================

        formulation_variationnelle_bloc = FormulationVariationnelleBloc(maillage)
        solution_bloc = formulation_variationnelle_bloc.resoudre_bloc(fonction_g)

        # =============================================================================

        erreur = calculateur_norme.calcul_erreur_h1_relative(formulation_variationnelle.matrice_masse,
                                                             formulation_variationnelle.matrice_rigidite,
                                                             solution_type_1, solution_bloc)
        erreurs.append(erreur)

    return h, erreurs

# =======================================================================

geometrie1_h, geometrie1_erreurs = calcul_erreur(fichiers_maillage_1)

print()
print("Géométrie 1 - h :", geometrie1_h)
print("Géométrie 1 - Erreur H1 Relative :", geometrie1_erreurs)
print()

# =======================================================================

geometrie2_h, geometrie2_erreurs = calcul_erreur(fichiers_maillage_2)

print()
print("Géométrie 2 - h :", geometrie2_h)
print("Géométrie 2 - Erreur H1 Relative :", geometrie2_erreurs)

title1 = "Géométrie 1\nErreur Relative Bloc $H^1$\n$u = |x|^2 / 2$ sur $\Gamma$"
title2 = "Géométrie 2\nErreur Relative Bloc $H^1$\n$u = |x|^2 / 2$ sur $\Gamma$"

moteur_rendu_erreur.rendre_erreur_subplots(geometrie1_h, geometrie1_erreurs, title1, geometrie2_h,
                                           geometrie2_erreurs, title2, "h")
