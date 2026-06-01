# -*- coding: utf-8 -*-
from steam_market_classes import *


market = steam_market()
market.loadFile("items_copy.csv")
# Budujemy nasze drzewo
market.basicBinaryTree()

# Wyświetlamy je za pomocą biblioteki binarytree
# market.drawTreeWithLibrary()
skin = "fade"
market.optimizedBinaryTree()
# market.searchPhrase(skin)
# print(market.searchOptimizedTree("fade"))
market.drawBasicTree()
market.drawOptimizedTree()
# print(market.searchPhrase(skin))
# print(market.getItemsList())