
import random, json

from global_func import *
from musics import play_sound, stop_sound


MAX_NAV_ITERATIONS = 30
FADE_OUT = 2500 #ms
MAX_ANALYSIS = 4
MISS_CHANCE = 0.05
red = "\033[1;31m"
blue = "\033[0;34m"
cyan = "\033[1;36m"

with open("JSON/cst_data.json", "r", encoding="utf-8") as read_file:
    cst = json.load(read_file)
    WEAKNESSES = cst.get("weaknesses", {})


class Fight:
    def __init__(self, player, enemy, level=1):
        self.player = player
        self.enemy = enemy
        self.turn_count = 0
        self.weakness_turns_remaining = 0
        self.analysis_count = MAX_ANALYSIS
        self.level = level
        self.txt_buffer = []


    def fight_loop(self):
        print(f"\n{cyan}{self.player.name}\033[0m engage le combat contre {red}{self.enemy.name}\033[0m")
        wait_input()
        play_sound("fight", True)

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
                time.sleep(FADE_OUT/1000)
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
        self.player.mana = min(self.player.mana + 1, self.player.max_mana)

        instruction, value = self.nav(self.player)

        if instruction == "Weapons":
            equiped_w = self.player.weapons[value]
            self.player.weapon = equiped_w

            if self.player.mana < equiped_w.mana:
                print(f"Mana insuffisant {self.player.mana}/{equiped_w.mana}")
                wait_input()
                return None

            self.player.mana -= equiped_w.mana

            self.player.attack(self.enemy)
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
                wait_input()
                return None

            self.analysis_count-=1

            print(f"\nMeilleure compréhension : {self.find_weakness()}")
            return "Ana"

        elif instruction == "Ultime":
            print("\nLa volonté des dieux vous accompagnent...")
            self.player.ult(self.enemy)
            return "Ult"

        elif instruction == "sus":
            return "gameover2"

        else:
            return None


    def enemy_turn(self):
        print("\n"+"="*5 + f"| {red}" + self.enemy.name + "'s turn"+"\033[0m |" + "="*(get_width()-16-len(self.enemy.name)))
        print()

        if random.random() < MISS_CHANCE or self.enemy.weapon.power == 0:
            play_sound("miss-swing")
            print(f""""{red+ self.enemy.name}\033[0m" rate lamentablement son attaque""")
        else:
            self.enemy.attack(self.player)

        input("Continuer...")
        clear_console()
        self.display_status()



    def check_end(self):
        if self.enemy.pv <= 0:
            print("\n VICTOIRE !!!")
            return True

        elif self.player.pv <= 0:
            print("\n Votre corps ne vous répond plus")
            return False

        return None


    def display_status(self):
        p_pv_ratio = self.player.pv * 10 // self.player.max_pv
        p_stim_ratio = self.player.stim * 10 // self.player.max_stim
        e_pv_ratio = self.enemy.pv * 10 // self.enemy.max_pv
        p_mana_ratio = self.player.mana * 10 // self.player.max_mana
        p_shield_ratio = self.player.shield_pv * 10 // self.player.max_pv
        left_offset = 2

        pv_bar = ""
        for i in range(10):
            if i < p_shield_ratio and i <= p_pv_ratio:
                pv_bar += blue + "█\033[0m"
            elif i < p_pv_ratio:
                pv_bar += "█"
            elif p_pv_ratio < i < p_shield_ratio:
                pv_bar += blue + "▄\033[0m"
            else:
                pv_bar += "_"

        line_0 = f"\n NIVEAU {self.level}"
        line_1 = "=" * 5 + f"| {cyan}" + self.player.name + "'s turn" + "\033[0m |" + "="*(get_width()-16-len(self.player.name))
        line_2 = " "*left_offset + cyan + self.player.name.upper() + "\033[0m" + " "*(get_width()//2-len(self.player.name))
        line_2 += red + "FRAGMENTUS " + self.enemy.name.upper() + "\033[0m"
        line_3 = " "*left_offset + pv_bar + " | " + str(self.player.pv) + "/" + str(self.player.max_pv) +" PV"
        if self.player.shield_pv > 0:
            line_3 += f" [Bouclier {self.player.shield_pv}PV]"
        line_3 += " "*(get_width()//2-len(line_3)+left_offset)
        line_3 += "█"*e_pv_ratio + "_"*(10-e_pv_ratio) + " | " + str(self.enemy.pv) + "/" + str(self.enemy.max_pv) +" PV"
        line_4 = " "*left_offset + "█"*p_stim_ratio + "_"*(10-p_stim_ratio) + " | " + str(self.player.stim) + "/" + str(self.player.max_stim) +" ULT"
        line_5 = " "*left_offset + "█"*p_mana_ratio + "_"*(10-p_mana_ratio) + " | " + str(self.player.mana) + "/" + str(self.player.max_mana) +" MANA"

        print(line_0)
        print(line_1)
        print()
        print(line_2)
        print(line_3)
        print(line_4)
        print(line_5)

        if self.weakness_turns_remaining > 0:
            print(" "*left_offset + f" -Analysis actif pour {self.weakness_turns_remaining} tour(s)")
        else:
            self.enemy.weapon.power = self.enemy.weapon.original_power
        print()

        if self.txt_buffer:
            print("\n".join(self.txt_buffer))
            print()

    def find_weakness(self):
        weakness = str(self.enemy.weakness)

        if weakness == "0" or weakness not in WEAKNESSES:
            return "Que dalle"

        weakness_data = WEAKNESSES[weakness]
        w_type = weakness_data["type"]
        w_value = weakness_data["value"]
        w_duration = weakness_data["duration"]
        w_message = weakness_data["message"]

        if w_type == "attack":
            self.enemy.weapon.power = max(self.enemy.weapon.power - int(self.enemy.weapon.original_power*(w_value/100)), 0)
            self.weakness_turns_remaining = w_duration + 1
            return w_message

        elif w_type == "heal":
            self.player.heal(w_value)
            return w_message

        else:
            return "[DEBUG] Big Error : la faiblesse n'existe pas"


    def nav(self, player):
        nav_menu = ["Weapons", "Objects", "Analysis"]

        if player.can_ult:
            nav_menu.append("Ultime")

        current_pos = "Nav"

        for it in range(MAX_NAV_ITERATIONS):
            clear_console()

            if current_pos == "Nav":
                def to_display():
                    self.display_status()

                    print("=" * 10 + "Menu" + "=" * 10)
                    for i, option in enumerate(nav_menu):
                        if option == "Analysis":
                            print(f"[{i + 1}] {option} ({self.analysis_count}/{MAX_ANALYSIS})")
                        elif option == "Objects":
                            print(f"[{i + 1}] {option} ({len(player.inventory)}/6)")
                        else:
                            print(f"[{i+1}] {option}")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(nav_menu)

                action = int(solid_input(conf,to_display))-1
                current_pos = nav_menu[action]

            elif current_pos == "Weapons":
                def to_display():
                    self.display_status()
                    print("="*15 + "Weapons" + "="*15)

                    max_len = max(len(w.name.replace('\033[0;93m', '').replace('\033[0m', '')) for w in player.weapons)
                    for i, option in enumerate(player.weapons):
                        clean_name = option.name.replace('\033[0;93m', '').replace('\033[0m', '') # Tt ça à cause du boss
                        offset = " " * (max_len+2-len(clean_name))
                        print(f"[{i+1}] {option.name}{offset}(Att:{option.power}, Ult:{option.stim}, Mana:{option.mana})")
                    print(f"[{len(player.weapons)+1}] Retour")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(player.weapons)+1

                action = int(solid_input(conf, to_display))-1

                if action == len(player.weapons):
                    current_pos = "Nav"
                else:
                    return "Weapons", action

            elif current_pos == "Objects":
                def to_display():
                    self.display_status()
                    print("=" * 10 + "Objects" + "=" * 10)

                    for i, option in enumerate(player.inventory):
                        effect = "Objet généré aléatoirement" if option.effect == "new_obj" \
                            else f"Soin de {option.value} PV" if option.effect == "heal" \
                            else f"Arme améliorée de {option.value} Att" if option.effect == "att_boost" \
                            else f"Bouclier de {option.value} PV" if option.effect == "shield" \
                            else f"Charge de {option.value} MANA" if option.effect == "mana_ult_charge" \
                            else "[DEBUG] Effet défaillant"

                        offset = " " * (max(len(o.name) for o in player.inventory)+2-len(option.name))
                        print(f"[{i+1}] {option.name}{offset}(Effet: {effect})")

                    print(f"[{len(player.inventory) + 1}] Retour")
                def conf(action_input):
                    return action_input.isdigit() and 0 < int(action_input) <= len(player.inventory)+1

                action = int(solid_input(conf, to_display))-1

                if action == len(player.inventory):
                    current_pos = "Nav"
                else:
                    return "Objects", action

            elif current_pos == "Analysis":
                return "Analysis", 0

            elif current_pos == "Ultime":
                return "Ultime", 0

        print("Arrête de naviguer sans rien faire, reviens quand tu sauras prendre des décisions")
        return "sus", None # Au cas où un con naviguerait 1000 fois sans jouer

