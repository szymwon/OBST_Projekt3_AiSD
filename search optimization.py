# -*- coding: utf-8 -*-

def loadFile(fileName):
    """Loading items file to a dictionary."""
    itemsDict ={}
    # file = open(nazwa_pliku,"r")3
    try:
        with open(fileName, "r") as file:
            for line in file:
                line = line.strip()
                if line == "": #bullet-proofing for empty lines
                    continue
                separated_line = line.split(",")
                itemsDict[separated_line[0]] = int(separated_line[1].strip())
        return itemsDict
    except Exception:
        print(f"Błąd wczytania pliku \"{fileName}\"")
        raise



dict = loadFile("items.csv")