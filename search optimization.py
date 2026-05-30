# -*- coding: utf-8 -*-
from turtledemo.clock import jump

from binarytree import Node

class treeNode:
    def __init__(self, itemName, frequency):
        self.itemName = itemName
        self.frequency = frequency
        self.left = None
        self.right = None

class steam_market:
    def __init__(self):
        self.listLength = 0
        self.itemNames=[]
        self.frequencies=[]
        self.wholeList = []
        self.basicTreeRoot = None
        self.optimizedTreeRoot = None


    def loadFile(self,fileName):
        """Splitting items and frequencies from file to 2 different alphabetically sorted lists without changing frequencies index."""
        temp_items = []
        try:
            with open(fileName, "r") as file:
                for line in file:
                    line = line.strip()
                    if line == "": #bullet-proofing for empty lines
                        continue
                    separated_line = line.split(",")
                    item = separated_line[0]
                    freq = int(separated_line[1].strip())
                    temp_items.append((item,freq))

                temp_items.sort(key=lambda tuple: tuple[0])
                self.itemNames = [line_tuple[0] for line_tuple in temp_items]
                self.frequencies = [line_tuple[1] for line_tuple in temp_items]
                self.listLength = len(self.itemNames)

        except Exception:
            print(f"Błąd wczytania pliku \"{fileName}\"")
            raise


    def getItemsList(self):
        """Returns list of items and frequencies"""
        if self.listLength == 0:
            fileName = str(input("Wprowadź nazwę pliku z danymi: "))
            self.loadFile(fileName)
        for i in range(len(self.itemNames)):
            self.wholeList.append((self.itemNames[i], self.frequencies[i]))
        return self.wholeList

    def basicBinaryTree(self):
        """Method for crating and printing basic binary tree."""
        if self.listLength == 0:
            return None

        def balancedTree(itemsList):
            if len(itemsList) == 0:
                return None

            middleItemIndex = len(itemsList) // 2
            node = treeNode(itemsList[middleItemIndex][0],itemsList[middleItemIndex][1])
            node.left = balancedTree(itemsList[:middleItemIndex])
            node.right = balancedTree(itemsList[middleItemIndex + 1:])

            return node
        if len(self.wholeList) == 0:
            self.wholeList = [(self.itemNames[i], self.frequencies[i]) for i in range(self.listLength)]

        self.basicTreeRoot = balancedTree(self.wholeList)



    # def searchPhrase(self,phrase):
    #     """Universal method for searching an item in tree by phrase. Method returns full phrase and steps needed for search."""
    #     if self.basicTreeRoot == None:
    #         return None, 0
    #
    #     found = []
    #     searched_phrase = phrase.lower()
    #     steps = [0]
    #
    #     def inOrderTraversal(node):
    #
    #         if node is None:
    #             return
    #         steps[0] += 1
    #         inOrderTraversal(node.left)
    #         if searched_phrase in node.itemName.lower():
    #             found.append((node.itemName, node.frequency))
    #         inOrderTraversal(node.right)
    #
    #     inOrderTraversal(self.basicTreeRoot)
    #
    #     if not found:
    #         print("Nie znaleziono danej rzeczy!")
    #     else:
    #         print("Znalezione itemy: ")
    #
    #         print("-----------------------------------")
    #         for item in found:
    #             print(f"Nazwa: {item[0]}")
    #             print(f"Częstotliwość wyszukiwania: {item[1]}",end="\n-----------------------------------\n")
    #         # print(str(item[0] for item in found)
    #         print(f"Liczba kroków: {steps}")
    #     return found, steps[0]
    def searchPhrase(self, phrase):
        """Wyszukuje pierwszy pasujący skin i natychmiast przerywa działanie drzewa."""
        if self.basicTreeRoot is None:
            return [], 0

        found = []
        searched_phrase = phrase.lower()
        steps = [0]

        print(f"\n[SYSTEM] Szukam TYLKO PIERWSZEGO dopasowania dla frazy: '{phrase}'")
        print("-" * 55)

        def inOrderTraversal(node):
            if node is None:
                return False # Ściana. Zwracamy False, czyli "szukaj dalej"

            # KROK A: Idziemy w lewo.
            # Jeśli lewa gałąź zwróci True (bo znalazła), my też natychmiast zwracamy True i przerywamy!
            if inOrderTraversal(node.left):
                return True

            # KROK B: Sprawdzamy obecny węzeł
            steps[0] += 1
            obecny_krok = steps[0]
            print(f" Krok {obecny_krok}: Sprawdzam węzeł -> {node.itemName}")

            if searched_phrase in node.itemName.lower():
                print(f"  >>> SUKCES! Znalazłem '{node.itemName}'. PRZERYWAM CAŁY PROCES!")
                found.append((node.itemName, node.frequency, obecny_krok))
                return True

            if inOrderTraversal(node.right):
                return True
            return False

        inOrderTraversal(self.basicTreeRoot)

        print("-" * 55)
        print("\n--- WYNIKI WYSZUKIWANIA ---")
        if not found:
            print("Brak wyników dopasowania.")
        else:
            item = found[0]
            print(f"Nazwa skina: {item[0]}")
            print(f"Popularność wyszukiwania: {item[1]}")
            print(f"Zlokalizowano i przerwano w kroku nr: {item[2]}")
            print("---------------------------")

        return found, steps[0]


    def optimizedBinaryTree(self):
        """Method for searching specific value in binary tree."""
        pass


    def searchOptimizedTree(self):
        """Method for searching specific item in optimized binary tree."""

        pass


    def costDifferenceCalculator(self):
        """Calculating difference in cost between using optimized and standard binary tree for searching same item"""
        pass

    def _convert_to_library_node(self, current_node):
        """Konwertuje nasze węzły na obiekty Node z biblioteki binarytree."""
        if current_node is None:
            return None

        # Tworzymy węzeł z biblioteki. Wrzucamy do niego nazwę i częstotliwość.
        # (W starszych wersjach biblioteki może być wymagana sama liczba, wtedy wpisz tu tylko current_node.frequency)
        lib_node = Node(f"{current_node.itemName} ({current_node.frequency})")

        # Rekurencyjnie tłumaczymy lewą i prawą gałąź
        lib_node.left = self._convert_to_library_node(current_node.left)
        lib_node.right = self._convert_to_library_node(current_node.right)

        return lib_node

    def drawTreeWithLibrary(self):
        """Wyświetla główne drzewo za pomocą biblioteki binarytree."""
        if self.basicTreeRoot is None:
            print("Drzewo jest puste!")
            return

        drzewo_do_druku = self._convert_to_library_node(self.basicTreeRoot)
        print(drzewo_do_druku)


market = steam_market()
market.loadFile("items.csv")
# Budujemy nasze drzewo
market.basicBinaryTree()

# Wyświetlamy je za pomocą biblioteki binarytree
# market.drawTreeWithLibrary()
skin = "f"
market.searchPhrase(skin)
# print(market.searchPhrase(skin))
# print(market.getItemsList())