'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: player.py
Purpose: This file contains the Player class that implements all characters in the game.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
from additional_func import *
from background import *

class Player:
    '''
    The Player() class represents a character in the game, including the main player and the monsters (the monsters are subclasses).
    '''
    
    def __init__(self, nick, items_list=None):
        '''
        __init__() initializes the character
        
        Parameters (required):
            nick - character 'nickname'; used to retrieve the correct images from the images folder
        
        Parameters (optional):
            items_list - the list of items that the character holds at a given time (i.e., its backpack); by default, set to None
        '''
                
        # retrieves the images for each frame of the character
        # there is 1 frame for each direction the character faces (up, down, right, or left)
        self.images = []
        for x in range(1,5):
            img = loadImage('images/' + nick + str(x) + '.png')
            self.images.append(img)
        
        # width and height of the character
        # determined based on the first image frame, but they are the same for all frames
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        
        # x and y positions in reference to the window
        # main player will always be in the middle of the screen
        self.x = 500 - (self.width // 2)
        self.y = 400 - (self.height // 2)
        
        self.held_item = None  # item that the character is currently holding in their hands
        self.possible_weapons = []  # list of items that the character has acquired
        self.items_list = items_list  # list of items the character has in their backpack or in their hand
        
        self.health = 100  # health points; starts at 100; this is also the maximum value
        
        # grid cell row and grid cell column numbers of character in the 9x9 labyrinth grid
        self.pos_row = 1
        self.pos_col = 1
        
        self.hit = False  # whether or not the character is being attacked; initially, the character is not being hit
        self.hit_count = 0  # implements a lag for being attacked (so that points are subtracted less frequently than each frame)
        
        # animation_images and image are only used if the character is the main player and has beat the game
        self.animation_images = {}  # dictionary images for character animation
        self.image = None  # image of character animation if the animation is running
    
    def get_new_loc(self, background):
        '''
        get_new_loc() retrieves the new location (i.e., grid row and grid column) in the 9x9 labyrinth grid
        
        Parameters (required):
            background - the background object the player is on
        '''
        
        # x and y positions of the character with respect to the background image
        if 'x_bg' in self.__dict__:
            x_bg = self.x_bg
            y_bg = self.y_bg
        else:
            x_bg = background.stagePosX
            y_bg = background.stagePosY
        
        # gets new grid cell row and column position of character
        # position = (background coordinate - starting center position + offset)//cooridor width
        self.pos_col = (x_bg - 1050 + 430)//620 + 1
        self.pos_row = (y_bg - 900 + 365)//620 + 1

    
    def place(self, background, frame):
        '''
        place() draws the character on screen
        
        Parameters (required):
            background - background the character is located on
            frame - frame number of player to be drawn (each frame represents a different orientation (up, left, down, or right))
        '''
        
        # draws the character facing in the specified direction
        background.screen.blit(self.images[frame], (self.x, self.y))
        
        # temporarily turns red if hit
        if self.hit:
            # creates surface allowing transparency
            shape_surf = pygame.Surface(pygame.Rect(0, 0, self.width, self.height).size, pygame.SRCALPHA)
            
            # draws semi transparent red rectange
            pygame.draw.rect(shape_surf, (255, 0, 0, 150), shape_surf.get_rect())
            
            # implements a lag for how long the red rectangle is visible
            # so that it is visible for about 20 frames of the game
            if self.hit_count <= 20:
                # draws the red rectange and increments the lag counter
                background.screen.blit(shape_surf, (self.x, self.y))
                self.hit_count += 1
            else:
                # resets the counter
                self.hit_count = 0
                
                # resets whether the character has been hit so that they can be hit again
                self.hit = False
    
    def touching(self, other, background, monster=True):
        '''
        touching() checks whether the character is touching a particular object
        
        Parameters (required):
            other - the object to be checked for contact
            background - background the character is on
        
        Parameters (optional):
            monster - whether the player is in contact with the monster
        
        Returns:
            Boolean - True if touching the other object; False if not
        '''
        
        # player's own coordinates
        x1 = self.x
        y1 = self.y
        
        # sets the other object's x and y coordinates
        if other in background.background_obj and monster == True:
            # if the other object is an object in the background and is a monster
            x2 = other.x_bg - (background.stagePosX - 500)
            y2 = other.y_bg - (background.stagePosY - 400)
        elif other in background.background_obj:
            # if the other object is an object in the background but is not a monster
            x2 = other.x_bg - background.stagePosX
            y2 = other.y_bg - background.stagePosY
        else:
            # if the other object is not a background object
            x2 = other.x
            y2 = other.y
        
        # checks whether the x and y positions of either object are inside the other object
        if (x2 >= x1 and x2 < (x1 + self.width)) or (x1 >= x2 and x1 < (x2 + other.width)):
            if (y2 >= y1 and y2 < (y1 + self.height)) or (y1 >= y2 and y1 < (y2 + other.height)):
                return True  # returns True if the objects are touching

        # returns False if the objects are not touching
        return False

    def decrease_health(self, pts):
        '''
        decrease_dealth() decreases the character's health points by the specified amount
                         and sets self.hit to True to show the character has been hit
        
        Parameter (required):
            pts - how many health points the character's health should be decreased by
        '''
        
        self.health -= pts
        self.hit = True
    
    def increase_health(self, pts):
        '''
        increase_health() increases the character's health by the specified number of points, but only if this value will not exceed 100
        
        Parameter (required):
            pts - how many helath points the character's health should be increased by
        '''
        
        self.health = min(self.health+pts, 100)

    def become_immortal(self, frames=44, delay=25):     
        '''
        become_immortal() retrieves the animation_images for the animation at the end of the game
        
        Parameters (optional):
            frames - the number of frames in the animation; set to 44 by default
            delay - how frequently the animation should be updated (i.e., how many game frames should pass between each animation frame); set to 25 by default 
        '''
        
        # loops through all frames and adds the to the animation_images dictionary
        for i in range(1,frames+1):
            img = loadImage('animation/' + str(i) + '.png')  # loads image
            self.animation_images[(i-1)*delay] = img  # key:value pair of game frame:image (game frame is the frame times delay)
        
        # sets character width and height to animation image width and height
        self.width = self.animation_images[0].get_width()
        self.height = self.animation_images[0].get_height()
        
        # x and y positions in reference to the window so that the character is always in the middle of the scren
        self.x = 500 - (self.width // 2)
        self.y = 400 - (self.height // 2)