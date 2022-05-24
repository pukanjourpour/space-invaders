 ```mermaid
 classDiagram
    ViewPyGame "1" *-- GameState

    ActorController --o ViewPyGame
    ObstacleController --o ViewPyGame
    ProjectileController --o ViewPyGame
    LevelController --o ViewPyGame
    SpriteController --o ViewPyGame

    GameState *-- Stage1Enemy
    GameState *-- Stage2Enemy
    GameState *-- Stage3Enemy
    GameState *-- BonusEnemy
    GameState *-- Player
    GameState *-- Obstacle
    GameState *-- Projectile

    BonusEnemy --|> Actor
    Stage1Enemy --|> Actor
    Stage2Enemy --|> Actor
    Stage3Enemy --|> Actor
    Player --|> Actor

    Actor --|> Drawable
    Obstacle --|> Drawable
    Projectile --|> Drawable

    class GameState{
        actors: List[Actor]
        obstacles: List[Obstacle]
        projectiles: List[Projectile]
        score: int
        level: int

    }

    class ViewPyGame{
        game: GameState
        sprites_by_type: map[Drawable, imgs]
        run()
        draw()
        draw_gui()
        update()
        get_keyboard_input()
        check_collisions()
        
    }

    class ActorController{
        act(actors, keyboard_input, delta_time)
        move(player, direction, delta_time)
        move(enemy, delta_time)
        change_enemies_direction(actors)
        shoot(player)
        shoot(enemy)
        receive_hit(actor)
    }

    class ObstacleController{
        receive_hit(obstacles, obstacle)
    }

    class ProjectileController{
        move(projectiles, delta_time)
        receive_hit(projectiles, projectile)
    }

    class SpriteController{
        convert_to_map(spritesheet)
    }

    class LevelController{
        generate_level(level: int)
    }
    
    class Actor{
        position: int
        size: int
        speed: int
        direction: int
    }

    class Player{
        lives_count: int
    }

    class Obstacle{
        position: int
        size: int
        hit_count: int
    }

    class Projectile {
        position: int
        size: int
        speed: int
        direction: int

    }

```