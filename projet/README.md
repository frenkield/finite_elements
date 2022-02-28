================================================================================

4M054 - Mise en oeuvre des éléments finis
Projet 2018/2019

David Frenkiel
28/04/2019

================================================================================

Le rapport au format PDF contenant les solutions des problèmes et d'autres
informations se trouve dans le répertoire docs :

    docs/rapport.pdf

================================================================================

Exécuter les tests unitaires avec le script Bash :

    ./test.sh

Ou a la main :

    PYTHONPATH=src python3 -m unittest discover -s test

================================================================================

Afficher la liste des questions :

    ./question.sh

Exécuter une question :

    ./question.sh [index_question] [fichier_maillage] [-o fichier_image]

Certaines des questions ont besoin du deuxième argument pour traiter un maillage
spécifique. Par exemple, pour lancer la question 1b :

    ./question.sh 1b data/maillages/maillage1_1.txt

L'option "-o" permet à sauvegarder une figure dans un fichier au lieu de
l'afficher directement. Par exemple,

    ./question.sh 9 -o figure1.png

================================================================================

Question 1 (questions/q1a_afficher_maillage.py) :

1a) Charger et afficher dans le console les tableaux des sommets et des
triangles :

    ./question.sh 1a [fichier_maillage]

Par exemple,

    ./question.sh 1a data/maillages/maillage1_1.txt

1b) Charger et afficher graphiquement un maillage :

    ./question.sh 1b [fichier_maillage]

Par exemple,

    ./question.sh 1b data/maillages/maillage1_1.txt

Ou pour sauvegarder l'image dans un fichier :

    ./question.sh 1b data/maillages/maillage1_1.txt -o [fichier_image]

================================================================================

Question 2 (questions/q2_afficher_maillage_bord.py) :

    ./question.sh 2 [fichier_maillage] [-o fichier_image]

Par exemple,

    ./question.sh 2 data/maillages/maillage3_3.txt

================================================================================

Question 3 (questions/q3_resoudre_probleme_poisson.py) :

    ./question.sh 3 [fichier_maillage] [-o fichier_image]

Par exemple,

    ./question.sh 3 data/maillages/maillage2_2.txt

================================================================================

Question 4 (questions/q4_verifier_solution_poisson_disque.py) :

    ./question.sh 4 [-o fichier_image]

Par exemple,

    ./question.sh 4

Ou

    ./question.sh 4 -o figure4.png

================================================================================

Question 5 (questions/q5_resoudre_probleme_poisson_tilde.py) :

    ./question.sh 5 [fichier_maillage] [-o fichier_image]

Par exemple,

    ./question.sh 5 data/maillages/maillage3_2.txt

Ou

    ./question.sh 5 data/maillages/maillage2_2.txt -o figure5.png

================================================================================

Question 6 (questions/q6_verifier_solution_poisson_tilde.py) :

    ./question.sh 6 [-o fichier_image]

Par exemple,

    ./question.sh 6

Ou

    ./question.sh 6 -o figure6.png

================================================================================

Question 9 (questions/q9_verifier_solution_bloc.py) :

    ./question.sh 9 [-o fichier_image]

Par exemple,

    ./question.sh 9

Ou

    ./question.sh 9 -o figure9.png
