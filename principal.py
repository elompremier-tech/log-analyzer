#Nom: AMEGASHIE     /    DZALLO
#Prenoms: Luke Benaia Ariel     /    Elom Ezechiel
#Etudiant: 3 Maths

from package.analyse_avancé import analyse_avancee
from package.fonctions_verifications import *
from package.fonctions_analyse import *
from package.statistique import *
from package.security_analysis import * 
from package.fonctions_affichage import *


def menu():
    choix= None
    while True:
        print("================Menu Principal================")
        print("1.Afficher les statistiques globales")
        print("2.Afficher l’analyse de sécurité")
        print("3.Afficher l’analyse avancée")
        print("4.Afficher le résumé par fichier")
        print("5.Générer un rapport")
        print("6.Exporter les lignes invalides")
        print("0.Quitter")

        try:
            choix=int(input("Bienvenue dans votre DataCenter. Que voulez-vous faire?"))
        except ValueError:
            print("Entrez un entier. Essayez a nouveau")
            menu()
        
        logs = trouver_logs()['fichiers_log']
        if choix == 1:
            for log in logs:
                print(f"\n Fichier : {log.upper()} \n")
                print("="*30, "\n")
                afficher_dictionnaire(dictionnaire=calcul_statistique(analyse_logs(log)['logs']))
                print("\n", "*"*30, "\n")

        elif choix == 2:

            for log in logs:
                print(f"\n Fichier : {log.upper()} \n")
                print("="*30, "\n")
                print(securite_analyse(analyse_logs(log)['logs']))
                print("\n", "*"*30, "\n")

        elif choix == 3:

            print(analyse_avancee())

        elif choix == 4:

            for log in logs:
                print("="*30, "\n")
                afficher_dictionnaire(dictionnaire=analyse_fichier(log,analyse_logs(log)['logs'], analyse_logs(log)['liste_erreurs']))
                print("\n", "*"*30, "\n")

        elif choix == 5:

            print("5.Générer un rapport")

        elif choix == 6:

            dossier_rapport = "Rapports_lignes_Invalides"
            if not os.path.exists("Rapports_lignes_Invalides"):
                os.mkdir("Rapports_lignes_Invalides")

            for log in logs:
                nom = os.path.basename(log)
                chemin = os.path.join(dossier_rapport, 'lignes_invalides_' +nom+ ".txt")
                export_lignes_invalides(chemin, analyse_logs(log)['liste_erreurs'])


        elif choix == 0:
            break
        else:
            print("Proposition Inconnue. Veuillez choisir parmi les numero donnes")
        
    return print("Vous quittez le programme. Nous esperons vous revoir sous peu!")  
  
menu()