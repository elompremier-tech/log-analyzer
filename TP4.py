#Nom: AMEGASHIE     /    DZALLO
#Prenoms: Luke Benaia Ariel     /    Elom Ezechiel
#Etudiant: 3 Maths

import csv
import os
from fonctions_verifications import date_valide,ip_valide,recup_nombre
from fonctions_analyse import recenser_elements,analyse_fichier,export_lignes_invalides,ajoutliste
from statistique import calcul_statistique
from security_analysis import securite_analyse
import re

def trouver_logs():
    chemin_actuel = os.getcwd()
    fichiers_logs = list()
    fichiers_intrus = list()

    #On verifie si un fichier log_data existe. Si oui, on y entre
    if os.path.exists("log_data"):
        #os.chdir(chemin_actuel + '\\' + "log_data")

        dossier = chemin_actuel + '\\' + "log_data"
        contenu_dossier= os.listdir(dossier)

        #pour chaque fichier dans le dossier on verifie son extension
        for fichier in contenu_dossier:
            chemin_complet = os.path.join(dossier, fichier)
            nom_fichier, extension = fichier.split(".")
            if extension == "csv":
                fichiers_logs.append(chemin_complet)       #On ajoute le fichier a la liste des fichiers a traiter
            else:
                fichiers_intrus.append(chemin_complet)     #On recupere les fichiers intrus
        
    #os.chdir(chemin_actuel)
        
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
                
                pattern_code = r"^\d{3}$"
                
                if not re.match(pattern_code, ligne[4].replace(" ","")):
                    liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Code HTTP non standard", 'Contenu': ligne})
                    continue
                else:
                    code = recup_nombre(ligne[4].replace(" ",""))
                    codes_HTTP = ajoutliste(ligne, codes_HTTP, 4)
                    if code not in codes_HTTP:
                        liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Code HTTP Invalide", 'Contenu': ligne})
                        continue
            #else:
                #liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Code HTTP Invalide", 'Contenu': ligne})
                #continue
            

            try:
                logs_valides.append({entetes[0]:ligne[0], entetes[1]:ligne[1], entetes[2]:ligne[2].replace(" ",""), entetes[3]:ligne[3], entetes[4]: code, entetes[5]: recup_nombre(ligne[5]), 'ligne': compteur_ligne})
            except ValueError:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Erreur de conversion,probablement le temps", 'Contenu': ligne})
                continue
            except:
                liste_erreurs.append({'Fichier': fichier ,'Ligne': compteur_ligne ,'Raison': "Erreur Inconnue,Verification requise", 'Contenu': ligne})
                continue
    
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
total_lignes_analysees = 0
logs = trouver_logs()['fichiers_log']
total_lignes_valides = list()
for log in logs:
    total_lignes_analysees += len(analyse_logs(log)['logs']) + len(analyse_logs(log)['liste_erreurs'])
    total_lignes_valides += analyse_logs(log)['logs'][::]

print(len(total_lignes_valides))
print(total_lignes_analysees)

#fichier3 = analyse_logs(logs[2])['logs']
#print((analyse_logs(logs[2])['logs']))

#afficher_dictionnaire(liste_dictionnaire=analyse_logs(logs[1])['logs'])
#print(len(analyse_logs(logs[1])['logs']))

#afficher_dictionnaire(dictionnaire=calcul_statistique(analyse_logs(logs[1])['logs']))
#afficher_dictionnaire(liste_dictionnaire=statistique(analyse_logs(logs[2])['logs'])[1])

#print(recenser_elements('methode','code',analyse_logs(logs[2])['logs']))
#print(recenser_elements('code','methode',analyse_logs(logs[2])['logs']))

#afficher_dictionnaire(dictionnaire=analyse_fichier(logs[2],analyse_logs(logs[2])['logs'],analyse_logs(logs[2])['liste_erreurs']))

#export_lignes_invalides(logs[2], analyse_logs(logs[2])['liste_erreurs'])
#afficher_dictionnaire(calcul_statistiques(fichier3))
#print(fichier3)

#analyse_logs(logs[1])

#print(securite_analyse(analyse_logs(logs[1])['logs']))

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

            print("2.Afficher l’analyse de sécurité")

        elif choix == 3:

            print("3.Afficher l’analyse avancée")

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