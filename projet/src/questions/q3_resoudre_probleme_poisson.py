from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage
from maillage.moteur_rendu_maillage import MoteurRenduMaillage
from formulation_variationnelle.formulation_variationnelle_poisson import FormulationVariationnellePoisson


filename = get_filename_maillage()

chargeur_maillage = ChargeurMaillage()
moteur_rendu = MoteurRenduMaillage()

maillage = chargeur_maillage.charger_maillage(filename, True)

formulation_variationnelle = FormulationVariationnellePoisson(maillage)

def fonction_second_membre(sommet): return 1
solution = formulation_variationnelle.resoudre_dirichlet(fonction_second_membre)

title = "f = 1, g = 0, pseudo-élimination, %s" % (extraire_petit_filename(filename))
moteur_rendu.rendre_maillage_valeurs_3d(maillage, solution, title)
