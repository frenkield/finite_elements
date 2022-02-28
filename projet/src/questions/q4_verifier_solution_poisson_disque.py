from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage
from formulation_variationnelle.moteur_rendu_erreur import MoteurRenduErreur
from formulation_variationnelle.formulation_variationnelle_poisson import FormulationVariationnellePoisson
from formulation_variationnelle.calculateur_norme import CalculateurNorme

chargeur_maillage = ChargeurMaillage()
moteur_rendu_erreur = MoteurRenduErreur()
calculateur_norme = CalculateurNorme()

fichiers_maillage = [
    "data/maillages/maillage1_1.txt",
    "data/maillages/maillage1_2.txt",
    "data/maillages/maillage1_3.txt",
    "data/maillages/maillage1_4.txt",
    "data/maillages/maillage1_5.txt"
]

def fonction_second_membre(sommet): return 1

erreurs = []
nombre_triangles = []

for fichier in fichiers_maillage:

    print("calcul de l'erreur avec le maillage", extraire_petit_filename(fichier))

    maillage = chargeur_maillage.charger_maillage(fichier, True)
    nombre_triangles.append(maillage.get_element_count())

    formulation_variationnelle = FormulationVariationnellePoisson(maillage)

    solution = formulation_variationnelle.resoudre_dirichlet(fonction_second_membre)
    solution_exacte = formulation_variationnelle.resoudre_disque_dirichlet_exacte()

    erreur = calculateur_norme.calcul_erreur_h1_semi(formulation_variationnelle.matrice_rigidite,
                                                     solution, solution_exacte)

    erreurs.append(erreur)

print()
print("Nombre de triangles :", nombre_triangles)
print("Erreur H1 Semi-Norme :", erreurs)

title = "Poisson Disque - Erreur $H^1$ Semi-Norme"
moteur_rendu_erreur.rendre_erreur(nombre_triangles, erreurs, title, "Nombre de Triangles", True)
