'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: menu.py
Purpose: This file contains the Menu class that displays all the items a user is carrying.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
import pandas as pd
from text import *
from weapons import *

#accesses csv file that stores the stats of all the weapons
weapon_stats = pd.read_csv('./stats/weapons.csv')
weapon_stats.index = weapon_stats["weapons"]
weapon_stats.drop(columns=["weapons"],inplace=True)
#data points can be accessed via weapon_stats[category, weapon_nick]
# for example, weapon_stats["lion"]["sword"] gives the damage the sword does against the lion

default_sfx = 0     # defines the default sfx, used for everything except instrument

# list of enemies to iterate through
enemies = ["lion","cerberus","hydra","boar","golden_deer","cattle"]

class Menu(pygame.surface.Surface):
    '''
    The Menu() class contains all items in a passed in list, typically the items that the player is holding.
    It is a subclass of the pygame Surface class.
    '''
    
    def __init__(self, x, y, title, menu_items, width, height, padding=20):
        '''
        __init__() initializes the Menu
        
        Parameters (required):
            x - x coordinate of menu
            y - y coordinate of menu
            title - menu title
            menu_items - list of slides for items/weapons and their corresponding stats windows
            width - width of menu
            height - height of menu
        
        Parameters (optional):
            padding - padding between slides in the menu
        '''
        
        # x and y coordinates of menu
        self.x = x
        self.y = y
        
        # width and height of menu
        self.width = width
        self.height = height
        
        # initializes a surface that can be transparent
        super().__init__([self.width, self.height], pygame.SRCALPHA)
        
        # gets all item slides and stats windows
        self.slides = []
        self.sub_windows = []
        for slide, stat_window in menu_items:
            self.slides.append(slide)
            self.sub_windows.append(stat_window)

        self.padding = padding  # padding between slides
        self.title_text = title  # title of menu
        
        self.selected = None  # the selected item; the stats window is displayed for this item
        self.redraw = True  # whetehr the menu needs to be redrawn or not

    def build(self):
        '''
        build() creates the menu with the title and items without drawing it on screen yet
        '''
        
        # background color of menu
        self.fill((205, 127, 50))
        
        # creates main menu title
        title = TextBox(self.padding+10, self.padding+10, self.width-2*self.padding, 80, text_size=55, text=self.title_text)
        title.place(self, text_color=(0,0,0))
        
        # title boxes for the menu, informing the user where each piece of information is
        menu_titles = pygame.surface.Surface([self.width-self.padding*2, 40], pygame.SRCALPHA)
        text = TextBox(self.padding,0,self.width-self.padding*4,40,text_size=30,text=' #         Item          Name')
        text.place(menu_titles, text_color=(0,0,0))
        self.blit(menu_titles, [self.padding, 95])
        
        # creates the item container below the title and sets its background color (slightly lighter than the main menu color)
        self.item_surface = pygame.surface.Surface([self.width-self.padding*2, self.height-200])
        self.item_surface.fill((225, 193, 110))
        
        # draws all slides in the item surface
        self.draw_all_items()
        
        # draws the item surface in the menu
        self.blit(self.item_surface, [self.padding, 130])
        
        # instructional text box at the bottom of the screen
        text = TextBox(self.padding, 130+self.height-200+12, self.width-self.padding*2, 30, text_size=25, text="Click the number key corresponding to a weapon\nto select it", padding=0)
        text.place(self, text_color=(0,0,0))
    
    def draw_all_items(self):
        '''
        draw_all_items() draws all items in the item container with the specified padding between slides
        '''
        
        # starting x and y values with respect to item container
        x = 0
        y = self.padding//2
        
        # loops through slides list and draws each slide below the previous
        for slide in self.slides:
            if self.selected == slide.val - 1:
                slide.displaying_stats = True
            else:
                slide.displaying_stats = False

            # creates the slide
            slide.make()
            
            # adds the slide to the item surface at the x and y locations
            self.item_surface.blit(slide, [x,y])
            
            # updates the item's x and y values with respect to the pygame window
            slide.x = self.x + self.padding + x
            slide.y = self.y + 130 + y
            
            # modifies the y height for the next element to be drawn
            y += slide.height + self.padding
    
    def place(self, screen):
        '''
        place() draws the menu but does not modify its contents
        
        Parameters (required)
            screen - where to draw the menu
        '''
        
        # draws the menu on the screen
        screen.blit(self, [self.x, self.y])
        
        # draws the sub window corresponding to the clicked on slide in the menu
        if self.selected != None:
            self.sub_windows[self.selected].place(screen)

