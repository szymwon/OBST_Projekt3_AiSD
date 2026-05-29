# -*- coding: utf-8 -*-

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
            middleItemIndex = len(itemsList) // 2

            node = treeNode(itemsList[middleItemIndex][0],itemsList[middleItemIndex][1])
            node.left(balancedTree(itemsList[:middleItemIndex]))
            node.right(balancedTree(itemsList[middleItemIndex + 1:]))

            return node
        if len(self.wholeList) == 0:
            self.wholeList = [(self.itemNames[i], self.frequencies[i]) for i in range(self.listLength)]

        self.basicTreeRoot = balancedTree(self.wholeList)



    def searchBinaryTree(self):
        """Method for crating and printing optimized binary tree."""
        pass


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
        lib_node = Node(f"{current_node.key} ({current_node.frequency})")

        # Rekurencyjnie tłumaczymy lewą i prawą gałąź
        lib_node.left = self._convert_to_library_node(current_node.left)
        lib_node.right = self._convert_to_library_node(current_node.right)

        return lib_node

    def drawTreeWithLibrary(self):
        """Wyświetla główne drzewo za pomocą biblioteki binarytree."""
        if self.basic_root is None:
            print("Drzewo jest puste!")
            return

        drzewo_do_druku = self._convert_to_library_node(self.basic_root)
        print(drzewo_do_druku)


market = steam_market()
market.loadFile("items.csv")
# print(market.getItemsList())