#Nom: AMEGASHIE     /    DZALLO
#Prenoms: Luke Benaia Ariel     /    Elom Ezechiel
#Etudiant: 3 Maths

import csv
import os
from fonctions_verifications import date_valide,ip_valide,recup_nombre
from fonctions_analyse import recenser_elements,analyse_fichier,export_lignes_invalides,ajoutliste

chemin_actuel = os.getcwd()

def trouver_logs():
    #On verifie si un fichier log_data existe. Si oui, on y entre
    if os.path.exists("log_data"):
        os.chdir(chemin_actuel + '\\' + "log_data")
        contenu_dossier= os.listdir(".")

        fichiers_logs = list()
        fichiers_intrus = list()
        #pour chaque fichier dans le dossier on verifie son extension
        for fichier in contenu_dossier:
            nom_fichier, extension = fichier.split(".")
            if extension == "csv":
                fichiers_logs.append(fichier)       #On ajoute le fichier a la liste des fichiers a traiter
            else:
                fichiers_intrus.append(fichier)     #On recupere les fichiers intrus
    
    return {'fichiers_log': fichiers_logs, 'fichiers_intru':fichiers_intrus}
    


def analyse_logs(fichier):
    with open (fichier, "r" , encoding = 'utf-8') as f:
        lecture_entetes = csv.reader(f)     #On recupere les entetes
        entetes = next(lecture_entetes)     #On les stocke sous forme de liste

        lecture = csv.reader(f, delimiter = "|")    #Uniquement les liste avec "|" comme separateur
        compteur_ligne=1

        logs_valides = list()
        liste_erreurs = list()
        codes_HTTP = list()
        for ligne in lecture:
            compteur_ligne+=1

            for element in ligne:
                element = element.strip()

            
            if "" in ligne:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Element vide", 'Contenu': ligne})
                continue
            elif len(ligne) != 6:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Nombre de colonnes incorrect/Mauvais separateur", 'Contenu': ligne})
                continue
            elif not date_valide(ligne[0]):
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Format de date incorrect", 'Contenu': ligne})
                continue
            elif not ip_valide(ligne[1]):
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Adresse IP invalide", 'Contenu': ligne})
                continue
            elif ligne[2].replace(" ","").lower() not in ["get", "post"]:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Methode Invalide", 'Contenu': ligne})
                continue

            
            if recup_nombre(ligne[4].replace(" ","")):
                code = ligne[4].replace(" ","")
                codes_HTTP = ajoutliste(ligne, codes_HTTP, 4)
                if code not in codes_HTTP:
                    liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Code HTTP Invalide", 'Contenu': ligne})
                    continue
            else:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Code HTTP Invalide", 'Contenu': ligne})
                continue
            

            try:
                logs_valides.append({entetes[0]:ligne[0], entetes[1]:ligne[1], entetes[2]:ligne[2].replace(" ",""), entetes[3]:ligne[3], entetes[4]:int(ligne[4]), entetes[5]: recup_nombre(ligne[5]), 'ligne': compteur_ligne})
            except ValueError:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Erreur de conversion,probablement le temps", 'Contenu': ligne})
                continue
            except:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Erreur Inconnue,Verification requise", 'Contenu': ligne})
                continue
    
    print(codes_HTTP)
    return {'logs': logs_valides, 'liste_erreurs': liste_erreurs}



def afficher_dictionnaire(dictionnaire=None,liste_dictionnaire=None):
    if dictionnaire:
        for element in dictionnaire:
            print(f"{(element+':'):<30} {dictionnaire[element]}")
            print("="*len(element))
    elif liste_dictionnaire:
        for chaque_dictionnaire in liste_dictionnaire:
            for paires in chaque_dictionnaire:
                #print(chaque_dictionnaire)
                print(f"{paires:<30} {chaque_dictionnaire[paires]}")
            print(end="")
            print("------------------------------------------------------------------------------------")
            print(end="\n")



#Bloc pour tester le code
logs = trouver_logs()['fichiers_log']   
#fichier3 = analyse_logs(logs[2])['logs']

#afficher_dictionnaire(liste_dictionnaire=analyse_logs(logs[1])['logs'])
#print(len(analyse_logs(logs[2])['logs']))

#afficher_dictionnaire(liste_dictionnaire=statistique(analyse_logs(logs[0])['logs'])[0])
#afficher_dictionnaire(liste_dictionnaire=statistique(analyse_logs(logs[2])['logs'])[1])

#print(recenser_elements('methode','code',analyse_logs(logs[2])['logs']))
#print(recenser_elements('code','methode',analyse_logs(logs[2])['logs']))

#afficher_dictionnaire(dictionnaire=analyse_fichier(logs[2],analyse_logs(logs[2])['logs'],analyse_logs(logs[2])['liste_erreurs']))

#export_lignes_invalides(logs[2], analyse_logs(logs[2])['liste_erreurs'])
#afficher_dictionnaire(calcul_statistiques(fichier3))
#print(fichier3)

analyse_logs(logs[1])