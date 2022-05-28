from telnetlib import SE
from typing import List, Tuple

from models.actor import Actor
from models.obstacle import Obstacle
from models.player import Player
from settings import Settings


class ControllerLevel:
    @staticmethod
    def generate_level(level: int) -> Tuple[List[Actor], List[Obstacle]]:
        #if level is 1 then a new player must be generated and added to actor list
        if level == 1:
            player: Player = Player(Settings.SCREEN_WIDTH/2 - 25, Settings.SCREEN_HEIGHT - 70, 50, 50, Settings.PLAYER_SPEED)
        actors: List[Actor] = [player]
        obstacles: List[Obstacle] = []

        return actors, obstacles
