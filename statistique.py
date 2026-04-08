code_erreurs = [404, 500]

def calcul_statistique(logs):

    requests_total = len(logs)
    nombres_get = 0
    nombres_post = 0
    nombres_erreurs = 0
    somme_tps = 0
    moyen_temps = 0
    result_statistique = dict()
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
         liste_code.append({'code':log["code"],
                         'nbre_requête':1})  

    if requests_total > 0:
        moyen_temps = somme_tps / requests_total

    result_statistique['Nombre total de requêtes']= requests_total
    result_statistique['Nombre de requêtes GET']= nombres_get
    result_statistique['Nombre de requêtes POST']= nombres_post
    result_statistique['Nombre d erreurs'] = nombres_erreurs
    result_statistique['Temps moyen'] = f"{round(moyen_temps,2)}ms"
    
    code_str=""
    for code in liste_code:
     code_str+=f"{code['code']} a effectué {code['nbre_requête']} requête(s)\n"
    result_statistique['codes'] = code_str
    return result_statistique