from maillage.LocalisateurFrontiereMaillage import LocalisateurFrontiereMaillage
from maillage.MaillageTriangulaire import MaillageTriangulaire


class GenerateurMaillage:

    def generer_maillage(self, nombre_noeuds_horizontal: int, nombre_noeuds_vertical: int,
                         largeur_domaine: float, longeur_domaine: float) -> MaillageTriangulaire:

        maillage = MaillageTriangulaire.vide(nombre_noeuds_horizontal, nombre_noeuds_vertical)

        self.ajouter_noeuds(maillage, nombre_noeuds_horizontal, nombre_noeuds_vertical, largeur_domaine,
                            longeur_domaine)

        self.ajouter_elements(maillage, nombre_noeuds_horizontal, nombre_noeuds_vertical)

        self.ajouter_aretes_du_bord(maillage)

        return maillage

    def ajouter_noeuds(self, maillage: MaillageTriangulaire, nombre_noeuds_horizontal: int, nombre_noeuds_vertical: int,
                       largeur_domaine: float, hauteur_domaine: float):

        largeur_cellule = largeur_domaine / (nombre_noeuds_horizontal - 1)
        hauteur_cellule = hauteur_domaine / (nombre_noeuds_vertical - 1)

        for j in range(nombre_noeuds_vertical):

            index_ligne = j * nombre_noeuds_horizontal

            for i in range(nombre_noeuds_horizontal):
                x = largeur_cellule * i
                y = hauteur_cellule * j
                maillage.set_node(index_ligne + i, [x, y, 0])

    def ajouter_aretes_du_bord(self, maillage: MaillageTriangulaire):
        localisateur = LocalisateurFrontiereMaillage(maillage)
        maillage.aretes_du_bord = localisateur.trouver_aretes_du_bord()

    # TODO - triangles pas correctement ordonnés
    def ajouter_elements(self, maillage: MaillageTriangulaire, nombre_noeuds_horizontal: int, nombre_noeuds_vertical: int):

        element_index = 0

        for j in range(nombre_noeuds_vertical - 1):

            index_ligne_bas = j * nombre_noeuds_horizontal
            index_ligne_haut = index_ligne_bas + nombre_noeuds_horizontal

            for i in range(nombre_noeuds_horizontal - 1):

                index_noeud_bas_gauche = index_ligne_bas + i
                index_noeud_bas_droite = index_noeud_bas_gauche + 1
                index_noeud_haut_gauche = index_ligne_haut + i
                index_noeud_haut_droite = index_noeud_haut_gauche + 1

                maillage.set_element(element_index, [index_noeud_bas_gauche, index_noeud_bas_droite, index_noeud_haut_droite])
                maillage.set_element(element_index + 1, [index_noeud_bas_gauche, index_noeud_haut_droite, index_noeud_haut_gauche])
                element_index += 2
