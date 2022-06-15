from gamestate import GameState
from models.obstacle import Obstacle


class ControllerObstacle:
    @staticmethod
    def receive_hit(obstacle: Obstacle, gamestate: GameState) -> None:
        obstacle.hit_count -= 1
        if obstacle.hit_count == 0:
            gamestate.obstacles.remove(obstacle)