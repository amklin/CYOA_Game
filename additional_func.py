'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: additional_func.py
Purpose: This file contains functions used throughout the game that aren't attached to any class, including image loading and key press detection.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame

# dictionary of pressed keys
keydict = {"space": pygame.K_SPACE, "esc": pygame.K_ESCAPE, "up": pygame.K_UP, "down": pygame.K_DOWN,
           "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "return": pygame.K_RETURN,
           "a": pygame.K_a,
           "b": pygame.K_b,
           "c": pygame.K_c,
           "d": pygame.K_d,
           "e": pygame.K_e,
           "f": pygame.K_f,
           "g": pygame.K_g,
           "h": pygame.K_h,
           "i": pygame.K_i,
           "j": pygame.K_j,
           "k": pygame.K_k,
           "l": pygame.K_l,
           "m": pygame.K_m,
           "n": pygame.K_n,
           "o": pygame.K_o,
           "p": pygame.K_p,
           "q": pygame.K_q,
           "r": pygame.K_r,
           "s": pygame.K_s,
           "t": pygame.K_t,
           "u": pygame.K_u,
           "v": pygame.K_v,
           "w": pygame.K_w,
           "x": pygame.K_x,
           "y": pygame.K_y,
           "z": pygame.K_z,
           "1": pygame.K_1,
           "2": pygame.K_2,
           "3": pygame.K_3,
           "4": pygame.K_4,
           "5": pygame.K_5,
           "6": pygame.K_6,
           "7": pygame.K_7,
           "8": pygame.K_8,
           "9": pygame.K_9,
           "0": pygame.K_0}

# loads image file based on filename
def loadImage(filename):
    '''
    loadImage() loads a png as a pygame image
    
    Parameter (required):
        filename - filename of image
        
    Returns:
        image - loaded pygame image
    '''
    
    image = pygame.image.load(filename)  # gets image
    image = image.convert_alpha()  # allows for transparency
    return image  # returns image

# checks key press
def keyPressed(key=""):
    '''
    keyPressed() determines if a specific key was presse
    
    Parameter (optional):
        key - key to be checked; set to empty string by default
    
    Returns:
        Boolean - True if the key was pressed; False if not
    '''
    
    keys = pygame.key.get_pressed()  # gets the keys that were pressed
    
    # if any key was pressed, checks if the key pressed was the target key
    # returns True if target key was pressed
    if sum(keys) > 0:
        if key == "" or keys[keydict[key.lower()]]:
            return True
    
    # returns False if target key was not pressed
    return False

def enter_or_click(events):
    '''
    enter_or_click() checks if either the enter key or the mouse was clicked
    
    Parameter (required):
        events - list of pygame events that occured
    
    Returns:
        Boolean - True if 'enter' is pressed or mouse is clicked; False if not
    '''
    
    for event in events:
        if (event.type == pygame.MOUSEBUTTONDOWN) or keyPressed('return'):
            return True

    return False
