'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: monster.py
Purpose: This file contains the Monster class and all subclasses that implements the monsters in the game.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

from player import Player
import pygame, os, sys,random

class Monster(Player):
    '''
    The Monster() class is a subclass of the Player() class that represents the monsters in the game.
    '''
    def __init__(self, nick,x_bg, y_bg, attack_pts, speed=5, state=False):
        '''
        __init__() initializes the monster

        Parameters (required): 
            nick - monster 'nickname'; used to reference monster and retrieve correct images from the images folder
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
            attack_pts - how much attack damage the monster does with each attack on the player

        Parameters (optional):
            speed - number of pixels the monster moves each time; by default, set to 5
            state - whether or not the monster is active; by default set to False i.e. inactive
        '''

        self.nick = nick            # nickname
        self.x_bg = x_bg            # x position in relation to the entire background
        self.y_bg = y_bg            # y position in relation ot the entire background
        self.attack_pts = attack_pts  # how much an attack is worth   
        self.speed = speed          # number of pixels the monster moves in one move
        self.state = state          # whether or not the monster is active (True is active, False is inactive)
        
        self.frame = 1              # direction the monster is facing (with a different image associate with each direction)
        self.walk_over = False      # whether the player can walk over the monster
        self.move_rate = 0.75       # how often it moves, probability between 0 and 1, inclusive

        self.previous = None        # the previous move (string "left","right","up","down")
                                    # used so there is a bias for moving in the same direction
        self.collide = None         # direction that the monster is colliding with the player in 
                                    # string: ("left", "right","up","down") or None

        # intializes parent class Player
        super().__init__(self.nick) # the image files should be namd the same as the nickname
        
        # attack delay counter
        self.n = 0

    def track_player(self, background, player, game):
        '''
        track_player() moves the monster in the direction of the player
        The closer the monster is to the player, the more likely it is to move towards them

        Parameters (required):
            background - game background object that the monster is located on
            player - character that the monster is tracking
            game - game object that encompasses the whole game

        '''

        vector = [background.stagePosX - self.x_bg, background.stagePosY - self.y_bg] # vector between monster and player
        vector_dir = [-1 if vector[0]<0 else 1, -1 if vector[1]<0 else 1] # defines the direction of the vector: -1 is up or left, 1 is down or right
        
        x_dir = (8000-abs(vector[0]))/8000    # probability of going towards the monster in x direction
        y_dir = (8000-abs(vector[1]))/8000    # probability of going towards the monster in y direction
        
        direction = [0,0,0,0]       # probabilites for each direction, in the order: left,right,up,down
        
        # this defines the probability for each direction
        # sets probabilities depending on where the player is in relation to the monster
        
        if vector_dir[0] < 0:               # player is to the left of the monster
            direction[0] = x_dir            # probability for moving left is the probability of going towards monster in x direction
            direction[1] = 1-x_dir          # probability for moving right is 1-(probability of moving left)

        elif vector_dir[0] > 0:             # player is to the right
            direction[1] = x_dir            # probability for moving right is the probability of going towards monster in x direction
            direction[0] = 1-x_dir          # probability for moving left is 1-(probability of moving right)

        if vector_dir[1] < 0:               # player is above the monster
            direction[2] = y_dir            # probability of moving up is the probability of going towards monster in y direction
            direction[3] = 1-y_dir          # probability of moving down is 1-(probability of moving up)        

        elif vector_dir[1] > 0:             # player is below the monster
            direction[3] = y_dir            # probability of moving down is the probability of going towards monster in y direction
            direction[2] = 1-y_dir          # probability of moving up is 1-(probability of moving down)

        # if the monster is within 10 px of the player in any direction, 
        # then sets the probabilities for moving in those directions to 0
        if vector[0] < (player.width/2 + self.width + 10) and vector[0] > -(player.width/2) - 10:
            direction[0] = 0
            direction[1] = 0
        if vector[1] < (player.height/2 + self.height + 10) and vector[1] > -(player.height/2) -10:
            direction[2] = 0
            direction[3] = 0

        # sum of the probabilities, used to normalize them later
        sum = (direction[0] + direction[1] + direction[2] + direction[3])*3
        
        # generates 2 random numbers from 0 to 1
        random_num_1 = random.random()         
        random_num_2 = random.random()

        # checks whether the monster is touching player and updates self.collide (direction of collission)
        self.touching(player,background)
        
        # checks whether the monster is colliding with a background object
        bg_collision = False
        for obj in background.background_obj:
            if self.touching(obj, background):
                bg_collision = True
        
        if background.monster_detect_wall_collision(self) or bg_collision:  # if collide with wall or background object
            if self.touching(player,background):       # and if touching player
                pass            # do not move

            else:   # if collide with wall previously and not touching player
                # moves away from the wall
                if self.collide == "left":
                    self.x_bg -= self.speed
                    self.previous == "left"
                if self.collide == "right":
                    self.x_bg += self.speed
                    self.previous == "right"
                if self.collide == "up":
                    self.y_bg -= self.speed
                    self.previous == "up"
                if self.collide == "down":
                    self.y_bg += self.speed
                    self.previous == "down"
        elif sum == 0: # if touching player but not colliding with wall/background object
            pass    # do not move
        else:       # if not touching player or wall or background object
            self.speed == 5         

            # if the random number is less than the move_rate, the monster will move
            # this allows the rate of movement of the monster to be changed without adjusting speed
            # chance of movement based on probability
            if random_num_1 < self.move_rate:       

                # uses probabilities to calculate thresholds by normalizing probabilities
                threshold = [direction[0]/sum, (direction[0]+direction[1])/sum, (direction[0]+direction[1]+direction[2])/sum, (direction[0]+direction[1]+direction[2]+direction[3])/sum,1] #[prob of going left, prob of going right, prob of going up, prob of going down]

                # uses random number to determine which direction to move in, depending on threshold probabilities
                if random_num_2 < threshold[0]:           # go left
                    self.move_left(background,direction)
                elif random_num_2 < threshold[1]:         # go right
                    self.move_right(background,direction)
                elif random_num_2 < threshold[2]:         # go up
                    self.move_up(background,direction)
                elif random_num_2 < threshold[3]:         # go down
                    self.move_down(background,direction)

                else:   # random_num_2 < 1 (all other cases)
                    # go in whatever direction you were going before
                    if self.previous == "left":         # go left
                        self.move_left(background,direction)
                    elif self.previous == "right":      # go right
                        self.move_right(background,direction)
                    elif self.previous == "up":         # go up
                        self.move_up(background,direction)
                    elif self.previous == "down":       # go down
                        self.move_down(background,direction)
            else:   # if the monster does not move in this frame (to slow the monster down relative to the sprite)
                pass
        
        self.attack(background,player,game) # attacks the player by doing damage to it
    
    def move_left(self,background,direction):            
        '''
        move_left() moves the monster to the left according to the speed and changes image frame

        Parameters (required):
            background - game background object that the monster is located on
            direction - list of direction probabilities, generated in the track_player function
        '''

        self.x_bg -= self.speed         # move to the left
        self.frame = 2                  # change frame
        self.previous = "left"

        # if the movement causes the monster to collide with the wall
        if background.monster_detect_wall_collision(self):
            self.x_bg += self.speed       # return to original position (by moving right)

            try:        # try if the sum of the y direction probabilites are not equal to 0
                # move up if a random number is under the probability for moving up 
                # else move down
                self.move_up(background,direction) if random.random() < (direction[2]/(direction[2]+direction[3])) else self.move_down(background,direction)
            
            except:     # if there is a divide by 0 error
                # move up if random number < 0.5
                # else move down
                self.move_up(background,direction) if random.random() < 0.5 else self.move_down(background,direction)


    def move_right(self,background,direction):       
        '''
        move_right() moves the monster to the right according to the speed and changes image frame

        Parameters (required):
            background - game background object that the monster is located on
            direction - list of direction probabilities, generated in the track_player function
        '''

        self.x_bg += self.speed         # move to the right
        self.frame = 1                  # change frame
        self.previous = "right"

        # if movement causes monster to collide with the wall
        if background.monster_detect_wall_collision(self):
            self.x_bg -= self.speed        # return to the original position (by moving left)

            try:    # try if the sum of the y direction probabilites are not equal to 0
                # move up if a random number is under the probability for moving up 
                # else move down
                self.move_up(background,direction) if random.random() < (direction[2]/(direction[2]+direction[3])) else self.move_down(background,direction)
            
            except: # if there is a divide by 0 error
                # move up if random number < 0.5
                # else move down
                self.move_up(background,direction) if random.random() < 0.5 else self.move_down(background,direction)
            
    
    def move_up(self,background,direction):           
        '''
        move_up() moves the monster up according to the speed and changes image frame

        Parameters (required):
            background - game background object that the monster is located on
            direction - list of direction probabilities, generated in the track_player function
        '''
        self.y_bg -= self.speed     # move up
        self.frame = 3              # change frame
        self.previous = "up"

        # if movement causes monster to collide with the wall
        if background.monster_detect_wall_collision(self):
            self.y_bg += self.speed         # return to the original position (by moving down)
            
            try:    # try if the sum of the x direction probabilites are not equal to 0
                # move left if a random number is under the probability for moving left 
                # else move right
                self.move_left(background,direction) if random.random() < (direction[0]/(direction[0]+direction[1])) else self.move_right(background,direction)
            except:     # if there is a divide by 0 error
                # move left if random number < 0.5
                # else move right
                self.move_left(background,direction) if random.random() < 0.5 else self.move_right(background,direction)


    def move_down(self,background,direction):       
        '''
        move_down() moves the monster down according to the speed and changes image frame

        Parameters (required):
            background - game background object that the monster is located on
            direction - list of direction probabilities, generated in the track_player function
        '''

        self.y_bg += self.speed         # move down
        self.frame = 0                  # change frame
        self.previous = "down"

        # if movement causes monster to collide with the wall
        if background.monster_detect_wall_collision(self):
            self.y_bg -= self.speed       # return to the original position (by moving up)
            
            try:    # try if the sum of the x direction probabilites are not equal to 0
                # move left if a random number is under the probability for moving left 
                # else move right
                self.move_left(background,direction) if random.random() < (direction[0]/(direction[0]+direction[1])) else self.move_right(background,direction)
            
            except:     # if there is a divide by 0 error
                # move left if random number < 0.5
                # else move right
                self.move_left(background,direction) if random.random() < 0.5 else self.move_right(background,direction)


    def place(self,background,extend=False):
        '''
        place() draws the monster on the screen

        Parameters (required):
            background - game background object the monster is located on

        Parameters (optional):
            extend - whether or not the monster is in attack mode; by default, set to False i.e. not attacking
        '''

        # calculates x and y positions using the background stage positions and the x_bg and y_bg
        self.x = self.x_bg - (background.stagePosX - 500)
        self.y = self.y_bg - (background.stagePosY - 400)

        # if extend, calls extend() function (shifts the monster over by 10px)
        if extend:
            self.extend()

        # calls parent class place function to draw the monster
        super().place(background,self.frame)

    def extend(self):
        '''
        extend() moves the monster forward by 10 pixels to show the monster is attacking the player
        '''
        if self.frame == 0:     # if moving down
            self.y += 10
        elif self.frame == 1:   # if moving right
            self.x += 10
        elif self.frame == 2:   # if moving left
            self.x -= 10
        elif self.frame == 3:   # if moving up
            self.y -= 10

    def touching(self,other,background,tolerance = 0):
        '''
        touching() checks whether the monster is touching a particular object

        Parameters (required):
            other - the object to be checked for contact
            background - the background object that the monster and the object are located on

        Parameters (optional):
            tolerance - how much leeway there is between whether the monster is actually touching the object or not;
                        by default, set to 0

        Returns:
            Boolean - True if touching the other object; False if not

        '''

        if other in background.door_list:  # if it's a door

            # calculates the x and y coordinates in relation to the screen
            x1 = self.x_bg + 505
            y1 = self.y_bg + 390
            
            x2 = other.x_bg
            y2 = other.y_bg
            
            # checks whether the x and y positions of either object are inside the other object
            if (x2 >= x1 and x2 < (x1 + self.width)) or (x1 >= x2 and x1 < (x2 + other.width)):
                if (y2 >= y1 and y2 < (y1 + self.height)) or (y1 >= y2 and y1 < (y2 + other.height)):
                    if x1 >= (x2 + other.width - abs(tolerance)) and x1 <= (x2 + other.width + abs(tolerance)):
                        self.collide= "left"       #the player is to the left of the monster
                    elif (x1 + self.width) >= (x2 - abs(tolerance)) and (x1 + self.width) <= (x2 + abs(tolerance)):
                        self.collide = "right"      # the player is to the right of the monster
                    elif y1 >= (y2 + other.height - abs(tolerance)) and y1 <= (y2 + other.height + abs(tolerance)):
                        self.collide = "up"
                    elif (y1 + self.height) >= (y2 - abs(tolerance)) and (y1 + self.height) <= (y2 + abs(tolerance)):
                        self.collide = "down"
                    
                    return True
            return False

        elif other in background.background_obj and other != self:  # if it's a plant or another object in background_obj list
            pass    

        # tolerance is used because otherwise the player keeps getting stuck on the monster
        else: # if it's the player

            # find x and y coordinates in relation to the visible screen
            x1 = self.x
            y1 = self.y
            
            x2 = other.x
            y2 = other.y
            
            # checks whether the x and y positions of either object are inside the other object
            if (x2 >= (x1 + tolerance) and x2 <= (x1 + self.width - tolerance)) or (x1 >= (x2 + tolerance) and x1 <= (x2 + other.width - tolerance)):
                if (y2 >= (y1 + tolerance) and y2 <= (y1 + self.height -tolerance)) or (y1 >= (y2 + tolerance) and y1 <= (y2 + other.height -tolerance)):
                    
                    # checks to see which side the monster is colliding with the player on
                    if x1 >= (x2 + other.width - abs(tolerance)) and x1 <= (x2 + other.width + abs(tolerance)):
                        self.collide= "left"       #the player is to the left of the monster
                    elif (x1 + self.width) >= (x2 - abs(tolerance)) and (x1 + self.width) <= (x2 + abs(tolerance)):
                        self.collide = "right"      # the player is to the right of the monster
                    elif y1 >= (y2 + other.height - abs(tolerance)) and y1 <= (y2 + other.height + abs(tolerance)):
                        self.collide = "up"         # the player is above the monster
                    elif (y1 + self.height) >= (y2 - abs(tolerance)) and (y1 + self.height) <= (y2 + abs(tolerance)):
                        self.collide = "down"       # the player is below the monster

                    return True
            
            return False

    def attack(self,background,player,game):
        '''
        attack() causes the monster to deal damage to the player

        Parameters (required):
            background - game background obejct that the monster is located on
            player - the character that is being attacked
            game - game object that encompasses the monster
        '''

        # if the player is not attacking the monster and the monster is touching the player and is colliding with the player in the same direction it is traveling in
        if (player.held_item == None or not game.extend or player.held_item.nick == 'key' or not player.held_item.touching(self, game.screen)) and (self.touching(player,background,-15) and self.previous == self.collide and self.previous != None and not game.extend):
            self.n += 1     # attack delay
            if self.n == 50:
                self.place(background,extend=True)      # draw monster with extend=True (attack mode)
                player.decrease_health(self.attack_pts)     # decrease player mode
                self.n = 0      # reset attack delay
            else:
                self.place(background)      # draw monster
        else:
            self.place(background)      # draw monster

