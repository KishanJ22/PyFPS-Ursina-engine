from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to have basic player controls and this will be built on further with guns and other player
# controls
from ursina.prefabs.health_bar import HealthBar
from ursina import *
# imports the Ursina Engine
from ursina.raycaster import raycast

# imports a raycaster
window.title = "PyFPS"
app = Ursina()


# initializes the Ursina app
# window.fullscreen = True


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
    def __init__(self, **kwargs):
        # **kwargs means that optional keyword arguments can be given in the class with the FirstPersonController.
        # so that in this case, I can use the weapons with the FirstPersonController so that they can be switched,
        # picked-up or discarded. I can also add more key bindings for cycling between weapons and showing a map.
        self.player_controls = FirstPersonController(**kwargs)
        super().__init__(parent=self.player_controls)

        self.pistol = Entity(model='Pistol_obj.obj',  # fetches the 3D model of the gun from the directory
                             parent=camera.ui,  # makes the gun move with the camera of the FirstPersonController
                             scale=.05,  # sets the scale of the gun
                             texture='Pistol_gloss.jpg',
                             # fetches the image of the gun texture and applies it to the model
                             position=(.35, -.3),  # sets the X and Y position of the gun on the display
                             rotation=(-90, -90, -5),  # sets the X, Y, Z rotation of the gun on the display
                             visible=False)  # sets the gun to not be seen or used
        self.shotgun_1 = Entity(model='870_mcs_shotgun.obj',
                                parent=camera.ui,
                                scale=.09,
                                texture='870mcs_texture.png',
                                position=(.35, -.3),
                                rotation=(180, 85, -3),
                                visible=False)
        self.desert_eagle = Entity(model='Deagle.obj',
                                   parent=camera.ui,
                                   scale=.09,
                                   texture='Deagle_Normal.png',
                                   color=color.gold,
                                   position=(-.003, -.65),
                                   rotation=(0, -90, -3),
                                   visible=False)
        self.berettaM9 = Entity(model='Beretta_M9.obj',
                                parent=camera.ui,
                                scale=.035,
                                texture='beretta_m9_brandon.png',
                                position=(.3, -.7),
                                rotation=(0, -95, -2),
                                visible=False)
        # all guns are currently set to not be visible because a function will determine which gun is visible because
        # only one gun can be out at a time
        self.weapons = [self.pistol, self.shotgun_1, self.desert_eagle, self.berettaM9]
        # all weapons are in an array so that a function can go through the weapons
        self.currentWeapon = 0
        # sets the current weapon to 0. This will be used in a function that changes the weapon that is out because this
        # number will be the index of the self.weapons array of the gun that will be visible
        self.switchweapon()  # this will run in the constructor because it will use self.currentWeapon to find a gun in
        # self.weapons, which it will then make the variable 'visible' True
        self.counter = 0

    def switchweapon(self):
        for i, v in enumerate(self.weapons):  # i is the index for the array and v is the 'visible' parameter
            if i == self.currentWeapon:
                # if i is the same as the integer stored in 'self.currentWeapon' then visible is 'True' for the weapon
                # in the self.weapons array that 'i' points to
                v.visible = True
                # print('visible is true ', self.currentWeapon)
                # 'visible' for the weapon will be set to 'True', meaning that the gun will be displayed
            else:
                v.visible = False
                # print('visible is false ', self.currentWeapon)
                # 'visible' for the weapon will be set to 'False', meaning that the gun will not be displayed

    def input(self, key):
        # print('before try statement:', self.currentWeapon)
        try:
            self.currentWeapon = int(key) - 1
            self.switchweapon()
            # print('try statement:', self.currentWeapon)
            # it will try and change the weapon before the game starts to make sure the user can change the weapon
        except ValueError:
            pass
        # if there is an error with the value, then it will be ignored

        if key == 'up arrow':
            print("up arrow is pressed")
            self.currentWeapon = (self.currentWeapon + 1) % len(self.weapons)
            # self.currentWeapon will be the remainder of self.currentWeapon added by 1 and divided by the number of
            # elements in the self.weapons array
            self.switchweapon()
            # the switchweapon function will be carried out with the new number in self.currentWeapon, meaning that the
            # weapon will change.
            print("up arrow is pressed")
        if key == 'down arrow':
            print("down arrow is pressed")
            self.currentWeapon = (self.currentWeapon - 1) % len(self.weapons)
            # self.currentWeapon will be the remainder of self.currentWeapon subtracted by 1 and divided by the number
            # of elements in the self.weapons array
            self.switchweapon()
            # the switchweapon function will be carried out with the new number in self.currentWeapon, meaning that the
            # weapon will change.
            print("down arrow is pressed")
        if key == 'tab':
            Bullet(model='sphere',
                   color=color.orange,
                   scale=0.1,
                   position=self.player_controls.camera_pivot.world_position,
                   rotation=self.player_controls.camera_pivot.world_rotation)


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
            collider="box",  # adds collision detection to the enemy sprite
            scale=(1, 2.5, 0),  # scale=(x,y,z)
            position=position,  # this is the spawn location for the enemy sprite. This isn't a fixed value because
        )
        # the spawn location is randomised in the for loop in the Gameplay class

    def update(self):
        # Enemy.enemy.look_at(Vec3(Player.player.x, Enemy.enemy.y, Player.player.z)) # uses the x coordinate and z coordinate
        self.look_at(player)
        # of the player and the y coordinate of the enemy
        self.position += self.forward * 30
        # this uses the enemy position and makes it go forward by 50 frames
        self.y = 1.2
        # This keeps the y-axis value of the enemy position at 1.2 so that it doesn't go through the floor
        origin = self.world_position
        # sets the start point for the ray (line 80)
        self.direction = [self.forward, self.back, self.left, self.right]
        # the different directions are stored in an array
        random_direction = random.choice(self.direction)
        # the self.direction array is shuffled
        # numbers in the range of 100 to 500 are randomised
        ray = raycast(origin, random_direction, distance=.5)
        '''
        This casts a ray from the position of the enemy, in a random direction picked from the variable
        'random_direction' and sets the distance of the ray to 0.5
        This has been done because every enemy has a mesh collider, which means that when a ray from an enemy hits
        another enemy, it will know that it shouldn't go into that enemy.
        '''
        # outputs when a ray has been hit
        if not ray.hit:
            self.position += random_direction
        # if the ray doesn't hit any object with a collider, it will move in a random direction


