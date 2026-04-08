from analyse_avancé import analyse_avancee
from statistique import calcul_statistique

#print(analyse_avancee())

with open('rapport.txt','w',encoding='utf-8')  as f:
    Message1 = analyse_avancee()
    f.write(f"ANALYSE AVANCE\n\n")
    f.write(Message1)


