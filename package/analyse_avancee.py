from package.fonctions_analyse import  analyse_logs, trouver_logs
logs = trouver_logs()['fichiers_log']

def mini_analy_fichier():
   fichier_ligne_valide = []
   nbre_total_invalides=0
   test = max(logs, key= lambda log : len(analyse_logs(log)['logs'])) # fichier avec plus de lignes valides
   nbre_fichier_traité = len(logs)    # nbre total de fichier traité
   for log in logs:
       nbre_total_invalides += len(analyse_logs(log)['liste_erreurs'])  # dénombrement du nombre de lignes invalides total ignoré
       fichier_ligne_valide+=analyse_logs(log)['logs']
   #print( test,nbre_fichier_traité,nbre_total_invalides)

   return fichier_ligne_valide,test,nbre_fichier_traité,nbre_total_invalides


fichier_à_traité,fichier_plus_valide,nbre_total_fichier_traité,nbre_total_ligne_ignorés = mini_analy_fichier()


def analyse_avancee():
    compteur_url = {}
    compteur = 0
    requeste_plus_lente = None
    Message = ""

    if len(fichier_à_traité) == 0:
        Message +=f"Aucune donnee valide a analyser\n"
        return Message

    for ligne in fichier_à_traité:
        url = ligne['url']
        compteur_url[url] = compteur_url.get(url, 0) + 1

        if requeste_plus_lente is None or ligne["temps"] > requeste_plus_lente["temps"]:
            requeste_plus_lente = ligne

    lien = None

    compteur_url_ordonné = sorted(compteur_url.items(), key=lambda x:x[1],reverse=True)
    lien = compteur_url_ordonné[0][0]

    Message +=f"Le url plus demande est : {lien}\n"
    Message =f"La requeste la plus lente est faite au {requeste_plus_lente['date']} sur url {requeste_plus_lente['url']}\n"
    Message +=f"{requeste_plus_lente}\n"
    Message +=f"\nLES 5 URL LES PLUS DEMANDEES:\n"
    for indice  in range(len(compteur_url_ordonné)):
        compteur+=1
        Message +=f"{compteur_url_ordonné[indice][0]}: {compteur_url_ordonné[indice][1]} requête\n\n"
        if compteur == 5:
            break  

 
    Message +=f"{fichier_plus_valide} est le fichier contenant plus de ligne valides\n\nLe nombre total de fichier à traiter est {nbre_total_fichier_traité}\n\nLe nombre total de ligne ignorés est {nbre_total_ligne_ignorés}\n"  
    return Message

