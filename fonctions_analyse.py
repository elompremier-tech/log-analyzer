code_erreurs = [404, 500]

def statistique(logs):

    requests_total = len(logs)
    nombres_get = 0
    nombres_post = 0
    nombres_erreurs = 0
    somme_tps = 0
    moyen_temps = 0
    statistique=[]
    liste_code=[]

    for log in logs:
        if log["methode"] == "GET":
            nombres_get += 1
        elif log["methode"] == "POST":
            nombres_post += 1

        if log["code"] in code_erreurs:
            nombres_erreurs += 1

        somme_tps += log["temps"]
        trouvé=False
        for code in liste_code:
       
         if code["code"] == log["code"]:
           code["nbre_requête"]+=1
           trouvé=True
           break

        if not trouvé:
         liste_code.append({'code':log["code"],
                         'nbre_requête':1})  

    if requests_total > 0:
        moyen_temps = somme_tps / requests_total

    
    statistique.append({
    "Nombre total de requêtes": requests_total,
    "Nombre de requêtes GET": nombres_get,
    "Nombre de requêtes POST": nombres_post,
    "Nombre d'erreurs": nombres_erreurs,
    "Temps moyen": f"{moyen_temps:.2f} ms"
   })
    return statistique ,liste_code


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
   nmbre_erreurs = statistique(logs_valides)[1]
   temps_moyen = statistique(logs_valides)[0][0]["Temps moyen"]


   rapport_fichier['Fichier'] = fichier
   rapport_fichier['Nombre de lignes lues'] = nmbre_lignes_lues
   rapport_fichier['Nombre de lignes valides'] = nmbre_lignes_valides
   rapport_fichier['Nombre de lignes invalides'] = nmbre_lignes_invalides
   rapport_fichier['Nombre d’erreurs HTTP'] = nmbre_erreurs
   rapport_fichier['Temps moyen de réponse du fichier'] = temps_moyen

   return rapport_fichier


def export_lignes_invalides(fichier, lignes_invalides):
   nom, extension = fichier.split('.')
   with open ('lignes_invalides_' +nom+ ".txt", 'w', encoding = 'utf-8') as f:
      f.write(f"EXPORT DES LIGNES INVALIDES DU FICHIER: {fichier}\n")
      f.write("===================================================\n\n")
      for dictionnaire in lignes_invalides:
            for element in dictionnaire:
                f.write(f"{(element+':'):<15} {dictionnaire[element]}\n")
                f.write("="*len(element))
                f.write("\n")
            f.write("\n*****************************************************\n")


def calcul_statistique(logs):

    requests_total = len(logs)
    nombres_get = 0
    nombres_post = 0
    nombres_erreurs = 0
    somme_tps = 0
    moyen_temps = 0
    result_statistique = ""
    liste_code = []

    for log in logs:
        if log["methode"] == "GET":
            nombres_get += 1
        elif log["methode"] == "POST":
            nombres_post += 1

        if log["code"] in code_erreurs:
            nombres_erreurs += 1

        somme_tps += log["temps"]

        code_trouvé = False
        for code in liste_code:
       
         if code["code"] == log["code"]:
           code["nbre_requête"]+=1
           code_trouvé = True
           break

        if not code_trouvé:
         liste_code.append({'code':log["code"],'nbre_requête':1})  

    if requests_total > 0:
        moyen_temps = somme_tps / requests_total

    result_statistique+=f"\n STATISTIQUE\nNombre total de requêtes: {requests_total}\nNombre de requêtes GET: {nombres_get}\nNombre de requêtes POST: {nombres_post}\nNombre d'erreurs: {nombres_erreurs}\nTemps moyen:{moyen_temps:.2f} ms\n"
    
    result_statistique+=f"\nNOMBRE DE REQUETE HTTP PAR CODE\n\n"
    for code in liste_code:
     result_statistique+=f"\n--------------------------------------------------------------\ncode:{code['code']}\n {code['nbre_requête']} requête(s)"
    
    return result_statistique