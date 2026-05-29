# -*- coding: utf-8 -*-

class steamMarket:
    def __init__(self):
        self.item_name=[]
        self.frequency=[]

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
                # [(awupa,500),(kosa,123),(dsaodsa,214)]
                # for line_tuple in lista: #(awupa,500)
                #   name = line_tuple[0]
                self.item_name = [line_tuple[0] for line_tuple in temp_items]
                self.frequency = [line_tuple[1] for line_tuple in temp_items]

                    # itemsDict[separated_line[0]] = int(separated_line[1].strip())
        except Exception:
            print(f"Błąd wczytania pliku \"{fileName}\"")
            raise

    def getItemsList(self):
        """Returns list of items and frequencies"""
        itemsList = []
        for item in self.item_name:
            # print(item,end=", ")
            for frequency in self.frequency:
                # print(frequency)
                itemsList.append((item,frequency))
                break
        return itemsList



# def loadFile(fileName):
#     """Loading items file to a dictionary."""
#     itemsDict ={}
#     # file = open(nazwa_pliku,"r")3
#     try:
#         with open(fileName, "r") as file:
#             for line in file:
#                 line = line.strip()
#                 if line == "": #bullet-proofing for empty lines
#                     continue
#                 separated_line = line.split(",")
#                 itemsDict[separated_line[0]] = int(separated_line[1].strip())
#         return itemsDict
#     except Exception:
#         print(f"Błąd wczytania pliku \"{fileName}\"")
#         raise



# dict = loadFile("items.csv")

market = steamMarket()
market.loadFile("items.csv")
# print(market.getItemsList())