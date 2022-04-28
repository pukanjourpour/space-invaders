 
 ```mermaid
 classDiagram
 

      Entity <|-- Player : extends
      Entity <|-- Enemy : extends
      

    class Entity{
        <<abstract>> 
        -int x_pos
        -int y_pos
        -int width
        -int height
        -boolean state
        +move()
        +shoot()
    }

    class Player{
        -int score
        -int lives_count
        +update_score()
        +get_score()
    }

    class Enemy{
        -int type
        -int speed
        +animate()
    }

    class Projectile{
        -int type
        +animate()
        +check_collisions()
    }

    class Wall{
        +animate()
    }

    

```