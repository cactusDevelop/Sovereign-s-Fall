import json
import random

from json_manager import get_cst_names, save_hs, clear_save
from weapon import generate_starters
from musics import play_sound, stop_sound
from characters import Monster
from weapon import Weapon, gen_boss_weapon
from object import Object, enemy_loot, MAX_INV_SIZE
from fight import Fight
from global_func import *
from online_highscores_hors_projet import save_score_with_fallback



incognito = " \033[1;32m???\033[0m"
red = "\033[1;31m"
green = "\033[1;32m"
cyan = "\033[1;36m"
blue = "\033[1;94m"

#starters = generate_starters() A cause de random.seed()
OBJ_STARTER = Object("Sac des abîmes", "new_obj", 0)
CHEAT_WEAPON = Weapon("Mange tes morts", 999, 999, 0, 0)

# EQUILIBRAGE
PLAYER_I_PV = 100
PLAYER_I_MANA = 10
PLAYER_I_ULT = 200
PLAYER_SCALE = 1.16

MONSTER_I_PV = 200
MONSTER_I_POWER = 10
MONSTER_SCALE = 1.18

BOSS_I_PV = 200
BOSS_I_POWER = 15
BOSS_SCALE = 1.20

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    cst = json.load(read_file)
    RANDOM_LINES = cst.get("rand_lines", ["\nTu t'enfonces dans les ténèbres à la recherche d'une réponse..."])
    WEAKNESSES = cst.get("weaknesses", {})


MAX_NAME_SIZE = get_width()//3
def clean_nick(nickname):
    nickname = nickname.strip()
    if not nickname:
        return f"Joueur{random.randint(1, 99)}"
    if len(nickname) > MAX_NAME_SIZE:
        return nickname[:MAX_NAME_SIZE-3]+"..."
    return nickname

def choose_starter(s_list):
    def to_display():
        left_offset = 8
        for j in s_list:
            print(f"[{s_list.index(j) + 1}] {j.name}:" + " "*(left_offset-len(j.name)) + f"Power {j.power}, Ult Charge {j.stim}, Mana {j.mana}")
    def conf(action_input):
        return action_input.isdigit() and 0 < int(action_input) <= len(s_list)

    choice = solid_input(conf, to_display)
    return s_list[int(choice)-1]

