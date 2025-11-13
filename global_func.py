
import os


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

def solid_input(conf, to_display):
    to_display()
    action_input = input(" > ").strip()

    while not conf(action_input):
        clear_console()
        to_display()
        print("\033[3m\nValeur invalide...\033[0m")
        action_input = input(" > ").strip()

    return action_input