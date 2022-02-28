import numpy as np
from questions.question_utils import *
from maillage.chargeur_maillage import ChargeurMaillage
from maillage.moteur_rendu_maillage import MoteurRenduMaillage
from formulation_variationnelle.formulation_variationnelle_poisson import FormulationVariationnellePoisson


filename = get_filename_maillage()

chargeur_maillage = ChargeurMaillage()
moteur_rendu = MoteurRenduMaillage()

maillage = chargeur_maillage.charger_maillage(filename, True)

formulation_variationnelle = FormulationVariationnellePoisson(maillage)

# laplacien de g est juste 1
fonction_laplacien_g = lambda sommet: 1
u_tilde = formulation_variationnelle.resoudre_dirichlet(fonction_laplacien_g)

fonction_g = lambda sommet: (sommet[0]**2 + sommet[1]**2) / 4
g = np.array(list(map(fonction_g, maillage.noeuds)))

u = u_tilde + g

title = r"$u = 0$ dans $\Omega$, $u = |x|^2 / 4$ sur $\Gamma$"
subtitle = "%s" % (extraire_petit_filename(filename))
title = title + "\n" + subtitle

moteur_rendu.rendre_maillage_valeurs(maillage, u, title)
