import sys
import logging
import math
from maillage.GenerateurMaillageRectangulaire import GenerateurMaillage
from maillage.MoteurRenduMaillage import MoteurRenduMaillage

logging.basicConfig(format="%(asctime)s %(levelname)7s - %(message)s",
                    level=logging.INFO, stream=sys.stdout,
                    datefmt="%Y-%m-%d %H:%M:%S")

# np.set_printoptions(threshold=numpy.inf)

PETIT_MAILLAGE = 'data/maillages/maillage-tp1.msh'
GROS_MAILLAGE = 'data/maillages/maill_rect_tri.msh'


longeur = 2
hauteur = 1

generateur_maillage = GenerateurMaillage()
maillage_genere = generateur_maillage.generer_maillage(3, 2, longeur, hauteur)

#print("maillage généré:\n", maillage_genere)


maillage_genere.point_dans_triangle(0, 0, 0)
maillage_genere.point_dans_triangle(0, 1, 0)
maillage_genere.point_dans_triangle(0, 1, 1)

maillage_genere.point_dans_triangle(0, 0.5, 0)

maillage_genere.point_dans_triangle(0, 0.49, 0.45)






# chargeur_maillage = ChargeurMaillage()
# maillage_charge = chargeur_maillage.charger_maillage(GROS_MAILLAGE)
#
# sauvegardeur_maillage = SauvegardeurMaillage()
# sauvegardeur_maillage.sauvegarder_maillage(maillage_genere, "test/test1.msh")

# assert(maillage_genere == maillage_charge)

# print("maillage généré:\n", maillage_genere)
# print("maillage:\n", maillage_charge)

# fonction_coleur1 = lambda node: math.cos((node[0] - 25) / 25 * math.pi) * math.cos((node[1] - 25) / 25 * math.pi)
# fonction_coleur2 = lambda node: math.erf(node[0] / longeur) * math.erf(node[1] / hauteur)
#
#
# MAX_ITERATIONS = 50
#
# def fonction_coleur3(node):
#     z = complex(node[0] / longeur * 2.5 - 2, node[1] / hauteur * 2.5 - 1.25)
#     c = z
#     for n in range(MAX_ITERATIONS):
#         if abs(z) > 2:
#             return n
#         z = z * z + c
#     return MAX_ITERATIONS * -1
#
# moteur_rendu = MoteurRenduMaillage()
# moteur_rendu.rendre_maillage_fonction(maillage_genere, fonction_coleur3)
