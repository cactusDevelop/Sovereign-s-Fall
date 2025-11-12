from random import *

NUM_CLASSIC_STARTER = 4
NUM_OP_STARTER = 1
WEAPON_MIN_MANA = 3
WEAPON_MAX_MANA = 5
NAME_MIN_LETTER = 4
NAME_MAX_LETTER = 7

starters_list = []

alphabet = 'a'*82+'b'*10+'c'*32+'d'*37+'e'*150+'f'*11+'g'*10+'h'*9+'i'*73+'j'*5+'k'*30+'l'*57+'m'*29+'n'*40+'o'*53+'p'*28+'q'*12+'r'*66+'s'*81+'t'*50+'u'*64+'v'*16+'w'*0+'x'*4+'y'*80+'z'*2


class Weapon:
    def __init__(self, name: str, power: int, stim: int, mana: int):
        self.name = name
        self.power = power
        self.original_power = power
        self.stim = stim
        self.mana = mana

def rand_names():
    x = randint(NAME_MIN_LETTER,NAME_MAX_LETTER)
    n = choice(alphabet).upper()
    for _ in range(x-1):
        n += (choice(alphabet))
    if n != "GILIS":
        return n
    else:
        return "ISA-LIBUR"

def rand_stats(x):
    mana=randint(WEAPON_MIN_MANA,WEAPON_MAX_MANA)
    power_value=randint(0,x+mana)
    stim_value=x+mana-power_value
    #print(power_value*10,stim_value*10,mana)
    return [power_value*10,stim_value*10,mana]

def gen_classic():
    stats = rand_stats(10)
    a = Weapon(rand_names(), stats[0], stats[1], stats[2])
    return a

def gen_op():
    stats = rand_stats(11)
    a = Weapon(rand_names(), stats[0], stats[1], stats[2])
    return a

def generate_starters():
    starter_list = []
    for _ in range(NUM_CLASSIC_STARTER):
        starter_list.append(gen_classic())
    for _ in range(NUM_OP_STARTER):
        starter_list.append(gen_op())

    shuffle(starter_list)
    return starter_list
