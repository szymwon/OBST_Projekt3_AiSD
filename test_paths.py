#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from steam_market_classes import steam_market

market = steam_market()
market.loadFile('items_copy0.csv')
print("Plik załadowany")

market.basicBinaryTree()
market.optimizedBinaryTree()
print("Drzewa zbudowane\n")

# Test search and PNG export with path highlighting
item = 'M4A4 | Asiimov'
print(f"Szukamy: {item}")
print("="*60)

found_basic, steps_basic, path_basic = market.searchPhrase(item)
print(f"\nBasic tree: {steps_basic} kroków, ścieżka ma {len(path_basic)} węzłów")

found_opt, steps_opt = market.searchOptimizedTree(item)
print(f"Optimized tree: {steps_opt} kroków")

print("\nZnakomicie — liczby kroków powinny się różnić!")
print("="*60)

try:
    market.exportBasicTreeToPng('basic_tree_test.png', highlight_path_ids=path_basic)
    print("✓ Basic tree PNG (CZERWONA ścieżka)")
except Exception as e:
    print(f"✗ Basic tree błąd: {type(e).__name__}: {e}")

try:
    market.exportOptimizedTreeToPng('optimized_tree_test.png', item_name=item)
    print("✓ Optimized tree PNG (ZIELONA ścieżka)")
except Exception as e:
    print(f"✗ Optimized tree błąd: {type(e).__name__}: {e}")

print("\nPNG zapisane!")

