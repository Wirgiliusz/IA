import copy
from itertools import permutations
import math
import timeit
from numpy import random
import numpy as np
import random


def loadDataB(path):
    plik = open(path, "r")
    linie = plik.readlines()
    n = int(linie[1].split()[0])
    m = int(linie[1].split()[1])

    zadania = []
    for i in range(2, n+2):
        linia = linie[i].split()
        maszyny = []
        for j in range(1, 2*m, 2):
            maszyny.append(int(linia[j]))
        maszyny.append(i-1)
        zadania.append(maszyny)
    plik.close()

    return zadania

def calculate_Cmax(zad):
    if len(zad) == 0:
        return math.inf

    S = []
    C = []
    Szad = []
    Czad = []

    Szad.append(0)
    Czad.append(zad[0][0])

    for i in range(0, len(zad)):
        for j in range(0, len(zad[i])-1):
            if i == 0 and j != 0:
                Szad.append(Czad[j-1])
                Czad.append(Szad[j] + zad[i][j])
            elif i != 0:
                if j == 0:
                    Szad.append(C[i-1][0])
                    Czad.append(Szad[0] + zad[i][0])
                else:
                    Szad.append(max(Czad[j-1], C[i-1][j]))
                    Czad.append(Szad[j] + zad[i][j])

        S.append(Szad.copy())
        C.append(Czad.copy())
        Szad.clear()
        Czad.clear()

    return C[-1][-1]

def IA(zad):
    wyspy = []
    populacja = []
    iloscWysp = 5
    wielkoscPopulacji = 50
    liczbaEpok = 100

    for i in range(0, iloscWysp):
        for j in range(0, wielkoscPopulacji):
            populacja.append(np.random.permutation(zad))
        wyspy.append(populacja)
        populacja.clear()

    for i in range(0, liczbaEpok):
        akcjaNaWyspie(wyspy)
        if not i % 4:
            migracjeNaWyspy(wyspy)

    return znajdzNajlepszegoOsobnika(wyspy)

def akcjaNaWyspie(wyspy):
    krzyzowanie(wyspy)
    mutacje(wyspy)

def krzyzowanie(wyspy):
    nowaPopulacja = []

    for wyspa in wyspy:
        for indeks in range(0, len(wyspa)):
            if indeks == 0:
                nowaPopulacja.append(krzyzujOsobniki(wyspa[indeks], wyspa[-1]))
                nowaPopulacja.append(krzyzujOsobniki(wyspa[-1], wyspa[indeks]))
            else:
                nowaPopulacja.append(krzyzujOsobniki(wyspa[indeks-1], wyspa[indeks]))
                nowaPopulacja.append(krzyzujOsobniki(wyspa[indeks], wyspa[indeks-1]))
        
        wyspa = copy.deepcopy(nowaPopulacja)
        nowaPopulacja.clear()
        # Czy na pewno podmieniaja sie wyzsze wyspy? Czy trzeba return?

def krzyzujOsobniki(osobnik1, osobnik2):
    nowyOsobnik = []
    for i in range(0, len(osobnik1)/2):
        nowyOsobnik.append(osobnik1[i])
    for i in range(0, len(osobnik2)):
        if osobnik2[i] not in nowyOsobnik:
            nowyOsobnik.append(osobnik2[i])

    return nowyOsobnik

def mutacje(wyspy):
    procentMutacji = 0.03
    for wyspa in wyspy:
        for indeks in range(0, len(wyspa)):
            prawdopodobienstwoMutacji = random.random()
            if prawdopodobienstwoMutacji <= procentMutacji:
                gen1 = random.randint(0, len(wyspa[0])-1)
                gen2 = random.randint(0, len(wyspa[0])-1)
                moveSwap(wyspa[indeks], gen1, gen2)

        # Czy na pewno podmieniaja sie wyzsze wyspy? Czy trzeba return?

def moveSwap(osobnik, i, j):
    osobnik[i], osobnik[j] = osobnik[j], osobnik[i]

def migracjeNaWyspy(wyspy):
    iloscEmigrantow = 2

    for indeks, wyspa in enumerate(wyspy):
        for i in range(0, iloscEmigrantow):
            numerOsobnika = random.randint(0, len(wyspa)-1)
            moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[indeks-1], numerOsobnika)
            numerOsobnika = random.randint(0, len(wyspa)-1)
            if indeks+1 > len(wyspy):
                moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[0], numerOsobnika)
            else:
                moveSwapPomiedzyWyspami(wyspy[indeks], wyspy[indeks+1], numerOsobnika)

def moveSwapPomiedzyWyspami(wyspa1, wyspa2, numerOsobnika):
    wyspa1[numerOsobnika], wyspa2[numerOsobnika] = wyspa2[numerOsobnika], wyspa1[numerOsobnika]

def znajdzNajlepszegoOsobnika(wyspy):
    Cmin = math.inf
    najlepszyOsobnik = None

    for wyspa in wyspy:
        for osobnik in wyspa:
            C = calculate_Cmax(osobnik)
            if C < Cmin:
                Cmin = C
                najlepszyOsobnik = osobnik
    
    return najlepszyOsobnik