def game_over(data,x:int,des:str):
    clear_console()
    stop_sound(1000)

    seed = data["seed"]
    nickname = data["player"]["nickname"]
    score = data["player"]["score"]
    level = data["player"]["current_level"]
    is_cheating = data.get("cheat", False)

    test_high = False
    if score > 0 and not is_cheating:
        new_hs = save_score_with_fallback(nickname, score, level, save_hs) # [BALISE ONLINE HIGHSCORES]
        test_high = (score == new_hs)

    print("\n\033[7m" + "=" * get_width())
    print(f"\033[1m  GAME OVER\033[0;7m" + " "*(get_width()-11))
    print(f"  Fin {x} - {des}" + " " * (get_width()-9-len(str(x))-len(des)))
    print(f"  Score - {score}" + " " * (get_width()-9-len(str(x))-len(str(score))))
    print(f"  Seed - {seed}" + " "*(get_width()-9-len(str(seed))))
    if is_cheating:
        print("  Pas de gloire aux tricheurs, score perdu !" + " "*(get_width()-45))
    if test_high:
        print(f" >>> NEW HIGHSCORE <<<" + " "*(get_width()-22))
    print(" " * get_width() + "\n" + " " * get_width())
    print("=" * get_width() + "\033[0m")

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
        f"\n{green}"
        "\n *sauvegarde auto*"
        "\n"
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
        "\n   Pour continuer : Appuyer sur -> \033[1mENTER <- \033[0;32m"))
    wait_input()

    play_sound("intro")
    title = center_txt((
        f"{blue}\n",
        "\n",
        "\n",
        "\n",
        "  ██████  ▒█████   ██▒   █▓▓█████  ██▀███  ▓█████  ██▓  ▄████  ███▄    █   ██████      █████▒▄▄▄       ██▓     ██▓    ",
        "▒██    ▒ ▒██▒  ██▒▓██░   █▒▓█   ▀ ▓██ ▒ ██▒▓█   ▀ ▓██▒ ██▒ ▀█▒ ██ ▀█   █ ▒██    ▒    ▓██   ▒▒████▄    ▓██▒    ▓██▒    ",
        "░ ▓██▄   ▒██░  ██▒ ▓██  █▒░▒███   ▓██ ░▄█ ▒▒███   ▒██▒▒██░▄▄▄░▓██  ▀█ ██▒░ ▓██▄      ▒████ ░▒██  ▀█▄  ▒██░    ▒██░    ",
        "  ▒   ██▒▒██   ██░  ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ▒▓█  ▄ ░██░░▓█  ██▓▓██▒  ▐▌██▒  ▒   ██▒   ░▓█▒  ░░██▄▄▄▄██ ▒██░    ▒██░    ",
        "▒██████▒▒░ ████▓▒░   ▒▀█░  ░▒████▒░██▓ ▒██▒░▒████▒░██░░▒▓███▀▒▒██░   ▓██░▒██████▒▒   ░▒█░    ▓█   ▓██▒░██████▒░██████▒",
        "▒ ▒▓▒ ▒ ░░ ▒░▒░▒░    ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░░░ ▒░ ░░▓   ░▒   ▒ ░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░    ▒ ░    ▒▒   ▓▒█░░ ▒░▓  ░░ ▒░▓  ░",
        "░ ░▒  ░ ░  ░ ▒ ▒░    ░ ░░   ░ ░  ░  ░▒ ░ ▒░ ░ ░  ░ ▒ ░  ░   ░ ░ ░░   ░ ▒░░ ░▒  ░ ░    ░       ▒   ▒▒ ░░ ░ ▒  ░░ ░ ▒  ░",
        "░  ░  ░  ░ ░ ░ ▒       ░░     ░     ░░   ░    ░    ▒ ░░ ░   ░    ░   ░ ░ ░  ░  ░      ░ ░     ░   ▒     ░ ░     ░ ░   ",
        "      ░      ░ ░        ░     ░  ░   ░        ░  ░ ░        ░          ░       ░                  ░  ░    ░  ░    ░  ░",
        "                       ░                                                                                              ",
        "\n",
        "\033[0m"))
    slow_print(title, max(random.gauss(0.2,0.06), 0))
    wait_input()

    clear_console()
    play_sound("wood-creak")
    quick_print((
        "\nVous vous réveillez dans un pièce sombre qui vous est inconnue.",
        "Un homme tout de noir vêtu vous tend un parchemin.",
        f"\n{incognito} : « Complétez ceci »"))
    play_sound("paper-collect")
    slow_print(center_txt((
        " _________________________________________________________________ ",
        "|                                                                 |",
        "|                                                                 |",
        "|   Vous avez eu l’exceptionnellement incroyable chance           |",
        "|   d’être sélectionné pour prendre part au programme *XXXXX*.    |",
        "|                                                                 |")), 0.2)
    wait_input()
    play_sound("paper-rustle")
    slow_print(center_txt((
        "|                                                                 |",
        "|   - Toute atteinte à la sécurité du participant durant le       |",
        "|   programme relève de son entière responsabilité.               |",
        "|   - Le participant n’est pas autorisé à interrompre le          |",
        "|   programme avant la fin.                                       |")), 0.2)
    wait_input()
    play_sound("paper-rustle")
    slow_print(center_txt((
        "|                                                                 |",
        "|   Je soussigné (nom, prénom)...............................     |",
        "|   accepte en toute connaissance de cause, les conditions        |",
        "|   présentée cfr supra.                                          |",
        "|                                                                 |",
        "|_________________________________________________________________|")), 0.05)

    print(f"\n{incognito} : « Avez-vous lu et accepté ce contrat » ")

    def to_display():
        print(f"\n{incognito} : « Nous réitérons notre demande... »")
        print(f"{incognito} : « Acceptez-vous ce contrat » (oui/non)")
        play_sound("hmm")
    def conf(action_input):
        return action_input.lower() in ["oui", "non"]

    agreement = input(" > ").strip().lower()
    if agreement != "oui" and agreement != "non":
        agreement = solid_input(conf,to_display)

    if agreement.lower() == "non":
        pseudo = clean_nick(input(f"\nPseudo > {cyan}"))
        data["player"]["nickname"] = pseudo

        print(f"\n {cyan + pseudo}\033[0m : « Va te faire foutre. »")
        wait_input()
        play_sound("laughter")
        print(f"{incognito} : « Pensez-vous avoir le choix ? »")
        time.sleep(2)
        return False

    else:
        pseudo = clean_nick(input(f"\nSignature (pseudo) > {cyan}"))
        play_sound("handwriting")
        play_sound("door-shut")
        data["player"]["nickname"] = pseudo

        quick_print((
            "\n\033[0mIl vous voile les yeux de force. Vous entendez le claquement sourd d'une porte métallique.",
            "Une nausée commence à vous prendre... Votre tête brule... Vos tympans bourdonnent...",
            "Vous vous sentez tel un Ampèremètre branché en parallèle...",
            "Et vous perdez connaissance."))
        print("...")
        play_sound("teleport")
        time.sleep(2)

        return True


