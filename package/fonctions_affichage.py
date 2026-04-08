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