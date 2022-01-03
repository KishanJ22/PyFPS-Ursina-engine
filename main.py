from ursina.prefabs.first_person_controller import FirstPersonController
# this will allow the user to have basic player controls and this will be built on further with guns and other player
# controls
from ursina.prefabs.health_bar import HealthBar
# this is a health bar for the player, which is in the library
from ursina import *
# imports the Ursina Engine
from ursina.raycaster import raycast
# imports a raycaster

app = Ursina()
# initializes the Ursina program

window.fullscreen_size = (1200, 1300)
# sets the fullscreen resolution
window.fullscreen = True
# uses the fullscreen_size to create a window with that size


class MainMenu(Entity):
    def __init__(self, **kwargs):
        super().__init__(parent=camera.ui)

        # The three entities below create empty entities that will be parents of the menu content
        self.main_menu = Entity(parent=self, enabled=True)
        # The main menu is responsible for holding buttons to start the game, quit the game, go to the options menu and
        # see the leaderboard
        self.options_menu = Entity(parent=self, enabled=False)
        # The options menu will be developed in post-development. This will be responsible for allowing the user to
        # change key bindings and the display resolution
        self.leaderboard_screen = Entity(parent=self, enabled=False)
        # The leaderboard screen is responsible for showing the top 5 scores as well as the usernames of the people that
        # achieved them

        mouse.locked = False
        mouse.visible = True
        # these two lines above allow the mouse to be moved and displayed in the game to navigate the main menu

        Text(text="MAIN MENU",
             parent=self.main_menu,
             size=.055,
             font="Fonts/osaka-re.ttf",
             y=0.4,
             x=0,
             origin=(0, 0),
             color=color.black)
        # this displays MAIN MENU at the top of the main menu

        Text(text="Please click on Input Name, enter a username and click Enter to register your username",
             parent=self.main_menu,
             size=.033,
             font="Fonts/osaka-re.ttf",
             y=0.35,
             x=0,
             origin=(0, 0),
             color=color.black)
        # this displays what the user should do before starting the game

        Text(text="Press the escape key or Quit button to quit the game",
             parent=self.main_menu,
             size=.035,
             font="Fonts/osaka-re.ttf",
             y=0.3,
             x=0,
             origin=(0, 0),
             color=color.black)
        # tells the user that they can quit the game easily by pressing the escape button

        Text(text="Press the escape button to go back to the main menu",
             parent=self.options_menu,
             size=.04,
             font="Fonts/osaka-re.ttf",
             y=0.4,
             x=0,
             origin=(0, 0),
             color=color.black)
        # tells the user that they can go back to the main menu easily by pressing the escape button

        Text(text="Press the escape button to go back to the main menu",
             parent=self.leaderboard_screen,
             size=.04,
             font="Fonts/osaka-re.ttf",
             y=0.4,
             x=0,
             origin=(0, 0),
             color=color.black)

        self.barry_r = Entity(
            parent=Gameplay.player,
            model='cube',
            position=(0, 0, .5),
            scale=(100, 100, .1),
            color=color.orange,
            enabled=True
        )
        # This is a cube, similar to the hitbox for detecting the bullets the enemies shoot at the player in the
        # Gameplay class

        input_username = InputField(y=-.20)
        # this is an input box for entering the username. This will be visible when the Input Name button is clicked
        input_username.visible = False
        # makes the input field for the username invisible so that the main menu is minimalistic
        Gameplay.player.ammo_text.visible = False
        # makes the bullet text in the game not visible

        def input_name():
            input_username.visible = True
            # this makes the input box for entering the username visible when the Input Name button is clicked on the
            # main menu
            enter_button = Button(
                "Enter",
                y=-.26,
                on_click=submit,
                parent=self.main_menu).fit_to_text()
            # this is a simple button that runs the submit function to pass the username to the Score class. This is
            # only accessible if the Input Name button is clicked

        def submit():
            print("Username: ", input_username.text)
            # this is used to test the username variable
            score_username = Score(input_username.text)
            # passes the username to the Score class by creating an instance of it and having the text typed into the
            # input box as a parameter for the attribute 'username'

        def start_button():
            self.barry_r.enabled = False
            # this disables the barry_r cube when the 'Start' button is clicked
            self.main_menu.disable()
            # this disables the main menu when the 'Start' button is clicked
            mouse.locked = True
            mouse.visible = False
            # the two lines of code above are for disabling the mouse and locking it so that it doesn't interfere with
            # the cross-hair
            input_username.visible = False
            # makes the input field for the username invisible once the start button is pressed
            Gameplay.hitbox.enabled = True
            # this will enable the player's hitbox when the Start button is clicked so that the player doesn't lose any
            # health in the main menu.
            Gameplay.player.ammo_text.visible = True
            # makes the bullet text in the game visible once the Start button is clicked

        def quit_game():
            application.quit()
            # this quits the game when the 'quit' button is clicked

        def options_menu_btn():
            self.options_menu.enable()
            # activates the options menu when the 'options' button is clicked
            self.main_menu.disable()
            # this disables the main menu when the 'options' button is clicked

        def leaderboard():
            self.main_menu.disable()
            # this disables the main menu when the 'leaderboard' button is clicked
            self.leaderboard_screen.enable()
            # this enables the leaderboard screen when the 'leaderboard' button is clicked
            text_entity = Text(
                parent=self.leaderboard_screen,
                font="Fonts/Formula1 Display-Italic.otf",
                y=.25,
                x=0,
                origin=(0, 0),
                color=color.black)
            # this is the text that will be displayed on the leaderboard screen. The actual text for it is generated
            # after sorting the array of scores and usernames and then it will hold the top 5 scores and usernames in
            # the text parameter
            score_array = []
            # blank array responsible for holding the scores and usernames from the score.txt file
            with open("score.txt", mode='r') as file:
                lines = file.readlines()
                # returns a list containing each line in score.txt as a list item
                for line in lines:
                    line = line.strip()
                    # removes "\n" from the end of each line
                    line = line.split(",")
                    # turns each line into an array and separates each line by a comma in the array
                    username_text = line[0]
                    # the first value of each line is the username
                    killcount_text = line[1]
                    # the second value of each line is the score, this will be useful for converting each score into an
                    # integer and for sorting the array
                    score_array.append([username_text, int(killcount_text)])
                    # appends the username as a string and killcount as an integer together for each line
                    score_array.sort(key=lambda x: x[1], reverse=True)
                    # the key creates a function and uses index[1], which is the integer in each tuple, to check if all
                    # other numbers are higher or lower than it. Because reverse is set to True, score_array will be
                    # sorted from the highest integer to smallest integer.
                    print(score_array)
                    # prints score_array for testing if the sorting algorithm worked properly
                score_array_lead = score_array[0:5]
                # selects the first 5 tuples in the array. These are the top 5 scores and usernames after sorting it
                print("Leaderboard:", score_array_lead)
                # this is used to test if the leaderboard works
                score_array_text = "\n".join(" ".join(map(str, item)) for item in score_array_lead)
                # here, an item is a single element. This means that there is a space between the username and score and
                # then the brackets, commas and quotation marks in the array are removed so that the leaderboard is
                # presentable on the leaderboard screen
                print(score_array_text)
                # outputs the text generated by score_array_text to test if the brackets, quotation marks and commas are
                # removed from each line
                text_entity.text = score_array_text
                # the text generated from score_array_text is used as the text in the text_entity for displaying the
                # leaderboard on the leaderboard screen

        # Button list
        ButtonList(button_dict={
            "Start": Func(start_button),
            "Options": Func(options_menu_btn),
            "Leaderboard": Func(leaderboard),
            "Exit": Func(quit_game),
            "Input Name": Func(input_name)
        }, y=0, parent=self.main_menu)
        #   'Button text': the function it will perform
        #   This is easy for making buttons for the main menu
        #   parenting this to the main menu makes sure the buttons only stay on the main menu

        for key, value in kwargs.items():
            setattr(self, key, value)

        # the attributes of this class can be changed when this class is called

    def input(self, key):
        # if the main menu is being displayed, then the escape key can be used to quit the game, making it easy to quit
        # the game. This will be done for all menus in this class.
        if self.main_menu.enabled:
            if key == "escape":
                application.quit()
                # when the escape key is pressed in the main menu, the game quits
        if self.options_menu.enabled:
            if key == "escape":
                self.options_menu.disable()
                self.main_menu.enable()
                # when the escape key is pressed in the options menu, the options menu is disabled and the main menu is
                # enabled
        if self.leaderboard_screen.enabled:
            if key == "escape":
                self.leaderboard_screen.disable()
                self.main_menu.enable()
                # when the escape key is pressed in the leaderboard screen, the leaderboard screen is disabled and the
                # main menu is enabled


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
        self.berettaM9 = Entity(model='Beretta_M9.obj',
                                parent=camera.ui,
                                scale=.035,
                                texture='beretta_m9_brandon.png',
                                position=(.3, -.7),
                                rotation=(0, -95, -2),
                                visible=False)
        # all guns are currently set to not be visible because a function will determine which gun is visible because
        # only one gun can be out at a time
        self.weapons = [self.pistol, self.shotgun_1, self.berettaM9]
        # all weapons are in an array so that a function can go through the weapons
        self.currentWeapon = 0
        # sets the current weapon to 0. This will be used in a function that changes the weapon that is out because this
        # number will be the index of the self.weapons array of the gun that will be visible
        self.switchweapon()  # this will run in the constructor because it will use self.currentWeapon to find a gun in
        # self.weapons, which it will then make the variable 'visible' True
        # self.collider = 'mesh'
        self.ammo = 100
        # the ammunition available to the player is set to 100 by default. An inventory/store will be made in post
        # development where the user can buy ammo from the store after accumulating coins from killing enemies
        self.ammo_text = Text(
            size=.04,
            font="Fonts/osaka-re.ttf",
            parent=camera.ui,
            origin=(.5, .5),
            y=0.5,
            x=0.45,
            color=color.black
        )

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
            # when the tab key is pressed, the integer stored in self.ammo in the constructor decreases by 1
            self.ammo -= 1
            if self.ammo > 0:
                Bullet(model='sphere',
                       color=color.orange,
                       scale=0.1,
                       position=self.player_controls.camera_pivot.world_position,
                       rotation=self.player_controls.camera_pivot.world_rotation,
                       )
                # the Bullet instance will run as long as self.ammo is higher than 0
                print('bullet: ', self.ammo)
        if key == 'left alt':
            mouse.locked = False
            mouse.visible = True
            # when the left alt/option key is pressed, the mouse can move. This will be useful for when I develop an
            # inventory/shop
        if key == 'left control':
            mouse.locked = True
            mouse.visible = False
            # when the left control key is pressed, the mouse is locked and disabled so that it doesn't interfere with
            # the cross-hair for shooting the gun

    def update(self):
        self.ammo_text.text = "Bullets: "+str(self.ammo)


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
            name='enemy'
        )
        self.delay = 0

    def update(self):
        self.look_at(Gameplay.player)
        # uses the position of the player to rotate the sprite to look at the player
        self.position += self.forward * 50
        # this uses the enemy position and makes it go forward by 50 frames
        self.y = 1.2
        # This keeps the y-axis value of the enemy position at 1.2 so that it doesn't go through the floor
        origin = self.world_position
        # sets the start point for the ray (line 80)
        # the different directions are stored in an array
        self.direction = [self.forward, self.back, self.left, self.right]
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
        if not ray.hit:
            self.position += random_direction
        # if the ray doesn't hit any object with a collider, it will move in a random direction
        self.delay += time.dt
        # the delay variable is set to 0 in the constructor and will increase by the delta time
        if self.delay > 1:
            # if the delay is larger than 1 second, it will reset the delay by setting it back to 0 and run an
            # instance of EnemyBullet, which will fire the bullet
            self.delay = 0
            EnemyBullet(
                model='sphere',
                color=color.green,
                scale=0.1,
                position=self.position,
                rotation=self.rotation
            )


