####################################################################
# c'est super moche tout ca mais il faut jouer avec les imports pour
# sauvegarder des images sur les machines sans écran

from questions.question_utils import get_filename_image

# comme ça on peut générer des images sur des machines sans écran
if get_filename_image():
    import matplotlib
    matplotlib.use('Agg')
####################################################################

import matplotlib

# c'est nécessaire - bien que l'on ne l'utilise pas directement
from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

from .maillage import Maillage


class MoteurRenduMaillage:

    def rendre_maillage_valeurs(self, maillage: Maillage, valeurs, title = ""):

        # from matplotlib.pyplot import figure
        # # figure(num=None, figsize=(12, 12))

        figure, axes = plt.subplots()
        # axes.set_aspect('equal')

        plot = matplotlib.pyplot.tripcolor(maillage.get_triangulation(), valeurs, cmap="hot",
                                           shading='flat')
        figure.colorbar(plot)

        if title:
            plt.title(title)

        self.afficher_ou_sauvegarder_plot()

    def rendre_maillage_fonction(self, maillage: Maillage, fonction):

        # from matplotlib.pyplot import figure
        # figure(num=None, figsize=(12, 12))

        couleurs_noeuds = np.array([fonction(node) for node in maillage.noeuds])

        figure, axes = plt.subplots()
        axes.set_aspect('equal')
        axes.set_title("Rendu du Maillage")

        plot = matplotlib.pyplot.tripcolor(maillage.get_triangulation(),
                                             couleurs_noeuds, cmap="hot",
                                             shading='flat')

        figure.colorbar(plot)

        self.afficher_ou_sauvegarder_plot()

    def rendre_maillage_valeurs_3d(self, maillage: Maillage, valeurs, title = ""):

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surface = ax.plot_trisurf(maillage.get_triangulation(), valeurs, cmap=plt.cm.CMRmap)

        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        fig.colorbar(surface, shrink=0.5, aspect=5)

        if title:
            plt.title(title)

        self.afficher_ou_sauvegarder_plot()

    def rendre_maillage(self, maillage: Maillage, title = ""):

        # from matplotlib.pyplot import figure
        # figure(num=None, figsize=(8, 8))

        matplotlib.pyplot.triplot(maillage.get_triangulation(), color='blue',
                                  marker='o', markersize=3, linestyle='solid')

        x1, x2, y1, y2 = plt.axis('tight')
        horizontal_buffer = (x2 - x1) / 50
        vertical_buffer = (y2 - y1) / 50

        plt.axis((x1 - horizontal_buffer, x2 + horizontal_buffer,
                  y1 - vertical_buffer, y2 + vertical_buffer))

        if title:
            plt.title(title)

        self.afficher_ou_sauvegarder_plot()

    def rendre_maillage_bord(self, maillage: Maillage, title = ""):

        for arete in maillage.aretes_du_bord:

            sommet1_index = arete[0]
            sommet2_index = arete[1]

            sommet1 = maillage.noeuds[sommet1_index]
            sommet2 = maillage.noeuds[sommet2_index]

            x = [sommet1[0], sommet2[0]]
            y = [sommet1[1], sommet2[1]]

            plt.plot(x, y, marker='.', color="blue")

        if title:
            plt.title(title)

        self.afficher_ou_sauvegarder_plot()

    def afficher_ou_sauvegarder_plot(self):

        plt.tight_layout()
        fichier_image = get_filename_image()

        if not fichier_image:
            plt.show()

        else:
            print("stockage de l'image dans", fichier_image)
            plt.savefig(fichier_image)
