import json
from os import path


class Highscores:
    current_directory = path.dirname(path.abspath(__file__))
    _HIGHSCORE_PATH = path.join(current_directory, "highscores.json")
    _DATA = None

    def __init__(self):
        try:
            with open(self._HIGHSCORE_PATH, "r") as f:
                self._DATA = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        self._DATA.sort(key=lambda entry: int(entry.split(":")[0]), reverse=True)
        self.game_saved = False

    def get_top_ten(self):
        return [
            (int(entry.split(": ")[0]), entry.split(": ")[1]) for entry in self._DATA
        ][:10]

    def _save_json(self, score, player_name):
        self.update_highscores(score, player_name)
        with open(self._HIGHSCORE_PATH, "w") as file:
            json.dump(self._DATA, file)

    def update_highscores(self, score, player_name):
        self._DATA.append(f"{score}: {player_name}")
        self._DATA.sort(key=lambda entry: int(entry.split(":")[0]), reverse=True)
