import matplotlib
from typing import Callable

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np

from maillage.MaillageTriangulaire import MaillageTriangulaire


class MoteurRenduMaillage:

    def rendre_maillage_valeurs(self, maillage: MaillageTriangulaire, valeurs):

        from matplotlib.pyplot import figure
        figure(num=None, figsize=(12, 12))

        figure, axes = plt.subplots()
        axes.set_aspect('equal')
        axes.set_title("Rendu du Maillage")

        plot = matplotlib.pyplot.tripcolor(maillage.get_triangulation(), valeurs, cmap="hot",
                                           shading='flat')

        figure.colorbar(plot)

        plt.show()

    def rendre_maillage_fonction(self, maillage: MaillageTriangulaire, fonction: Callable):

        from matplotlib.pyplot import figure
        figure(num=None, figsize=(12, 12))

        couleurs_noeuds = np.array([fonction(node) for node in maillage.noeuds])

        figure, axes = plt.subplots()
        axes.set_aspect('equal')
        axes.set_title("Rendu du Maillage")

        plot = matplotlib.pyplot.tripcolor(maillage.get_triangulation(),
                                             couleurs_noeuds, cmap="hot",
                                             shading='flat')

        figure.colorbar(plot)

        plt.show()

    def rendre_maillage_valeurs_3d(self, maillage: MaillageTriangulaire, valeurs):

        fig = plt.figure()
        ax = fig.gca(projection='3d')

        surface = ax.plot_trisurf(maillage.get_triangulation(), valeurs, cmap=plt.cm.CMRmap)

        # surf = ax.plot_trisurf(maillage.get_triangulation(), rstride = 1, cstride = 1,
        #                        linewidth = 0, antialiased = False, cmap = 'coolwarm')

        #ax.set_zlim(-1.01, 1.01)
        ax.zaxis.set_major_locator(LinearLocator(10))
        ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

        fig.colorbar(surface, shrink=0.5, aspect=5)

        plt.show()

    def rendre_maillage(self, maillage: MaillageTriangulaire):

        matplotlib.pyplot.triplot(maillage.get_triangulation(), color='blue',
                                  marker='o', markersize=3, linestyle='solid')

        x1, x2, y1, y2 = plt.axis('tight')
        horizontal_buffer = (x2 - x1) / 50
        vertical_buffer = (y2 - y1) / 50

        plt.axis((x1 - horizontal_buffer, x2 + horizontal_buffer,
                  y1 - vertical_buffer, y2 + vertical_buffer))

        plt.show()

    def rendre_frontiere(self, maillage: MaillageTriangulaire):

        x = []
        y = []

        for arete in maillage.aretes_du_bord:
            x.append(maillage.noeuds[arete[0]][0])
            y.append(maillage.noeuds[arete[0]][1])

        plt.plot(x, y)

        # matplotlib.pyplot.triplot(maillage.get_triangulation(), color='blue',
        #                           marker='o', markersize=3, linestyle='solid')
        #
        # x1, x2, y1, y2 = plt.axis('tight')
        # horizontal_buffer = (x2 - x1) / 50
        # vertical_buffer = (y2 - y1) / 50
        #
        # plt.axis((x1 - horizontal_buffer, x2 + horizontal_buffer,
        #           y1 - vertical_buffer, y2 + vertical_buffer))

        plt.show()
