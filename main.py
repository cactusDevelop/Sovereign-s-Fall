# cd..\..\Users\Cactusdev\OneDrive\Desktop\Roguelike\RoguelikeProject
# https://github.com/cactusDevelop/RoguelikeProject/tree/master

import pygame, random

from json_manager import *
from global_func import *
from musics import play_sound, stop_sound
from online_highscores_hors_projet import get_online_highscore, get_online_leaderboard
from scenes import launch_cutscene, launch_starters_scene, launch_tuto_fight, game_over


CHEAT_CODE = "zahoe"

# CACHER LES MESSAGES D'ERREUR (parce que c moche)
"""import sys

class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()"""


def add_score(l:int):
    data["player"]["score"] += l

# MENU
def display_menu():
    def to_display_m():
        if not pygame.mixer.music.get_busy():
            play_sound("menu", True)
        print("\n" + "="*5 + "| \033[1mMAIN MENU\033[0m |" + "="*(get_width()-18))

        try:   # [BALISE ONLINE HIGHSCORES]
            online_hs = get_online_highscore()
            if online_hs > 0:
                line_2 = f"░█\033[33;7m RECORD MONDIAL : {online_hs} \033[0m░█"

                print("\n ░█"+"█"*(len(line_2)-15))
                print(line_2)
                #print(f"| par {best['nickname']} (Niveau {best['level']})")
                print(" ░█" + "█"*(len(line_2)-15))
        except:
            if hs["highscore"] > 0:
                print("\n " + "_" * 10)
                print(f"| TOP LOCAL : {hs['highscore']}")
                print("|" + "_" * 20)


        print("\n [1] Nouvelle Partie")
        print(f" [2] Charger Une Partie")
        print(" [3] Classement")
        print(" [4] Dev Mode")
        print(" [0] Quitter :‹")

    def conf_m(action_input):
        return action_input.lower() in ["0", "1", "2", "3", "4", CHEAT_CODE]

    clear_console()
    direc = solid_input(conf_m, to_display_m)

    if direc == CHEAT_CODE:
        print("\n\033[42m >>> CHEAT MODE ACTIVED <<< \033[0m")
        play_sound("win")
        time.sleep(2.5)
        data["cheat"] = True
        return 1

    return int(direc)


def show_hs():  # [BALISE ONLINE HIGHSCORES]
    clear_console()
    print("\n" + "=" * 5 + "| \033[1mALL TIME TOP 10\033[0m |" + "=" * (get_width() - 24))

    GOLD = "\033[38;5;220m"
    SILVER = "\033[38;5;250m"
    BRONZE = "\033[38;5;208m"
    RESET = "\033[0m"

    try:
        online_scores = get_online_leaderboard()
        if online_scores is None:  # <- Changez ici : testez explicitement None
            print("Aucun score en ligne...")
        elif len(online_scores) == 0:  # <- Ajoutez ce test pour liste vide
            print("Aucun score enregistré pour le moment...")
        else:
            for rank, entry in enumerate(online_scores, 1):
                date = entry.get('date', '')[:10] if 'date' in entry else ''

                if rank == 1:
                    color = GOLD
                    medal = "🥇"
                elif rank == 2:
                    color = SILVER
                    medal = "🥈"
                elif rank == 3:
                    color = BRONZE
                    medal = "🥉"
                else:
                    color = ""
                    medal = "  "

                nickname_display = f"{entry['nickname']}"
                score_info = f"{entry['score']} pts (niveau {entry['level']})"
                date_display = f" [{date}]" if date else ""

                print(f"{medal} {rank:2}) {color}{nickname_display:<20}{RESET} - {score_info}{date_display}")
    except:
        print("⚠ Impossible de récupérer les scores en ligne")
        print("\n--- SCORES LOCAUX ---")
        if not hs["history"]:
            print("Aucun score local...")
        else:
            for rank, entry in enumerate(hs["history"], 1):
                nickname = str(entry['nickname'])[:20]
                score_info = f"{entry['score']} pts (niveau {entry['level']})"
                print(f"   {rank:2}) {nickname:<20} - {score_info}")

    input("\nRetour >")


# CUTSCENE
def run_intro():
    if data.get("seed") is None:
        data["seed"] = int((random.getstate()[1][0]*time.time())%67676767)
        random.seed(data["seed"])
    data["player"]["score"] = 0
    data["player"]["current_level"] = 0
    data["used_monsters"] = []
    data["cheat"] = False

    if not launch_cutscene(data):
        game_over(data,1,"Tié mort vite")
        return None

    launch_starters_scene(data)

    player = get_player_data()
    save_game(player, 0, data["used_monsters"])

    tuto_result = launch_tuto_fight(player)

    if not tuto_result:
        game_over(data, 3, "T'abuses...")
        return None
    elif tuto_result == "gameover2":
        game_over(data, 2, "Tu n'es pas la chips la plus croustillante toi")
        return None

    add_score(100)
    data["player"]["current_level"] = 1
    save_game(player, 1, data["used_monsters"])
    run_fight_loop()
    return None


def run_fight_loop():
    from scenes import launch_keep_fighting, game_over

    fighting = True

    while fighting:
        player = get_player_data()
        lvl = data["player"]["current_level"]

        u_m = get_used_monsters()
        fight_result = launch_keep_fighting(lvl, player, u_m)

        if fight_result:
            add_score(20 * lvl)
            lvl += 1
            data["player"]["current_level"] = lvl
            save_game(player, lvl, u_m)
        else:
            fighting = False
            game_over(data, 4, "Parti si tôt...")


# GAME LOOP
if __name__ == "__main__":
    running = True

    while running:
        menu_to = display_menu()

        if menu_to == 0:
            print("\nTu reviendras quand tu seras prêt")
            stop_sound(1500)
            time.sleep(1.7)
            running = False
        if menu_to == 1:
            run_intro()
        elif menu_to == 2:
            if not saved_game():
                input("\nAucune partie sauvegardée... ¯\_(ツ)_/¯")
                continue
            print(f"\nPartie Trouvée: ({get_save()['nickname']} - Niveau {get_save()['level']})")
            print("Let's go ! > ", end="")
            wait_input()
            run_fight_loop()
        elif menu_to == 3:
            show_hs()
        elif menu_to == 4:
            clear_console()
            def to_display():
                print("\n" + "=" * 5 + "| \033[1mDEV MODE\033[0m |" + "=" * (get_width() - 17))
                print("\nVeuillez entrer la seed désirée (0 pour retour)")
            def conf(x):
                return x.isdigit() or (x.startswith("-") and x[1:].isdigit())

            seed = int(solid_input(conf, to_display))

            if seed != 0:
                random.seed(seed)
                data["seed"] = seed
                print(f"[SEEDED RUN] /{seed}/")
                time.sleep(2)

                import scenes
                scenes.starters = None

                run_intro()
            else:
                continue