class WeaponSlide(pygame.surface.Surface):
    '''
    The WeaponSlide() class represents a 'slide'/rectangle showing information about a given item.
    It is a subclass of the pygame Surface class.
    '''
    
    def __init__(self, nick, image, width, height, val, bg_color=(225, 193, 110)):
        '''
        __init__() initializes the slide
        
        Parameters (required):
            nick - slide nickname
            image - image to be shown on slide
            width - width of slide
            height - height of slide
            val - id of slide in menu
        
        Parameters (optional):
            bg_color - default slide background color; set by default to a medium dark brown
        '''
        
        self.nick = nick  # slide nickname
        self.image = image  # image to be shown on slide
        
        # x and y coordinates of slide; both are 0 by default and are updated as the slide is drawn
        self.x = 0
        self.y = 0
        
        # slide width and height
        self.width = width
        self.height = height
        
        # initializes slide as a surface
        super().__init__([self.width, self.height], pygame.SRCALPHA)
        
        self.padding = 5  # padding between items in slide
        self.val = val  # number of the slide in the menu
        self.bg_color = bg_color  # background color of slide
        self.stats_btn = None  # triangle showing whether stats are being displayed for the item or not
        self.displaying_stats = False  # whether stats are being displayed for the slide or not
        
    def make(self):
        '''
        make() creates the slide for the item
        '''
        
        # fills the background of the slide with the background color
        self.fill(self.bg_color)
        
        # creates and draws the textbox for the number of the item in the menu
        num = TextBox(10, 10, 40, 40, text_size=70, text=" " + str(self.val) + " ")
        num.place(self, text_color=(50, 0, 0))
        
        # draws the image representing the list item
        self.blit(self.image, [60+self.padding*6, self.padding])
        
        # creates and draws the textbox for the name of the item in the menu
        # formatting includes replacing dashes with spaces in the item nickname
        formatted_list = self.nick.split('-')
        formatted_text = formatted_list[0]
        for x in formatted_list[1:]:
            formatted_text += ' ' + x
        name = TextBox(130+self.padding*12, 20, 200, 40, text_size=40, text=formatted_text)
        name.place(self, text_color=(50, 0, 0))
        
        # if the stats for the item should be displayed, draws the arrow pointing towards them
        if self.displaying_stats:
            # gets and draws the arrow image
            self.stats_btn = loadImage('images/open_stats.png')
            self.blit(self.stats_btn, [name.x+name.width+self.padding*4, self.padding+20])
    
    def hover(self):
        '''
        hover() checks if the user is hovering over the slide
        
        Returns:
            Boolean - True if the slide is being hovered over; False if it is not
        '''
        
        # compares mouse position to slide position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_y > 100 and (mouse_x > self.x and mouse_x <= self.x + self.width) and (mouse_y > self.y and mouse_y <= self.y + self.height):
            return True
        return False

    def detectClick(self, events):
        '''
        detectClick() checks if the user has clicked the slide
        
        Parameter (required):
            events - pygame events occured in the game
        
        Returns:
            Boolean - True if clicked on; False if not
        '''
        
        # compares location of potential mouse click to location of slide
        for event in events:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN and (mouse_x > self.x and mouse_x <= self.x + self.width) and (mouse_y > self.y and mouse_y <= self.y + self.height):
                return True
        
        return False

class Stats(pygame.surface.Surface):
    '''
    The Stats() class represents a statistic window displaying how many damage points each item does to each monster.
    It is a subclass of the pygame Surface class.
    '''
    
    def __init__(self, nick, width=300, height=300, x=600, y=200, padding=20):
        '''
        __init__() initializes the stats window
        
        Parameters (required):
            nick - stats nickname; corresponds to its slide's nickname and the item it displays stats for
        
        Parameters (optional):
            width - width of stats window; set to 300 by default
            height - height of stats window; set to 300 by default
            x - x coordinate of stats window; set to 600 by default
            y - y coordinate of stats window; set to 200 by default
            padding - padding around text; set to 20 by default
        '''
        
        self.nick = nick  # stats window nickname
        
        # stats window width and height
        self.width = width
        self.height = height
        
        # initializes window as a surface
        super().__init__([self.width, self.height], pygame.SRCALPHA)
        
        # x and y coordinates of window
        self.x = x
        self.y = y
        
        # padding around text in window
        self.padding = padding
        
        # stats dictionary
        self.stats = {}
        for enemy in enemies:
            self.stats[enemy] = weapon_stats[enemy][self.nick]
     
    def get_stats(self):
        '''
        get_stats() retrieves all of the statistics for the item
        
        Returns:
            stats - string of all monsters and their corresponding item damage points'''
        
        stats = ""
        
        for (enemy, value) in self.stats.items():
            # replaces underscores in monster names with spaces and capitalizes first letters of names
            formatted_name_list = enemy.split('_')
            formatted_name = formatted_name_list[0].capitalize()
            for x in formatted_name_list[1:]:
                formatted_name += " " + x.capitalize()
            
            # adds the monster's stats to stats string
            stats += "  {e}: {v}\n".format(e=formatted_name, v=value)
        
        return stats
    
    def place(self, screen):
        '''
        place() draws the stats window on screen
        
        Parameter (required):
            screen - where the text box should be drawn
        '''
        
        # medium dark background background color
        self.fill((205, 127, 50))
        
        # stats window title
        titles = TextBox(self.padding+5, self.padding, self.width-5-self.padding*2, 50, text_size=35, text='Damage Points to\nMonsters', padding=-5)
        titles.place(self, text_color=(0,0,0))
        
        # stats text box
        stats = self.get_stats()
        text = TextBox(self.padding, 70+self.padding, self.width-2*self.padding, self.height-70-self.padding*2, text=stats, top_padding=10)
        text.place(self, background_color=(225, 193, 110), text_color=(50,0,0))
        
        # draws stats window to screen
        screen.blit(self, [self.x,self.y])