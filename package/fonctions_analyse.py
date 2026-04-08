from package.fonctions_verifications import recup_nombre, date_valide, ip_valide
from package.statistique import calcul_statistique
import os
import csv
import re

def ajoutliste(listedepart,listearrivee,index_element):
    """Pour recenser des elements d'une liste de depart dans une liste d'arrivee tout en evitant les doublons dans la liste d'arrivee"""
    
    if recup_nombre(listedepart[index_element].strip()) not in listearrivee:
        listearrivee.append(recup_nombre(listedepart[index_element]))
    else:
        return listearrivee
    return listearrivee

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


def analyse_fichier(fichier,logs_valides,logs_invalides):
   rapport_fichier = dict()
   nmbre_lignes_lues = (len(logs_valides) + len(logs_invalides))
   nmbre_lignes_valides = len(logs_valides)
   nmbre_lignes_invalides = len(logs_invalides)
   nmbre_erreurs = calcul_statistique(logs_valides)['Nombre d erreurs']
   temps_moyen = calcul_statistique(logs_valides)["Temps moyen"]


   rapport_fichier['Fichier'] = fichier
   rapport_fichier['Nombre de lignes lues'] = nmbre_lignes_lues
   rapport_fichier['Nombre de lignes valides'] = nmbre_lignes_valides
   rapport_fichier['Nombre de lignes invalides'] = nmbre_lignes_invalides
   rapport_fichier['Nombre d’erreurs HTTP'] = nmbre_erreurs
   rapport_fichier['Temps moyen de réponse du fichier'] = temps_moyen

   return rapport_fichier


def export_lignes_invalides(fichier, lignes_invalides):
   #nom, extension = fichier.split('.')
   with open (fichier, 'w', encoding = 'utf-8') as f:
      f.write(f"EXPORT DES LIGNES INVALIDES DU FICHIER: {fichier}\n")
      f.write("===================================================\n\n")
      for dictionnaire in lignes_invalides:
            for element in dictionnaire:
                f.write(f"{(element+':'):<15} {dictionnaire[element]}\n")
                f.write("="*len(element))
                f.write("\n")
            f.write("\n*****************************************************\n")
