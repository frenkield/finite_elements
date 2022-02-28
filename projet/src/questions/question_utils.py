import os
import re

def set_filename_maillage(fichier_maillage):
    global _fichier_maillage
    _fichier_maillage = fichier_maillage

def get_filename_maillage():

    if not _fichier_maillage:
        print("Merci de specifier le nom (chemin) d'un fichier qui contient un maillage.")
        exit(0)

    if not os.path.isfile(_fichier_maillage):
        print("Le fichier %s n'existe pas." % (_fichier_maillage))
        exit(0)

    return _fichier_maillage

def extraire_petit_filename(filename):
    return re.sub(".*/", "", filename)

def set_filename_image(fichier_image):
    global _fichier_image
    _fichier_image = fichier_image

def get_filename_image():
    return _fichier_image
