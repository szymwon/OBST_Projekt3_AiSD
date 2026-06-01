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


    def searchPhrase(self, phrase):
        """Method search for a first item matching search phrase and returns steps needed to reach item."""
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
        n = self.listLength
        if n == 0:
            return

        # 1. Tworzymy puste macierze na costs (C) i roots (R)
        costs = [[0] * n for _ in range(n)]
        roots = [[0] * n for _ in range(n)]

        # 2. Baza DP: Wypełniamy przekątną (drzewa 1-elementowe)
        for i in range(n):
            costs[i][i] = self.frequencies[i]
            roots[i][i] = i

        # 3. Główny algorytm Programowania Dynamicznego (budujemy coraz szersze poddrzewa)
        for length in range(2, n + 1):          # 'length' to liczba elementów w poddrzewie
            for i in range(n - length + 1):     # 'i' to indeks początkowy
                j = i + length - 1              # 'j' to indeks końcowy
                costs[i][j] = float('inf')      # Ustawiamy nieskończoność jako koszt startowy

                frequencySum = sum(self.frequencies[i:j + 1])

                # Szukamy, który węzeł 'r' sprawdzi się najlepiej jako korzeń dla tego przedziału
                for r in range(i, j + 1):
                    # Zabezpieczenie przed wyjściem poza tablicę dla lewego i prawego dziecka
                    leftCost = costs[i][r - 1] if r > i else 0
                    rightCost = costs[r + 1][j] if r < j else 0

                    totalCost = leftCost + rightCost  + frequencySum

                    # Zapisujemy, jeśli znaleźliśmy lepszego kandydata na korzeń
                    if totalCost < costs[i][j]:
                        costs[i][j] = totalCost
                        roots[i][j] = r

        # 4. Rekurencyjna budowa fizycznego drzewa na podstawie macierzy korzeni (R)
        def makeTree(i, j):
            if i > j:
                return None

            # Odczytujemy indeks najlepszego korzenia z macierzy
            r = roots[i][j]
            node = treeNode(self.itemNames[r], self.frequencies[r])

            # Budujemy lewe i prawe poddrzewo
            node.left = makeTree(i, r - 1)
            node.right = makeTree(r + 1, j)

            return node

        self.optimizedTreeRoot = makeTree(0, n - 1)


    def searchOptimizedTree(self, item_name):
        """Method for searching specific item in optimized binary tree."""
        curr = self.optimizedTreeRoot
        steps = 0

        while curr is not None:
            steps += 1
            # Jeśli znaleźliśmy dokładny strzał, kończymy
            if curr.itemName == item_name:
                return curr, steps

            # Własność BST: Odrzucamy połowę drzewa przy każdym kroku!
            elif item_name < curr.itemName:
                curr = curr.left
            else:
                curr = curr.right

        # Skina nie ma w bazie
        return None, steps


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

    def drawBasicTree(self):
        """Wyświetla główne drzewo za pomocą biblioteki binarytree."""
        if self.basicTreeRoot is None:
            print("Drzewo jest puste!")
            return

        print("\nWIZUALIZACJA DRZEWA BINARNEGO (BST):")
        convertedTree = self._convert_to_library_node(self.basicTreeRoot)
        print(convertedTree )
        print("-" * 52)

    def drawOptimizedTree(self):
        """Wyświetla zoptymalizowane drzewo (OBST) za pomocą biblioteki binarytree."""
        if self.optimizedTreeRoot is None:
            print("Drzewo jest puste!")
            return

        print("\nWIZUALIZACJA ZOPTYMALIZOWANEGO DRZEWA (OBST):")

        # Używamy tego samego tłumacza, ale przekazujemy mu KORZEŃ OBST!
        convertedTree = self._convert_to_library_node(self.optimizedTreeRoot)

        print(convertedTree)
        print("-" * 52)

    def _export_tree_to_png(self, root, file_path, title):
        """Zapisuje drzewo jako obraz PNG używając matplotlib."""
        if root is None:
            raise ValueError("Drzewo jest puste!")

        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise ImportError(
                "Do eksportu PNG potrzebny jest pakiet matplotlib. "
                "Zainstaluj go poleceniem: pip install matplotlib"
            ) from exc

        positions = {}
        labels = {}
        x_counter = [0]

        def assign_positions(node, depth=0):
            if node is None:
                return

            assign_positions(node.left, depth + 1)
            positions[id(node)] = (x_counter[0], -depth)
            labels[id(node)] = f"{node.itemName}\n({node.frequency})"
            x_counter[0] += 1
            assign_positions(node.right, depth + 1)

        def draw_edges(ax, node):
            if node is None:
                return

            x, y = positions[id(node)]
            for child in (node.left, node.right):
                if child is None:
                    continue
                child_x, child_y = positions[id(child)]
                ax.plot([x, child_x], [y, child_y], color="#666666", linewidth=1.2, zorder=1)
                draw_edges(ax, child)

        def draw_nodes(ax, node):
            if node is None:
                return

            x, y = positions[id(node)]
            ax.scatter([x], [y], s=1800, color="#cfe8ff", edgecolors="#2b6cb0", linewidths=1.5, zorder=2)
            ax.text(
                x,
                y,
                labels[id(node)],
                ha="center",
                va="center",
                fontsize=9,
                zorder=3,
            )
            draw_nodes(ax, node.left)
            draw_nodes(ax, node.right)

        assign_positions(root)

        height = self._tree_height(root)
        width = max(6, x_counter[0] * 1.2)
        fig, ax = plt.subplots(figsize=(width, max(4, height * 1.6)))
        ax.set_title(title)
        ax.axis("off")

        draw_edges(ax, root)
        draw_nodes(ax, root)

        ax.relim()
        ax.autoscale_view()
        ax.margins(x=0.15, y=0.2)
        fig.savefig(file_path, dpi=200, bbox_inches="tight")
        plt.close(fig)

    def _tree_height(self, node):
        """Zwraca wysokość drzewa."""
        if node is None:
            return 0
        return 1 + max(self._tree_height(node.left), self._tree_height(node.right))

    def exportBasicTreeToPng(self, file_path="basic_tree.png"):
        """Eksportuje główne drzewo do pliku PNG."""
        self._export_tree_to_png(self.basicTreeRoot, file_path, "Basic binary tree")

    def exportOptimizedTreeToPng(self, file_path="optimized_tree.png"):
        """Eksportuje zoptymalizowane drzewo do pliku PNG."""
        self._export_tree_to_png(self.optimizedTreeRoot, file_path, "Optimized binary tree")
