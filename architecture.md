 ```mermaid
 classDiagram
    Game <--> ActorController
    Game <--> ObstacleController
    Game <--> ProjectileController
    Game <--> GUIController
    Game <--> GameController
    Game <--> SpriteController

    ActorController <--> Stage1Enemy
    ActorController <--> Stage2Enemy
    ActorController <--> Stage3Enemy
    ActorController <--> BonusEnemy
    ActorController <--> Player

    ObstacleController <--> Obstacle
    ProjectileController <--> Projectile

    BonusEnemy --|> Actor
    Stage1Enemy --|> Actor
    Stage2Enemy --|> Actor
    Stage3Enemy --|> Actor
    Player --|> Actor


    class Game{
        actors: List[Actor]
        particles: List[Particles]
        obstacles: List[Obstacle]

        run_game()
        check_events()
        check_input()
        update_screen()
        check_collisions()
        
    }

    class ActorController{
        draw(screen, actors: List[Actor])
        move(actors: List[Actor])
        move(player)
        move(enemy)
        shoot(player)
        shoot(enemy)
    }

    class SpriteController{
        convert_to_list(spritesheet: img)
        get_player_sprites(sprites: List[img])
        get_stage1_enemy_sprites(sprites: List[img])
        get_stage2_enemy_sprites(sprites: List[img])
        get_stage3_enemy_sprites(sprites: List[img])
        get_bonus_enemy_sprites(sprites: List[img])
        get_obstacle_sprites(sprites: List[img])
        get_particle_sprites(sprites: List[img])
    }

    class GameController{
        generate_level(level:int)
    }

    class ObstacleController{
        draw(screen, obstacles List[Obstacle])
        deform(obstacles)
    }

    class ProjectileController{
        draw(screen, particles: List[Particle])
        move(particles:List[Particle])
    }

    class GUIController{
        draw_main_menu()
        draw_side_gui(score, lives_count)
        handle_click()
    }
    
    class Actor{
        position: int
        size: int
        sprites: List[img]
    }

    class Obstacle{
        sprites: List[img]
        position: int
        size: int
    }

    class Projectile {
        sprites: List[img]
        position: int
        size: int
        y_speed: int

    }

```