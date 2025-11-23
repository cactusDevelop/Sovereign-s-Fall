
from random import choices, randint

import json

from global_func import solid_input

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    cst_data = json.load(read_file)
    OBJECT_BLUEPRINTS = cst_data.get("object_blueprints", [])

MAX_INV_SIZE = 6
OBJECT_SCALE = 1.17
OBJECT_SCALE_SLOWDOWN = 0.8 # became speed up instead of slowdown

class Object:
    def __init__(self, name: str, effect: str, value):
        self.name = name
        self.effect = effect
        self.value = value

    def use(self, player): # Ajouter un para enemy=None si un obj a des effets sur enemy
        if self.effect == "new_obj":
            player.mana -= 3
            new_object = rand_obj_inv(player.inventory)
            #print(f"[DEBUG] rand_obj() : {new_object}")
            player.inventory.append(new_object)
            print(f""""{self.name}" a invoqué l'objet "{new_object.name}" """)
            return True

        elif self.effect == "heal":
            delta_pv = min(self.value, player.max_pv-player.pv)
            player.heal(self.value)
            print(f"{self.name} régénère {delta_pv} PV")
            return True

        elif self.effect == "att_boost" or self.effect == "att_mult":
            def to_display():
                print("\n" + "="*10 + "Arme à améliorer" + "="*10)
                for i, weapon in enumerate(player.weapons):
                    remaining = weapon.MAX_BUFFS - weapon.buff_count
                    print(f"[{i+1}] {weapon.name} (Att: {weapon.power}, Buffs restants: {remaining}/{weapon.MAX_BUFFS})")
                print(f"[{len(player.weapons)+1}] Retour")
            def conf(action_input):
                return action_input.isdigit() and 0 < int(action_input) <= len(player.weapons) + 1

            which_one = int(solid_input(conf, to_display))

            if int(which_one) == len(player.weapons) + 1:
                print("Annulation du buff...")
                return False

            which_one -= 1

            if player.weapons[which_one].buff_count >= player.weapons[which_one].MAX_BUFFS:
                print(f"{self.name} ne peut plus être amélioré")
                return False
            else:
                if self.effect == "att_boost":
                    boost = self.value
                else:
                    boost = int((self.value-1)*player.weapons[which_one].power)

                player.weapons[which_one].add_buff(boost)
                remaining = player.weapons[which_one].MAX_BUFFS - player.weapons[which_one].buff_count
                print(f"""{self.name} augmente la puissance de "{player.weapons[which_one].name}" de {boost}""")
                print(f"{remaining}/{player.weapons[int(which_one)].MAX_BUFFS} utilisable(s) sur cette arme")
                return True

        elif self.effect == "shield":
            player.shield(self.value)
            print(f"{self.name} érige un bouclier ayant {self.value} PV")
            return True

        elif self.effect == "mana_ult_charge":
            player.mana_ult_charge(self.value)
            player.charge(self.value*10)

            print(f"{self.name} recharge de {self.value*10} ULT et {self.value} MANA")
            return True

        else:
            print("[DEBUG] Je n'ai pas programmé cet effet")
            return True

def get_rand_obj(inv, lvl_bonus=False, lvl=1):
    if not OBJECT_BLUEPRINTS: # Fallback si le json merde
        return Object("Potion par défaut", "heal", 50)

    owned_obj = [obj.name for obj in inv if obj.effect != "new_obj"]
    available_obj = []
    probabilities = []

    for obj in OBJECT_BLUEPRINTS:
        name, effect, min_value, max_value, prob = obj
        if name not in owned_obj:
            available_obj.append(obj)
            probabilities.append(prob)

    if not available_obj:
        print("[DEBUG] Shouldn't happen")
        if lvl_bonus:
            available_obj = OBJECT_BLUEPRINTS
            probabilities = [objet[4] for objet in OBJECT_BLUEPRINTS]
        else:
            return None

    tot = sum(probabilities)
    norm_prob = [p / tot for p in probabilities]

    template = choices(available_obj, weights=norm_prob, k=1)[0]
    name, effect, min_value, max_value, _ = template

    if lvl_bonus and effect != "mana_ult_charge":
        bonus = int(min_value*OBJECT_SCALE**(lvl/OBJECT_SCALE_SLOWDOWN))
        value = randint(min_value + bonus, max_value + bonus)
    else:
        value = randint(min_value, max_value)

    return Object(name, effect, value)


def rand_obj_inv(inv):
    return get_rand_obj(inv, lvl_bonus=False)

def enemy_loot(lvl, inv):
    return get_rand_obj(inv, lvl_bonus=True, lvl=lvl)