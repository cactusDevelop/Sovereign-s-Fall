
# TOUTES LES MUSIQUES SONT COPYRIGHT FREE A CE JOUR, JE M'ENGAGE A IMMEDIATEMENT LES RETIRER SI J'APPRENDS QUE LES DROITS DEVIENNENT PROTEGES
"""
Horror Tense Music (Tunetank)
Nightwalker (Cyberpunk)
Password Infinity (Evgeny_Bardyuzha)
SFX issus de Pixabay
"""

import os, random, pygame
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

NOMBRE_CHANNEL = 10


pygame.mixer.init()
pygame.mixer.set_num_channels(NOMBRE_CHANNEL)


def play_sound(which, is_bg=False):
    variantes = []

    if is_bg:
        pygame.mixer.music.load(f"MUSICS/{which}.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.15)
        print("[DEBUG] Music Volume : "+str(pygame.mixer.music.get_volume()))
    else:
        for _ in os.listdir("SFX"):
            if _.startswith(which) and _.endswith(".mp3"):
                variantes.append(_)
        sound = random.choice(variantes)

        f_sound = pygame.mixer.Sound(f"SFX/{sound}")
        pygame.mixer.find_channel(True).play(f_sound)

def stop_sound(ms):
    pygame.mixer.music.fadeout(ms)