
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
            print(f"B??d wczytania pliku \"{fileName}\"")
            raise


    def getItemsList(self):
        """Returns list of items and frequencies"""
        if self.listLength == 0:
            fileName = str(input("Wprowad? nazw? pliku z danymi: "))
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
                return False # ?ciana. Zwracamy False, czyli "szukaj dalej"

            # KROK A: Idziemy w lewo.
            # Je?li lewa ga??? zwr?ci True (bo znalaz?a), my te? natychmiast zwracamy True i przerywamy!
            if inOrderTraversal(node.left):
                return True

            # KROK B: Sprawdzamy obecny w?ze?
            steps[0] += 1
            obecny_krok = steps[0]
            print(f" Krok {obecny_krok}: Sprawdzam w?ze? -> {node.itemName}")

            if searched_phrase in node.itemName.lower():
                print(f"  >>> SUKCES! Znalaz?em '{node.itemName}'. PRZERYWAM CA?Y PROCES!")
                found.append((node.itemName, node.frequency, obecny_krok))
                return True

            if inOrderTraversal(node.right):
                return True
            return False

        inOrderTraversal(self.basicTreeRoot)

        print("-" * 55)
        print("\n--- WYNIKI WYSZUKIWANIA ---")
        if not found:
            print("Brak wynik?w dopasowania.")
        else:
            item = found[0]
            print(f"Nazwa skina: {item[0]}")
            print(f"Popularno?? wyszukiwania: {item[1]}")
            print(f"Zlokalizowano i przerwano w kroku nr: {item[2]}")
            print("---------------------------")

        return found, steps[0]


    def optimizedBinaryTree(self):
        """Method for searching specific value in binary tree."""
        """Metoda buduj?ca optymalne drzewo poszukiwa? (OBST) za pomoc? Programowania Dynamicznego."""
        n = self.listLength
        if n == 0:
            return

        # 1. Tworzymy puste macierze na koszty (C) i korzenie (R)
        koszty = [[0] * n for _ in range(n)]
        korzenie = [[0] * n for _ in range(n)]

        # 2. Baza DP: Wype?niamy przek?tn? (drzewa 1-elementowe)
        for i in range(n):
            koszty[i][i] = self.frequencies[i]
            korzenie[i][i] = i

        # 3. G??wny algorytm Programowania Dynamicznego (budujemy coraz szersze poddrzewa)
        for dlugosc in range(2, n + 1):          # 'dlugosc' to liczba element?w w poddrzewie
            for i in range(n - dlugosc + 1):     # 'i' to indeks pocz?tkowy
                j = i + dlugosc - 1              # 'j' to indeks ko?cowy
                koszty[i][j] = float('inf')      # Ustawiamy niesko?czono?? jako koszt startowy

                suma_czestotliwosci = sum(self.frequencies[i:j + 1])

                # Szukamy, kt?ry w?ze? 'r' sprawdzi si? najlepiej jako korze? dla tego przedzia?u
                for r in range(i, j + 1):
                    # Zabezpieczenie przed wyj?ciem poza tablic? dla lewego i prawego dziecka
                    koszt_lewy = koszty[i][r - 1] if r > i else 0
                    koszt_prawy = koszty[r + 1][j] if r < j else 0

                    calkowity_koszt = koszt_lewy + koszt_prawy + suma_czestotliwosci

                    # Zapisujemy, je?li znale?li?my lepszego kandydata na korze?
                    if calkowity_koszt < koszty[i][j]:
                        koszty[i][j] = calkowity_koszt
                        korzenie[i][j] = r

        # 4. Rekurencyjna budowa fizycznego drzewa na podstawie macierzy korzeni (R)
        def zbuduj_drzewo(i, j):
            if i > j:
                return None

            # Odczytujemy indeks najlepszego korzenia z macierzy
            r = korzenie[i][j]
            wezel = treeNode(self.itemNames[r], self.frequencies[r])

            # Budujemy lewe i prawe poddrzewo
            wezel.left = zbuduj_drzewo(i, r - 1)
            wezel.right = zbuduj_drzewo(r + 1, j)

            return wezel

        self.optimizedTreeRoot = zbuduj_drzewo(0, n - 1)


    def searchOptimizedTree(self, item_name):
        """Method for searching specific item in optimized binary tree."""
        obecny = self.optimizedTreeRoot
        kroki = 0

        while obecny is not None:
            kroki += 1
            # Je?li znale?li?my dok?adny strza?, ko?czymy
            if obecny.itemName == item_name:
                return obecny, kroki

            # W?asno?? BST: Odrzucamy po?ow? drzewa przy ka?dym kroku!
            elif item_name < obecny.itemName:
                obecny = obecny.left
            else:
                obecny = obecny.right

        # Skina nie ma w bazie
        return None, kroki


    def costDifferenceCalculator(self):
        """Calculating difference in cost between using optimized and standard binary tree for searching same item"""
        pass

    def _convert_to_library_node(self, current_node):
        """Konwertuje nasze w?z?y na obiekty Node z biblioteki binarytree."""
        if current_node is None:
            return None

        # Tworzymy w?ze? z biblioteki. Wrzucamy do niego nazw? i cz?stotliwo??.
        # (W starszych wersjach biblioteki mo?e by? wymagana sama liczba, wtedy wpisz tu tylko current_node.frequency)
        lib_node = Node(f"{current_node.itemName} ({current_node.frequency})")

        # Rekurencyjnie t?umaczymy lew? i praw? ga???
        lib_node.left = self._convert_to_library_node(current_node.left)
        lib_node.right = self._convert_to_library_node(current_node.right)

        return lib_node

    def drawBasicTree(self):
        """Wy?wietla g??wne drzewo za pomoc? biblioteki binarytree."""
        if self.basicTreeRoot is None:
            print("Drzewo jest puste!")
            return

        print("\nWIZUALIZACJA DRZEWA BINARNEGO (BST):")
        convertedTree = self._convert_to_library_node(self.basicTreeRoot)
        print(convertedTree )
        print("-" * 52)

    def drawOptimizedTree(self):
        """Wy?wietla zoptymalizowane drzewo (OBST) za pomoc? biblioteki binarytree."""
        if self.optimizedTreeRoot is None:
            print("Drzewo jest puste!")
            return

        print("\nWIZUALIZACJA ZOPTYMALIZOWANEGO DRZEWA (OBST):")

        # U?ywamy tego samego t?umacza, ale przekazujemy mu KORZE? OBST!
        convertedTree = self._convert_to_library_node(self.optimizedTreeRoot)

        print(convertedTree)
        print("-" * 52)