import pandas as pd
import numpy as np
import math
import gzip
import json

PLAYER_COLORS = [
    [255, 255, 255],   # N
    [50, 153, 187],  # 1 Blue
    [199, 57, 11],     # 2 red
    [255, 153, 0],
    [191, 250, 55],
    [32, 250, 55],
    [191, 99, 99]
]

try:
    from IPython.display import display, HTML
except:
    pass


class GameMap(pd.DataFrame):
    _metadata = ['width', 'height']

    def _constructor(self):
        return GameMap


class Replay(object):

    def __init__(self, filename=None, width=None, height=None):
        """
        Loads a replay file from disk, or creates a new replay.

        Replay files may be gzip encoded (with a .gz filename). Because that's awesome. Keep your replays in gzip kids.
        """

        if ".gz" in filename:
            with gzip.open(filename, 'rb') as f:
                data = json.load(f)
        else:
            with open(filename) as f:
                data = json.load(f)

        self.data = data
        self.width = data["width"]
        self.height = data["height"]
        self.num_players = data["num_players"]
        self.num_frames = data["num_frames"]
        self.player_names = data["player_names"]

    def map_at(self, turn, include_moves=False):
        """
        Returns a game map for a given turn.
        """
        production = pd.Series(np.array(self.data['productions']).flatten())
        frame = np.array(self.data['frames'][turn]).reshape(
            self.width * self.height, 2)
        strength = pd.Series(frame[:, 1])
        owner = pd.Series(frame[:, 0])
        move = pd.Series(np.array(self.data['moves'][turn]).flatten())
        gm = GameMap({"production": production,
                      "strength": strength, "owner": owner, "move": move})
        gm.width = self.width
        gm.height = self.height
        return gm


def show_map(board, values=None):
    html = []
    html.append("""
    <style>
	table.map { border-spacing: 1px; border-collapse: separate; border:none; background: #333 }
	table.map td { margin:0px; padding:0px;}
	table.map td { width: 24px; height: 24px; text-align:center; padding:0px; margin:0px; vertical-align: middle; color: white; font-size:10px; border:none;}
	table.map td .piece {background: white; margin:auto;}
    </style>
    """)
    html.append("<table class=map>")
    width = board.width
    strength = board["strength"]
    owner = board["owner"]
    production = board["production"]

    for y in range(0, board.height):
        html.append("<tr>")
        for x in range(0, width):
            i = y * width + x
            color = PLAYER_COLORS[owner[i]]
            production_color = "rgba(%d, %d, %d, %0.3f)" % (
                color[0], color[1], color[2], production[i] * 0.04 + 0.1)
            strength_color = "rgb(%d, %d, %d)" % (color[0], color[1], color[2])
            strength_size = math.sqrt(strength[i])
            if values is not None:
                if i in values.index:
                    value = values[i]
                else:
                    value = ''
            else:
                value = "<div class=\"piece\" style=\"width: %0.1fpx; height: %0.1fpx; background: %s\"></div>" % (
                    strength_size, strength_size, strength_color)
            html.append("<td class=\"site\" style=\"background: %s\" title=\"s: %d p: %d\">%s</td>" %
                        (production_color, strength[i], production[i], value))
        html.append("</tr>")
    html.append("</table>")

    display(HTML("\n".join(html)))
