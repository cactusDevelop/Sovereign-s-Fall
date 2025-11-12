
# cd..\..\Users\Cactusdev\OneDrive\Desktop\Roguelike\RoguelikeProject

import pygame

from json_manager import *
from scenes import *


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
    clear_console()
    if not pygame.mixer.music.get_busy():
        play_sound("menu", True)
    print("\n" + "="*5 + "MAIN MENU" + "="*20)

    if hs["highscore"] > 0:
        print("\n " + "_"*10)
        print(f"| TOP 1 : {hs['highscore']} pts")
        if hs["history"]:
            best = hs["history"][0]
            print(f"| par {best['nickname']} (Niveau {best['level']})")
        print("|" + "_"*20)

    print("\n [1] Nouvelle partie")

    if saved_game():
        safe_info = get_save()
        print(f" [2] Charger une partie (Niveau {safe_info['level']})")
    print(" [3] Classement")
    print(" [0] Quitter :‹")

    direc = input("\n > ")
    while direc not in ["0", "1", "2", "3"]:
        if not saved_game() and direc == "2":
            print("Nada...")
        else:
            print("Valeur invalide")
        direc = input("\n > ")
    return int(direc)

def show_hs():
    clear_console()
    print("\n" + "="*get_width())
    print(" "*(get_width()//2-7)+"TOP 10 ALL TIME")
    print()

    if not hs["history"]:
        print("Aucun score...")
    else:
        for rank, p in enumerate(hs["history"], 1):
            print(f"{rank:2}) {str(p['nickname'])[:20]:25} - {p['score']} pts (niveau {p['level']})")
    input("\nRetour >")
    

# CUTSCENES
def run_intro():
    data["player"]["score"] = 0
    data["player"]["current_level"] = 0
    data["used_monsters"] = []

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
                input("Aucune partie sauvegardée ¯\_(ツ)_/¯")
                continue
            print(f"Partie Trouvée! ({get_save()['nickname']} - Niveau {get_save()['level']})")
            input("Let's go >")
            run_fight_loop() # Recommencer au bon niveau !!!!!
        elif menu_to == 3:
            show_hs()