class Lion(Monster):
    '''
    The Lion() class is a subclass of the Monster() class that represents the lion monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes lion monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "lion" and attack_pts 5
        super().__init__("lion",x_bg, y_bg, 5)

class Cerberus(Monster):
    '''
    The Cerberus() class is a subclass of the Monster() class that represents the cerberus monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes cerberus monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "cerberus" and attack_pts 6
        super().__init__("cerberus",x_bg, y_bg, 6)

class Hydra(Monster):
    '''
    The Hydra() class is a subclass of the Monster() class that represents the hydra monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes hydra monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "hydra" and attack_pts 7
        super().__init__("hydra",x_bg, y_bg, 7)

class Golden_Deer(Monster):
    '''
    The Golden_Deer() class is a subclass of the Monster() class that represents the golden deer monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes golden deer monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "golden_deer" and attack_pts 8
        super().__init__("golden_deer",x_bg, y_bg, 8)

class Cattle(Monster):
    '''
    The Cattle() class is a subclass of the Monster() class that represents the cattle monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes cattle monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "cattle" and attack_pts 9
        super().__init__("cattle",x_bg, y_bg, 9)

class Boar(Monster):
    '''
    The Boar() class is a subclass of the Monster() class that represents the boar monster
    '''
    def __init__(self,x_bg, y_bg):
        '''
        __init__ initializes boar monsters

        Parameters (required):
            x_bg - x coordinate with relation to the background
            y_bg - y coordinate with relation to the background
        '''

        # intiates Monster parent class with nickname "boar" and attack_pts 10
        super().__init__("boar",x_bg, y_bg, 10)