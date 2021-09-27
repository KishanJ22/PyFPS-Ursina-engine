from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to move using WASD and use space bar to jump
from ursina import *

# imports the Ursina Engine

app = Ursina()


# initializes the Ursina app

class Map():
    ground = Entity(model='plane',
                    texture='brick',
                    collider='mesh',
                    scale=(500, 100, 500))
    wall_left = Entity(model='cube',
                       texture='wall',
                       collider='mesh',
                       scale=(500, 10, 1),  # scale=(x,y,z)
                       position=(0, 5, 249.5))  # position=(right,up,forward)
    wall_right = duplicate(wall_left, position=(0, 5, -249.5))
    wall_front = duplicate(wall_left,
                           position=(249.5, 5, 0),
                           rotation_y=90)
    wall_back = duplicate(wall_front,
                          position=(-249.5, 5, 0))
    Sky()  # sets the background to the sky for a better appearance


class Player(Entity):
    player = FirstPersonController(
        position=(5, 0, 200),
        speed=10,  # the speed of the player movement
        air_time=3,  # the amount of seconds spent in the air when the player jumps
        jump_height=50  # the height the player reaches when it jumps
    )


# Has basic controls for moving the player in a first person game
# Controls:
# W = Move forward
# A = Move left
# D = Move right
# S = Move Backwards
# Space Bar = Jump


app.run()
# opens the window and runs the game
