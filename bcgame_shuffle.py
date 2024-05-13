import hashlib
import random
import uuid
CARDS = ["", "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
FLOWER = ["♠", "♥", "♣", "♦"]
all_cards = []
all_cards1 = []
all_cards2 = [161, 180, 199, 218, 162, 205, 181, 200, 219, 163, 182, 220, 201, 177, 196, 215, 170, 178, 221, 197, 216, 171, 179, 198, 172, 217, 193, 212, 167, 186, 194, 173, 213, 168, 187, 195, 214, 188, 169, 209, 164, 183, 202, 210, 189, 165, 184, 203, 211, 166, 204, 185]


for i in range(12):
    for c in range(10, 14):
        for v in range(1, 14):
            all_cards1.append(c * 16 + v)


random.shuffle(all_cards1)
print(len(all_cards1))