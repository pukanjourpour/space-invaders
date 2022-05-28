 ```mermaid
 classDiagram
    ViewPyGame "1" *-- GameState

    GameState o-- EnemyStage1
    GameState o-- EnemyStage2
    GameState o-- EnemyStage3
    GameState o-- EnemyBonus
    GameState o-- Player
    GameState o-- Obstacle
    GameState o-- Projectile

    EnemyBonus --|> Actor
    EnemyStage1 --|> Actor
    EnemyStage2 --|> Actor
    EnemyStage3 --|> Actor
    Player --|> Actor

    ControllerActor .. Actor
    ControllerObstacle .. Obstacle
    ControllerProjectile .. Projectile

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

    class ControllerActor{
        act(actors, keyboard_input, delta_time)
        move(player, direction, delta_time)
        move(enemy, delta_time)
        change_enemies_direction(actors)
        shoot(player)
        shoot(enemy)
        receive_hit(actor)
    }

    class ControllerObstacle{
        receive_hit(obstacles, obstacle)
    }

    class ControllerProjectile{
        move(projectiles, delta_time)
        receive_hit(projectiles, projectile)
    }

    class ControllerSprite{
        convert_to_map(spritesheet)
    }

    class ControllerLevel{
        generate_level(level: int)
    }
    
    class Actor{
        speed: int
        direction: int
    }

    class Player{
        lives_count: int
        score: int
    }

    class Obstacle{
        hit_count: int
    }

    class Projectile {
        speed: int
        direction: int
    }

    class Drawable {
        position: int
        size: int
    }

```