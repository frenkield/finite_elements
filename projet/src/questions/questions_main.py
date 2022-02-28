import argparse
from questions.question_utils import *

questions = {

    "1a": {"filename": "q1a_afficher_maillage",
           "description": "charger et afficher tableaux du maillage"},

    "1b": {"filename": "q1b_afficher_maillage_graphe",
           "description": "charger et afficher graphe du maillage"},

    "2": {"filename": "q2_afficher_maillage_bord",
           "description": "charger et afficher graphe du bord du maillage"},

    "3": {"filename": "q3_resoudre_probleme_poisson",
          "description": "resoudre le problème 1 (poisson) avec f = 1 et g = 0"},

    "4": {"filename": "q4_verifier_solution_poisson_disque",
          "description": "verifier la solution de la question 3 (poisson disque)"},

    "5": {"filename": "q5_resoudre_probleme_poisson_tilde",
          "description": "resoudre le problème 1 (poisson) avec f = grad(g)"},

    "6": {"filename": "q6_verifier_solution_poisson_tilde",
          "description": "afficher l'erreur de la solution de la u-tilde (poisson disque)"},

    "9": {"filename": "q9_verifier_solution_bloc",
          "description": "afficher l'erreur entre la solution bloc et la solution u-tilde"}
}

parser = argparse.ArgumentParser(description='Lancer une question')

parser.add_argument("index_question", nargs="?", help="l'index de la question à lancer")
parser.add_argument("fichier_maillage", nargs="?", help="nom du fichier qui contient un maillage")
parser.add_argument("-l", action='store_true', help="afficher liste des questions et leurs indices")
parser.add_argument("-o", metavar="fichier_image", help="nom du fichier où sauvegarder l'image de la figure")

args = parser.parse_args()

if args.l or not args.index_question or args.index_question not in questions :

    print("Merci de specifier l'index d'une des questions suivantes :")

    for question in sorted (questions):
        print("   ", question, ":", questions[question]["description"])

    exit(0)

_question_filename = questions[args.index_question]["filename"]

set_filename_maillage(args.fichier_maillage)
set_filename_image(args.o)
__import__(_question_filename)
