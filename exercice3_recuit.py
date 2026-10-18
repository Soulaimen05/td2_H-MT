import random
from math import exp

d = [[-1, 14, 15, -1, -1, -1, -1, 17],
     [14, -1, 13, 14, 20, -1, -1, 21],
     [15, 13, -1, 11, 21, 17,  9,  9],
     [-1, 14, 11, -1, 11, 10,  8, 20],
     [-1, 20, 21, 11, -1, 15, 18, -1],
     [-1, -1, 17, 10, 15, -1,  9, -1],
     [-1, -1,  9,  8, 18,  9, -1, 13],
     [17, 21,  9, 20, -1, -1, 13, -1]]


def longueur(ch):
    """Longueur du circuit (retour à la ville de départ compris)."""
    return sum(d[ch[i] - 1][ch[(i + 1) % 8] - 1] for i in range(8))


def est_valide(ch):
    return all(d[ch[i] - 1][ch[(i + 1) % 8] - 1] != -1 for i in range(8))


def voisins(ch):
    """Voisin = échanger 2 villes (la ville 1 reste au départ)."""
    res = []
    for i in range(1, 8):
        for j in range(i + 1, 8):
            v = ch[:]
            v[i], v[j] = v[j], v[i]
            if est_valide(v):
                res.append(v)
    return res


def recuit_simule(ch, iterations=5, T=100):
    meilleur = ch
    for i in range(iterations):
        v = random.choice(voisins(ch))           
        delta = longueur(v) - longueur(ch)
        if delta < 0 or random.random() < exp(-delta / T):
            ch = v
        if longueur(ch) < longueur(meilleur):
            meilleur = ch
        print(f"  itération {i+1} : T={T:.1f}  chemin={ch}  longueur={longueur(ch)}")
        T = T * 0.5                              
    return meilleur


random.seed(1)   #
initial = [1, 2, 3, 4, 5, 6, 7, 8]
print("Solution initiale :", initial + [1], "longueur =", longueur(initial))
print()
r = recuit_simule(initial)
print("\nMeilleur chemin :", r + [1], "longueur =", longueur(r))
