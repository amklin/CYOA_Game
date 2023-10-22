'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: text.py
Purpose: This file contains the TextBox class that implements all the text boxes that appear
        on the screen as well as all associated subclasses
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

import pygame
from additional_func import *
from button import *
from weapons import *

class TextBox(pygame.surface.Surface):
    '''
    The TextBox() class represents a basic textbox that can be used in the game.
    It is a subclass of the pygame Surface Class.
    '''

    def __init__(self,x,y, width, height, text_size=25, text="", padding=5, top_padding=0, left_padding=0):

        '''
        __init__() initializes the text box

        Parameters (required):
            x - x coordinate of the text box with respect to the screen
            y - y coordinate of the text box with respect to the screen
            width - width of the text box
            height - height of the text box
        
        Parameters (optional):
            text_size - font size of the text; by default, set to 25
            text - text that is being displayed; by default, set to an empty screen
            padding - padding between the lines of text; by default, set to 5
            top_padding - padding at the top of the text box before the text; by default, set to 0
            left_padding - padding at the left of the text box before the text; by default, set to 0

        '''

        # initiates the pygame.surface.Surface super class
        super().__init__([width,height], pygame.SRCALPHA)

        # initiates pygame fonts
        pygame.font.init()

        self.x = x      # x coordinate of textbox
        self.y = y      # y coordinate of textbox
        self.width = width      # width of textbox
        self.height = height    # height of textbox

        self.text = text                # text inside textbox
        self.text_size = text_size      # font size of text
        
        # sets font of text to Free Sans Bold
        self.font = pygame.font.SysFont('freesansbold.ttf', self.text_size)

        # creates a pygame.rect.Rect object that encompasses the rectangle containing the text box
        self.rect = pygame.rect.Rect(x,y,width,height)
        
        # sets padding (in between lines of text, on top of text, to the left of text)
        self.padding = padding
        self.top_padding = top_padding
        self.left_padding = left_padding
    
    def place(self, background ,background_color=None,text_color=(0,255,0)):

        '''
        place() draws the text box on the screen

        Parameters (required):
            background - game background object that the text box is located on 

        Parameters (optional):
            background_color - (r,g,b) tuple representing the background color of the text box; by default, set to None (i.e. default color)
            text_color - (r,g,b) tuple representing the color of the text; by default, set to (0,255,0) (i.e. green)
        '''

        # fills the text box with color
        self.fill((0,0,0))
        
        # if a specific background color is used, fills the screen with that color
        if background_color:
            background.fill(background_color, self.rect)
        
        # creates a list of lines of text
        lines = self.text.splitlines()
        
        # adds the text to the screen based on the list of lines
        for x in range(len(lines)):
            line = lines[x]
            textAdded = self.font.render(line, True, text_color, None)
            background.blit(textAdded, (self.x+self.left_padding, self.y + (self.text_size + self.padding)*x+self.top_padding))

    def updateText(self, background, new_text=None, background_color=None,text_color=(0,255,0)):

        '''
        updateText() updates the text in the textbox

        Parameters (required):
            background - game background object that the text box is located on 
        
        Parameters (optional):
            new_text - new text that the text should be updated to; by default, set to None
            background_color - background color of the text box; by default, set to None
            text_color - color of the text; by default, set to (0,255,0) i.e. green
        '''

        # if the new_text isn't None, update self.text
        if new_text != None:
            self.text = new_text
        
        # place updated text box on the screen
        self.place(background, background_color,text_color)

    def detectClick(self, events):

        '''
        detectClick() detects whether the mouse has clicked on the text box

        Parameters (required):
            events - list of pygame events
        '''

        for event in events:    # loops through list pygame events 
            mouse_x, mouse_y = pygame.mouse.get_pos()       # gets position of mouse
            
            # if mouse is clicked and mouse pointer is within the boundaries of the textbox, return true
            if event.type == pygame.MOUSEBUTTONDOWN and (mouse_x > self.x and mouse_x <= self.x + self.width) and (mouse_y > self.y and mouse_y <= self.y + self.height):
                return True

