import time

from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to move using WASD and use space bar to jump
from ursina import *

# imports the Ursina Engine

app = Ursina()
window.title = "PyFPS"


# initializes the Ursina app

class Map:
    ground = Entity(model='plane',
                    texture='brick',
                    color=color.light_gray,
                    collider='mesh',  # the wall will be made up of polygons that the player cannot go through
                    scale=(500, 100, 500))  # scale=(x,y,z)
    wall_left = Entity(model='cube',
                       texture='brick',
                       color=color.dark_gray,
                       collider='mesh',
                       scale=(500, 10, 1),  # scale=(x,y,z)
                       position=(0, 5, 249.5))  # position=(right,up,forward)
    wall_right = duplicate(wall_left, position=(0, 5, -249.5))  # copies wall_left and changes the position of the wall
    wall_front = duplicate(wall_left,
                           position=(249.5, 5, 0),
                           rotation_y=90)  # copies wall_left, changes the position of the wall and rotates it
    wall_back = duplicate(wall_front,
                          position=(-249.5, 5, 0))  # copies wall_left and changes the position of the wall
    object1 = Entity(model='plane',
                     color=color.white,
                     collider='mesh',
                     scale=(10, 100, 1))
    Sky()  # sets the background to the sky for a better appearance


class Player(Entity):
    player = FirstPersonController(
        position=(5, 0, 195),
        speed=20,  # the speed of the player movement
        air_time=3,  # the amount of seconds spent in the air when the player jumps
        jump_height=10,  # the height the player reaches when it jumps
        height=5
    )


# Has basic controls for moving the player in a first person game
# Controls:
# W = Move forward
# A = Move left
# D = Move right
# S = Move Backwards
# Space Bar = Jump


class Enemy(Entity):
    enemy = Entity(model="cube",
                   texture="enemy_tommy.png",  # uses the image "enemy_tommy.png" on the cube
                   collider="mesh",  # adds collision detection to the enemy sprite
                   scale=(1, 2.5, 0),  # scaled so that the sprite is just about the right size for the player camera
                   position=(5, 1.2, 190))

def update():
    #Enemy.enemy.look_at(Vec3(Player.player.x, Enemy.enemy.y, Player.player.z)) # uses the x coordinate and z coordinate
    Enemy.enemy.look_at(Player.player)
    # of the player and the y coordinate of the enemy
    Enemy.enemy.position += Enemy.enemy.forward*50
    # this uses the enemy position and makes it go forward by 50 frames
    Enemy.enemy.y = 1.2
    # This keeps the y-axis value of the enemy position at 1.2 so that it doesn't go through the floor

class Gameplay():
    Player = Player()
    Enemy = Enemy()

# uses the position of the player on the map to look at the player
# Enemy.enemy.y = 3
# Enemy.enemy.position += Enemy.enemy.forward * 0.05
# enemy position goes forward slowly when the player moves


app.run()
# opens the window and runs the game
