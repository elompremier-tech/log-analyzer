#Nom: AMEGASHIE     /    DZALO
#Prenoms: Luke Benaia Ariel     /    Elom Ezechiel
#Etudiant: 3 Maths
import csv
import json
import os

chemin_actuel = os.getcwd()
print(f"Je suis ici: {chemin_actuel}")

#On verifie si un fichier log_data se trove dans le dossier actuel. Si oui, on y entre
if os.path.exists("log_data"):
    os.chdir(chemin_actuel+ '\\'+ "log_data")
    contenu_dossier= os.listdir(".")

    #pour chaque fichier dans le dossier on verifie l'extension
    fichiers_logs = list()
    fichiers_intrus = list()
    for fichier in contenu_dossier:
        nom_fichier, extension = fichier.split(".")
        if extension == "csv":
            fichiers_logs.append(fichier)
        else:
            fichiers_intrus.append(fichier)


