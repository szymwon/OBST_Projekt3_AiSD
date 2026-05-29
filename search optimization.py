# -*- coding: utf-8 -*-

def loadFile(fileName):
    """"""
    itemsDict ={}
    # file = open(nazwa_pliku,"r")3
    try:
        with open(fileName, "r") as file:
            for line in file:
                line.strip()
                if line == "": #bullet-proofing for empty lines
                    continue
                separated_line = line.split(",")
                itemsDict[separated_line[0]] = separated_line[1]
    except Exception:
        print(f"Błąd wczytania pliku {fileName}")
        raise



#
# with open("items.csv", "r") as file:
#     items = file.

# items_dic = {}


# for item,freq in items:



print(items)