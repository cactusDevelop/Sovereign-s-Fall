
import os, time
import random

from musics import play_sound, stop_sound


MAX_NAV_ITERATIONS = 30
FADE_OUT = 3500 #ms
MAX_ANALYSIS = 10
MISS_CHANCE = 0.05

def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def get_width(): # La fct était déjà dans scenes.py mais je ne vx pas d'import circulaire
    try:
        columns = os.get_terminal_size().columns
    except OSError:
        columns = 80
    return columns


class Fight:
    def __init__(self, player, enemy, level=1):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.weakness_turns_remaining = 0
        self.analysis_count = MAX_ANALYSIS
        self.level = level


    def fight_loop(self):
        input("\nPrêt ?")
        print(f"\n{self.player.name} engage le combat contre \033[1;32m{self.enemy.name}\033[0;0m")
        play_sound("nightwalker", True)

        while True:
            self.turn_count += 1

            self.weakness_turns_remaining = max(self.weakness_turns_remaining - 1, 0)

            p_turn_conclu = self.player_turn()
            if p_turn_conclu == "Att":
                play_sound("sword-sound")
            elif p_turn_conclu == "Obj":
                play_sound("bell")
            elif p_turn_conclu == "Ana":
                play_sound("bell")
            elif p_turn_conclu == "gameover2":
                return "gameover2"
            elif p_turn_conclu is None:
                continue

            gagne = self.check_end()
            if gagne and p_turn_conclu == "Att":
                stop_sound(FADE_OUT)
                play_sound("sword-finish")
                time.sleep(1)
                play_sound("win")
                time.sleep(FADE_OUT/1000-1)
                return gagne # Boléen
            elif gagne and p_turn_conclu != "Att":
                stop_sound(FADE_OUT)
                play_sound("win")
                time.sleep(FADE_OUT/1000)
                return gagne


            self.enemy_turn()
            gagne = self.check_end()
            if gagne is False:
                stop_sound(FADE_OUT)
                time.sleep(1)
                play_sound("laughter")
                time.sleep(FADE_OUT/1000-1)
                return gagne # Idem Boléen



    def player_turn(self):
        print("\n" + "=" * 5 + "| \033[1;36m" + self.player.name + "'s turn" + "\033[0m |" + "=" * 15)

        self.player.mana_charge(1)

        instruction, value = self.nav(self.player)

        if instruction == "Weapons":
            equiped_w = self.player.weapons[value]
            self.player.weapon = equiped_w

            if self.player.mana < equiped_w.mana:
                print(f"Mana insuffisant {self.player.mana}/{equiped_w.mana}")
                input()
                return None

            self.player.mana -= equiped_w.mana

            self.player.attack(self.enemy) # Parce qu'on a décidé d'attaquer dès le choix de l'arme
            self.player.charge(self.player.weapon.stim)

            return "Att"

        elif instruction == "Objects":
            action_check = self.player.use_obj(value)
            if action_check:
                return "Obj"
            else:
                return None

        elif instruction == "Analysis":
            if self.analysis_count <= 0:
                print("T'as trop spam la passivité mon gars")
                input()
                return None

            self.analysis_count-=1

            print(f"Point faible adverse : {self.find_weakness()}")
            return "Ana"

        elif instruction == "Ultime":
            print("La volonté des dieux vous accompagnent...")
            self.player.ult(self.enemy)
            return "Ult"

        elif instruction == "sus":
            return "gameover2"

        else:
            return None


    def enemy_turn(self): # ENEMY IA PLS
        clear_console()
        print("\n"+"="*5+"| \033[31m"+self.enemy.name+"'s turn"+"\033[0m |"+"="*15)

        if random.random() < MISS_CHANCE:
            play_sound("miss-swing")
            print(f"{self.enemy.name} rate lamentablement son attaque")
        else:
            self.enemy.attack(self.player)
            play_sound("monster-attack")

        self.display_status()
        input()



    def check_end(self):
        if self.enemy.pv <= 0:
            print("\n VICTOIRE !!!")
            return True

        elif self.player.pv <= 0:
            print("\n Votre corps ne vous répond plus")
            return False

        return None


    def display_status(self): # Vs ici Thomas stv rendre ça stylé
        p_pv_ratio = self.player.pv * 10 // self.player.max_pv
        p_stim_ratio = self.player.stim * 10 // self.player.max_stim
        e_pv_ratio = self.enemy.pv * 10 // self.enemy.max_pv
        left_offset = 2

        line_0 = f" NIVEAU {self.level}"
        line_1 = " "*left_offset + self.player.name.upper() + " "*(get_width()//2-len(self.player.name))
        line_1 += self.enemy.name.upper()
        line_2 = " "*left_offset + "█"*p_pv_ratio + "_"*(10-p_pv_ratio) + " | " + str(self.player.pv) + "/" + str(self.player.max_pv) +" PV"
        if self.player.shield_pv > 0:
            line_2 += f" [Bouclier {self.player.shield_pv}PV]"
        line_2 += " "*(get_width()//2-len(line_2)+left_offset)
        line_2 += "█"*e_pv_ratio + "_"*(10-e_pv_ratio) + " | " + str(self.enemy.pv) + "/" + str(self.enemy.max_pv) +" PV"
        line_3 = " "*left_offset + "█"*p_stim_ratio + "_"*(10-p_stim_ratio) + " | " + str(self.player.stim) + "/" + str(self.player.max_stim) +" ULT"


        print(line_0)
        print()
        print(line_1)
        print(line_2)
        print(line_3)
        if self.weakness_turns_remaining > 0:
            print(" "*left_offset + f" Analysis actif pour {self.weakness_turns_remaining} tour(s)")
        else:
            self.enemy.weapon.power = self.enemy.weapon.original_power
        print()


    def find_weakness(self): #Attention la faiblesse n'est activée qu'à l'appel de la fct, après si c fait exprès...
        if self.enemy.weakness == 0:
            return "Que dalle"
        if self.enemy.weakness == 1:
            self.enemy.weapon.power = max(self.enemy.weapon.power-10, 0)
            self.weakness_turns_remaining = 3
            return "Enemy affaibli (-10 Att) pour 3 tours"

        print("[DEBUG] Big Error : le num de faiblesse n'existe pas")
        return None


    def nav(self, player):
        nav_menu = ["Weapons", "Objects", "Analysis"]

        if player.can_ult:
            nav_menu.append("Ultime")

        current_pos = "Nav"

        for it in range(MAX_NAV_ITERATIONS):
            clear_console()
            self.display_status()


            if current_pos == "Nav":
                print("=" * 10 + "Menu" + "=" * 10)
                for i, option in enumerate(nav_menu):
                    if option == "Analysis":
                        print(f"[{i + 1}] {option} ({self.analysis_count})")
                    else:
                        print(f"[{i+1}] {option}")

                action = nav_def(nav_menu)
                current_pos = nav_menu[action]

            elif current_pos == "Weapons":
                print("="*10 + "Weapons" + "="*10)
                for i, option in enumerate(player.weapons):
                    print(f"[{i+1}] {option.name} (Att:{option.power}, Stim:{option.stim}, Mana:{option.mana})")
                print(f"[{len(player.weapons)+1}] Retour")

                action = nav_wea_obj(player.weapons)
                if action < 0:
                    current_pos = "Nav"
                else:
                    return "Weapons", action

            elif current_pos == "Objects":
                print("=" * 10 + "Objects" + "=" * 10)
                for i, option in enumerate(player.inventory):
                    effect = "Objet généré aléatoirement" if option.effect == "new_obj" \
                        else f"Soin de {option.value} PV" if option.effect == "heal" \
                        else f"Arme améliorée de {option.value} Att" if option.effect == "att_boost" \
                        else f"Bouclier de {option.value} PV" if option.effect == "shield" \
                        else "[DEBUG] Effet défaillant"
                    print(f"[{i+1}] {option.name} (Effet: {effect})")
                print(f"[{len(player.inventory) + 1}] Retour")

                action = nav_wea_obj(player.inventory)
                if action < 0:
                    current_pos = "Nav"
                else:
                    return "Objects", action

            elif current_pos == "Analysis":
                return "Analysis", 0

            elif current_pos == "Ultime":
                return "Ultime", 0

        print("Arrête de naviguer sans rien faire, reviens quand tu sauras prendre des décisions")
        return "sus", None # Au cas où un con naviguerait 1000 fois sans jouer

def nav_def(nav_s):
    x = input(" > ")
    while not (x.isdigit() and 0 < int(x) <= len(nav_s)): # ² ³ détruisent tt
        print("Valeur invalide")
        x = input(" > ")
    return int(x)-1

def nav_wea_obj(items):
    x = input(" > ")
    while not (x.isdigit() and 0 < int(x) <= (len(items)+1)):
        print("Valeur invalide")
        x = input(" > ")
    if int(x) == (len(items)+1):
        return -1
    else:
        return int(x)-1
