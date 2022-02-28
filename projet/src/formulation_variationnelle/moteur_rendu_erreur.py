####################################################################
# c'est super moche tout ca mais il faut jouer avec les imports pour
# sauvegarder des images sur les machines sans écran

from questions.question_utils import get_filename_image

# comme ça on peut générer des images sur des machines sans écran
if get_filename_image():
    import matplotlib
    matplotlib.use('Agg')
####################################################################

import matplotlib.pyplot as plt
import math

class MoteurRenduErreur:

    def rendre_erreur(self, abscisse, erreurs, titre, xaxis_titre, echelle_log = False):

        fig, ax = plt.subplots()
        ax.plot(abscisse, erreurs, label=r"$H^1$ Semi-Norme")

        if echelle_log:

            plt.xscale('log')
            plt.yscale('log')
            titre = "%s (Log)" % (titre)
            xaxis_titre = "%s (Échelle Log)" % (xaxis_titre)

            xticks = self.generer_ticks(abscisse)
            ax.xaxis.set_major_locator(plt.NullLocator())
            ax.xaxis.set_minor_locator(plt.NullLocator())
            plt.xticks(xticks, [self.format_nombre(i) for i in xticks], rotation=35)

            yticks = self.generer_ticks(erreurs)
            ax.yaxis.set_major_locator(plt.NullLocator())
            ax.yaxis.set_minor_locator(plt.NullLocator())
            plt.yticks(yticks, [self.format_nombre(i) for i in yticks])

        # plt.legend()
        plt.title(titre)
        plt.xlabel(xaxis_titre)

        self.afficher_ou_sauvegarder_plot()

    def rendre_erreur_multiple(self, valeurs, titre, echelle_log = False):

        fig, ax = plt.subplots()
        
        abscisse = valeurs["abscisse"]["valeurs"]
        xaxis_titre = valeurs["abscisse"]["label"]
        
        for ligne in valeurs["ordonnee"]:        
            ax.plot(abscisse, ligne["valeurs"], label=ligne["label"])

        if echelle_log:

            plt.xscale('log')
            plt.yscale('log')
            titre = "%s (Log)" % (titre)

        plt.legend()
        plt.title(titre)
        plt.xlabel(xaxis_titre)

        self.afficher_ou_sauvegarder_plot()

    def rendre_erreur_subplots(self, abscisse1, erreurs1, titre1, abscisse2,
                               erreurs2, titre2, xaxis_titre):

        fig = plt.figure()
        fig.set_figwidth(10)

        plot1 = fig.add_subplot(121)
        plot1.set_title(titre1)
        plot1.set_xlabel(xaxis_titre)
        plot1.plot(abscisse1, erreurs1)
        self.configurer_plot(plot1, abscisse1, erreurs1)

        # ========================================================

        plot2 = fig.add_subplot(122)
        plot2.set_title(titre2)
        plot2.set_xlabel(xaxis_titre)
        plot2.plot(abscisse2, erreurs2)
        self.configurer_plot(plot2, abscisse2, erreurs2)

        self.afficher_ou_sauvegarder_plot()

    def generer_ticks(self, valeurs):

        if len(valeurs) <= 5:
            return valeurs

        divisor = math.ceil(len(valeurs) / 5)
        dernier = valeurs[-1]
        valeurs = valeurs[:-1][::divisor]
        valeurs.append(dernier)

        return valeurs

    def format_nombre(self, nombre):

        if isinstance(nombre, int):
            return nombre

        return self.format_float(nombre)

    def format_float(self, x):
        return "{:.4f}".format(x)

    def configurer_plot(self, plot, abscisse, erreurs):

        plot.set_xscale('log')
        plot.set_yscale('log')

        plot.xaxis.set_major_locator(plt.NullLocator())
        plot.xaxis.set_minor_locator(plt.NullLocator())
        xticks = self.generer_ticks(abscisse)
        plot.set_xticks(xticks)
        plot.set_xticklabels([self.format_nombre(i) for i in xticks], rotation=35)

        plot.yaxis.set_major_locator(plt.NullLocator())
        plot.yaxis.set_minor_locator(plt.NullLocator())
        yticks = self.generer_ticks(erreurs)
        plot.set_yticks(yticks)
        plot.set_yticklabels([self.format_nombre(i) for i in yticks])

    def afficher_ou_sauvegarder_plot(self):

        plt.tight_layout()
        fichier_image = get_filename_image()

        if not fichier_image:
            plt.show()

        else:
            print("stockage de l'image dans", fichier_image)
            plt.savefig(fichier_image)
