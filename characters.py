
from random import choice

from object import rand_obj


class Character:
    def __init__(self, name: str, pv: int, max_pv:int):
        self.name = name
        self.pv = pv
        self.max_pv = max_pv
        self.weapon = None

    def attack(self, target):
        if hasattr(target, "calc_dmg"):
            target.calc_dmg(self.weapon.power)
        else:
            target.pv = max(target.pv - self.weapon.power, 0)

        print(f"{self.weapon.name} inflige {self.weapon.power} dégats à {target.name} ({target.pv} PV restants)")


class Player(Character):
    def __init__(self, name:str, pv:int, max_pv:int, stim:int, max_stim:int, mana:int, max_mana:int, weapons:list, inventory:list):
        super().__init__(name, pv, max_pv)
        self.stim = stim
        self.max_stim = max_stim
        self.mana = mana
        self.max_mana = max_mana
        self.weapons = weapons
        self.inventory = inventory
        self.shield_pv = 0
        self.can_ult = (self.stim == self.max_stim)

    def charge(self, x):
        self.stim = min(self.stim+x, self.max_stim)
        self.can_ult = (self.stim == self.max_stim)

    def mana_charge(self, x):
        self.mana = min(self.mana + x, self.max_mana)

    def ult(self, target):
        if self.can_ult:
            dgt = 0
            for weapon in self.weapons:
                dgt += weapon.power
            self.can_ult = False
            target.pv = max(target.pv-dgt, 0)
            print(f"Vos armes attaquent de {dgt}")

            self.can_ult = False
            self.stim = 0
            return None
        else:
            return "[DEBUG] NE PEUT PAS ULT"

    def heal(self, x):
        self.pv = min(self.pv+x, self.max_pv)

    def use_obj(self, obj_position): # AJouter enemy=None ici aussi
        if 0 <= obj_position < len(self.inventory):
            obj = self.inventory[obj_position]

            if obj.effect == "new_obj" and len(self.inventory) >= 6:
                print("Inventaire plein...")
                return False
            else:
                obj.use(self)
                if obj.effect != "new_obj":
                    self.inventory.pop(obj_position) # pop or remove ?
                return True
        else:
            print("[DEBUG] Pas d'objet")
            return False

    def shield(self, s_pv):
        self.shield_pv = max(self.shield_pv, s_pv) # Bouclier fort écrase bouclier faible
        print(f"Bouclier de {self.shield_pv} Pv actif")

    def calc_dmg(self, damage):
        if self.shield_pv > 0:
            self.shield_pv = max(self.shield_pv - damage, 0)
            """if damage <= self.shield_pv:
                self.shield_pv -= damage
            else:
                remaining_dmg = damage - self.shield_pv
                self.shield_pv = 0
                self.pv = max(self.pv - remaining_dmg, 0)
                print(f"{remaining_dmg} dégats traversent le bouclier ({self.pv} PV restants)")"""
        else:
            self.pv = max(self.pv - damage, 0)



class Monster(Character):
    HORNS = ["^  ^",""]
    FACE = ["O, O", "o.o", "-. -", "@ @", "P^ P"]
    TEETH = ["___", "^^^^", "==="]
    BODY = ["||", "| |", "//\\\\"]
    FEET = ["'''", "^  ^", "{} {}"]

    def draw_ascii(self):
        horns = choice(self.HORNS)
        face = choice(self.FACE)
        teeth = choice(self.TEETH)
        body = choice(self.BODY)
        feet = choice(self.FEET)

        return f"""{horns}\n{face}\n{teeth}\n{body}\n{feet}\n"""

    def __init__(self, name: str, pv: int, weapon, weakness=0):
        super().__init__(name, pv, pv)
        self.weapon = weapon
        self.weakness = weakness

        self.picture = self.draw_ascii()

    def die(self):
        pass