class EnemyBullet(Entity):
    def __init__(self, speed=60, lifetime=5, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed  # uses the integer '50' as the speed
        self.lifetime = lifetime  # uses the integer '5' for how long the bullet will last
        self.start = time.time()  # uses time to remove the bullet from the game if it has been there for too long
        # time.time is also used to get the time the bullet is fired and counts from when it was fired

    def update(self):
        enemy_bullet_ray = raycast(
            self.world_position,
            # sets the start position for the ray, which is from the player
            self.forward,
            # sets the direction the ray will go
            traverse_target=Gameplay.player,
            # makes sure that the ray only registers with the player
            ignore=(Map.ground, Map.wall_left, Map.wall_back, Map.wall_front, Map.wall_right, Gameplay.enemies),
            # this is a list of entities that the ray will not affect. This is because the ray would remove anything it
            # touches
            distance=self.speed * time.dt,
            # uses the speed of the bullet and multiplies it by the delta time (the difference between
            # the previous frame and the current frame) as the distance of the ray
        )
        if not enemy_bullet_ray.hit and time.time() - self.start < self.lifetime:
            # if the bullet doesn't hit anything with a collider and the bullet doesn't get timed out, the bullet
            # will move forward
            self.world_position += self.forward * self.speed * time.dt
            # time.dt is delta time, which means the difference between the previous frame and current frame
        else:
            destroy(self)
            # if the bullet doesn't hit anything or stays on the ground for too long, then it will be deleted for
            # performance purposes
        if enemy_bullet_ray.hit:
            # if the bullet shot by the enemy collides with anything with a collider, it will reduce the health bar for
            # the player by 5 each time
            print(enemy_bullet_ray.entity)
            # outputs the entity the enemy bullet hits
            Gameplay.healthBar.value -= 5
            print('Player health:', Gameplay.healthBar.value)
            # this is used for testing the health of the player to see whether or not the health decreases when it is
            # shot


class Bullet(Entity):
    def __init__(self, speed=50, lifetime=10, **kwargs):
        super().__init__(**kwargs)
        self.speed = speed  # uses the integer '50' as the speed
        self.lifetime = lifetime  # uses the integer '10' for how long the bullet will last
        self.start = time.time()  # uses time to remove the bullet from the game if it has been there for too long
        # time.time is also used to get the time the bullet is fired and counts from when it was fired

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
            if bullet_ray.entity in Gameplay.enemies:
                # This outputs the entity it touches, which can be very useful when making a persistent storage solution
                # for logging the amount of kills the player gets
                print(bullet_ray.entity)
                # casts a ray from the position of the gun and returns anything it hits with a collider.
                # this outputs the instance the bullet collides with. In this case, it will only output
                # 'render/scene/enemy' because it will only register with an enemy instance
                destroy(bullet_ray.entity)
                # if the bullet hits anything with a collider, it will remove/destroy the entity that is hit
                # if the instance hit by the bullet is in the enemies array in the Gameplay class
                # the counter in the gameplay class will increment by 1
                Gameplay.enemies.remove(bullet_ray.entity)
                # this removes the enemy instance the bullet hit from the enemies array inside the Gameplay class
                print(Gameplay.enemies)
                # outputs the enemies array to make sure the enemy instance was removed
                print('Length of array:', len(Gameplay.enemies))
                # outputs the length of the enemies array
                Score.killcount += 1
                # increases the player's score by 1
                print(Score.killcount)
                # this outputs the counter for testing.


class Gameplay:
    enemies = []
    # the array for holding enemy instances
    for x in range(8):
        # spawns (x) enemies in by running this loop (x) times
        random_spawn_position = random.randint(100, 200)
        '''
this generates a random number between 100 and 200 so that it can be used as the 'Z' parameter in the position attribute
this is then used in enemy_instance so that each enemy spawns at a random location on the map when the game starts
        '''
        enemy_instance = Enemy(position=Vec3(x, 0, random_spawn_position))
        # creates an instance of Enemy and changes 'random_spawn_position' is used to generate a random spawn point
        enemies.append(enemy_instance)
        # puts each instance in the enemies array
    healthBar = HealthBar()
    # a health bar in the library used to show the player's health
    player = Player(speed=40)
    # instance of the Player class with speed set to 40
    hitbox = Entity(model='cube',
                    parent=player,
                    scale=(1.2, 5, .2),
                    collider='box',
                    position=(0, 0, -.5),
                    alpha=0,
                    enabled=False
                    )
    '''
    this is the collider that is assigned to the player instance so that when an enemy shoots a bullet at the player,
    the hitbox gets detected by the enemy bullet ray and then health can be taken off the health bar for the player. The
    hitbox is slightly behind the player position so that it doesn't interfere with the movement of the player
    '''


class Score:
    killcount = 0

    # this counter is for the number of kills the player gets

    def __init__(self, username):
        self.username = username
        # holds the username entered in input_username in the MainMenu class
        print('Score class:', username)
        # used to test if the username has been passed to the Score class
        global global_username
        # globalises the global_username variable so that it can be used in the update function below this class
        global_username = str(self.username)
        # this variable converts the attribute into a string and is accessible by other classes and the main body of the
        # code by 'global global_username'


def update():
    # this function will update every frame, meaning that the if statement below will work
    if Gameplay.healthBar.value == 0 or len(Gameplay.enemies) == 0:
        # if the health bar for the player's health reaches 0 or the length of the enemy array is 0, then the game
        # will end
        application.quit()
        # quits the game
        username = global_username
        # gets global_username from the Score class so that it can be used to write the username to the text file
        score = str(Score.killcount)
        print("Username at end of game", username)
        # used to check if the username has been globalised for testing
        with open("score.txt", mode='a') as score_file:
            score_file.write(username + ", " + score + "\n")
            # writes the username and score separated by a comma. The newline command at the end makes sure that a new
            # line is created for the next username and score


main_menu = MainMenu()
# initialises the MainMenu class
app.run()
# opens the window and runs the game
