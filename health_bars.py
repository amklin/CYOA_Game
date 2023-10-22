'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: health_bars.py
Purpose: This file contains the HealthBar class that displays how many health points a character has.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
from text import *

class HealthBar(pygame.surface.Surface):
    '''
    The HealthBar() class represents how much health out of the maximum a particular character has.
    It is a subclass of the pygame Surface class.
    '''
    
    def __init__(self, value, x, y, nick):
        '''
        __init__() initializes a HealthBar
        
        Parameters (required):
            value - starting and maximum health points value of the bar
            x - x coordinate of bar on screen
            y - y coordinate of bar on screen
            nick - nickname of bar
        '''
        
        super().__init__([300,30])  # creates a 300x30 pixel surface for the bar
        self.value = value  # current number of health points
        self.max_value = value  # maximum number of health points
        self.x = x  # x coordinate of bar
        self.y = y  # y coordinate of bar
        self.nick = nick  # nickname of character the bar represents
        self.text = TextBox(5,5,50,30)  # text box located in bar
        self.text.text = self.nick + ": " + str(self.value) + '/' + str(self.max_value)  # text to place on top of bar; shows number of points out of the maximum
    
    def place(self,screen):
        '''
        place() draws the health bar on screen with the appropriate percentage filled and showing the number of health points
        
        Parameters (required):
            screen - the screen the bar is drawn on
        '''
        
        # rectangle representing current health
        # draws the bar as a certain percentage full
        rect = pygame.rect.Rect(0,0,int(300*self.value/self.max_value),30)
        pygame.draw.rect(self,(255,0,0),rect)
        
        # place text
        self.text.updateText(self, new_text = self.nick + ": " + str(self.value) + '/' + str(self.max_value))
        
        # place self on screen
        screen.blit(self, [self.x,self.y])
    
    def update_bar(self,screen, new_val=None):
        '''
        update_bar() redraws the bar with the new specified number of health points
        
        Parameter (required):
            screen - where to draw the health bar
        
        Parameter (optional):
            new_val - new number of health points
        '''
        
        # resets value if a new value is inputted
        if new_val != None:
            self.value = new_val
        
        # redraws bar
        self.fill((100,0,0))
        self.place(screen)