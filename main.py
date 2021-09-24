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
                    scale=(100, 1, 100))

    player = FirstPersonController()
    # Has basic controls for moving the player in a first person game
    # Controls:
    # W = Move forward
    # A = Move left
    # D = Move right
    # S = Move Backwards
    # Space Bar = Jump


app.run()
# opens the window and runs the game
