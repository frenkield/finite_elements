from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage


filename = get_filename_maillage()

chargeur_maillage = ChargeurMaillage()
maillage = chargeur_maillage.charger_maillage(filename)

print(maillage)
