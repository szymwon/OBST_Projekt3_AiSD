# -*- coding: utf-8 -*-
from steam_market_classes import *
# from matlibplot import *


#tworzenie obiektu
market = steam_market()
#ladowanie pliku do obiektu
market.loadFile("items_copy0.csv")

#tworzenie drzew: binarnego i zwyklego
# print()
market.basicBinaryTree()
market.optimizedBinaryTree()

#wyswietlanie drzew
market.drawBasicTree()
market.drawOptimizedTree()

#wyszukiwanie przedmiotu
# itemName = str(input("Podaj nazwę przedmiotu który chcesz wyszukać: "))
# itemName = "Sawed-Off - Copper"
itemName = "SCAR-20 | Grotto"

print("Normalne wyszukiwanie")
market.searchPhrase(itemName)
print("Przeszukiwanie zoptymalizowanego drzewa poszukiwań")
market.searchOptimizedTree(itemName)

#eksport drzew do PNG
market.exportBasicTreeToPng("basic_tree.png", item_name=itemName)
market.exportOptimizedTreeToPng("optimized_tree.png", item_name=itemName)
print("Drzewa wyeksportowane do PNG! (ścieżki podświetlone)")
# print(market.searchOptimizedTree(itemName))

# print(market.getItemsList())