#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from steam_market_classes import steam_market

market = steam_market()
market.loadFile('items_copy0.csv')
print("Plik załadowany")

market.basicBinaryTree()
market.optimizedBinaryTree()
print("Drzewa zbudowane")

try:
    market.exportBasicTreeToPng('basic_tree.png', item_name='M4A4 | Asiimov')
    print("Basic tree PNG - OK (highlighted search path)")
except Exception as e:
    print(f"Basic tree błąd: {type(e).__name__}: {e}")

try:
    market.exportOptimizedTreeToPng('optimized_tree.png', item_name='M4A4 | Asiimov')
    print("Optimized tree PNG - OK (highlighted search path)")
except Exception as e:
    print(f"Optimized tree błąd: {type(e).__name__}: {e}")

import os
print(f"basic_tree.png exists: {os.path.exists('basic_tree.png')}")
print(f"optimized_tree.png exists: {os.path.exists('optimized_tree.png')}")