def launch_starters_scene(data):
    clear_console()
    starters = generate_starters()
    nickname = data["player"]["nickname"]

    quick_print((
                f"\n {cyan + nickname}\033[0m : « ... Qu’est que... Où suis-je tombé ? »",
                "\nDevant vous, se trouve plusieurs armes difformes éparpillées sur le sol.",
                f"\n{incognito} : « Bienvenue dans la tête du Roi, agent {nickname} »",
                f"{incognito} : « Votre objectif sera de le {red}TuER\033[0m »",
                f"{incognito} : « Pour ce faire, détruisez les fragments de son esprit que vous rencontrerez »",
                f"{incognito} : « Choisissez une arme. »"))

    print()
    weapon_slot_1 = choose_starter(starters)
    starters.remove(weapon_slot_1)
    play_sound("bell")

    quick_print((f"\n{incognito} : « Ah, j'ai oublié de préciser que vous pourrez faire une attaque combinée... »",
                f"{incognito} : « Donc vous aurez besoin de deux autres armes supplémentaires. »"))

    print("\n <2e arme>")
    weapon_slot_2 = choose_starter(starters)
    starters.remove(weapon_slot_2)
    play_sound("bell")

    print("\n <3e arme>")
    weapon_slot_3 = choose_starter(starters)
    starters.remove(weapon_slot_3)
    play_sound("bell")

    quick_print((f"\n{incognito} : « Je te donne un dernier objet : un sac dans lequel tu devras mettre tes trouvailles »",
               f"{incognito} : « Tu n'es pas le premier à t'en servir c'est pour ça qu'il y a quelques déchets dedans »"))
    play_sound("bell")
    data["player"]["objects_inv"] =  {"object_slot_1":{"name": OBJ_STARTER.name, "effect": OBJ_STARTER.effect, "value": OBJ_STARTER.value}}

    selected_weapons = [weapon_slot_1,weapon_slot_2,weapon_slot_3]

    if data.get("cheat", False):
        print(f"\n{incognito} : « Tiens tiens tiens... tu as triché ? Bah tiens chacal »")
        wait_input()

        selected_weapons.append(CHEAT_WEAPON)
        play_sound("bell")
        print(f""" > Arme "{CHEAT_WEAPON.name}" récupérée""")
        print()

    for n, weapon in enumerate(selected_weapons):
        data["player"]["weapons_inv"][f"weapon_slot_{n+1}"]={
            "name": weapon.name,
            "power": weapon.power,
            "stim": weapon.stim,
            "mana": weapon.mana
        }


    # DEFAULT STATS
    data["player"]["pv"] = data["player"]["max_pv"] = 100
    data["player"]["stim"] = 100
    data["player"]["max_stim"] = 200 # Attention ce n'est pas pris en compte ici mais dans le scale d'ult et mana
    data["player"]["mana"] = data["player"]["max_mana"] = 10

    stop_sound(2000)

    print(f"{incognito} : « Attention un fragment a été repéré ! »")
    wait_input()

