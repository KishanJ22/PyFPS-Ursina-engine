from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to move using WASD and use space bar to jump
from ursina import *

# imports the Ursina Engine

app = Ursina(vsync=True)


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
    Sky()  # sets the background to the sky for a better appearance


class Player(Entity):
    player = FirstPersonController(
        position=(5, 0, 195),
        speed=30,  # the speed of the player movement
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
                   position=(5, 0, 190))


def update():
    Enemy.enemy.look_at(Player.player.world_position)
    # uses the position of the player on the map to look at the player
    Enemy.enemy.position += Enemy.enemy.forward
    # enemy position goes forward slowly when the player moves
    Enemy.enemy.y = 3


app.run()
# opens the window and runs the game