class ImageBox(TextBox):
    '''
    The ImageBox() class is a subclass of TextBox() which represents a textbox with an image background
    '''

    def __init__(self,x,y,filename='scroll'):

        '''
        __init__() initializes the image box

        Parameters (required):
            x - x coordinate of the image box with respect to the screen
            y - y coordinate of the image box with respect to the screen

        Parameters (optional):
            filename - the filename of the image file, without the .png extension; by default, set to 'scroll'
        '''

        # loads image from filename
        self.image = loadImage('images/' + filename + '.png')

        # determines width and height of the textbox from the image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # initializes the TextBox super class
        super().__init__(x,y,self.width,self.height)
    
    def place(self, background, text_color=(0,255,0)):

        '''
        place() draws the image box on the screen

         Parameters (required):
            background - game background object that the text box is located on 

        Parameters (optional):
            text_color - (r,g,b) tuple representing the color of the text; by default, set to (0,255,0) (i.e. green)
        '''

        # draws the image
        self.blit(self.image, (0,0))
        
        # creates a list of lines of text
        lines = self.text.splitlines()

        # adds text to the screen based on the list of lines
        for x in range(len(lines)):
            line = lines[x]
            textAdded = self.font.render(line, True, text_color, None)
            
            # the text is offset by 150 px on each direction, and 20 px between lines
            self.blit(textAdded, (150, 150+20*x))
        
        # draws the image box onto the screen
        background.blit(self, (self.x,self.y))

