# -*- coding: utf-8 -*-
# 14. Optymalne drzewa poszukiwań

def sum_freq(freq, i, j):
    """Pomocnicza funkcja licząca sumę częstotliwości w przedziale."""
    return sum(freq[i:j + 1])


def optimal_search_tree(keys, freq):
    """
    Algorytm programowania dynamicznego do budowy Optymalnego Drzewa Poszukiwań.
    Zwraca minimalny oczekiwany koszt wyszukiwania.
    """
    n = len(keys)
    # Tworzymy macierz kosztów. cost[i][j] to optymalny koszt dla elementów od i do j.
    # Inicjujemy ją zerami.
    cost = [[0 for _ in range(n)] for _ in range(n)]

    # Przypadek bazowy: koszt dla pojedynczego elementu to po prostu jego częstotliwość (poziom 1)
    for i in range(n):
        cost[i][i] = freq[i]

    # L to długość sprawdzanego łańcucha elementów (od 2 do n)
    for L in range(2, n + 1):
        for i in range(n - L + 1):
            j = i + L - 1
            cost[i][j] = float('inf') # Ustawiamy początkowo na nieskończoność

            # Suma wyszukiwań w obecnym podzbiorze 
            # (dodajemy ją, bo wybierając korzeń, cała reszta spada o 1 poziom w dół)
            f_sum = sum_freq(freq, i, j)

            # Testujemy każdy element 'r' jako potencjalny korzeń w przedziale i..j
            for r in range(i, j + 1):
                # Koszt lewego poddrzewa
                c_left = cost[i][r - 1] if r > i else 0
                # Koszt prawego poddrzewa
                c_right = cost[r + 1][j] if r < j else 0

                # Całkowity koszt = lewe poddrzewo + prawe poddrzewo + przesunięcie wszystkich w dół
                c_total = c_left + c_right + f_sum

                # Zapisujemy najlepszy wynik dla tego przedziału
                if c_total < cost[i][j]:
                    cost[i][j] = c_total

    return cost[0][n - 1]

# --- SYMULACJA SYSTEMU RYNKU STEAM ---

# 1. Dane wejściowe (muszą być posortowane alfabetycznie jako klucze BST)
keys = [
    "AK-47 Slate",        # Indeks 0
    "AWP Dragon Lore",    # Indeks 1
    "Karambit Fade",      # Indeks 2
    "Kilowatt Case",      # Indeks 3
    "M4A4 Asiimov"        # Indeks 4
]

# 2. Częstotliwości zapytań (np. na godzinę) odpowiadające posortowanym kluczom
freq = [
    2000, # AK-47 Slate
    5,    # AWP Dragon Lore (bardzo rzadko szukany)
    50,   # Karambit Fade
    5000, # Kilowatt Case (najczęstszy obrót na rynku)
    800   # M4A4 Asiimov
]

# 3. Naiwne porównanie - co by było w standardowym, zbalansowanym drzewie?
# Zbalansowane drzewo z 5 elementów miałoby korzeń w środku (indeks 2: Karambit), 
# dzieci na poziomie 2 (AK-47 i Kilowatt) oraz dzieci na poziomie 3 (AWP i M4A4).
# Koszt naiwny = freq * poziom_w_drzewie
naive_cost = (freq[2] * 1) + (freq[0] * 2) + (freq[3] * 2) + (freq[1] * 3) + (freq[4] * 3)

# 4. Uruchomienie naszego algorytmu
optimized_cost = optimal_search_tree(keys, freq)

# 5. Wyświetlenie wyników (idealne do screena w dokumentacji)
print("="*50)
print("SYMULACJA WYSZUKIWARKI RYNKU STEAM (OBST)")
print("="*50)
print("Dane zapytań (ostatnia godzina):")
for i in range(len(keys)):
    print(f"- {keys[i]}: {freq[i]} zapytań")
print("-" * 50)
print(f"Oczekiwany koszt (Standardowe Drzewo Zbalansowane): {naive_cost} operacji")
print(f"Oczekiwany koszt (Optymalne Drzewo Poszukiwań):    {optimized_cost} operacji")
print("-" * 50)
savings = round(((naive_cost - optimized_cost) / naive_cost) * 100, 2)
print(f"Oszczędność czasu procesora: {savings}% !")
print("="*50)