def launch_tuto_fight(player):
    tuto_enemy = Monster("Tuto", 200, Weapon("Épée classique", 10, 0, 0, 0), 1)
    result = Fight(player, tuto_enemy, 0, True).fight_loop()
    return result

def launch_keep_fighting(difficulty, player, used_monsters):
    clear_console()
    stop_sound(1000)

    MONSTER_NAMES, BOSS_NAMES, WEAPON_NAMES = get_cst_names()
    is_bossfight = (difficulty % 5 == 0 and difficulty != 0)

    if is_bossfight:
        print("\nBoss puissant en approche !")
        boss_name = f"BOSS {random.choice(BOSS_NAMES).upper()}"

        boss_pv = int(BOSS_I_PV*BOSS_SCALE**difficulty)
        boss_power = int(BOSS_I_POWER*BOSS_SCALE**difficulty)

        boss_weapon = Weapon("Arme très puissante", boss_power, 0, 0, 0)
        new_enemy = Monster(boss_name, boss_pv, boss_weapon, 0)

        player.pv = int(player.max_pv//(4/3))
        player.mana = player.max_mana//2

    else:
        print()
        print(random.choice(RANDOM_LINES))

        available_enemies = []
        for i in MONSTER_NAMES:
            if i not in used_monsters:
                available_enemies.append(i)

        if len(available_enemies) == 0:
            available_enemies = MONSTER_NAMES.copy()
            used_monsters.clear()

        new_enemy_name = random.choice(available_enemies)
        used_monsters.append(new_enemy_name)
        new_enemy_pv = int(MONSTER_I_PV*MONSTER_SCALE**difficulty)
        new_weapon_name = random.choice(WEAPON_NAMES)
        new_weapon_power = int(MONSTER_I_POWER*MONSTER_SCALE**difficulty)
        new_weakness = random.choice(list(WEAKNESSES.keys()))

        new_enemy = Monster(new_enemy_name, new_enemy_pv, Weapon(new_weapon_name, new_weapon_power, 0, 0, 0), new_weakness)

        player.max_pv = int(PLAYER_I_PV*PLAYER_SCALE**difficulty)
        player.pv = player.max_pv
        player.max_mana = int(PLAYER_I_MANA*PLAYER_SCALE**difficulty)
        player.mana = player.max_mana
        player.max_stim = int(PLAYER_I_ULT*PLAYER_SCALE**difficulty)

    # START FIGHTIN'
    result = Fight(player, new_enemy, difficulty).fight_loop()

    if result is True:
        if is_bossfight:
            print("\nTu as battu un haut offier de l'espace mental Roi")
            print("Son arme a l'air forte...")
            wait_input()
            clear_console()
            play_sound("bell")

            b_weapon = gen_boss_weapon(difficulty)

            def to_display():
                print("Choisir une arme à jeter :")
                for i, weapon in enumerate(player.weapons):
                    print(f"[{i+1}] {weapon.name} (Att: {weapon.power}, Ult: {weapon.stim}, Mana: {weapon.mana}, Buffs: {weapon.buff_count})")
                print(f"[{len(player.weapons)+1}] {b_weapon.name} (Att: {b_weapon.power}, Ult: {b_weapon.stim}, Mana: {b_weapon.mana}, Buffs: 0)")
            def conf(action_input):
                return action_input.isdigit() and 0 < int(action_input) <= len(player.weapons) +1

            choice = int(solid_input(conf, to_display)) - 1

            if choice < len(player.weapons):
                print(f"""\n"{player.weapons[choice].name}" jetée""")
                play_sound("bell") # Throw sound better
                player.weapons[choice] = b_weapon
            else:
                print(f"\n{b_weapon.name} jetée")
                play_sound("bell")

            wait_input()


        else:
            if len(player.inventory) >= MAX_INV_SIZE:
                print("Inventaire plein, pas de loot")
                wait_input()
            else:
                loot = enemy_loot(difficulty,player.inventory)
                player.inventory.append(loot)
                print(f"""\n L'ennemi a laissé tomber "{loot.name}" (Effet: {loot.effect} {loot.value})""")
                wait_input()

    return result