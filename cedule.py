import random
from itertools import product

CAPACITES = [20, 15, 35, 40, 15, 15, 10]
DEMANDES = [80, 90, 65, 70]

PUISSANCE_TOTALE = sum(CAPACITES)
NB_UNITES = 7
NB_INTERVALLES = 4

GENES_2_INTERVALLES = ["1100", "0110", "0011"]
GENES_1_INTERVALLE = ["1000", "0100", "0010", "0001"]

GENES_PAR_UNITE = [
    GENES_2_INTERVALLES,
    GENES_2_INTERVALLES,
    GENES_1_INTERVALLE,
    GENES_1_INTERVALLE,
    GENES_1_INTERVALLE,
    GENES_1_INTERVALLE,
    GENES_1_INTERVALLE,
]

TAILLE_POPULATION = 49
NOMBRE_GENERATIONS = 200
PC = 0.8
PM = 0.2
TYPE_MUTATION = "inversion"


def creer_planning():
    planning = []

    for unite in range(NB_UNITES):
        planning.append(random.choice(GENES_PAR_UNITE[unite]))

    return planning


def creer_population():
    population = []

    for i in range(TAILLE_POPULATION):
        population.append(creer_planning())

    return population


def calculer_reserves(planning):
    reserves = []

    for intervalle in range(NB_INTERVALLES):

        puissance_perdue = 0

        for unite in range(NB_UNITES):
            if planning[unite][intervalle] == "1":
                puissance_perdue += CAPACITES[unite]

        reserve = PUISSANCE_TOTALE - puissance_perdue - DEMANDES[intervalle]
        reserves.append(reserve)

    return reserves


def fitness(planning):
    reserves = calculer_reserves(planning)

    if min(reserves) < 0:
        return 0

    return min(reserves)


def selection_loterie(population):
    scores = [fitness(p) for p in population]
    total = sum(scores)

    if total == 0:
        return random.choice(population).copy()

    tirage = random.uniform(0, total)
    cumul = 0

    for planning, score in zip(population, scores):
        cumul += score
        if tirage <= cumul:
            return planning.copy()

    return population[-1].copy()


def croisement(parent1, parent2):
    point = random.randint(1, NB_UNITES - 1)

    enfant1 = parent1[:point] + parent2[point:]
    enfant2 = parent2[:point] + parent1[point:]

    return enfant1, enfant2


def mutation_inversion(planning):
    planning = planning.copy()

    for unite in range(NB_UNITES):
        if random.random() < PM:
            planning[unite] = planning[unite][::-1]

    return planning


def mutation_remplacement(planning):
    planning = planning.copy()

    for unite in range(NB_UNITES):
        if random.random() < PM:
            autres = []

            for gene in GENES_PAR_UNITE[unite]:
                if gene != planning[unite]:
                    autres.append(gene)

            planning[unite] = random.choice(autres)

    return planning


def mutation(planning):
    if TYPE_MUTATION == "inversion":
        return mutation_inversion(planning)
    return mutation_remplacement(planning)


def algorithme_genetique():
    population = creer_population()
    meilleur = max(population, key=fitness)

    for generation in range(NOMBRE_GENERATIONS):

        nouvelle_population = [meilleur.copy()]

        while len(nouvelle_population) < TAILLE_POPULATION:

            parent1 = selection_loterie(population)
            parent2 = selection_loterie(population)

            if random.random() < PC:
                enfant1, enfant2 = croisement(parent1, parent2)
            else:
                enfant1, enfant2 = parent1.copy(), parent2.copy()

            nouvelle_population.append(mutation(enfant1))

            if len(nouvelle_population) < TAILLE_POPULATION:
                nouvelle_population.append(mutation(enfant2))

        population = nouvelle_population

        candidat = max(population, key=fitness)
        if fitness(candidat) > fitness(meilleur):
            meilleur = candidat.copy()

        if (generation + 1) % 20 == 0:
            print(f"Generation {generation + 1} : Fitness = {fitness(meilleur)} MW")

    return meilleur


def afficher_solution(planning):
    print("\n========== CEDULE DE MAINTENANCE ==========")
    print("            Int.1  Int.2  Int.3  Int.4")

    for unite in range(NB_UNITES):
        ligne = ""

        for bit in planning[unite]:
            if bit == "1":
                ligne += "  X    "
            else:
                ligne += "  .    "

        print(f"Unite {unite + 1} :", ligne, f"({planning[unite]})")

    print("\nReserves :", calculer_reserves(planning))
    print("Fitness :", fitness(planning), "MW")


def optimum_exact():
    meilleur_f = 0

    for combinaison in product(*GENES_PAR_UNITE):
        meilleur_f = max(meilleur_f, fitness(list(combinaison)))

    return meilleur_f


if __name__ == "__main__":
    print(f"Mutation utilisee : {TYPE_MUTATION}\n")
    solution = algorithme_genetique()
    afficher_solution(solution)
    print("Optimum exact (force brute) :", optimum_exact(), "MW")