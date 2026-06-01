# -*- coding: utf-8 -*-
from steam_market_classes import *
# from matlibplot import *


#tworzenie obiektu
market = steam_market()
#ladowanie pliku do obiektu
market.loadFile("items_copy.csv")

#tworzenie drzew: binarnego i zwyklego
# print()
market.basicBinaryTree()
market.optimizedBinaryTree()

#wyswietlanie drzew
# market.drawBasicTree()
# market.drawOptimizedTree()

#wyszukiwanie przedmiotu
# itemName = str(input("Podaj nazwę przedmiotu który chcesz wyszukać: "))
# itemName = "Sawed-Off - Copper"
itemName = "eSports 2014 Summer Case"
# itemName = "SCAR-20 | Grotto"

print("Normalne wyszukiwanie")
found, steps_basic, path_basic = market.searchPhrase(itemName)
print("Przeszukiwanie zoptymalizowanego drzewa poszukiwań")
found_opt, steps_opt = market.searchOptimizedTree(itemName)

#eksport drzew do PNG
market.exportBasicTreeToPng("basic_tree.png", highlight_path_ids=path_basic)
market.exportOptimizedTreeToPng("optimized_tree.png", item_name=itemName)

# print(market.getItemsList())