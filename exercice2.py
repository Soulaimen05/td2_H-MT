
stock = [8, 9]                 
cout = [[5, 3, 4],             
        [6, 7, 2]]             
demande = [4, 5, 8]             

magasin = [0] * 4 + [1] * 5 + [2] * 8


def cout_total(sol):
    return sum(cout[sol[k] - 1][magasin[k]] for k in range(len(sol)))


def est_valide(sol):
    return sol.count(1) <= stock[0] and sol.count(2) <= stock[1]


def voisins(sol):
    res = []
    for k in range(len(sol)):
        v = sol[:]
        v[k] = 3 - sol[k]              
        if est_valide(v):
            res.append(v)
    for k in range(len(sol)):
        for l in range(k + 1, len(sol)):
            if sol[k] != sol[l]:
                v = sol[:]
                v[k], v[l] = v[l], v[k]
                res.append(v)
    return res


def taboue(sol, iterations=30, taille_liste=10):
    meilleur = sol
    liste_taboue = [sol]
    for _ in range(iterations):
        # voisins non tabous
        candidats = [v for v in voisins(sol) if v not in liste_taboue]
        if not candidats:
            break
        sol = min(candidats, key=cout_total)     
        liste_taboue.append(sol)
        if len(liste_taboue) > taille_liste:
            liste_taboue.pop(0)                 
        if cout_total(sol) < cout_total(meilleur):
            meilleur = sol
    return meilleur



initiale = [1] * 8 + [2] * 9
print("Coût initial :", cout_total(initiale))

best = taboue(initiale)
print("Coût minimal :", cout_total(best))

for d in (1, 2):
    ligne = [sum(1 for k in range(17) if best[k] == d and magasin[k] == m)
             for m in range(3)]
    print(f"D{d} envoie (M1, M2, M3) :", ligne)
