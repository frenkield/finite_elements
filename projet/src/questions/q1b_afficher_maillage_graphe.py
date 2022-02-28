from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage
from maillage.moteur_rendu_maillage import MoteurRenduMaillage


filename = get_filename_maillage()

chargeur_maillage = ChargeurMaillage()
moteur_rendu = MoteurRenduMaillage()

maillage = chargeur_maillage.charger_maillage(filename)

moteur_rendu.rendre_maillage(maillage, "Maillage du %s" % (extraire_petit_filename(filename)))
