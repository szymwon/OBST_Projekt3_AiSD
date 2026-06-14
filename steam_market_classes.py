# -*- coding: utf-8 -*-
from binarytree import Node

class treeNode:
    def __init__(self, itemName: str, frequency: int) -> None:
        """Initializing method"""
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
        print("\nDRZEWO BST ZOSTALO WYGENEROWANE")


    def searchPhrase(self, phrase):
        """Metoda wykorzystująca wyszukiwanie binarne w strukturze drzewa BST."""
        if self.basicTreeRoot is None:
            print("Drzewo podstawowe jest puste!")
            return [], 0, []

        searched_phrase = phrase
        obecny = self.basicTreeRoot
        kroki = 0
        found = []
        path = []

        print(f"\n[SYSTEM] Wyszukiwanie binarne dla frazy: '{phrase}'")
        print("-" * 55)

        while obecny is not None:
            kroki += 1
            path.append(obecny)
            print(f" Krok {kroki}: Sprawdzam węzeł -> {obecny.itemName}")


            if searched_phrase == obecny.itemName:
                print(f"  >>> SUKCES! Znaleziono '{obecny.itemName}'.")
                found.append((obecny.itemName, obecny.frequency, kroki))
                break


            elif searched_phrase < obecny.itemName:
                print("  --- Fraza mniejsza alfabetycznie. Skręcam w LEWO.")
                obecny = obecny.left


            else:
                print("  --- Fraza większa alfabetycznie. Skręcam w PRAWO.")
                obecny = obecny.right

        print("-" * 55)
        print("\n--- WYNIKI WYSZUKIWANIA ---")
        if not found:
            print("Brak wyników dopasowania.")
            print(f"Zakończono poszukiwania po {kroki} krokach.")
        else:
            item = found[0]
            print(f"Nazwa skina: {item[0]}")
            print(f"Popularność wyszukiwania: {item[1]}")
            print(f"Zlokalizowano w kroku nr: {item[2]}")
            print("---------------------------")

        return found, kroki, path

    def optimizedBinaryTree(self):
        """Metoda budująca optymalne drzewo poszukiwań (OBST) za pomocą Programowania Dynamicznego."""
        n = self.listLength
        if n == 0:
            return

        koszty = [[0] * n for _ in range(n)]
        korzenie = [[0] * n for _ in range(n)]

        for i in range(n):
            koszty[i][i] = self.frequencies[i]
            korzenie[i][i] = i

        for dlugosc in range(2, n + 1):
            for i in range(n - dlugosc + 1):
                j = i + dlugosc - 1
                koszty[i][j] = float('inf')

                suma_czestotliwosci = sum(self.frequencies[i:j + 1])

                for r in range(i, j + 1):
                    koszt_lewy = koszty[i][r - 1] if r > i else 0
                    koszt_prawy = koszty[r + 1][j] if r < j else 0

                    calkowity_koszt = koszt_lewy + koszt_prawy + suma_czestotliwosci

                    if calkowity_koszt < koszty[i][j]:
                        koszty[i][j] = calkowity_koszt
                        korzenie[i][j] = r

        def zbuduj_drzewo(i, j):
            if i > j:
                return None

            r = korzenie[i][j]
            wezel = treeNode(self.itemNames[r], self.frequencies[r])

            wezel.left = zbuduj_drzewo(i, r - 1)
            wezel.right = zbuduj_drzewo(r + 1, j)

            return wezel

        self.optimizedTreeRoot = zbuduj_drzewo(0, n - 1)
        print("`DRZEWO OBST ZOSTALO WYGENEROWANE \n")

    def searchOptimizedTree(self, item_name):
        """Klasyczne poszukiwanie binarne z graficznym podglądem kroków na żywo."""
        print(f"\n[SYSTEM] Szukam DOKŁADNEGO dopasowania dla: '{item_name}' w drzewie OBST...")
        print("-" * 55)

        obecny = self.optimizedTreeRoot
        kroki = 0

        while obecny is not None:
            kroki += 1
            print(f" Krok {kroki}: Sprawdzam węzeł -> {obecny.itemName}")

            if obecny.itemName == item_name:
                print(f"  >>> SUKCES! Znaleziono '{obecny.itemName}'.")
                print("-" * 55)
                print("\n--- WYNIKI WYSZUKIWANIA OBST ---")
                print(f"Nazwa skina: {obecny.itemName}")
                print(f"Popularność: {obecny.frequency}")
                print(f"Zlokalizowano w zaledwie: {kroki} krokach! (Odrzucanie gałęzi)")
                print("--------------------------------")
                return obecny, kroki

            elif item_name < obecny.itemName:
                print("  --- Fraza mniejsza alfabetycznie. Skręcam w LEWO.")
                obecny = obecny.left

            else:
                print("  --- Fraza jest większa alfabetycznie. Skręcam w PRAWO.")
                obecny = obecny.right

        print("-" * 55)
        print(f"  >>> NIE ZNALEZIONO. Dotarto do końca gałęzi po {kroki} krokach.")
        return None, kroki


    def costDifferenceCalculator(self):
        """Oblicza i porównuje oczekiwany koszt całkowity struktur BST i OBST."""
        def oblicz_koszt_drzewa(node, poziom=1):
            if node is None:
                return 0
            obecny_koszt = poziom * node.frequency
            koszt_lewy = oblicz_koszt_drzewa(node.left, poziom + 1)
            koszt_prawy = oblicz_koszt_drzewa(node.right, poziom + 1)
            return obecny_koszt + koszt_lewy + koszt_prawy

        koszt_zwykle = oblicz_koszt_drzewa(self.basicTreeRoot)
        koszt_optymalne = oblicz_koszt_drzewa(self.optimizedTreeRoot)

        print("\n" + "=" * 65)
        print(" PORÓWNANIE WYDAJNOŚCI STRUKTUR (Całkowity Oczekiwany Koszt)")
        print("=" * 65)
        print(f" Koszt podstawowego drzewa BST:   {koszt_zwykle}")
        print(f" Koszt zoptymalizowanego OBST:    {koszt_optymalne}")
        print("-" * 65)
        print(f" Zaoszczędzone operacje serwera:  {koszt_zwykle - koszt_optymalne} jednostek!")
        print("=" * 65)

    def _convert_to_library_node(self, current_node):
        """Konwertuje nasze węzły na obiekty Node z biblioteki binarytree."""
        if current_node is None:
            return None

        lib_node = Node(f"{current_node.itemName} ({current_node.frequency})")

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

        convertedTree = self._convert_to_library_node(self.optimizedTreeRoot)

        print(convertedTree)
        print("-" * 52)

    def _export_tree_to_png(self, root, file_path, title, highlight_path_ids=None, highlight_color="#ff6666"):
        """Zapisuje drzewo jako obraz PNG używając matplotlib.

        highlight_path_ids: optional set of node ids to highlight OR ordered list/tuple of nodes (path)
        highlight_color: color used for highlighted nodes/edges
        """
        if root is None:
            raise ValueError("Drzewo jest puste!")

        try:
            import matplotlib.pyplot as plt
        except ImportError as exc:
            raise ImportError(
                "Do eksportu PNG potrzebny jest pakiet matplotlib. "
                "Zainstaluj go poleceniem: pip install matplotlib"
            ) from exc

        # If user passed an ordered path (list of nodes), convert to ids and compute edges
        highlight_edges = set()
        if isinstance(highlight_path_ids, (list, tuple)):
            path_nodes = highlight_path_ids
            path_ids = [id(n) for n in path_nodes]
            for a, b in zip(path_ids, path_ids[1:]):
                highlight_edges.add((a, b))
            highlight_path_ids = set(path_ids)

        if highlight_path_ids is None:
            highlight_path_ids = set()

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

        assign_positions(root)

        def draw_edges(ax, node):
            if node is None:
                return

            x, y = positions[id(node)]
            for child in (node.left, node.right):
                if child is None:
                    continue
                child_x, child_y = positions[id(child)]
                pair = (id(node), id(child))
                if pair in highlight_edges:
                    color = highlight_color
                    lw = 2.6
                    z = 2
                else:
                    color = "#666666"
                    lw = 1.2
                    z = 1
                ax.plot([x, child_x], [y, child_y], color=color, linewidth=lw, zorder=z)
                draw_edges(ax, child)

        def draw_nodes(ax, node):
            if node is None:
                return

            x, y = positions[id(node)]
            nid = id(node)
            if nid in highlight_path_ids:
                node_color = highlight_color
                edge_color = "#333333"
                size = 2400
                text_color = "black"
            else:
                node_color = "#cfe8ff"
                edge_color = "#2b6cb0"
                size = 1800
                text_color = "black"

            ax.scatter([x], [y], s=size, color=node_color, edgecolors=edge_color, linewidths=1.5, zorder=3)
            ax.text(
                x,
                y,
                labels[nid],
                ha="center",
                va="center",
                fontsize=9,
                zorder=4,
                color=text_color,
            )
            draw_nodes(ax, node.left)
            draw_nodes(ax, node.right)


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

    def get_search_path_basic(self, item_name):
        """Wykonuje wyszukiwanie w podstawowym drzewie (BST) i zwraca listę odwiedzonych węzłów (kolejność)."""
        path = []
        curr = self.basicTreeRoot
        while curr is not None:
            path.append(curr)
            if curr.itemName == item_name:
                return path, True
            if item_name < curr.itemName:
                curr = curr.left
            else:
                curr = curr.right
        return path, False

    def exportBasicTreeToPng(self, file_path="basic_tree.png", item_name=None, highlight_path_ids=None):
        """Eksportuje główne drzewo do pliku PNG. 
        Jeśli podano highlight_path_ids (lista węzłów), podświetla ścieżkę na czerwono."""
        highlight = highlight_path_ids
        if highlight is None and item_name is not None:
            path, found = self.get_search_path_basic(item_name)
            highlight = path
        self._export_tree_to_png(self.basicTreeRoot, file_path, "Basic binary tree", highlight_path_ids=highlight, highlight_color="#ff6666")

    def get_search_path_optimized(self, item_name):
        """Wykonuje wyszukiwanie w zoptymalizowanym drzewie (BST) i zwraca listę odwiedzonych węzłów (kolejność)."""
        path = []
        curr = self.optimizedTreeRoot
        while curr is not None:
            path.append(curr)
            if curr.itemName == item_name:
                return path, True
            if item_name < curr.itemName:
                curr = curr.left
            else:
                curr = curr.right
        return path, False

    def exportOptimizedTreeToPng(self, file_path="optimized_tree.png", item_name=None):
        """Eksportuje zoptymalizowane drzewo do pliku PNG. Jeśli podano item_name, podświetla ścieżkę wyszukiwania na zielono."""
        highlight = None
        if item_name is not None:
            path, found = self.get_search_path_optimized(item_name)
            highlight = path
        self._export_tree_to_png(self.optimizedTreeRoot, file_path, "Optimized binary tree", highlight_path_ids=highlight, highlight_color="#66cc66")
