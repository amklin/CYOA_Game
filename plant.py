'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: plant.py
Purpose: This file contains the Plant class that implements all plants which can be dug up and eaten.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
from additional_func import *

class Plant:
    '''
    The Plant() class represents a flower in the game, which can be dug up using a shovel and eaten for increased health points.
    '''
    
    def __init__(self, x_bg, y_bg):
        '''
        __init__() initializes the plant
        
        Parameters (required):
            x_bg - x coordinate of plant with respect to background
            y_bg - y coordinate of plant with respect to background
        '''
        
        self.x_bg = x_bg  # plant x coordinate
        self.y_bg = y_bg  # plant y coordinate
        
        self.frame = 0  # starting frame of plant (not dug up at all)
        self.walk_over = False  # plant cannot be walked over by the player
        self.dig_lag = 0  # digging lag so that, if digging continously, plant is only dug after a certain number of frames
        
        # list of sprites
        self.images = [] 
        for x in range(1,5):
            img = loadImage('images/plant' + str(x) + '.png')
            self.images.append(img)
        
        # width and height of plant
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
    
    def draw(self, background):
        '''
        draw() draws the plant in the background
        
        Parameter (required):
            background - the background to draw the plant on
        '''
        
        background.surface.blit(self.images[self.frame], (self.x_bg, self.y_bg))
    
    def eat(self, player, background):
        '''
        eat() allows the player to get health points when the player is fully dug up
        
        Parameters (required):
            player - the character who ate the plant
            background - background the plant was drawn on
        '''
        
        # player gets 20 health points for eating the plant
        player.increase_health(20)
        
        # removes the plant from the background
        background.background_obj.remove(self)
        background.set_background_image()