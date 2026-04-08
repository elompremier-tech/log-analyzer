from fonctions_verifications import recup_nombre
from statistique import calcul_statistique

def ajoutliste(listedepart,listearrivee,element):
    """Pour recenser des elements d'une liste de depart dans une liste d'arrivee tout en evitant les doublons dans la liste d'arrivee"""
    for chaque in listedepart:
        if chaque[element] not in listearrivee:
            listearrivee.append(chaque[element])
        else:
            continue
    return listearrivee

def ajoutliste(listedepart,listearrivee,index_element):
    """Pour recenser des elements d'une liste de depart dans une liste d'arrivee tout en evitant les doublons dans la liste d'arrivee"""
    
    if recup_nombre(listedepart[index_element].strip()) not in listearrivee:
        listearrivee.append(recup_nombre(listedepart[index_element]))
    else:
        return listearrivee
    return listearrivee

def recenser_elements(identifiant,objet_comparer,chaine):
    """Elle permet de faire le cumul de valeurs tout en leur attribuant des identifiants. Ex: Nom du client et somme depensee. Pour chaque 
    client, la fonction calcule alors la somme totale depensee en parcourant la liste"""
    listestock={}
    for ch in chaine:
        objet=ch[identifiant]
        valeur=ch[objet_comparer]
        #if type(valeur)!=str and type(valeur)!= bool:
            #listestock[objet]=listestock.get(objet, 0)+valeur
        #elif type(valeur) == str:
        listestock[objet]=listestock.get(objet, 0)+1

    return listestock

def analyse_fichier(fichier,logs_valides,logs_invalides):
   rapport_fichier = dict()
   nmbre_lignes_lues = (len(logs_valides) + len(logs_invalides))
   nmbre_lignes_valides = len(logs_valides)
   nmbre_lignes_invalides = len(logs_invalides)
   nmbre_erreurs = calcul_statistique(logs_valides)[1]
   temps_moyen = calcul_statistique(logs_valides)[0][0]["Temps moyen"]


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
