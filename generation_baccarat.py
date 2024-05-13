from deap import base, creator, tools, algorithms
import random
import numpy as np
import sys


def evaluate(individual):
    CARDS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    VALUE = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]
    OUTCOME = ['Player wins', 'Banker wins', 'Tie']

    # Inclusive range function
    irange = lambda start, end: range(start, end + 1)

    def compute_score(hand):
        """Compute the score of a hand"""
        total_value = 0
        for card in hand:
            total_value += VALUE[CARDS.index(card)]
        return total_value % 10

    def play():
        """Returns the winner"""
        player_hand = [
            random.choice(CARDS),
            random.choice(CARDS)
        ]
        banker_hand = [
            random.choice(CARDS),
            random.choice(CARDS)
        ]

        player_score = compute_score(player_hand)
        banker_score = compute_score(banker_hand)


        # Natural
        if player_score in [8, 9] or banker_score in [8, 9]:
            if player_score != banker_score:
                return OUTCOME[banker_score > player_score]
            else:
                return OUTCOME[2]

        # Player has low score
        if player_score in irange(0, 5):
            # Player get's a third card
            player_hand.append(random.choice(CARDS))
            player_third = compute_score([player_hand[2]])

            # Determine if banker needs a third card
            if (banker_score == 6 and player_third in [6, 7]) or \
            (banker_score == 5 and player_third in irange(4, 7)) or \
            (banker_score == 4 and player_third in irange(2, 7)) or \
            (banker_score == 3 and player_third != 8) or \
            (banker_score in [0, 1, 2]):
                banker_hand.append(random.choice(CARDS))

        elif player_score in [6, 7]:
            if banker_score in irange(0, 5):
                banker_hand.append(random.choice(CARDS))

        # Compute the scores again and return the outcome
        player_score = compute_score(player_hand)
        banker_score = compute_score(banker_hand)


        if player_score != banker_score:
            return OUTCOME[banker_score > player_score]
        else:
            return OUTCOME[2]

    print(play())

creator.create("FitnessMax", base.Fitness, weights=(0.4462)) # Player win percentage
creator.create("Individual", list, fitness=creator.FitnessMax)

NGEN = int(sys.argv[1])
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 2) 
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=170)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=5)
pop = toolbox.population(n=NGEN)

                                             
hof = tools.ParetoFront()
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)


try:
    for individual in pop:
        individual.fitness.values = toolbox.evaluate(individual)
    hof = tools.ParetoFront()

    algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.1, ngen=NGEN, halloffame=hof, stats=stats, verbose=True)

except KeyboardInterrupt:
    pass
finally:
    print("結果を保存します")
    best_individual = tools.selBest(pop, k=1)[0]
    print(f"最良個体 : {best_individual}")
    np.save(sys.argv[2], best_individual)
    print("DONE!")
