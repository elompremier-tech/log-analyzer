code_erreurs = [404, 500]

def securite_analyse(logs):
    ip_suspecte_trouve = False
    erreur_ip = {}
    tentatives_connexion = 0
    compteur = 0
    nbre_requête_ip = {}
    Message_à_afficher = ""

    for log in logs:
        if log["code"] in code_erreurs:
            adresse_ip = log["ip"]
            erreur_ip[adresse_ip] = erreur_ip.get(adresse_ip, 0) + 1

        if log["methode"] == "POST" and log["url"] == "/login":
            tentatives_connexion += 1

        if log["ip"] in nbre_requête_ip:
            nbre_requête_ip[log['ip']]+=1
        else:
            nbre_requête_ip[log['ip']] = 1       

    Message_à_afficher+=f"Analyse de securite\n\n"
    Message_à_afficher+=f" \nIP SUSPECTS:\n\n"

    
    for ip, nombre_essaie in erreur_ip.items():
        if nombre_essaie >= 2:
            Message_à_afficher+=f"{ip} est suspecte\n\n"
            ip_suspecte_trouve = True

    if not ip_suspecte_trouve:
        Message_à_afficher+=f"Aucun IP suspecte"

    nbre_requête_ip_ordoné = dict(sorted(nbre_requête_ip.items(), key=lambda x:x[1],reverse=True))

    Message_à_afficher+=f"\n les 03 IP les plus actives\n"

    for ip, nbre_requête in nbre_requête_ip_ordoné.items():
        compteur+=1
        Message_à_afficher+=f"{ip}: {nbre_requête} requête\n\n"  
        if compteur == 3:
            break  

    Message_à_afficher+=f"Nombre de tentatives de connexion : {tentatives_connexion}"
    
    
    return Message_à_afficher
