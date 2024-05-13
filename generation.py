from deap import base, creator, tools, algorithms
import random
import numpy as np


################################################################################################################################
# Submitted by : Sheetal Bongale
# Python script simulates a simple command-line Blackjack game implemented using Python and Object Oriented Programming concepts
################################################################################################################################
import sys
import random

# 個体表現と適応度関数
creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # 勝率を最大化する
creator.create("Individual", list, fitness=creator.FitnessMax)

def evaluate(individual):
    suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")

    #time.sleep(0.0001)
    #playing = True

    class Card:
        def __init__(self, suit, rank):
            self.suit = suit
            self.rank = rank

        def __str__(self):
            return self.rank + " of " + self.suit


    class Deck:
        
        def __init__(self):
            self.deck = []  # start with an empty list
            self.ranks = (
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
                "A",
            )
            for suit in suits:
                for rank in self.ranks:
                    self.deck.append(Card(suit, rank))

        def __str__(self):
            deck_comp = ""  # start with an empty string
            for card in self.deck:
                deck_comp += "\n " + card.__str__()  # add each Card object's print string
            return "The deck has:" + deck_comp

        def shuffle(self):
            random.shuffle(self.deck)

        def deal(self):
            single_card = self.deck.pop()
            return single_card


    class Hand:

        def __init__(self):
            self.cards = []  # start with an empty list as we did in the Deck class
            self.value = 0  # start with zero value
            self.aces = 0  # add an attribute to keep track of aces
            self.values = {
                "2": 2,
                "3": 3,
                "4": 4,
                "5": 5,
                "6": 6,
                "7": 7,
                "8": 8,
                "9": 9,
                "10": 10,
                "J": 10,
                "Q": 10,
                "K": 10,
                "A": 11,
            }
            self.ranks = (
                "1",
                "2",
                "3",
                "4",
                "5",
                "6",
                "7",
                "8",
                "9",
                "10",
                "J",
                "Q",
                "K",
                "A",
            )
        def add_card(self, card):
            self.cards.append(card)
            if (card.rank == "A") or (card.rank == "1"):
                self.aces += 1  # add to self.aces
                self.value += self.values["A"]
            else:
                self.value += self.values[card.rank]

        def adjust_for_ace(self):
            while self.value > 21 and self.aces:
                self.value -= 10
                self.aces -= 1




    def show_all(player, dealer):
        return 


    def player_busts(player, dealer):
        return -1,


    def player_wins(player, dealer):
        return 1,

    def dealer_busts(player, dealer):
        return 1,


    def dealer_wins(player, dealer):
        return -1,

    def push(player, dealer):
        return 0,

    # FUNCTION DEFINITIONS:


    def hit(deck, hand):
        hand.add_card(deck.deal())
        hand.adjust_for_ace()

    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    dealer_hand = Hand()
    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    player_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    x = None
    while True:
        
        index = (player_hand % 11)* 10 % 13 
        index += dealer_hand
        if individual[index] == 0:
            x = "s"
        elif individual[index] == 1:
            x = "h"
        elif individual[index] == 2:
            x = "d" # double down
        
        if x[0].lower() == "h":
            hit(deck, player_hand)  # hit() function defined above
            if player_hand.value > 21:
                return player_busts(player_hand, dealer_hand)
            
        if x[0].lower() == "d":
            if (player_hand.value != 10) or (player_hand.value != 11) or (player_hand.value != 9):
                hit(deck, player_hand)  # hit() function defined above
                if player_hand.value > 21:
                    return player_busts(player_hand, dealer_hand)
            else:
                hit(deck, player_hand)  # hit() function defined above
                if player_hand.value > 21:
                    return player_busts(player_hand, dealer_hand)

                while dealer_hand.value < 17:
                    hit(deck, dealer_hand)


                if dealer_hand.value > 21:
                    return dealer_busts(player_hand, dealer_hand)

                elif dealer_hand.value > player_hand.value:
                    return dealer_wins(player_hand, dealer_hand)

                elif dealer_hand.value < player_hand.value:
                    return player_wins(player_hand, dealer_hand)

                else:
                    return push(player_hand, dealer_hand)
            

        if player_hand.value <= 21:
            while dealer_hand.value < 17:
                hit(deck, dealer_hand)


            if dealer_hand.value > 21:
                return dealer_busts(player_hand, dealer_hand)

            elif dealer_hand.value > player_hand.value:
                return dealer_wins(player_hand, dealer_hand)

            elif dealer_hand.value < player_hand.value:
                return player_wins(player_hand, dealer_hand)

            else:
                return push(player_hand, dealer_hand)

NGEN = int(sys.argv[1])
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1, 2)  # ルールを0/1で表現する場合
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=100)  # 100個のルールを持つ個体
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=5)

pop = toolbox.population(n=int(sys.argv[2]))
                                             
hof = tools.ParetoFront()
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
stats.register("std", np.std, axis=0)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)


population = toolbox.population(n=int(sys.argv[3]))  #n = 個体 
for individual in pop:
    individual.fitness.values = toolbox.evaluate(individual)
hof = tools.ParetoFront()

algorithms.eaSimple(pop, toolbox, cxpb=0.9, mutpb=0.1, ngen=NGEN, halloffame=hof, stats=stats, verbose=True)

#for gen in range(NGEN):
#    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
#    fits = toolbox.map(toolbox.evaluate, offspring)
#    for fit, ind in zip(fits, offspring):
#        ind.fitness.values = fit
#    population = toolbox.select(offspring, k=len(population))

# 結果の保存
print("結果を保存します")
best_individual = tools.selBest(population, k=1)[0]
np.save(sys.argv[4], best_individual)
print("DONE!")