
import json

from characters import Player
from weapon import Weapon
from object import Object


# CONSTANTS
with open("JSON/cst_data.json", "r", encoding="utf-8") as read_cst:
    cst = json.load(read_cst)
with open("JSON/highscores.json", "r", encoding="utf-8") as read_hs:
    hs = json.load(read_hs)

def get_cst_names():
    return cst["monster_names"], cst["boss_names"], cst["weapon_names"]

def save_hs(nickname, score, level):
    hs["history"].append({"nickname": nickname, "score": int(score), "level": int(level)})
    hs["history"] = sorted(hs["history"], key=lambda x: x["score"], reverse=True)[:10]
    if score > hs["highscore"]:
        hs["highscore"] = score
    with open("JSON/highscores.json", "w", encoding="utf-8") as write_file:
        json.dump(hs, write_file, ensure_ascii=False, indent=4)
    return hs["highscore"]


# SAVED VARIABLES
with open("JSON/active_data.json", "r", encoding="utf-8") as read_file:
    data = json.load(read_file) # Au début je changeais tout en temps réel et crachais sur json parce que c'est éclaté mais en réalité il ne fallait juste pas l'uiliser de cette manière, désormais mon âme est en paix

def save_game(new_player, level=1, used_monsters=None):
    data["player"]["nickname"] = new_player.name
    data["player"]["pv"] = new_player.pv
    data["player"]["max_pv"] = new_player.max_pv
    data["player"]["stim"] = new_player.stim
    data["player"]["max_stim"] = new_player.max_stim
    data["player"]["current_level"] = level

    if used_monsters is not None: # Ens vide accepté mais pas None
        data["used_monsters"] = used_monsters

    data["player"]["weapons_inv"].clear()
    for n, weapon in enumerate(new_player.weapons):
        data["player"]["weapons_inv"][f"weapon_slot_{n+1}"]={
            "name": weapon.name,
            "power": weapon.power,
            "stim": weapon.stim,
            "mana": weapon.mana,
            "buff_count": weapon.buff_count
        }

    data["player"]["objects_inv"].clear()
    for n, obj in enumerate(new_player.inventory):
        data["player"]["objects_inv"][f"object_slot_{n+1}"]={
            "name": obj.name,
            "effect": obj.effect,
            "value": obj.value
        }

    with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)

def saved_game(): # Retourne un boléen
    return data["player"]["nickname"] is not None and data["player"]["pv"] > 0 and data["player"]["max_pv"] is not None and data["player"]["stim"] is not None

def get_save():
    if saved_game():
        return {
            "nickname": data["player"]["nickname"],
            "level": data["player"].get("current_level", 1), #Merci StackOverflow pour l'incroyable méthode get()
            "pv": data["player"]["pv"],
            "max_pv": data["player"]["max_pv"],
            "score": data["player"].get("score", 0)
        }
    return None

def clear_save():
    global data # Le temps que j'ai mis à trouver ça ¯\_(ツ)_/¯

    def clear_dict(dicts):
        for key, value in list(dicts.items()):
            if isinstance(value, dict):
                clear_dict(value)
            else:
                dicts[key] = None

    clear_dict(data)
    data["used_monsters"] = []
    data["cheat"] = False

    if "weapon_slot_4" in data["player"]["weapons_inv"]:
        del data["player"]["weapons_inv"]["weapon_slot_4"]

    with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, indent=4, ensure_ascii=False)


#def dump_json(data_to_save):
#    with open("JSON/active_data.json", "w", encoding="utf-8") as write_file:
#        json.dump(data_to_save, write_file, ensure_ascii=False, indent=4)
#
#    player = data["player"]
#    save_hs(player["nickname"], player["score"], player["current_level"])

def get_player_data():
    weapons_inventory = []
    for i in data["player"]["weapons_inv"].keys():
        a = data["player"]["weapons_inv"][i]["name"]
        b = data["player"]["weapons_inv"][i]["power"]
        c = data["player"]["weapons_inv"][i]["stim"]
        d = data["player"]["weapons_inv"][i]["mana"]
        e = data["player"]["weapons_inv"][i].get("buff_count", 0)
        weapons_inventory.append(Weapon(a, b, c, d, e))

    objects_inventory = [] # A faire plus tard
    for i in data["player"]["objects_inv"].keys():
        a = data["player"]["objects_inv"][i]["name"]
        b = data["player"]["objects_inv"][i]["effect"]
        c = data["player"]["objects_inv"][i]["value"]
        objects_inventory.append(Object(a,b,c))

    return Player(data["player"]["nickname"],
            data["player"]["pv"],
            data["player"]["max_pv"],
            data["player"]["stim"],
            data["player"]["max_stim"],
            data["player"]["mana"],
            data["player"]["max_mana"],
            weapons_inventory,
            objects_inventory)

def get_used_monsters():
    return data.get("used_monsters", [])

