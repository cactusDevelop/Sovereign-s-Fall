
from musics import play_sound


ULT_COEFFICIENT = 4
red = "\033[1;31m"
cyan = "\033[1;36m"

class Character:
    """
    Classe commune à tous les personnages du jeu
    """
    def __init__(self, name: str, pv: int, max_pv:int):
        self.name = name
        self.pv = pv
        self.max_pv = max_pv
        self.weapon = None

    def attack(self, target):
        """
        Sert à diminuer les PV de la cible
        :param target: cible de l'attaque
        :return:
        """
        if hasattr(target, "calc_dmg"): #quand l'ennemi attaque
            return target.calc_dmg(self.weapon.power, self.weapon.name)
        else: # qd joueur attaque
            target.pv = max(target.pv - int(self.weapon.power*target.nerf_defense), 0)
            print(f"""Arme "{cyan + self.weapon.name}\033[0m" inflige {self.weapon.power} dégats à "{red + target.name}\033[0m" ({target.pv} PV restants)""")
            return None


class Player(Character):
    def __init__(self, name:str, pv:int, max_pv:int, stim:int, max_stim:int, mana:int, max_mana:int, weapons:list, inventory:list):
        super().__init__(name, pv, max_pv)
        self.stim = stim
        self.max_stim = max_stim
        self.mana = mana
        self.max_mana = max_mana
        self.weapons = weapons
        self.inventory = inventory
        self.shield_pv = 0
        self.can_ult = (self.stim == self.max_stim)

    def charge(self, x):
        """
        Sert à charger l'ult et la variable can_ult devient true si la jauge d'ult est pleine
        :param x: valeur de rechargement de l'ult
        :return: /
        """
        self.stim = min(self.stim+x, self.max_stim)
        self.can_ult = (self.stim == self.max_stim)

    def mana_ult_charge(self, x):
        """
        Sert à charger l'ult et donner du mana en même temps, utile car certains objets font les deux
        :param x: valeur de rechargement
        :return: /
        """
        self.mana = min(self.mana + x, self.max_mana)
        self.stim = min(self.stim + 10*x, self.max_stim)

    def ult(self, target):
        """
        Vérifie si le joueur peut ult grâce à la variable can_ult et diminue les PV de la cible
        Moyenne géométrique des dégats des armes
        :param target: cible de l'ult
        :return: succès-> None, erreur-> [DEBUG]
        """
        if self.can_ult:
            dgt = 1
            for weapon in self.weapons:
                dgt *= max(weapon.power,1)

            dgt = int(ULT_COEFFICIENT*(dgt**(1/len(self.weapons)))*target.nerf_defense)

            target.pv = max(target.pv-dgt, 0)
            print(f"Vos armes s'unissent et attaquent de {dgt} dégats !")

            self.can_ult = False
            self.stim = 0
            return None
        else:
            return "[DEBUG] NE PEUT PAS ULT"

    def heal(self, x):
        """
        Sert à soigner
        :param x: valeur du soin
        :return: /
        """
        self.pv = min(self.pv+x, self.max_pv)

    def use_obj(self, obj_position):# AJouter enemy=None ici aussi
        """
        stocke le numéro de place de l'objet dans l'inventaire dans la variable obj
        :param obj_position: objet à utiliser
        :return: False si l'objet ne peut pas être utiliser
        """
        if 0 <= obj_position < len(self.inventory):
            obj = self.inventory[obj_position]

            if obj.effect == "new_obj" and len(self.inventory) >= 6:
                print("Inventaire plein...")
                return False
            else:
                check = obj.use(self)
                if obj.effect != "new_obj" and check:
                    self.inventory.pop(obj_position) # pop or remove ?
                return True if check is not False else False
        else:
            print("[DEBUG] Pas d'objet")
            return False

    def shield(self, s_pv):
        """
        Sert à donner un bouclier
        :param s_pv: valeur du bouclier
        :return: /
        """
        self.shield_pv = max(self.shield_pv, s_pv) # Bouclier fort écrase bouclier faible
        print(f"Bouclier de {self.shield_pv} Pv actif")

    def calc_dmg(self, damage, weapon_name="Attaque ennemie"):
        """
        diminue les PV en fonction des dégats de l'arme et en tenant compte d'éventuel bouclier
        :param damage: nombre de dégats de l'arme
        :param weapon_name: nom de l'arme
        :return:
        """
        if self.shield_pv > 0:
            if damage >= self.shield_pv:
                self.shield_pv = 0
                print(f"""Arme "{red + weapon_name}\033[0m" détruit votre Bouclier""")
                play_sound("drop-shield")
            else:
                self.shield_pv = self.shield_pv - damage
                print(f"""Arme "{red + weapon_name}\033[0m" inflige {damage} dégats au bouclier ({cyan + str(self.shield_pv)}\033[0m PV bouclier restants)""")
                play_sound("shield")

        else:
            self.pv = max(self.pv - damage, 0)
            print(f"""Arme "{red + weapon_name}\033[0m" inflige {damage} dégats à "{cyan + self.name}\033[0m" ({self.pv} PV restants)""")
            play_sound("monster-attack")


class Monster(Character):
    def __init__(self, name: str, pv: int, weapon, weakness=0):
        """
        :param name: nom du monstre
        :param pv: pv du montre
        :param weapon: arme du monstre
        :param weakness: faiblesse du montre
        """
        super().__init__(name, pv, pv)
        self.weapon = weapon
        self.weakness = weakness
        self.nerf_defense = 1.0
