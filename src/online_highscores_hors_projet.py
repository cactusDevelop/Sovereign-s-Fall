#  ____________________
# /                    \
# !     ATTENTION      !
# !                    !
# \____________________/
#          !  !
#          !  !               Code généré par IA, l'unique but de ce fichier
#          L_ !               est de rendre le jeu plus agréable aux beta-testeurs
#         / _)!               En aucun cas, ce fichier ne fait parti de l'évaluation.
#        / /__L
#  _____/ (____)              cfr [BALISE ONLINE HIGHSCORES] pour code associé
#         (____)
#  _____  (____)
#       \_(____)
#          !  !
#          !  !
#          \__/
#


"""
Système de highscores en ligne via GitHub - VERSION SÉCURISÉE
"""
import time

import requests
import json
import base64
import os


# CHARGEMENT SÉCURISÉ DE LA CONFIGURATION
def load_config():
    """Charge la config depuis config.json (ignoré par git)"""
    config_path = "JSON/config.json"

    if not os.path.exists(config_path):
        print("[INFO] Aucune configuration trouvée - Mode local uniquement")
        return None

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)

        if not config.get("github_token") or not config.get("github_repo"):
            print("[INFO] Configuration incomplète - Mode local uniquement")
            return None

        return config
    except Exception as e:
        print(f"[ERREUR] Impossible de charger la config: {e}")
        return None


# Chargement de la config au démarrage
CONFIG = load_config()

# Si pas de config, les fonctions fonctionneront en mode local uniquement
GITHUB_TOKEN = CONFIG.get("github_token") if CONFIG else None
GITHUB_REPO = CONFIG.get("github_repo") if CONFIG else None
FILE_PATH = "JSON/highscores.json"

API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{FILE_PATH}" if GITHUB_REPO else None


class OnlineHighscores:
    def __init__(self):
        self.enabled = CONFIG is not None

        if self.enabled:
            self.headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            self.local_cache = None
            self.last_sha = None
        else:
            print("[INFO] Highscores en ligne désactivés (pas de config)")

    def fetch_online_scores(self):
        """Récupère les scores depuis GitHub"""
        if not self.enabled:
            return None

        try:
            response = requests.get(API_URL, headers=self.headers, timeout=5)

            if response.status_code == 200:
                data = response.json()
                self.last_sha = data['sha']

                # DEBUG: Afficher le contenu brut
                #print(f"[DEBUG] Content encodé (100 premiers chars): {data['content'][:100]}")

                content = base64.b64decode(data['content']).decode('utf-8')

                # DEBUG: Afficher le contenu décodé
                #print(f"[DEBUG] Content décodé: {content}")

                self.local_cache = json.loads(content)
                #print(f"[DEBUG] JSON parsé: {self.local_cache}")

                return self.local_cache

        except requests.exceptions.Timeout:
            print("[ERREUR] Timeout - Vérifiez votre connexion internet")
            return None
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la récupération: {e}")
            import traceback
            traceback.print_exc()
            return None

    def create_initial_file(self, data):
        """Crée le fichier initial sur GitHub"""
        if not self.enabled:
            return False

        try:
            content = json.dumps(data, indent=4, ensure_ascii=False)
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

            payload = {
                "message": "Initialisation du classement",
                "content": encoded_content
            }

            response = requests.put(API_URL, headers=self.headers, json=payload, timeout=5)

            if response.status_code == 201:
                self.last_sha = response.json()['content']['sha']
                print("[INFO] Fichier de scores créé avec succès !")
                return True
            else:
                print(f"[ERREUR] Création échouée: {response.status_code}")
                return False
        except Exception as e:
            print(f"[ERREUR] Erreur lors de la création: {e}")
            return False

    def push_score(self, nickname, score, level):
        """Envoie un nouveau score sur GitHub"""
        if not self.enabled:
            return False

        try:
            current_data = self.fetch_online_scores()

            if current_data is None:
                print("[ERREUR] Impossible de synchroniser les scores")
                return False

            current_data["history"].append({
                "nickname": nickname,
                "score": int(score),
                "level": int(level)
            })

            current_data["history"] = sorted(
                current_data["history"],
                key=lambda x: x["score"],
                reverse=True
            )[:10]

            if score > current_data.get("highscore", 0):
                current_data["highscore"] = score

            content = json.dumps(current_data, indent=4, ensure_ascii=False)
            encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

            payload = {
                "message": f"Nouveau score: {nickname} - {score} pts",
                "content": encoded_content,
                "sha": self.last_sha
            }

            response = requests.put(API_URL, headers=self.headers, json=payload, timeout=5)

            if response.status_code == 200:
                self.last_sha = response.json()['content']['sha']
                print(f"[SUCCESS] Score envoyé en ligne ! 🎉")
                return True
            else:
                print(f"[ERREUR] Envoi échoué: {response.status_code}")
                return False

        except Exception as e:
            print(f"[ERREUR] Erreur lors de l'envoi: {e}")
            return False

    def get_top_10(self):
        """Récupère le top 10 actuel"""
        if not self.enabled:
            return None

        data = self.fetch_online_scores()
        if data:
            return data.get("history", [])
        return None

    def get_highscore(self):
        """Récupère le meilleur score"""
        if not self.enabled:
            return None

        data = self.fetch_online_scores()
        if data:
            return data.get("highscore", 0)
        return None


# FONCTIONS SIMPLES À UTILISER
def save_online_score(nickname, score, level):
    """Sauvegarde un score en ligne - Retourne True si succès, False sinon"""
    online = OnlineHighscores()
    return online.push_score(nickname, score, level)


def get_online_leaderboard():
    """Récupère le classement en ligne - Retourne None si pas disponible"""
    online = OnlineHighscores()
    return online.get_top_10()


def get_online_highscore():
    """Récupère le meilleur score - Retourne None si pas disponible"""
    online = OnlineHighscores()
    return online.get_highscore()


# MODE HYBRIDE (Online + Local fallback)
def save_score_with_fallback(nickname, score, level, local_save_func):
    """
    Essaie de sauvegarder en ligne, sinon sauvegarde localement
    Retourne toujours le highscore (online ou local)
    """
    online_success = False

    try:
        if save_online_score(nickname, score, level):
            online_success = True
            print("✓ Score sauvegardé en ligne")
    except:
        pass

    # Toujours sauvegarder localement aussi (backup)
    local_highscore = local_save_func(nickname, score, level)

    if not online_success:
        print("⚠ Sauvegarde locale uniquement")

    return local_highscore