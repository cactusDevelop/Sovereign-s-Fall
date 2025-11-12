
import os, random, time

from json_manager import get_cst_names, save_hs, clear_save
from weapon import generate_starters
from musics import play_sound, stop_sound
from characters import Monster
from weapon import Weapon
from object import Object, enemy_loot, MAX_INV_SIZE
from fight import Fight


# from getpass import getpass   Ca marche pas ses grands morts

incognito = " \033[1;32m???\033[0m"
starters = generate_starters()
OBJ_STARTER = Object("Sac des abimes", "new_obj", 0)

def slow_print(txt: tuple):
    for _ in txt:
        print(_, end="")
        input()

def choose_starter(s_list):
    print()
    for j in s_list:
        print(f"[{starters.index(j) + 1}] {j.name}: Power {j.power}, Ult Charge {j.stim}, Mana {j.mana}")
    choice = input(" > ")
    while not (choice.isdigit() and 0 < int(choice) <= len(s_list)):
        print("Valeur invalide")
        choice = input(" > ")
    return s_list[int(choice) - 1]

def player_speaks(pseudo):
    return f" \033[1;36m{pseudo}\033[0m"

def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_width():
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    return columns

def game_over(data,x:int,des:str):
    clear_console()
    stop_sound(1000)

    nickname = data["player"]["nickname"]
    score = data["player"]["score"]
    level = data["player"]["current_level"]

    test_high = False
    if score > 0:
        new_hs = save_hs(nickname, score, level)
        test_high = (score == new_hs)

    print("\n\x1b[7m" + "=" * get_width())
    print(f"\x1b[1m  GAME OVER\x1b[0;7m" + " "*(get_width()-11))
    print(f"  Fin {x} - {des}" + " " * (get_width()-9-len(str(x))-len(des)))
    print(f"  Score - {score}" + " " * (get_width()-9-len(str(x))-len(str(score))))

    if test_high:
        print(f" >>> NEW HIGHSCORE <<<" + " "*(get_width()-22))

    print(" " * get_width() + "\n" + " " * get_width())
    print("=" * get_width() + "\x1b[0m")
    #dump_json(data)
    clear_save()
    input("\nAppuyez sur ENTER pour revenir à l'écran d'accueil")
    return False # Parce que j'ai fait running = game_over() mais est-ce vrm utile ??? on vera si je créé une class Game


