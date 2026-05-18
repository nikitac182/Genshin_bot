from random import randint

def roll_rarity(pity_4, pity_5, banner_type: str = "characters"):

    if banner_type == "weapons":
        HARD_PITY_5 = 79
    else:
        HARD_PITY_5 = 89
    
    #хард гарант 5
    if pity_5 >= HARD_PITY_5:
        return 5

    #хард гарант 4
    if pity_4 >= 9:
        return 4

    roll = randint(1, 1000)

    #софт гарант 5
    soft_pity_table_5 = {
        73: 60,
        74: 120,
        75: 180,
        76: 240,
        77: 320,
        78: 400,
        79: 480,
        80: 560,
        81: 640,
        82: 720,
        83: 800,
        84: 860,
        85: 920,
        86: 960,
        87: 980,
        88: 990,
    }
    if banner_type == "weapons":
        chance5 = soft_pity_table_5.get(pity_5+10, 6)
    else:
        chance5 = soft_pity_table_5.get(pity_5, 6)
    if roll <= chance5:
        return 5

    #софт гарант 4
    soft_pity_table_4 = {
        7: 300,
        8: 550,
    }
    chance4 = soft_pity_table_4.get(pity_4, 57)
    if roll <= chance4:
        return 4

    return 3

async def update_pity(rarity, user_id, pity_4, pity_5):

    if rarity == 5:
        return 0, 0
    elif rarity == 4:
        return 0, pity_5 + 1
    else:
        return pity_4 + 1, pity_5 + 1