import re

def date_valide(chaine):

    match_date = re.search(r"(\d{4})[/-](\d{2})[/-](\d{2})", chaine)
    match_heure = re.search(r"(\d{2}):(\d{2}):(\d{2})", chaine)
    
    if match_date and match_heure:
        date = match_date.group(1) +'-'+ match_date.group(2) +'-'+ match_date.group(3)
        heure = match_heure.group(1) +':'+ match_heure.group(2) +':'+ match_heure.group(3)

        if date+heure != chaine.replace(" ",""):
            return False

        return {'date':date, 'heure': heure, 'annee': int(match_date.group(1)), 'mois': int(match_date.group(2)), 'jour' :int(match_date.group(3))}
    else:
        return False
    

def ip_valide(chaine):
    """Fonction simple de test d'adresse IP. Elle prend une chaine et verifie que l'adresse
    est bien constituee d'une suite de 1 a 3 chiffres separes par des points. A ameliorer"""
    pattern_simple = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"

    if re.match(pattern_simple, chaine.replace(" ","")):
        return True
    else:
        print(chaine)
        return False
    

def recup_nombre(chaine):
    """Pour extraire le temps(separer les chiffres des lettres). La fonction prend une chaine de caracteres et retourne un entier"""
    chiffre = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    test = list(chaine)
    entier =""
    for x in test:
        if x in chiffre:
            entier+=x

    if entier != chaine.lower().replace("m","",1).replace("s","",1).replace(" ",""):
        return False

    return int(entier)