# SCENES
def launch_cutscene(data):
    clear_console()
    stop_sound(1500)
    time.sleep(1.7)
    play_sound("tense-bgm", True)

    print((
        "\n\033[32m"
        "\n          ⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷"
        "\n   ⠀⠀⠀⠀ ⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⠀⠀⠀⠀⠀ ⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⠀⣠⣤⣤⣤⣤⣴⣿⣿⣿⣿⣿⣿⡟⠛⠛⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣿⣿⠟⢹⣿⣿⣿⣿⡇⠀⠀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⠟⠁⠀⠸⠿⠿⠿⠿⠃⠀⢀⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣷⣄⠀⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⣿⣿⣿⣿⣿⣿⣿⣷⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"
        "\n   ⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿"
        "\n"
        "\n   Pour continuer : Touche -> \033[1mENTER <- \033[0;32m"))
    input()
    print((
        "\n\n\n"
        "\n           _____  ___________             ____        _______     _______   _____    _____     "
        "\n      _____\    \_\          \        ____\_  \__    /      /|   |\      \ |\    \   \    \    "
        "\n     /     /|     |\    /\    \      /     /     \  /      / |   | \      \ \\\\    \   |    |   "
        "\n    /     / /____/| |   \_\    |    /     /\      ||      /  |___|  \      | \\\\    \  |    |   "
        "\n   |     | |____|/  |      ___/    |     |  |     ||      |  |   |  |      |  \|    \ |    |   "
        "\n   |     |  _____   |      \  ____ |     |  |     ||       \ \   / /       |   |     \|    |   "
        "\n   |\     \|\    \ /     /\ \/    \|     | /     /||      |\\\\/   \//|      |  /     /\      \  "
        "\n   | \_____\|    |/_____/ |\______||\     \_____/ ||\_____\|\_____/|/_____/| /_____/ /______/| "
        "\n   | |     /____/||     | | |     || \_____\   | / | |     | |   | |     | ||      | |     | | "
        "\n    \|_____|    |||_____|/ \|_____| \ |    |___|/   \|_____|\|___|/|_____|/ |______|/|_____|/  "
        "\n           |____|/                   \|____|                                                   "
        "\n                                                                                               "))
    time.sleep(0.8)
    print((
        "\n           ___________    ______   _____                _____    ________    ________          "
        "\n          /           \   \     \  \    \          _____\    \  /        \  /        \         "
        "\n         /    _   _    \   \    |  |    |         /    / \    ||\         \/         /|        "
        "\n        /    //   \\\\    \   |   |  |    |        |    |  /___/|| \            /\____/ |        "
        "\n       /    //     \\\\    \  |    \_/   /|     ____\    \ |   |||  \______/\   \     | |        "
        "\n      /     \\\\_____//     \ |\         \|    /    /\    \|___|/ \ |      | \   \____|/         "
        "\n     /       \ ___ /       \| \         \__ |    |/ \    \       \|______|  \   \              "
        "\n    /________/|   |\________\\\\ \_____/\    \|\____\ /____/|               \  \___\             "
        "\n   |        | |   | |        |\ |    |/___/|| |   ||    | |                \ |   |             "
        "\n   |________|/     \|________| \|____|   | | \|___||____|/                  \|___|             "
        "\n                                     |___|/                                                    "))
    time.sleep(0.8)
    print((
        "\n          _____                                                                                "
        "\n    ____  \    \      _____       _____           _____                                        "
        "\n    \   \ /____/|   /      |_    |\    \         |\    \                                       "
        "\n     |  |/_____|/  /         \    \\\\    \         \\\\    \                                      "
        "\n     |  |    ___  |     /\    \    \\\\    \         \\\\    \                                     "
        "\n     |   \__/   \ |    |  |    \    \|    | ______  \|    | ______                             "
        "\n    /      /\___/||     \/      \    |    |/      \  |    |/      \                            "
        "\n   /      /| | | ||\      /\     \   /            |  /            |                            "
        "\n   |_____| /\|_|/ | \_____\ \_____\ /_____/\_____/| /_____/\_____/|                            "
        "\n   |     |/       | |     | |     ||      | |    |||      | |    ||                            "
        "\n   |_____|         \|_____|\|_____||______|/|____|/|______|/|____|/                            "
        "\n\033[0m"))
    input()
    clear_console()
    play_sound("wood-creak")
    slow_print((
        "\nVous vous réveillez dans un pièce sombre qui vous est inconnue.",
        "Un homme tout de noir vêtu vous tend un parchemin.",
        f"\n{incognito} : « Complétez ceci »"))
    play_sound("paper-collect")
    slow_print((
        "\n               _________________________________________________________________"
        "\n              |                                                                 |"
        "\n              |                                                                 |"
        "\n              |   Vous avez eu l’exceptionnellement incroyable chance           |"
        "\n              |   d’être sélectionné pour prendre part au programme *XXXXX*.    |"
        "\n              |                                                                 |",
        "              |                                                                 |"
        "\n              |   - Toute atteinte à la sécurité du participant durant le       |"
        "\n              |   programme relève de son entière responsabilité.               |"
        "\n              |   - Le participant n’est pas autorisé à interrompre le          |"
        "\n              |   programme avant la fin.                                       |",
        "              |                                                                 |"
        "\n              |   Je soussigné (nom, prénom)...............................     |"
        "\n              |   accepte en toute connaissance de cause, les conditions        |"
        "\n              |   présentée cfr supra.                                          |"
        "\n              |                                                                 |"
        "\n              |_________________________________________________________________|"))

    print(f"\n{incognito} : « Avez-vous lu et acceptez-vous ce contrat » ")
    agreement = str(input(" > ")).strip()

    while agreement.lower() != "oui" and agreement.lower() != "non":
        print(f"\n{incognito} : « Nous réitérons notre demande... »")
        print(f"{incognito} : « Acceptez-vous ce contrat » (oui/non)")
        play_sound("hmm")
        agreement = str(input(" > ")).strip()

    if agreement.lower() == "non":
        pseudo = str(input("\nPseudo > \033[1;36m")).strip()
        if pseudo == "":
            pseudo = "Vous"
        data["player"]["nickname"] = pseudo

        print(f"\n{player_speaks(pseudo)} : « Va te faire foutre. »")
        input()
        play_sound("laughter")
        print(f"{incognito} : « Pensez-vous avoir le choix ? »")
        time.sleep(2)
        return False

    else:
        pseudo = str(input("\nSignature (pseudo) > \033[1;36m")).strip()
        play_sound("handwriting")
        if pseudo == "":
            pseudo = "Vous"
        data["player"]["nickname"] = pseudo

        slow_print((
            "\n\033[0mIl vous voile les yeux de force. Vous entendez le claquement sourd de la porte métallique.",
            "Une nausée commence à vous prendre... Votre tête brule... Vos tympans bourdonnent...",
            "Vous vous sentez tel un Ampèremètre branché en parallèle...",
            "Et vous perdez connaissance."))
        print("...")
        play_sound("teleport")
        time.sleep(2)

        return True


