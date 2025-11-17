
from random import shuffle, randint, gauss, choice

NUM_CLASSIC_STARTER = 4
NUM_OP_STARTER = 1
WEAPON_MIN_MANA = 3
WEAPON_MAX_MANA = 5
NAME_MIN_LETTER = 4
NAME_MAX_LETTER = 7
GEN_ATTEMPTS = 111

starters_list = []
alphabet = 'a'*82+'b'*10+'c'*32+'d'*37+'e'*150+'f'*11+'g'*10+'h'*9+'i'*73+'j'*5+'k'*30+'l'*57+'m'*29+'n'*40+'o'*53+'p'*28+'q'*12+'r'*66+'s'*81+'t'*50+'u'*64+'v'*16+'w'*0+'x'*4+'y'*80+'z'*2


class Weapon:

    MAX_BUFFS = 5

    def __init__(self, name: str, power: int, stim: int, mana: int, buff_count: int=0):
        self.name = name
        self.power = power
        self.original_power = power
        self.stim = stim
        self.mana = mana
        self.buff_count = buff_count

    def add_buff(self, x):
        if self.buff_count >= self.MAX_BUFFS:
            return False
        self.power += x
        self.buff_count += 1
        return True

def rand_names():
    x = randint(NAME_MIN_LETTER,NAME_MAX_LETTER)
    n = choice(alphabet).upper()
    for _ in range(x-1):
        n += (choice(alphabet))
    if n != "GILIS": # Trouver la seed qui génère cette pépite
        return n
    else:
        return "ISA-LIBUR"

def rand_stats(x):
    mana = randint(WEAPON_MIN_MANA,WEAPON_MAX_MANA)
    power_ratio = gauss(0.5, 0.15)
    power_value = int((x+mana)*power_ratio)
    stim_value = x+mana-power_value
    #print(power_value*10,stim_value*10,mana)

    return [power_value*10, stim_value*10, mana]

def gen_classic():
    stats = rand_stats(10)
    c_name = rand_names()

    if c_name == "ISA-LIBUR":
        a = Weapon(c_name, 99999, 99999, 0, 0)
        print()  # Faire une animation ascii que prsn ne verra ici
        print("UNE ARME EXCEPTIONNELLE T'EST ACCORDEE")
        print("LA DIVINITE 61L15 TE PRETE ISA-LIBUR !")
    else:
        a = Weapon(c_name, stats[0], stats[1], stats[2], 0)

    return a

def gen_op():
    stats = rand_stats(11)
    o_name = rand_names()

    if o_name == "ISA-LIBUR":
        a = Weapon(o_name, 99999, 99999, 0, 0)
        print() # Faire une animation ascii que prsn ne verra ici
        print("UNE ARME EXCEPTIONNELLE T'EST ACCORDEE")
        print("LA DIVINITE 61L15 TE PRETE ISA-LIBUR !")
    else:
        a = Weapon(o_name, stats[0], stats[1], stats[2], 0)

    return a

def gen_boss_weapon(lvl):
    b_name = rand_names().upper()
    stats = rand_stats(10+(lvl//2))
    return Weapon(b_name, stats[0], stats[1], stats[2], 0)

def generate_starters():
    starter_list = []
    already_used_stats = set()

    attempt = 0
    while len(starter_list) < NUM_CLASSIC_STARTER and GEN_ATTEMPTS > attempt :
        weapon = gen_classic()
        if weapon not in already_used_stats:
            starter_list.append(weapon)
            already_used_stats.add(weapon)
        attempt += 1

    attempt = 0
    approved = True
    while len(starter_list) < (NUM_CLASSIC_STARTER+NUM_OP_STARTER) and GEN_ATTEMPTS > attempt :
        op_weapon = gen_op()
        for classic_weapon in starter_list:
            if ((op_weapon.power == classic_weapon.power + 10 and
                op_weapon.stim == classic_weapon.stim and
                op_weapon.mana == classic_weapon.mana) or
                (op_weapon.power == classic_weapon.power and
                op_weapon.stim == classic_weapon.stim +10 and
                op_weapon.mana == classic_weapon.mana)):
                approved = False
                break

        if op_weapon not in already_used_stats and approved:
            starter_list.append(op_weapon)
            already_used_stats.add(op_weapon)
        attempt += 1

    while len(starter_list) < (NUM_CLASSIC_STARTER + NUM_OP_STARTER):
        if len(starter_list) < NUM_CLASSIC_STARTER:
            starter_list.append(gen_classic())
        else:
            starter_list.append(gen_op()) # Dernière chance

    shuffle(starter_list)
    return starter_list
