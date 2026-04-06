#Nom: AMEGASHIE     /    DZALO
#Prenoms: Luke Benaia Ariel     /    Elom Ezechiel
#Etudiant: 3 Maths
import csv
import os

chemin_actuel = os.getcwd()

#On verifie si un fichier log_data se trouve dans le dossier actuel. Si oui, on y entre
def trouver_logs():
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
    
    return {'fichiers_logs': fichiers_logs, 'fichiers_intrus':fichiers_intrus}
    
def analyse_logs(fichier):
    with open (fichier, "r" , encoding = 'utf-8') as f:
        lecture = csv.reader(f)
        entetes = next(lecture)

        logs = list()
        x=1
        liste_erreurs = list()
        for ligne in lecture:
            x+=1
            if "" in ligne:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': x ,'Raison': "Element vide", 'Contenu': ligne})
                continue
            elif len(ligne) != 6:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': x ,'Raison': "Nombre de colonnes incorrect", 'Contenu': ligne})
                continue

            try:
                logs.append({entetes[0]:ligne[0],entetes[1]:ligne[1],entetes[2]:ligne[2],entetes[3]:ligne[3],entetes[4]:int(ligne[4]),entetes[5]:ligne[5]})
            except:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': x ,'Raison': "Inconnue,verification requise", 'Contenu': ligne})

    return {'logs': logs, 'liste_erreurs': liste_erreurs}