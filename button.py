'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: button.py
Purpose: This file contains the Button and BackgroundButton classes that can be clicked on with mouse for certain actions to occur.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
from additional_func import *

class Button(pygame.rect.Rect):
    '''
    The Button() class represents a button on any screen that can be clicked.
    '''
    
    def __init__(self, x, y, screen_loc, nick):
        '''
        __init__() initializes a button
        
        Parameters (required):
            x - x coordinate of button
            y - y coordinate fo button
            screen_loc - the screen the button should be placed on
            nick - button nickname for images
        '''
        
        # gets button sprites
        self.images = []
        for i in range(1,3):
            img = loadImage('images/' + nick + str(i) + '.png')
            self.images.append(img)
        
        # default button frame
        self.frame = 0
        
        # button width and height
        self.width = self.images[0].get_width()
        self.height = self.images[0].get_height()
        
        # button x and y coordinates
        self.x = x
        self.y = y
        
        self.screen_loc = screen_loc  # screen to draw button on
        self.nick = nick  # pause nickname
        self.count = 0  # implements a lag to ensure that the button click only registers once
        self.prev_clicked = False  # whether the button has already been clicked
    
    def place(self):
        '''
        place() draws the button on the screen
        '''
        
        self.screen_loc.blit(self.images[self.frame], [self.x, self.y])
    
    def detectClick(self, events, pos=None):
        '''
        detectClick() checks whether the button was clicked or not
        
        Parameter (required):
            events - list of pygame events that have occured in the game (e.g., mouse click)
        
        Parameter (optional):
            pos - manually inputted x and y coordinates as a tuple
        
        Returns:
            Boolean - True if the button was clicked; False if not
        '''
        
        # if a position was specified, uses those coordinates
        if pos:
            x = pos[0]
            y = pos[1]
        
        # otherwise uses the default x and y positions of the button
        else:
            x = self.x
            y = self.y
        
        # gets current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        
        # detects whether the mouse has been clicked and whether it was clicked on top of the button
        for event in events:
            # if the button was clicked, changes the button frame to have the opposite appearance and returns True
            if not self.prev_clicked and event.type == pygame.MOUSEBUTTONDOWN and (mouse_x > x and mouse_x <= x + self.width) and (mouse_y > y and mouse_y <= y + self.height):
                if self.frame == 1:
                    self.frame -= 1
                else:
                    self.frame += 1
                
                self.prev_clicked = True
                
                return True
            elif self.prev_clicked and not event.type == pygame.MOUSEBUTTONDOWN:
                self.prev_clicked = False
        
        # returns False if not clicked
        return False

class BackgroundButton(Button):
    '''
    The BackgroundButton() class is a subclass of Button() and represents a button that is part of the labyrinth background.
    '''
    
    def __init__(self, x, y, screen_loc, nick):
        super().__init__(x, y, screen_loc, nick)
        self.walk_over = False
        
        self.x_bg = x
        self.y_bg = y
    
    def detectClick(self, background, events):
        '''
        detectClick() checks whether the button was clicked or not
        
        Parameter (required):
            background - where the button is located
            events - list of pygame events that have occured in the game (e.g., mouse click)
        
        Returns:
            Boolean - True if the button was clicked; False if not
        '''
        
        # x and y coordinates with respect to the pygame window
        x = self.x - background.stagePosX
        y = self.y - background.stagePosY
        
        return super().detectClick(events,pos=(x,y))  # calls and returns the parent detectClick() function

    def detect_collision(self, other):
        '''
        detect_collision() detects a collision between the button and another object/sprite
        
        Parameters (required):
            other - the object for collision detection
        
        Returns:
            Boolean - True if a collision is detected; False if not
        '''
        
        # checks if any of the item coordinates overlap and returns True if yes or False if no
        if (other.x >= self.x and other.x < (self.x + self.width)) or (self.x >= other.x and self.x < (other.x + other.width)):
            if (other.y >= self.y and other.y < (self.y + self.height)) or (self.y >= other.y and self.y < (other.y + other.height)):
                return True
        
        return False