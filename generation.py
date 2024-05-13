from deap import base, creator, tools, algorithms
import random
import numpy as np
import sys

# 個体表現と適応度関数
creator.create("FitnessMax", base.Fitness, weights=(0.509,))
creator.create("Individual", list, fitness=creator.FitnessMax)

def evaluate(individual):

    ################################################################################################################################
    # Submitted by : Sheetal Bongale
    # Python script simulates a simple command-line Blackjack game implemented using Python and Object Oriented Programming concepts
    ################################################################################################################################
    suits = ("Spades ♠", "Clubs ♣", "Hearts ♥", "Diamonds ♦")

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
        print("\nPlayer's Hand:", *player.cards, sep="\n ")
        print("Player's Hand =", player.value)
        print("\nDealer's Hand:", *dealer.cards, sep="\n ")
        print("Dealer's Hand =", dealer.value)

    def player_busts(player, dealer):
        #print("\n--- Player busts! ---")
        return -1.25,


    def player_wins(player, dealer):
        #print("\n--- You win! ---")
        return 1,

    def dealer_busts(player, dealer):
        #print("\n--- You win! ---")
        return 1,


    def dealer_wins(player, dealer):
        #print("\n--- Dealer wins! ---")
        return -1,

    def push(player, dealer):
        #print("\nIts a tie!")
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
    print(individual)
    while True:
        index = ((player_hand.value % 11) * 13 % len(individual)) - 1
        index *= dealer_hand.value * 13 
        index -= 1
        index %= len(individual)
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
            
        elif x[0].lower() == "d":
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
        else:
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
