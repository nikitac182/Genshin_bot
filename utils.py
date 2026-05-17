from random import randint

def roll_rarity(pity_4, pity_5):

    # гарант 5
    if pity_5 >= 89:
        return 5

    # гарант 4
    if pity_4 >= 9:
        return 4

    roll = randint(1, 1000)

    if roll <= 6:
        return 5

    elif roll <= 57:
        return 4

    return 3

async def update_pity(rarity, user_id, pity_4, pity_5):

    if rarity == 5:
        return 0, 0
    elif rarity == 4:
        return 0, pity_5 + 1
    else:
        return pity_4 + 1, pity_5 + 1