def launch_starters_scene(data):
    clear_console()
    nickname = data["player"]["nickname"]

    slow_print((
                f"\n{player_speaks(nickname)} : « ... Qu’est que... Où suis-je tombé ? »",
                "\nDevant vous, se trouve plusieurs armes difformes éparpillées sur le sol.",
                f"\n{incognito} : « Bienvenue dans la tête du Roi, agent {nickname} »",
                f"{incognito} : « Votre objectif sera de le \033[1;31mTuER\033[0m »",
                f"{incognito} : « Faites vos preuves et vous deviendrez un héros national »",
                f"{incognito} : « Choisissez une arme. »"))

    weapon_slot_1 = choose_starter(starters)
    starters.remove(weapon_slot_1)
    play_sound("bell")

    print(f"\n{incognito} : « Ah, j'ai oublié de préciser que vous pourrez faire une attaque combinée... si vous êtes à la hauteur ? »")

    weapon_slot_2 = choose_starter(starters)
    starters.remove(weapon_slot_2)
    play_sound("bell")

    weapon_slot_3 = choose_starter(starters)
    starters.remove(weapon_slot_3)
    play_sound("bell")

    slow_print((f"\n{incognito} : « Ce dernier objet est un sac dans lequel tu devras mettre tes trouvailles »",
               f"{incognito} : « Tu n'es pas le premier à t'en servir c'est pour ça qu'il est miteux »"))
    play_sound("bell")
    data["player"]["objects_inv"] =  {"object_slot_1":{"name": OBJ_STARTER.name, "effect": OBJ_STARTER.effect, "value": OBJ_STARTER.value}}

    selected_weapons = [weapon_slot_1,weapon_slot_2,weapon_slot_3]

    for n, weapon in enumerate(selected_weapons):
        data["player"]["weapons_inv"][f"weapon_slot_{n+1}"]={
            "name": weapon.name,
            "power": weapon.power,
            "stim": weapon.stim,
            "mana": weapon.mana
        }


    # DEFAULT STATS
    data["player"]["pv"] = data["player"]["max_pv"] = 100
    data["player"]["stim"] = 300
    data["player"]["max_stim"] = 500

    stop_sound(2000)

    print(f"{incognito} : « Attention un ennemi a été repéré ! »")
    input()

def launch_tuto_fight(player):
    tuto_enemy = Monster("Enemy gez", 200, Weapon("Arme éclaté", 20, 0, 0), 1)
    result = Fight(player, tuto_enemy).fight_loop()
    return result

def launch_keep_fighting(difficulty, player, used_monsters):
    MONSTER_NAMES, WEAPON_NAMES = get_cst_names()
    clear_console()

    print("Tu t'enfonces dans les ténèbres à la recherche d'une réponse")

    available_enemies = []
    for i in MONSTER_NAMES:
        if i not in used_monsters:
            available_enemies.append(i)

    if len(available_enemies) == 0:
        available_enemies = MONSTER_NAMES.copy()
        used_monsters.clear()

    new_enemy_name = random.choice(available_enemies)
    used_monsters.append(new_enemy_name)
    new_enemy_pv = int(200*1.2**difficulty)
    new_weapon_name = random.choice(WEAPON_NAMES)
    new_weapon_power = int(10*1.2**difficulty)

    new_enemy = Monster(new_enemy_name, new_enemy_pv, Weapon(new_weapon_name, new_weapon_power, 0, 0), 1)
    # FAIRE DES RANDOMS WEAKNESSES !!!!!!!!!!!!!

    player.max_pv = int(100*1.1**difficulty)
    player.pv = int(min(player.pv, player.max_pv)) # Mettre int a corrigé qqch, jsp quoi

    result = Fight(player, new_enemy).fight_loop()

    if result is True:
        if len(player.inventory) >= MAX_INV_SIZE:
            print("Inventaire plein, pas de loot")
            input()
        else:
            loot = enemy_loot(difficulty,player.inventory)
            player.inventory.append(loot)
            print(f"\n L'ennemi a laissé tomber {loot.name} (Effet: {loot.effect} {loot.value})")
            input()

    return result