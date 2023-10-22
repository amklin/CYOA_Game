'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: chest.py
Purpose: This file contains the Chest class that implements all the chests that appear on the screen
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

import pygame
from additional_func import *

class Chest(pygame.surface.Surface):
    '''
    The Chest() class represents a chest that can be used in the game. 
    It is a subclass of the pygame Surface class.
    '''
    def __init__(self,x_bg,y_bg):
        '''
        __init__ initializes chest items
        
        Parameters (required):
            x_bg - x coordinate with respect to the background
            y_bg - y coordinate with respect to the background
        '''

        # x and y coordinates with respect to the background
        self.x_bg = x_bg
        self.y_bg = y_bg

        # loads images into a list
        self.images = []
        for i in range(1,3):
            img = loadImage('images/chest' + str(i) + '.png')
            self.images.append(img)
        
        # sets width and height of the chest to the image width and height
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()

        self.content = None     # content of the chest (what's inside them)

        self.walk_over = False      # can the player walk over them

        self.frame = 0              # image frame, changes based on open/close state
        self.state = False          # true if open, false if closed
        
        self.lag = 0                # lag counter

        # intializes parent class with width and height
        super().__init__([self.width,self.height], pygame.SRCALPHA)

    def place_object(self,object):
        '''
        place_object() places a Holdable() class object into the chest

        Parameters (required):
            object - object to be placed into the chest
        '''

        # sets object's x and y coordinates to the chest's x and y coordinates
        object.x_bg = self.x_bg
        object.y_bg = self.y_bg

        # sets the object equal to the content of the chest
        self.content = object

        # sets the object location to chest
        self.content.loc = "chest"


    def pick_up_object(self,player,background):
        '''
        pick_up_object() allows the player to retrieve the object from the chest

        Parameters (required):
            player - the character that is retriving the object
            background - the game background object that the chest and player are located on
        '''

        # if the player is touching the chest with a tolerance of 10 and the chest is open
        if self.touching(player,background,tolerance=-10) and self.state:
            self.content.pick_up(background,player)         # object is picked up by player
            self.content = None                             # content of chest is set to None

    def toggle(self,player,background):
        '''
        toggle() opens or closes the chest depending on current state

        Parameters (required):
            player - the character in the game
            background - the game background object that the chest and player are located on
        '''
        if self.state:  # if chest is open
            self.close(player,background)       # closes chest

        else:   # if chest is closed
            self.open(player,background)        # opens chest

    def open(self,player,background):
        '''
        open() opens the chest and changes image

        Parameters (required):
            player - the character in the game
            background - the game background object that the chest and player are located on
        '''
        if self.touching(player,background,tolerance=-20):      # if player is touching chest with tolerance -20
            self.frame = 1          # changes image
            self.state = True       # sets state to True (open)

    def close(self,player,background):
        '''
        close() opens the chest and changes image

        Parameters (required):
            player - the character in the game
            background - the game background object that the chest and player are located on
        '''

        if self.touching(player,background,tolerance=-20):      # if player is touching chest with tolerance -20
            self.frame = 0          # changes image
            self.state = False      # sets state to False (closed)

    def place(self,background):
        '''
        place() draws the chest on the screen

        Parameter (required):
            background - the game background object the chest should be drawn on
        '''

        # sets x and y coordinates with relation to the screen based on the x_bg and y_bg values
        self.x = self.x_bg - (background.stagePosX) 
        self.y = self.y_bg - (background.stagePosY)

        # places the chest image on the background in appropriate postion
        background.screen.blit(self.images[self.frame], (self.x,self.y))

        if self.content and self.state:     # if chest is open and it contains an item
            # adjusts the object's x and y coordinates so it is aligned properly in the chest
            self.content.x = self.content.x_bg - background.stagePosX + 20
            self.content.y = self.content.y_bg - background.stagePosY + 7

            # draws the holdable object image on the background in the appropriate position
            background.screen.blit(self.content.images[0],(self.content.x,self.content.y))

    def touching(self,other,background,tolerance=0,player=True):
        '''
        touching() checks whether the chest is touching another object

        Parameters (required):
            other - the other object that should be checked for collision
            background - the game background object that the chest and other object are located on

        Parameters (optional):
            tolerance - how much leeway there is between whether the chest is actually touching the object or not;
                        by default, set to 0
            player - whether the other object is the player or not; by default, set to True

        Returns:
            Boolean - True if touching the other object; False if not
        '''
        if player and other.held_item:          # if other is the player and the player is holding an item

            #calculates the x and y positions with respect to the screen accordingly 
            x1 = self.x_bg - (background.stagePosX)
            y1 = self.y_bg - (background.stagePosY)
                
            x2 = other.held_item.x  # this is the player's item's x and y positions
            y2 = other.held_item.y
            
            # checks whether the x and y positions of either object are inside the other object
            if (x2 >= (x1 + tolerance) and x2 <= (x1 + self.width - tolerance)) or (x1 >= (x2 + tolerance) and x1 <= (x2 + other.held_item.width - tolerance)):
                if (y2 >= (y1 + tolerance) and y2 <= (y1 + self.height -tolerance)) or (y1 >= (y2 + tolerance) and y1 <= (y2 + other.held_item.height -tolerance)):
                    return True
                
            return False

        else:       # if other is not player or if other is the player but is not holding an item

            # calculates the x and y positions with respect to the screen accordingly
            x1 = self.x_bg - (background.stagePosX)
            y1 = self.y_bg - (background.stagePosY)
                
            x2 = other.x
            y2 = other.y
            
            # checks whether the x and y positions of either object are inside the other object
            if (x2 >= (x1 + tolerance) and x2 <= (x1 + self.width - tolerance)) or (x1 >= (x2 + tolerance) and x1 <= (x2 + other.width - tolerance)):
                if (y2 >= (y1 + tolerance) and y2 <= (y1 + self.height -tolerance)) or (y1 >= (y2 + tolerance) and y1 <= (y2 + other.height -tolerance)):
                    return True
                
            return False