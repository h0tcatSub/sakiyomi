import sys
import numpy as np


def calculate_index(player_hand, dealer_hand):

    print("----- result -----")
    print()

    if (dealer_hand == 11) and (player_hand >= 17):
        print("No Insurance")
    elif (dealer_hand == 11) and (player_hand < 17):
        print("Bet Insurance")
    print()
    index = ((player_hand % 11) * 13 % len(model)) - 1
    index += dealer_hand * 13 
    index -= 1
    index %= len(model)

    # best_strategyのインデックスに対応する行動を取得
    action = model[index]
    if action == 0:
        print("stand")
    elif action == 1:
        print("hit")
    else:
        print("double")
    return index


if len(sys.argv) != 4:
    print("Usage: simulation.py model_file_name dealer_first_hand_score player_hand_score", file=sys.stderr)
else:
    model = np.load(sys.argv[1])
    dealer_hand = int(sys.argv[2])    
    player_hand = int(sys.argv[3])
    print()
    print("----------------")
    print("Model DNA Info")
    print(model)
    print("----------------")
    print()
    calculate_index(player_hand, dealer_hand) 
