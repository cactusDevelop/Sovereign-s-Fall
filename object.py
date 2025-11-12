
from random import choice, randint

import json

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    cst_data = json.load(read_file)
    OBJECT_BLUEPRINTS = cst_data.get("object_blueprints", [])

MAX_INV_SIZE = 6

class Object:
    def __init__(self, name: str, effect: str, value):
        self.name = name
        self.effect = effect
        self.value = value

    def use(self, player): # Ajouter un para enemy=None si un obj a des effets sur enemy
        if self.effect == "new_obj":
            if len(player.inventory) >= MAX_INV_SIZE:
                print("Inventaire plein...")
            else:
                new_object = rand_obj_inv(player.inventory)
                #print(f"[DEBUG] rand_obj() : {new_object}")
                player.inventory.append(new_object)
                print(f"{self.name} a invoqué l'objet {new_object.name}")

        elif self.effect == "heal":
            delta_pv = min(self.value, player.max_pv-player.pv)
            player.heal(self.value)
            print(f"{self.name} régénère {delta_pv} PV")

        elif self.effect == "att_boost":
            print("\n" + "="*10 + "Arme à améliorer" + "="*10)
            for i, weapon in enumerate(player.weapons):
                print(f"[{i+1}] {weapon.name} (Att: {weapon.power})")

            which_one = input(" > ")
            while not (which_one.isdigit() and 0 < int(which_one) <= len(player.weapons)):
                print("Valeur invalide")
                which_one = input(" > ")

            player.weapons[int(which_one)-1].power += self.value
            print(f"{self.name} augmente la puissance de {player.weapons[int(which_one)-1]} de {self.value}")

        elif self.effect == "shield":
            player.shield(self.value)
            print(f"{self.name} érige un bouclier ayant {self.value} PV")

        else:
            print("[DEBUG] Je n'ai pas programmé cet effet")

def rand_obj():
    if not OBJECT_BLUEPRINTS: # Fallback si le json merde
        return Object("Potion par défaut", "heal", 50)

    blueprint = choice(OBJECT_BLUEPRINTS)
    name, effect, min_value, max_value = blueprint
    value = randint(min_value, max_value)
    return Object(name, effect, value)

def rand_obj_inv(inv):
    if not OBJECT_BLUEPRINTS:  # Fallback si le json merde
        return Object("Potion par défaut", "heal", 50)
    owned_obj = []
    available_obj = []
    for obj in inv:
        if obj.effect != "new_obj":
            owned_obj.append(obj.name)
    for obj in OBJECT_BLUEPRINTS:
        if obj[0] not in owned_obj:
            available_obj.append(obj)
    if not available_obj:
        return None
    name, effect, min_v, max_v = choice(available_obj)
    value = randint(min_v, max_v)
    return Object(name, effect, value)

def enemy_loot(lvl, inv):
    if not OBJECT_BLUEPRINTS:  # Fallback si le json merde
        return Object("Potion par défaut", "heal", 50)

    owned_obj = []
    available_obj = []
    for obj in inv:
        if obj.effect != "new_obj":
            owned_obj.append(obj.name)
    for obj in OBJECT_BLUEPRINTS:
        if obj[0] not in owned_obj:
            available_obj.append(obj)
    if not available_obj:
        template = choice(OBJECT_BLUEPRINTS)
    else:
        template = choice(available_obj)

    name, effect, min_value, max_value = template

    lvl_bonus = lvl * 5
    value = randint(min_value + lvl_bonus, max_value + lvl_bonus)
    return Object(name, effect, value)