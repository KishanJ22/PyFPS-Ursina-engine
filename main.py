import time
from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to move using WASD and use space bar to jump
from ursina import *
from ursina.raycaster import raycast

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
    def __init__(self, position):
        super().__init__(
            model="cube",
            texture="enemy_tommy.png",  # uses the image "enemy_tommy.png" on the cube
            collider="mesh",  # adds collision detection to the enemy sprite
            scale=(1, 2.5, 0),  # scale=(x,y,z)
            position=position)

    def update(self):
        # Enemy.enemy.look_at(Vec3(Player.player.x, Enemy.enemy.y, Player.player.z)) # uses the x coordinate and z coordinate
        self.look_at(Player.player)
        # of the player and the y coordinate of the enemy
        self.position += self.forward * 80
        # this uses the enemy position and makes it go forward by 50 frames
        self.y = 1.2
        # This keeps the y-axis value of the enemy position at 1.2 so that it doesn't go through the floor
        origin = self.world_position
        # sets the start point for the ray (line 80)
        self.direction = [self.forward, self.back, self.left, self.right]
        # the different directions are stored in an array
        random_direction = random.choice(self.direction)
        # the self.direction array is shuffled
        randint = random.randint(100, 500)
        # numbers in the range of 100 to 500 are randomised
        ray = raycast(origin, random_direction, distance=.5)
        '''
        This casts a ray from the position of the enemy, in a random direction picked from the variable
        'random_direction' and sets the distance of the ray to 0.5
        This has been done because every enemy has a mesh collider, which means that when a ray from an enemy hits
        another enemy, it will know that it shouldn't go into that enemy.
        '''
        print(ray)
        # outputs when a ray has been hit
        if not ray.hit:
            self.position += random_direction
        # if the ray doesn't hit any object with a collider, it will move in a random direction


class Gameplay:
    Player = Player()
    enemies = []
    # the array for enemy instances
    for x in range(3):
        # spawns 3 enemies in by running this loop 3 times
        random_spawn_position = random.randint(100, 200)
# this creates a random number between 100 and 200 so that it can be used as the 'Z' parameter in the position attribute
# this is then used in enemy_instance so that each enemy spawns at a random location on the map when the game starts
        enemy_instance = Enemy(position=Vec3(x, 0, random_spawn_position))
        # creates an instance of Enemy and changes 'random_spawn_position' is used to generate a random spawn point
        enemies.append(enemy_instance)
        # puts each instance in the enemies array


# uses the position of the player on the map to look at the player
# Enemy.enemy.y = 3
# Enemy.enemy.position += Enemy.enemy.forward * 0.05
# enemy position goes forward slowly when the player moves


app.run()
# opens the window and runs the game
