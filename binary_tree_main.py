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
market.drawBasicTree()
market.drawOptimizedTree()

#wyszukiwanie przedmiotu
itemName = str(input("Podaj nazwę przedmiotu który chcesz wyszukać: "))
# itemName = "fade"

market.searchPhrase(itemName)

#eksport drzew do PNG
market.exportBasicTreeToPng("basic_tree.png")
market.exportOptimizedTreeToPng("optimized_tree.png")
print("Drzewa wyeksportowane do PNG!")
# print(market.searchOptimizedTree(itemName))

# print(market.getItemsList())