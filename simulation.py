import sys
import numpy as np


def calculate_index(player_hand, dealer_hand):

    if dealer_hand == 11 and ((player_hand >= 17)):
        print("No Insurance + Stand")
        return
    elif dealer_hand == 11 and ((player_hand < 10)):
        print("Bet Insurance + Hit")
        return
    index = (player_hand % 11)* 10 % 13 
    index += dealer_hand

    print("----- result -----")
    print()
    # best_strategyのインデックスに対応する行動を取得
    action = model[index]
    if action == 0:
        print("stand")
    else:
        print("hit")
    return index


if len(sys.argv) != 4:
    print("Usage: simulation.py model_file_name player_hand_score dealer_first_hand_score", file=sys.stderr)
else:
    model = np.load(sys.argv[1])
    player_hand = int(sys.argv[2])    
    dealer_hand = int(sys.argv[3])    

    print("Model DNA Info")
    print(model)
    print("----------------")
    print()
    calculate_index(player_hand, dealer_hand) 
