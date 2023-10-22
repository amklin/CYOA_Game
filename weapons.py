'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: weapons.py
Purpose: This file contains the Holdable class and all subclasses that implements all items that the player can pick up in the game.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
import pandas as pd
from additional_func import *
from game import *

# accesses csv file that stores the stats of all the weapons/items
weapon_stats = pd.read_csv('./stats/weapons.csv')
weapon_stats.index = weapon_stats["weapons"]
weapon_stats.drop(columns=["weapons"],inplace=True)
# data points can be accessed via weapon_stats[category, weapon_nick]
# for example, weapon_stats["lion"]["sword"] gives the damage the sword does against the lion

# list of enemies to iterate through
enemies = ["lion","hydra","golden_deer","boar","cattle","cerberus"]

class Holdable:
    '''
    The Holdable() class represents an item that the player can hold in the game.
    '''
    
    def __init__(self,wielder,loc,nick, x_bg=0, y_bg=0, defaultImages=True):  
        '''
        __init__() initializes Holdable items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
            nick - item 'nickname' for retrieving images
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
            defaultImages - Boolean representing whether to retrieve the item's images as shown below; set to True by default
        '''
        
        # retrieves the images for each frame of the item
        # there is 1 frame for each direction the item faces (up, down, right, or left)
        if defaultImages:
            self.images = []
            for x in range(1,5):
                img = loadImage('images/' + nick + str(x) + '.png')
                self.images.append(img)
        
        # width and height of holdable item
        # determined based on the first image frame, but they are the same for all frames
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        
        self.frame = 0  # which frame image should be used
        self.walk_over = True # whether you are able to walk over the item, set True by default
        
        # x and y positions of item on player
        self.x = 500
        self.y = 400
        
        # x and y positions of item when not being held
        self.x_bg = x_bg
        self.y_bg = y_bg
        
        self.wielder = wielder  # who is in control of the item
        
        # if someone if in control of the item, that weilder's item is set to self
        if self.wielder != None:
            wielder.held_item = self
    
        self.loc = loc  # keeps track of where the item is, either: "hands", "backpack", or "ground"
        
        self.nick = nick  # internal name of the item, used for dictionary keys
        
        self.times_picked_up = 0  # number of times the item has been picked up
        
    def detect_collision(self, other):
        '''
        detect_collision() detects a collision between the item and another object/sprite
        
        Parameter (required):
            other - the item to detect collision with
        
        Returns:
            Boolean - True if collided; False if not collided
        '''
        
        # checks whether the points of the item and other object overlap
        if (other.x >= self.x and other.x < (self.x + self.width)) or (self.x >= other.x and self.x < (other.x + other.width)):
            if (other.y >= self.y and other.y < (self.y + self.height)) or (self.y >= other.y and self.y < (other.y + other.height)):
                return True
        
        return False

    def draw(self, background, extend=False):
        '''
        draw() draws the item on the screen
        
        Parameter (required):
            background - the background object the item should be drawn on
        
        Parameter (optional):
            extend - whether the item should be extended
        '''
        
        # if the player is holding the item
        if self.loc == 'hands':
            # positions the item with reference to the player using preset values
            # preset values ensure the item appears to be in the player's hand
            if self.frame == 0:
                self.x = self.wielder.x - 5
                self.y = self.wielder.y + 70
            elif self.frame == 1:
                self.x = self.wielder.x + 60
                self.y = self.wielder.y + 25
            elif self.frame == 2:
                self.x = self.wielder.x - 45
                self.y = self.wielder.y + 25
            elif self.frame == 3:
                self.x = self.wielder.x - 5
                self.y = self.wielder.y
            
            # gets new x and y positions with respect to the background
            self.x_bg = background.stagePosX + self.x
            self.y_bg = background.stagePosY + self.y
            
            # if the item should be extended, draw the item extended using the extend() function
            if extend:
                self.extend(background)
            
            # if not, draws the item on screen on top of the player
            else:
                background.screen.blit(self.images[self.frame], (self.x, self.y))
        
        # if the item is on the ground (not held by the player), draws the item in the background
        elif self.loc == 'ground':
            background.surface.blit(self.images[self.frame], (self.x_bg,self.y_bg))
    
    def extend(self, background):
        '''
        extend() extends the item so that it is 10 pixels further from the hands of the player to show that it is in use
        
        Parameters (required):
            background - where the item should be drawn
        '''
        
        # creates local variables equal to the x and y positions of the item
        # local variables are used so that the extension is temporary
        x = self.x
        y = self.y
        
        # extends the x or y position of the item by 10 pixels whichever way the item is facing
        if self.frame == 0:  # facing down
            y += 10
        elif self.frame == 1:  # facing right
            x += 10
        elif self.frame == 2:  # facing left
            x -= 10
        elif self.frame == 3:  # facing up
            y -= 10
        
        # resets the background x and y positions with the extended x and y values
        self.x_bg = background.stagePosX + x
        self.y_bg = background.stagePosY + y
        
        # draws the item on screen
        background.screen.blit(self.images[self.frame], (x, y))
    
    def pick_up(self, background, player):
        '''
        pick_up() picks the item up from the ground and places it into the player's hands
        
        Parameters (required):
            background - the background the player should be drawn on
            player - the character that picked up the item
        '''
        
        # picks the item up from the background and updates the background image
        background.background_obj.remove(self)
        background.set_background_image()
        
        # adds the item into the player's hands
        self.wielder = player
        player.held_item = self
        self.loc = 'hands'
        
        # adds the item into the list of items the player can loop through and hold
        player.items_list.append(self)
        
        # increments how many times the item has been picked up
        self.times_picked_up += 1

    def drop(self, background, player):
        '''
        drop() drops the item from the player's hands onto the ground (i.e., into the background)
        
        Parameters (required):
            background - the background the player should be drawn on
            player - the character that dropped the item
        '''
        
        # removes item from the player's hands and places it onto the ground
        player.held_item = None
        self.wielder = None
        self.loc = 'ground'
        
        # removes the item from the list of items that the player can loop through and hold
        player.items_list.remove(self)
        
        # updates background x and y locations
        self.x_bg = background.stagePosX + self.x
        self.y_bg = background.stagePosY + self.y
        
        # adds the item to the background and updates the background image
        background.background_obj.append(self)
        background.set_background_image()
    
    def place_in_backpack(self, player):
        '''
        place_in_backpack() removes the item from the player's hands and adds it into the backpack so that the player can carry the item
        
        Parameters (required):
            player - the character that placed the item into their backpack
        '''
        
        # removes the item from the player's hands and places it into the backpack
        # the item is kept in the list of items the player can loop through and hold
        player.held_item = None
        self.wielder = None
        self.loc = 'backpack'
    
    def select_from_backpack(self, player):
        '''
        select_from_backpack() takes the item out of the backpack and places it into the player's hands
        
        Parameters (required):
            player - the character that took the item out of their backpack
        '''
        
        # adds the item into the player's hands
        self.wielder = player
        player.held_item = self
        self.loc = 'hands'
    
    def touching(self, other, background):
        '''
        touching() checks whether the item is touching a particular object
        
        Parameters (required):
            other - the object to be checked for contact
            background - background the item is on
        
        Returns:
            Boolean - True if touching the other object; False if not
        '''
        
        # item's own coordinates with respect to the window
        x1 = self.x_bg - background.stagePosX
        y1 = self.y_bg - background.stagePosY
        
        # sets the other object's x and y coordinates
        if other in background.background_obj or other in background.door_list:  # if the object is a background object or a door
            x2 = other.x_bg - background.stagePosX
            y2 = other.y_bg - background.stagePosY
        else:  # if the object isn't in the background
            x2 = other.x
            y2 = other.y
        
        # checks whether the x and y positions of either object are inside the other object
        if (x2 >= x1 and x2 < (x1 + self.width)) or (x1 >= x2 and x1 < (x2 + other.width)):
            if (y2 >= y1 and y2 < (y1 + self.height)) or (y1 >= y2 and y1 < (y2 + other.height)):
                return True  # returns True if the objects are touching
        
        # returns False if the objects aren't touching
        return False