class Story(ImageBox):
    '''
    The Story() class is a subclass of the ImageBox() class that contains all the text and related function for the storyline
    '''

    def __init__(self, x, y):

        '''
        __init__() initializes the story

        Parameters (required):
            x - x coordinate of the image box with respect to the screen
            y - y coordinate of the image box with respect to the screen

        '''

        # initializes the ImageBox superclass
        super().__init__(x, y)

        # a list of the introductory story text at the very beginning of the game
        self.story_text = ["You open your eyes. It is dark. The sound of your \nbreathing echoes around you. You sit up and try \nto look around, but you can’t see anything. \nWhere are you?",
                        "Then you remember. The gods had offered you a \nonce-in-a-lifetime opportunity to gain immortality \nby completing their quest.",
                        "Your task is to kill the six monsters in the \nlabyrinth. But if you fail, your death awaits. Do \nyou accept this quest?"]
        
        # a list of the instruction text at the beginning of the game
        self.instruction_text = ["Use the arrow keys to move around the labyrinth. \nPick up weapons by pressing \"d\" and drop items \nby pressing \"f\". You can use these items \nby pressing the \"space\" key.",
                        "Kill the monsters using weapons. Each of the \nsix monsters have their own room, and they \nautomatically leave their room once the previous \nmonster has been killed.",
                        "Beware: the monsters have many special powers, \none of which is tracking you down. Unlike you, \nthey are also able to walk through objects (although \nthey have not yet evolved to walk through walls).", 
                        "If you are not using a weapon, you can place it \ninto your backpack by pressing \"e\" and pressing \"r\" \nto cycle through the items in your backpack. \nYou can keep a maximum of five weapons in \nyour backpack at any one point.",
                        "You can view the menu of items you have by \npressing \"a\". From this menu, you can view the \nstats of all the weapons as well as selecting which \nweapon you wish to equip by pressing a number \n1-5. Close the menu by pressing \"s\".", 
                        "The labyrinth is at the center of the maze and \ndark at the beginning. There\'s an entrance to it \nat the top and bottom of the map. Find the \nflashlight to enter the labyrinth. There are many \nspecial power-ups hidden in the labyrinth.", 
                        "Most importantly of all, there are gems hidden \nwithin the labyrinth. Without these gems, you \ncan\'t enter the final room and attain immortality. \nThese gems disappear once the timer runs out \nthough, so don\'t delay!",
                        "Tip: if you forget what the controls are, you can \nalways view the help box in the bottom right corner \nof the game screen.",
                        "Ready to start?"]

        # a list of the introduction text that pops up on the first encounter with each type of item
        self.introduction_text = {"plant":"Use the shovel to dig up the plant in order to \ngain 20 health points. Remember, you can only \nhave a maximum health of 100, so don\'t try to dig \nup a plant when you are at maximum health.",
                                "key":"Congratulations, you just killed your first monster! \nYou can use the key to access the monster\'s rooms \nin order to find treasure and stronger weapons. \nThe key can only open the correct door, and the \nkeys and doors are color coded.",
                                "chest":"Press \"w\" to open or close the chest. Each chest \ncontains a treasure of some kind, usually a powerful \nweapon that can help you kill monsters. Remember, \nyou can view weapon stats by pressing \"a\" and \nlooking at the menu of items.",
                                "flashlight":"Congratulations, you found the flashlight! Now \nyou can venture into the labyrinth. To turn the \nflashlight on and off, press \"q\". You will only be \nable to see one square, but if you find the light \nswitch in the middle of the labyrinth, you \nwill be able to see everything.",
                                "light switch":"Click the light switch to permanently turn \non the light in the labyrinth. Now, you won\'t need \nto hold the flashlight in order to see.",
                                "gem":"Congratulations, you found your first gem. \nCollect at least five in order to access the final room \nand attain immortality. You'll need to bring them to\nthe room at the bottom of the map to use them.\nKeep an eye on the clock though, and make sure\nthat time doesn\'t run out first!"}

        # string of the final level text that pops up after killing all monsters
        self.final_level = "Congrats! You have killed all the monsters.\nThe key in the chest of the final monster's room\nunlocks a room at the bottom of the map. Enter\nthis room and place your 5 collected gems inside\nto unlock the final door to get the elixir of immortality!"
        
        # string of the text that appears in the end screen when the player achieves immortality i.e. beats the game
        self.win_end_screen = "Congratulations! You achieved immortality."

        # string of the text that appears when the player dies
        self.lose_end_screen = "You died."


    def story_display(self, background, text,next = "[Press enter or click to continue]"):

        '''
        story_display displays the story text
        
        Parameters (Required):
            background - game background object that the story is on
            text - text to be displayed 

        Parameters (optional):
            next - message that displays, telling the player what to do next; by default, string: "[Press enter or click to continue]"
        '''

        # sets the text to the text to be displayed plus the next message
        self.text = text + "\n\n" + next

        # calls the place function, placing the story box onto the screen
        super().place(background, text_color=(0,0,0))


class ErrorBox(TextBox):
    '''
    The ErrorBox() text is a subclass of TextBox() that represents the error pop up text boxes
    '''
    def __init__(self, x, y, width, height, text_size=25):
        '''
        __init__() intializes the error box

        Parameters (required):
            x - x coordinate of the text box with respect to the screen
            y - y coordinate of the text box with respect to the screen
            width - width of the text box
            height - height of the text box

        Parameters (optional):
            text_size - font size of text; by default, set to 25
        '''

        # initializes super class TextBox
        super().__init__(x,y,width,height,text_size=text_size)
        
        self.count = 0      # number of frames it has appeared on screen
        self.viewable = 240 # total number of frames it will appear on screen for 
    
    def update_text(self, new_text):
        '''
        update_text() updates the error text

        Parameters (required):
            new_text - new text that the text should be updated to
        '''

        #updates the text to new text
        self.text = new_text
    
    def place(self, background, game):
        '''
        place() displays the error text

        Parameters (required):
            background - game background object that the error message is located on
            game - game object that the error message is located within
        '''

        # places error message on screen with text color red
        super().place(background, text_color=(200,0,0))
        self.count += 1
        
        # if the number of frames that the error message has been displayed is greater than the number
        # of frames that it should be viewable
        if self.count > self.viewable:
            # no more erro, resets counter
            game.error = False
            self.count = 0
            game.prev_click = None