class Gameplay:
    enemies = []
    # the array for enemy instances
    for x in range(3):
        # spawns 3 enemies in by running this loop 3 times
        random_spawn_position = random.randint(100, 200)
        '''
this creates a random number between 100 and 200 so that it can be used as the 'Z' parameter in the position attribute
this is then used in enemy_instance so that each enemy spawns at a random location on the map when the game starts
        '''
        enemy_instance = Enemy(position=Vec3(x, 0, random_spawn_position))
        # creates an instance of Enemy and changes 'random_spawn_position' is used to generate a random spawn point
        enemies.append(enemy_instance)
        # puts each instance in the enemies array

    healthBar = HealthBar()


class Bullet(Entity):
    def __init__(self, speed=50, lifetime=10, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed  # uses the integer '10' as the speed
        self.lifetime = lifetime  # uses the integer '10' for how long the bullet will last
        self.start = time.time()  # uses time to remove the bullet from the game if it has been there for too long
        # time.time is also used to get the time the bullet is fired and counts from when it was fired
        self.counter = 0

    def update(self):
        enemygroup = Gameplay.enemy_instance.parent
        # this parents all enemy instances generated to a single entity, which will allow the ray from the bullet to
        # only collide with an enemy instance. This means that only the enemy instance hit will be removed from the game
        bullet_ray = raycast(self.world_position,
                             # sets the start position for the ray, which is from the player
                             self.forward,
                             # sets the direction the ray will go
                             traverse_target=enemygroup,
                             # makes sure that the ray only registers with enemy instances
                             ignore=(Map.ground, Map.wall_left, Map.wall_back, Map.wall_front, Map.wall_right),
                             # this is a list of entities that the ray will not affect. This is because the ray would
                             # remove anything it touches
                             distance=self.speed * time.dt,
                             # uses the speed of the bullet and multiplies it by the delta time (the difference between
                             # the previous frame and the current frame) as the distance of the ray
                             )
        if bullet_ray.hit:
            #self.counter = self.counter + 1
            #print(self.counter)
            print(bullet_ray.entity)
            # This outputs the entity it touches, which can be very useful when making a persistent storage solution
            # for logging the amount of kills the player gets
            destroy(bullet_ray.entity)
            # if the bullet hits anything with a collider, it will remove/destroy the entity that is hit
        # casts a ray from the position of the gun and returns anything it hits with a collider.
        if not bullet_ray.hit and time.time() - self.start < self.lifetime:
            # if the bullet doesn't hit anything with a collider and the bullet doesn't get timed out, then the bullet
            # will move forward
            self.world_position += self.forward * self.speed * time.dt
            # time.dt is delta time, which means the difference between the previous frame and current frame
        else:
            destroy(self)
            # if the bullet doesn't hit anything or stays on the ground for too long, then it will be deleted for
            # performance purposes
        if bullet_ray.hit:
            #self.counter = self.counter + 1
            #print(self.counter)
            print(bullet_ray.entity)
            # This outputs the entity it touches, which can be very useful when making a persistent storage solution
            # for logging the amount of kills the player gets
            destroy(bullet_ray.entity)
            # if the bullet hits anything with a collider, it will remove/destroy the entity that is hit


# uses the position of the player on the map to look at the player
# Enemy.enemy.y = 3
# Enemy.enemy.position += Enemy.enemy.forward * 0.05
# enemy position goes forward slowly when the player moves

player = Player(speed=40)
app.run()
# opens the window and runs the game