class Weapon(Holdable):
    '''
    The Weapon() class is a subclass of Holdable() that represents all weapons the player can hold.
    '''
    
    def __init__(self,wielder,loc,nick, x_bg=0, y_bg=0, defaultImages=True):
        '''
        __init__() initializes Weapon items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
            nick - item 'nickname' for retrieving images
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
            defaultImages - Boolean representing whether to retrieve the item's images as shown below; set to True by default
        '''
        
        # calls parent class initialization
        super().__init__(wielder,loc,nick, x_bg=x_bg,y_bg=y_bg, defaultImages=defaultImages)
        
        # dictionary of damage caused towards each enemy
        self.damage_pts = {}
        for enemy in enemies:
            self.damage_pts[enemy] = weapon_stats[enemy][self.nick]

class Sword(Weapon):
    '''
    The Sword() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc, x_bg=0, y_bg=0):
        '''
        __init__() initializes Sword items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'sword' nickname
        super().__init__(wielder,loc,"sword",x_bg=x_bg,y_bg=y_bg)

class Trident(Weapon):
    '''
    The Trident() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc,x_bg=0, y_bg=0):
        '''
        __init__() initializes Trident items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'trident' nickname
        super().__init__(wielder,loc,"trident",x_bg=x_bg, y_bg=y_bg)

class Boxing_Glove(Weapon):
    '''
    The Boxing_Glove() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc, x_bg=0, y_bg=0):
        '''
        __init__() initializes Boxing_Glove items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'boxing-glove' nickname
        super().__init__(wielder,loc,"boxing-glove", x_bg=x_bg, y_bg=y_bg)

