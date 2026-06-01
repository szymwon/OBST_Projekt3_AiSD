# -*- coding: utf-8 -*-
from steam_market_classes import *


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
# print(market.searchOptimizedTree(itemName))

# print(market.getItemsList())