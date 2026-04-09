from package.analyse_avancee import analyse_avance
from package.statistique import calcul_statistique
from package.fonctions_analyse import trouver_logs,analyse_logs,analyse_fichier
from package.security_analysis import securite_analyse

compteur_ligne_total_traité =0
def ecrire_dict(le_dict ):
    with open('package/rapport.txt', 'a' , encoding='utf-8') as f:
        for key  in le_dict:
            f.write(f"\n{key} : {le_dict[key]}\n")

def ecrire_message(message_à_écrire):
    with open('package/rapport.txt','a',encoding='utf-8') as f:
        f.write(message_à_écrire)


def génération_rapport():
    compteur_ligne_total_traité =0
    fusion_fichier_à_traiter =[]
    chemin_fichiers_à_traité= trouver_logs()['fichiers_log']
    for chemin in chemin_fichiers_à_traité:
        
        fusion_fichier_à_traiter += analyse_logs(chemin)['logs']
        compteur_ligne_total_traité +=(len(analyse_logs(chemin)['logs'])+len(analyse_logs(chemin)['liste_erreurs']))

    nbre_lignes_total_valide = len (fusion_fichier_à_traiter)    
    statistique = calcul_statistique(fusion_fichier_à_traiter)
    sécurity_analyse = securite_analyse(fusion_fichier_à_traiter)  
    Message1 = analyse_avance()  

    with open('package/rapport.txt','w',encoding='utf-8')  as f:

        f.write(f"RAPPORT DE L'ANALYSE AVANCE\n\n")
        f.write(Message1)
        
    ecrire_message(f"\nLe nombre total de ligne lues est :{compteur_ligne_total_traité}\n")
    ecrire_message(f"\nLe nombre total de ligne valide est :{nbre_lignes_total_valide}\n")

    ecrire_message(f"\n********************************************************\n")
    ecrire_message(f"\n\n  RAPPORT DE L'ANALYSE DE SECURITE\n\n")
    ecrire_message(sécurity_analyse)
    ecrire_message(f"\n*************************************************\n")

    ecrire_dict(statistique)
    ecrire_message(f"\n******************************************\n")
    ecrire_message(f"\n\nRAPPORT PAR FICHIER TRAITES\n\n")
    for chemin in chemin_fichiers_à_traité:
    
     ecrire_dict(analyse_fichier(chemin,analyse_logs(chemin)['logs'],analyse_logs(chemin)['liste_erreurs']))
     ecrire_message(f"\n******************************************\n")
    ecrire_message("FIN DU RAPPORT")

  