class Shovel(Weapon):
    '''
    The Shovel() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc, x_bg=0, y_bg=0):
        '''
        __init__() initializes Shovel items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'shovel' nickname
        super().__init__(wielder,loc,"shovel", x_bg=x_bg,y_bg=y_bg)
    
    def dig(self, plant, background):
        '''
        dig() allows the player to dig up plants using a shovel
        
        Parameters (required):
            plant - the plant to be dug up
            background - the background the plant is on
        '''
        
        # if the plant is almost fully dug up and the shovel is touching it, the player eats the plant and gains health 
        if plant.frame == 3 and self.touching(plant, background):
            plant.eat(self.wielder, background)
            plant.frame += 1
        
        # if the plant is a background object, the shovel is touching the plant, and the plant isn't fully dug up, digs plant and draws it
        if plant in background.background_obj and self.touching(plant, background) and plant.frame <= 2:
            plant.frame += 1
            plant.draw(background)

class Flashlight(Weapon):
    '''
    The Flashlight() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc,x_bg=0, y_bg=0):
        '''
        __init__() initializes Flashlight items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        self.state = False   # tracks whether the flash light is on or off (boolean)

        # flashlight sprites when turned on
        self.images_on = []
        for x in range(1,5):
            img = loadImage('images/flashlight' + str(x) + 'on.png')
            self.images_on.append(img)
        
        # flashlight sprites when turned off
        self.images_off = []
        for x in range(1,5):
            img = loadImage('images/flashlight' + str(x) + 'off.png')
            self.images_off.append(img)
        
        # by default, the flashlight starts off, so off images are used
        self.images = self.images_off

        # calls parent class initialization with 'flashlight' nickname; doesn't use default images
        super().__init__(wielder,loc,"flashlight", x_bg=x_bg, y_bg=y_bg, defaultImages=False)
    
    def change_state(self):
        '''
        change_states() turns on flashlight off and off flashlight on
        '''
        
        if self.state:
            self.turn_off()
        else:
            self.turn_on()
    
    def turn_on(self):
        '''
        turn_on() turns the flashlight on by switching state and sprites
        '''
        
        self.state = True
        self.images = self.images_on
    
    def turn_off(self):
        '''
        turn_off() turns the flashlight on by switching state and sprites
        '''
        
        self.state = False
        self.images = self.images_off

class Flame_Thrower(Weapon):
    '''
    The Flame_Thrower() class is a subclass of Weapon()
    '''
    
    def __init__(self,wielder,loc,x_bg=0, y_bg=0):
        '''
        __init__() initializes Flame_Thrower items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'flame-thrower' nickname
        super().__init__(wielder,loc,"flame-thrower",x_bg=x_bg, y_bg=y_bg)

class Key(Holdable):
    '''
    The Key() class is a subclass of Holdable()
    '''
    
    def __init__(self,wielder,loc,id,x_bg=0, y_bg=0):
        '''
        __init__() initializes Key items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        self.id = id  # corresponds to the door that the key can open
        
        # gets key sprites
        self.images = []
        for x in range(1,5):
            img = loadImage('images/' + "key" + str(self.id) + str(x) + '.png')
            self.images.append(img)
    
        # calls parent class initialization with 'key' nickname and doesn't use default images
        super().__init__(wielder,loc,"key",x_bg=x_bg,y_bg=y_bg,defaultImages=False)

class Gem(Holdable):
    '''
    The Gem() class is a subclass of Holdable()
    '''
    
    def __init__(self,wielder,loc,x_bg=0, y_bg=0):  
        '''
        __init__() initializes Gem items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'gem' nickname
        super().__init__(wielder,loc,"gem",x_bg=x_bg,y_bg=y_bg)
    
    def in_space(self, x_right, x_left, y_top, y_bottom):
        '''
        in_space() checks if the gem is in a certain area based on the coordinate parameters
        
        Parameters (required):
            x_right - right x coordinate of space
            x_left - left x coordinate of space
            y_top - top y coordinate of space
            y_bottom - bottom x coordinate of space
        
        Returns:
            Boolean - True if item is in the designated space; False if not
        '''
        
        # checks if item is in the area
        if (self.x_bg > x_right and self.x_bg < x_left) and (self.y_bg > y_top and self.y_bg < y_bottom):
            return True

        return False

class Potion(Holdable):
    '''
    The Potion() class is a subclass of Holdable()
    '''
    
    def __init__(self,wielder,loc,x_bg=0,y_bg=0):
        '''
        __init__() initializes Gem items
        
        Parameters (required):
            wielder - the character holding the item
            loc - location of the item; 'ground', 'backpack', or 'hands'
        
        Parameters (optional):
            x_bg - x coordinate with respect to background; 0 by default
            y_bg - y coordinate with respect to background; 0 by default
        '''
        
        # calls parent class initialization with 'potion' nickname
        super().__init__(wielder,loc,'potion',x_bg=x_bg,y_bg=y_bg)
        
    def use_potion(self, player):
        '''
        use_potion() allows player to become immortal when they pick it up
        
        Parameter (required):
            player - the player using the potion
        '''
        
        player.become_immortal()