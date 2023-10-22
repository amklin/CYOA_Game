'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: game.py
Purpose: This file contains the Game class that implements the game functionality.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
from background import *
from player import *
from weapons import *
from monster import *
from plant import *
from additional_func import *
from health_bars import *
from text import *
from button import *
from menu import *
import pygame,sys

class Game():
    '''
    The Game() class represents the game that the player plays, all items in it, and allows for user interaction.
    '''
    
    def __init__(self, screen, player, weapons, monsters, keys, gems, plants, buttons, text, story, chests, items_list, potion, rooms, level=-1, frame=0, tutorial=True, pause=False):
        '''
        __init__() initializes the Game
        
        Parameters (required):
            screen - the labyrinth Background object of the game
            player - the player object
            weapons - a list of all weapons that may be placed into the labyrinth
            monsters - a list of all monsters that the player will face
            keys - a list of all keys that open doors
            gems - a list of all gems to be placed in the labyrinth
            plants - a list of all plants to be placed in the labyrinth
            buttons - a list of all buttons to be drawn on screen (not including background buttons)
            text - instructional text in the corner of the screen
            story - Story object representing all storyline and tutorial text
            chests - list of all chest objects to be placed in the monsters' rooms
            items_list - list of items the player is holding or has in their backpack
            postion - elixir of immortality that the player picks up/drinks at the end of the game
            rooms - tuple of list of horizontal rooms and list of vertical rooms to be placed in the game
            
        Parameters (optional):
            level - starting level of game; by default, set to -1 (tutorial level)
            frame - starting frame number of game; by default, set to 0
            tutorial - Boolean representing whether the game starts off in tutorial; set to True if yes; set to False if no; by default, set to True
            pause - Boolean representing whether the game starts off paused or not; by default, set to False
            extend - Boolean representing whether the player's weapon starts exended; by default, set to False 
        '''
        
        self.screen = screen  # main screen of the game
        self.frame = frame  # current frame number
        self.buttons = buttons  # list of all buttons
        self.labyrinth_lights_on = False  # whether or not the labyrinth should be fully visible
        self.pause = pause  # whether the game is paused or not
        
        # characters
        self.player = player  # player object
        self.monsters = monsters  # list of all monsters
        self.active_monster = None  # monster for current level, initially set to None
        
        # items
        self.weapons = weapons  # list of all items the player can hold (except keys)
        self.available_weapons = []  # list of available items the player can hold (i.e., all items the player has 'found'), depends on level
        self.keys = keys  # list of all keys
        self.potion = potion
        self.items_list = items_list  # list of all items the player is holding
        self.extend = False  # whether the item the player is holding should be extended

        # background interactable elements
        self.plants = plants  # list of all plants
        self.chests = chests   # list of all chests
        self.rooms = rooms  # horizontal and vertical rooms to be placed in the game
        
        # story and text
        pygame.font.init()
        self.font = pygame.font.SysFont('freesansbold.ttf', 50)
        self.text = text  # text that should be displayed on screen
        self.story = story  # storyline object
        self.instruction_text_num = 0   # tracks what slide of the instructions screen is present
        self.final_story_instructions = False  # tracks if final story instructions should be displayed; this is tracked to ensure it only happens once
        
        # tracks whether you have encountered these objects for the first time yet, and if not, pops up with instructions
        self.introductions = {"plant":False,
                                "key":False,
                                "chest":False,
                                "flashlight":False,
                                "light switch":False,
                                "gem":False}
        
        # levels
        self.level = level  # current level number
        self.max_levels = len(self.monsters)  # total number of levels, determined based on the number of monsters
        self.tutorial = tutorial # whether the game is in the tutorial or not
        self.complete = False  # if the game is complete; if the last level has been beaten
        
        # health bars
        self.player_health_bar = None  # health bar for player
        self.monster_health_bar = None  # health bar for the active monster
        
        # menu
        self.menu = None  # menu for showing items the player is holding
        self.menu_pause = False  # whether the game was paused to display the menu or not

        # counters
        self.flashlight_lag = 0  # lag for turning flashlight on/off
        self.damage_lag = 0  # lag for doing damage to monster
        self.items_list_lag = 0  # lag for looping through items list
        self.c = 0  # animation frame counter
        
        # initializes clock for game
        self.clock = pygame.time.Clock()

        # gem and gem countdown
        self.gems = gems  # list of all gems
        self.collected_gems = 0  # tracks how many gems the player has collected so far
        self.time_left = 8*7200  # time left until gems disappear; 8 minutes
        self.fps = 120  # frame rate of game; 120 fps
        self.countdown = pygame.surface.Surface([95,50], pygame.SRCALPHA)  # countdown object to be drawn
        
        # retrieves the flashlight out of the weapons list
        for weapon in weapons:
            if weapon.nick == "flashlight":
                self.flashlight = weapon
        
        # errors
        self.error = False  # whether error message shoudl be displayed
        self.error_msg = None  # error message
        self.bp_error_type = None  # type of error if occuring with backpack items
        
        # pygame events (e.g., key clicks)
        self.events = []
    
    
    ## Game Setup ##
    
    def setup(self):
        '''
        setup() sets up all items needed for the first level of the game
        '''
        
        # retrieves the monster and available weapons for the first level
        self.levels()
        
        # draws player
        self.player.place(self.screen, 0)

        # creates and places walls
        self.screen.place_walls(hor_rooms=self.rooms[0], vert_rooms=self.rooms[1], corridor_room=self.rooms[1][0])
        self.screen.make_doors()
        
        # places the gems the player must collect at random locations in the labyrinth
        self.random_gem_locations()
        for gem in self.gems:
            self.available_weapons.append(gem)

        # places all items the player possesses is not holding into the background
        for weapon in self.available_weapons:
            if self.player.held_item != weapon and weapon.loc != "chest":
                self.screen.background_obj.append(weapon)
        
        # adds the player's starting weapon to the item list
        self.items_list.append(self.player.held_item)
        
        # adds the potion to available weapons and to the background
        self.available_weapons.append(self.potion)
        self.screen.background_obj.append(self.potion)
        
        # places all plants into background
        for plant in self.plants:
            self.screen.background_obj.append(plant)

        # places all monsters that are not active into the background
        for monster in self.monsters:
            if monster != self.active_monster:
                self.screen.background_obj.append(monster)
        
        # places all chests into the background
        for chest in self.chests:
            self.screen.background_obj.append(chest)

        # background map image
        self.screen.set_background_image()
        
        # creates player and monster health bars
        self.player_health_bar = HealthBar(self.player.health, 20, 20, 'You')
        self.monster_health_bar = HealthBar(self.active_monster.health, 20, 60, "Monster")
        
        # places the player and monster health bars on screen
        self.player_health_bar.place(self.screen.screen)
        self.monster_health_bar.place(self.screen.screen)
        
        # retrieves the grid row and column positions of the monster
        self.active_monster.get_new_loc(self.screen)
        
        # creates the error message box
        self.error_msg = ErrorBox(200,750,400,100)
    
    
    ## Main Gameplay ##
    
    def gameplay(self, tutorial=False):
        '''
        gameplay() implements all main game functionality
        
        Parameter (optional):
            tutorial - Boolean representing whether the game is being player in tutorial or real game mode; default value is False
        '''
        
        # if the key 'space' is pressed, the item the player is holding should be extended
        # this means an item is being used
        if keyPressed("space"):
            self.extend = True
        else:
            self.extend = False
        
        # if 'a' is pressed, displays a menu of the items the player possesses in their backpack
        if keyPressed('a'):
            self.pause = True
            self.menu_pause = True
            self.make_menu()
        
        self.manipulate_backpack()  # allows the player to drop items, pick up items, cycle through backpack items, or add items to backpack
        self.move_player()  # moves player's location in the map
        self.item_interaction()  # allows player to use certain items
        
        # checks for the correct number of gems collected at final level
        if not tutorial and self.level == self.max_levels and self.screen.door_list[7].frame != 1:
            # gets the gems that have been collected and adds them to a list
            collected = []
            for gem in self.gems:
                if gem.times_picked_up > 0:
                    collected.append(gem)
            
            # if the player has retrieved 5 gems, opens the last room for them to enter into
            self.screen.door_list[7].open_with_items(collected, 5, self)
        
        
        # draws all chests on screen
        for chest in self.chests:
            chest.place(self.screen)
        
        # draws the player in the center of the screen
        self.place_player()
        
        # toggles lights in the labyrinth if the light switch is clicked
        if self.screen.light_switch.detectClick(self.screen, self.events):
            # lights up labyrinth if it was previously dark
            if self.screen.light_switch.frame == 1:
                self.labyrinth_lights_on = True
            
            # darkens labyrinth if it was previously light
            elif self.screen.light_switch.frame == 0:
                self.labyrinth_lights_on = False
            
            self.screen.set_background_image()  # redraws background
        
        # if the last level hasn't been reached and if the player isn't in the tutorial, calls monster code
        if not tutorial and self.level < self.max_levels:
            self.monster_interaction()  # allows player to kill monster
            
            if self.active_monster != None:
                self.place_monster()  # draws monster on screen
        
        # draws dark parts of labyrinth
        self.darken_labyrinth()
        
        # updates player and monster health bars if the last level hasn't been reached and if the player isn't in the tutorial
        if not tutorial and self.level < self.max_levels:
            self.update_health_bars()
        
        # loops through and draws all buttons if the player isn't in the tutorial
        if not tutorial:
            for button in self.buttons:
                button.place()  # draws button on screen
                
                if button.detectClick(self.events):
                    # if the pause button is clicked, the game is paused
                    if button.nick == "pause":
                        self.pause = True
        
        # places error message, if any, on screen
        if self.error == True:
            self.error_msg.place(self.screen.screen, self)

        # calls instructional text box and intro screen only if not in tutorial
        if not tutorial:
            # sets & updates new text if certain items are held
            self.text_update()
            
            # introduces new items if certain conditions are met
            self.introduction_screen()

        # displays final story if needed
        if self.final_story_instructions:
            self.story_display(self.story.final_level)
            self.final_story_instructions = False  # resets final story variable to ensure final story isn't displayed again
        
        # if the 'esc' key is pressed, exits the game
        if (keyPressed("esc")):
            pygame.quit()
            sys.exit()
    
    
    ## Storyline Functions ##
    
    def story_screen(self):
        '''
        story_screen() loops through story text blocks and displays them on screen
        '''
        
        for text in self.story.story_text:
            # retrieves pygame events
            self.events = pygame.event.get()
            
            # displays new story text
            self.story_display(text=text)
        
    def story_display(self,text="", next = None):
        '''
        story_display() displays the specified text
        
        Parameters (optional):
            text - string of the text to be displayed; default is empty string
            next - if there is a custom next message to be used; default is None
        '''
        
        # displays the specified text until the player presses enter or clicks
        while not enter_or_click(self.events):
            # retrieves pygame events
            self.events = pygame.event.get()
            
            if next:    # if there is a custom next message, uses that
                self.story.story_display(self.screen.screen,text, next=next)
            else:       # if there is not a custom next messsage, uses the default message
                self.story.story_display(self.screen.screen,text)
            
            # if the 'esc' key is pressed, exits the game
            if (keyPressed("esc")):
                pygame.quit()
                sys.exit()
            
            # updates screen
            pygame.display.update()
            self.tick(120, self.events)

    def instruction_screen(self):
        '''
        instruction_screen() brings player through tutorial prior to starting the game
        '''
        
        # places tutorial text at the top of the screen
        self.story.y = 0
        
        for text in self.story.instruction_text:
            # retrieves pygame events
            self.events = pygame.event.get()
            
            # waits until the player presses enter or clicks the screen before moving to the next instructional text
            while not enter_or_click(self.events):
                # retrieves pygame events
                self.events = pygame.event.get()
                
                # gameplays in tutorial mode
                self.gameplay(tutorial=True)
                
                # displays story info screens
                self.story.story_display(self.screen.screen,text)

                # displays menu if needed
                while self.pause:
                    # gets pygame events
                    self.events = pygame.event.get()
                    
                    # displays menu
                    self.menu_display()

                    # updates screen
                    pygame.display.update()
                    self.tick(120, self.events)

                # updates screen
                pygame.display.update()
                self.tick(120, self.events)

        # once out of the tutorial, begins the game by going to the first level and setting the first monster free
        self.level = 0
        self.screen.door_list[self.level].open_door()
        self.levels()  # gets all level materials needed

    def introduction_screen(self):
        '''
        introduction_screen() displays certain instructions on te first encounter with a particular item
        '''
        
        # first plant encounter
        if not self.introductions['plant']:
            for plant in self.plants:
                self.check_introduce (plant, 'plant')
        
        # first key encounter
        if not self.introductions['key']:
            for key in self.keys:
                self.check_introduce (key, 'key')

        # first chest encounter
        if not self.introductions['chest']:
            for chest in self.chests:
                self.check_introduce (chest, 'chest')

        # first flashlight encounter
        if not self.introductions['flashlight']:
            if self.player.held_item != None and self.player.held_item.nick == 'flashlight':
                self.introduce ('flashlight')
        
        # first light switch encounter
        if not self.introductions['light switch']:
            if self.player.pos_col == 5 and self.player.pos_row == 5:
                self.introduce('light switch')

        # first gem encounter
        if not self.introductions['gem']:
            for gem in self.gems:
                self.check_introduce(gem, 'gem')

    def check_introduce (self, obj, str):
        '''
        check_introduce() determines if an item is being encountered for the first time and, if so, displays instructional text for the item
        
        Parameters (required):
            obj - the object being encountered
            str - a string representing the object's name; corresponds to name in introduction dictionary
        '''
        
        # gets object location before introducing
        self.screen.get_new_loc(obj)
        
        # if the player and object are in the same area, introduces the object
        if obj.pos_col == self.player.pos_col and obj.pos_row == self.player.pos_row:   # checks if they are in the same row/col
            self.introduce(str)  # displays introduction screen
    
    def introduce (self,str):
        '''
        introduce() displays instructional text for an item on its first encounter
        
        Parameter (required):
            str - a string representing the object's name; corresponds to name in introduction dictionary
        '''
        
        # pauses game and displays instructions
        self.pause = True
        self.story_display(self.story.introduction_text[str])

        # once the player has moved on, unpauses the game and sets the item to encountered (instructional text won't be displayed on the next encounter)
        self.pause = False
        self.introductions[str] = True
    
    
    ## Menu Functions ##
    
    def make_menu(self):
        '''
        make_menu() creates the menu without actually drawing (so that the menu isn't remade during every frame
        '''
        
        # list of items in menu
        menu_items = []
        
        # cycles through all items in the player's item list (i.e., backpack)
        for i in range(len(self.items_list)):
            # obtains each item
            weapon = self.items_list[i]
            
            # creates the menu slide and corresponding stats window for each item in the list
            slide = WeaponSlide(weapon.nick, weapon.images[1], 460, 70, i+1)
            stats_window = Stats(weapon.nick)
            
            # adds the slide and stats window to the menu list
            menu_items.append((slide, stats_window))
        
        # creates a menu that will be based on the menu list passed in
        self.menu = Menu(50, 50, 'Backpack Menu', menu_items, 500, 700)
    
    def menu_display(self):
        '''
        menu_display() draws the menu on screen
        '''
        
        # recreates menu and menu items if needed
        if self.menu.redraw == True:
            self.menu.build()
            self.menu.redraw = False
        
        # draws the menu on the screen
        self.menu.place(self.screen.screen)
    
        # checks if any slide in the menu is being hovered over or clicked
        for slide in self.menu.slides:
            # if it is being hovered over
            if slide.hover():
                # lightens the color of the slide
                slide.bg_color = (234, 221, 202)
                self.menu.redraw = True
                
                # if it is clicked, prompts the menu to begin displaying the stats for the particular item
                if slide.detectClick(self.events):
                    self.menu.selected = slide.val - 1
            
            # if it is not being hovered over but was recently hovered over
            elif slide.bg_color == (234, 221, 202):
                # resets color to the default darker background
                slide.bg_color = (225, 193, 110)
                self.menu.redraw = True
        
        for i in range(0, len(self.menu.slides)):
            if keyPressed(str(i+1)):
                self.pause = False
                self.menu_pause = False
                
                if self.player.held_item != None:
                    self.player.held_item.place_in_backpack(self.player)
                
                self.items_list[i].select_from_backpack(self.player)
        
        # close menu of items
        if keyPressed('s'):
            self.pause = False
            self.menu_pause = False
            
            # changes pause button frame back to default
            for button in self.buttons:
                if button.nick == 'pause' and button.frame == 1:
                    button.frame -= 1
    
    
    ## Item Interaction and Labyrinth ##
    
    def manipulate_backpack(self):
        '''
        manipulate_backpack() allows the player to pick up items, drop items, add items to backpack, and cycle through backpack items
        '''
        
        # if the player is holding an item and presses 'f', the item is dropped
        if self.player.held_item != None and keyPressed("f"):
            # sets backpack error type
            self.bp_error_type = 'f'
            
            # drops the item into the background and redraws the player without it
            self.player.held_item.drop(self.screen, self.player)
            self.player.place(self.screen, self.frame)
        
        # if the player isn't holding an item but presses 'f', displays error message that there is nothing to drop
        elif keyPressed('f') and self.player.held_item == None and self.bp_error_type != 'f':
            # sets backpack error type
            self.bp_error_type = 'f'
            
            # sets error message
            self.error = True
            self.error_msg.update_text("There is nothing to drop.")
        
        # resets backpack error type if 'f' is unpressed
        elif not keyPressed('f') and self.bp_error_type == 'f':
            self.bp_error_type = None
        
        # loops through all weapons and determines which one, if any, can be picked up
        can_pick_up = None
        for weapon in self.available_weapons:
            # if the player is not holding any items, the item that they are on top of (if any) is an item that can be picked up
            if weapon.touching(self.player, self.screen) and self.player.held_item == None and weapon.wielder == None and weapon not in self.items_list and len(self.items_list) < 5:
                can_pick_up = weapon
                break  # if one item can be picked up, there is no need to look for others
        
        if can_pick_up and self.bp_error_type != 'd_chest':
            if keyPressed("d"):  # if they player presses 'd' while an object can be picked up
                # picks up the item from the background and places it in the player's hand
                can_pick_up.pick_up(self.screen, self.player)
                self.player.place(self.screen, self.frame)
                self.bp_error_type = 'd'
                
                # if the gem is picked up for the first time, adds 1 to the number of collected gems
                if weapon.nick == 'gem' and weapon.times_picked_up == 1:
                    self.collected_gems += 1
                
                # if the potion is picked up, marks the game as complete
                if weapon.nick == 'potion':
                    self.complete = True
        
        # if there is nothing the player can pick up but the player clicked 'd', detemines and displays the error
        elif keyPressed('d') and self.bp_error_type != 'd':
            # if the player is already holding something, informs them that they can only hold 1 item at a time
            if self.player.held_item != None:
                self.bp_error_type = 'd'
                self.error = True
                self.error_msg.update_text("You can only hold one item at a time.")
            
            # if there are 5 items in the backpack already, informs them that they can't pick up any more
            elif len(self.items_list) >= 5:
                self.bp_error_type = 'd'
                self.error = True
                self.error_msg.update_text("You can't carry more than 5 items.")
            
            # if the player isn't standing on anything that can be picked up, informs the player that nothing can be picked up
            else:
                self.bp_error_type = 'd'
                self.error = True
                self.error_msg.update_text("There is nothing to pick up.")
            
        # resets backpack error type if 'd' is unpressed
        elif not keyPressed('d') and (self.bp_error_type == 'd' or self.bp_error_type == 'd_chest'):
            self.bp_error_type = None

        # place in backpack
        if self.player.held_item != None and keyPressed("e") and self.bp_error_type != 'e':
            self.player.held_item.place_in_backpack(self.player)
            self.bp_error_type = 'e'
        elif keyPressed('e') and self.player.held_item == None and self.bp_error_type != 'e':  # if the player isn't holding anything they can put in their backpack
            self.error = True
            self.error_msg.update_text("There is nothing to place in your backpack.")
            self.bp_error_type = 'e'
        elif not keyPressed('e') and self.bp_error_type == 'e':
            self.bp_error_type = None
        
        # cycles through backpack items if the player has at least 1 item in the items_list
        if keyPressed("r") and len(self.items_list) > 0:
            # implements a lag so that the items will be cycled through automatically every 40 frames
            
            # increments counter
            self.items_list_lag += 1
            
            # selects item
            if self.items_list_lag == 1:
                # if the player is holding a weapon, places that weapon into the backpack and gets its index location in the items_list
                if self.player.held_item != None:
                    i = self.items_list.index(self.player.held_item)
                    self.items_list[i].place_in_backpack(self.player)
                # if the player isn't holding anything, the index is 0
                else:
                    i = 0
                
                # increments the index  by 1 if there is more than 1 element and makes it 0 if there is only 1 element
                if i < (len(self.items_list) - 1):
                    i += 1
                else:
                    i = 0
                
                # selects the next element from the backpack and redraws the player with it
                self.items_list[i].select_from_backpack(self.player)
                self.player.place(self.screen, self.frame)
                
                self.bp_error_type = 'r'
            
            # resets counter after 40 frames
            if self.items_list_lag == 40:
                self.items_list_lag = 0
                        
        # if there is nothing in the player's backpack, informs them of this
        elif keyPressed('r') and len(self.items_list) == 0 and self.bp_error_type != 'r':
            self.error = True
            self.error_msg.update_text("There is nothing in your backpack.")
            self.bp_error_type = 'r'
        
        # resets the counter if not pressed
        elif not keyPressed('r') and self.bp_error_type == 'r':
            self.items_list_lag = 0
            self.bp_error_type = None
    
    def item_interaction(self):
        '''
        item_interaction() allows for certain actions to be taken if the player is using certain objects
        '''
        
        ## flashlight functionality ##
        
        # if the player is holding the flashlight and pressed 'q', the flashlight is turned off if it's on and on if it's off
        # state is changed either every 80 frames or every time the flashlight is reextended
        if keyPressed('q') and self.player.held_item != None and self.player.held_item.nick == 'flashlight':
            # implements a lag so that, if the 'q' key is held, the flashlight state is changed every 80 frames
            
            # increments lag counter
            self.flashlight_lag += 1
            
            # changes flashlight state
            if self.flashlight_lag == 1:
                self.player.held_item.change_state()
            
            # resets lag counter after 80 frames
            if self.flashlight_lag == 80:
                self.flashlight_lag = 0
        
        # if the player presses 'q' while holding another item, informs them that they can only use that functionality with the flashlight
        elif keyPressed('q') and self.player.held_item != None and self.player.held_item.nick != 'flashlight':  # if the player is holding something that isn't a flashlight
            self.error = True
            self.error_msg.update_text('You can only turn a flashlight on/off.')
        
        # if 'q' is not pressed, resets the counter for turning flashlight on/off
        elif not keyPressed('q'):
            self.flashlight_lag = 0
        
        # turns off the flashlight if the player is not holding it
        if self.player.held_item != self.flashlight:
            self.flashlight.turn_off() 
        
        
        ## chest functionality ##
        
        # loops through all chests
        for chest in self.chests:
            # if 'w' is pressed, opens a closed chest and closes an opened chest
            # chest state is changed either every 40 frames or each time 'w' is pressed
            if keyPressed('w'):
                # implements a lag so that the chest state is changed every 40 frames if the player holds 'w'
                
                # increments lag counter
                chest.lag += 1
                
                # changes the chest state if the player is touching the chest
                if chest.lag == 1:
                    chest.toggle(self.player, self.screen)

                # resets lag every 40 frames
                if chest.lag == 40:
                    chest.lag = 0
            
            # resets the chest lag if 'w' is not pressed
            else:
                chest.lag = 0
            
            # allows the player to take an item out of an open, not empty chest if they aren't holding anything
            if keyPressed('d') and self.player.held_item == None and chest.content != None and chest.content.wielder == None and chest.content not in self.items_list and len(self.items_list) < 5:
                chest.pick_up_object(self.player,self.screen)
                self.bg_error_type = 'd_chest'
                self.error_msg.update_text("")
        
        
        ## shovel functionality ##
        
        # loops through all of the plants
        for plant in self.plants:
            # digs up a plant if a shovel is being extended and is in contact with the plant
            if self.player.held_item != None and self.player.held_item.nick == 'shovel' and self.extend:
                # digs if the plant is not fully dug up, either every 40 frames or every time the shovel is reextended
                if plant.frame != 4:
                    # slows down speed of digging to every 40 frames if the shovel held extended
                    
                    # digs up plant
                    if plant.dig_lag == 1:
                        self.player.held_item.dig(plant, self.screen)
                    
                    # increments counter and resets counter after 40 frames
                    plant.dig_lag += 1
                    if plant.dig_lag == 40:
                        plant.dig_lag = 0
                
                # if the plant is fully dug up, removes it from the list of plants
                if plant.frame == 4:
                    self.plants.remove(plant)
            
            # if the player tries to dig with an item that isn't a shovel, informs them that they can only dig with a shovel
            elif self.extend and self.player.held_item != None and self.player.held_item.touching(plant, self.screen):
                self.error = True
                self.error_msg.update_text("You can only dig with a shovel.")
        
        # resets digging lag if the weapon is not extended
        if not self.extend:
            for plant in self.plants:
                plant.dig_lag = 0
        
        
        ## key functionality ##
        
        # loops through list of all doors
        for door in self.screen.door_list:
            # opens a door if the key that matches the door is extended and is touching the door
            if self.extend and self.player.held_item != None and self.player.held_item.touching(door, self.screen) and door.frame == 0:
                if self.player.held_item.nick == 'key':
                    # opens door if the key id and door index match
                    if self.player.held_item.id == self.screen.door_list.index(door)+1:
                        door.open_door()
                    
                    # if the key id and door index do not match, informs the player that the wrong key was used
                    else:
                        self.error = True
                        self.error_msg.update_text("Wrong key. Hint: door and key colors should match.")
                
                # if the player tries to unlock a door with an item that isn't a key, informs them that doors can only be opened with keys
                else:
                    self.error = True
                    self.error_msg.update_text("You can only open a door with a key.")
    
    def darken_labyrinth(self):
        '''
        darken_labyrinth() places squares of darkness onto the labyrinth to decrease the player's visibility if the lights are off
        '''
        
        # if the flashlight is on and the player is inside the labyrinth, but the light switch has not been clicked (i.e., lights are off), lights up only the grid square the player is in
        if self.labyrinth_lights_on != True and self.flashlight.state == True and (self.player.pos_row > 1 and self.player.pos_row < 9) and (self.player.pos_col > 1 and self.player.pos_col < 9):
            self.screen.place_dark(self.player)  # darkens all labyrinth grid squares except for the player's square

        # if the light switch has not been clicked and either the player is not in the labyrinth or the flashlight is not turned on, the labyrinth is fully dark
        elif self.labyrinth_lights_on != True:
            # if the player is in the labyrinth, informs them that they should find the flashlight to increase visibility
            if (self.player.pos_row > 1 and self.player.pos_row < 9) and (self.player.pos_col > 1 and self.player.pos_col < 9):
                self.error = True
                self.error_msg.update_text("Find and turn on the flashlight to see in the labyrinth.")
            
            self.screen.place_dark(self.player, all=True)  # darkens all labyrinth grid squares
    
    
    ## Player Functions ##
    
    def move_player(self):
        '''
        move_player() allows the player to move around the map (by shifting the map in the background in the opposite direction) and
                      changes the game's frame number to ensure the player and any item the player is holding are facing the correct direction
        '''
        
        # if the down key is pressed and player is not touching the monster's top side, moves the player 5 pixels down
        if keyPressed("down"):
            if self.active_monster != None and self.active_monster.previous == 'up' and self.active_monster.touching(self.player, self.screen):  # checks if te player is collided with the monster's top side
                self.screen.scroll(0, 0, self.player, self.player.held_item)  # redraws without moving
            else:
                self.screen.scroll(0, 5, self.player, self.player.held_item)  # moves screen 5 pixels up
            
            self.frame = 0  # corresponds to down orientation
        
        # if the right key is pressed and player is not touching the monster's left side, moves the player 5 pixels right
        elif keyPressed("right"):
            if self.active_monster != None and self.active_monster.previous == 'left' and self.active_monster.touching(self.player, self.screen):  # checks if te player is collided with the monster's left side
                self.screen.scroll(0, 0, self.player, self.player.held_item)  # redraws without moving
            else:
                self.screen.scroll(5, 0, self.player, self.player.held_item)  # moves screen 5 pixels left
            
            self.frame = 1  # corresponds to right orientation
            
        # if the left key is pressed and player is not touching the monster's right side, moves the player 5 pixels left
        elif keyPressed("left"):
            if self.active_monster != None and self.active_monster.previous == 'right' and self.active_monster.touching(self.player, self.screen):  # checks if te player is collided with the monster's right side
                self.screen.scroll(0, 0, self.player, self.player.held_item)  # redraws without moving
            else:
                self.screen.scroll(-5, 0, self.player, self.player.held_item)  # moves screen 5 pixels right
            
            self.frame = 2  # corresponds to left orientation

        # if the up key is pressed and player is not touching the monster's bottom side, moves the player 5 pixels up
        elif keyPressed("up"):
            if self.active_monster != None and self.active_monster.previous == 'down' and self.active_monster.touching(self.player, self.screen):  # checks if te player is collided with the monster's bottom side
                self.screen.scroll(0, 0, self.player, self.player.held_item)  # redraws without moving
            else:
                self.screen.scroll(0, -5, self.player, self.player.held_item)  # moves screen 5 pixels down
            
            self.frame = 3  # corresponds to up orientation
    
        # if no directional keys are pressed, redraws the player without moving
        else:
            self.screen.scroll(0, 0, self.player, self.player.held_item)
    
    def place_player(self):
        '''
        place_player() draws the player and the weapon the player is holding, if any
        '''
        
        # draws the player behind the weapon if the player is not facing up
        if self.frame in (0,1,2):
            self.player.place(self.screen, self.frame)
        
        # draw weapon on player if holding weapon
        if self.player.held_item != None:
            self.player.held_item.frame = self.frame
            self.player.held_item.draw(self.screen,self.extend)
        
        # draw the player in front of weapon if the player is facing up
        if self.frame == 3:
            self.player.place(self.screen, self.frame)
        
        # retrieves the new labyrinth grid row and column position of the player
        self.player.get_new_loc(self.screen)
    
    
    ## Monster Functions ##
    
    def monster_interaction(self):
        '''
        monster_interaction() allows the player to do damage to the monster and moves the game to the next level if the monster is killed
        '''
        
        # if the player is using an item (if the item is extended) and that weapon comes into contact with the monster, does damage to the monster
        if self.player.held_item != None and self.extend and self.player.held_item.touching(self.active_monster, self.screen):
            # alerts the used that they cannot do damage to the monster with the key, flashlight, or gem
            if self.player.held_item.nick in ('key', 'flashlight', 'gem'):
                self.error = True
                self.error_msg.update_text("You can't kill with the {}.".format(self.player.held_item.nick))
            
            # does damage to the monster either each time the weapon is extended or every 100 frames if the weapon is kept extended
            # this means the player can either repeatedly press space or hold the spacebar to do damage
            else:
                # increments the frame counter
                self.damage_lag += 1
                
                # damages monster (specific number of damage points differs for different weapons and monsters)
                if self.damage_lag == 1:
                    self.active_monster.decrease_health(self.player.held_item.damage_pts[self.active_monster.nick])
                
                # implements the 100 frame lag for killing if the weapon stays extended
                if self.damage_lag == 100:
                    self.damage_lag = 0
                
                # advances the game to the next level if the monster dies
                if self.active_monster.health <= 0:
                    self.next_level()
        
        # resets the frame lag counter if the weapon is unextended
        elif not self.extend:
            self.damage_lag = 0
    
    def place_monster(self):
        '''
        place_monster() allows the monster to track the player and draws the monster on screen
        '''
        
        # once the monster leaves its room at the beginning of each level, closes the door behind it
        if self.active_monster.pos_row > 0 and self.active_monster.pos_col > 0 and self.active_monster.pos_row < 10 and self.active_monster.pos_col < 10 and not self.active_monster.touching(self.screen.door_list[self.level], self.screen):
            self.screen.door_list[self.level].close_door()

        # if the level has a monster associated with it, the monster tracks the player location
        # the monster is then drawn
        if self.active_monster != None:
            self.active_monster.track_player(self.screen,self.player, self)
        
        # retrieves monster position in the labyrinth grid
        self.active_monster.get_new_loc(self.screen)
    
    ## Updater Functions ##
    
    def update_health_bars(self):
        '''
        update_health_bars() draws player and monster health bars with updated health values
        '''
        
        self.player_health_bar.update_bar(self.screen.screen, new_val=self.player.health)
        self.monster_health_bar.update_bar(self.screen.screen, new_val=self.active_monster.health)
    
    def text_update(self):
        '''
        text_update() updates the instructional text in the corner of the screen depending on which actions can be taken;
                      text may change if different items are held or if the player is in the same room as a particular item
        '''
        
        self.text.text = "Controls:\narrow keys to move"
        
        # if the player isn't holding an item
        if self.player.held_item == None:
            self.text.text += "\n'd' to pick up object"

            # if there are items in the items list (i.e., backpack)
            if len(self.items_list) > 0:
                self.text.text += "\n'r' to cycle through backpack"

                # if the menu is open
                if self.menu_pause:
                    self.text.text += "\n's' to close menu of items"
                
                # if the menu is not open
                else: 
                    self.text.text += "\n'a' to open menu of items"
            
        # if the player is holding an object
        else:
            self.text.text += "\nspace to use object\n'f' to drop object\n'e' to place object in backpack"

            # if there are things in the items_list other than the object you're carrying (in the backpack)
            if len(self.items_list) > 1:
                self.text.text += "\n'r' to cycle through backpack"

            # if the menu is open
            if self.menu_pause:
                self.text.text += "\n's' to close menu of items"
            
            # if the menu is not open
            else: 
                self.text.text += "\n'a' to open menu of items"

            if self.player.held_item.nick == 'flashlight':
                self.text.text += "\n'q' to turn the flashlight on/off"
        
        # if the player is in the same room as any of the chests
        for chest in self.chests:
            self.screen.get_new_loc(chest)
            if chest.pos_col == self.player.pos_col and chest.pos_row == self.player.pos_row:
                self.text.text += "\n'w' to open or close chest"

        # info for closing the game
        self.text.text += "\n'esc' to quit game"

        # updates the text shown on screen
        self.text.updateText(self.screen.screen,background_color =(255,233,155),text_color=(0,0,0))


    ## Gem Functions ##
    
    def random_gem_locations(self):
        '''
        random_gem_location() places the gems into random locations inside the labyrinth
        '''
        
        # list of gem locations
        gem_locs = []
        
        # loops through all gems
        for gem in self.gems:
            # loops getting random location to ensure that each gem has a unique location
            loop = True
            while loop:
                # gets random x and y locations in the labyrinth grid
                x_row = random.randint(2, 8)
                y_row = random.randint(2, 8)
                
                # if the grid locations are the same as previously placed gem, gets new x and y locations
                if (x_row, y_row) not in gem_locs:
                    loop = False
            
            # adds the new gem locations to 
            gem_locs.append((x_row, y_row))
            
            # sets the x and y background coordinates of the gem so that it is in the center of the grid square it was placed in
            # bg coordinate = x or y coordinate of top right of labyrinth + (wall thickness + corridor width or height)*(number of corridors skipped over) + (half the corridor width) - (half the gem width or height)
            gem.x_bg = 1245 + (60 + 540)*(x_row - 1) + 540//2 - gem.width//2
            gem.y_bg = 1050 + (60 + 540)*(y_row - 1) + 540//2 - gem.height//2
    
    def gem_countdown(self):
        '''
        gem_countdown() draws the countdown for gems before they disappear from the background
        '''
        
        # frame rate per minute is 60 times the frame rate per second of the game
        fpm = 60*self.fps
        
        # gets the minutes and second left
        total_mins = self.time_left//fpm  # minutes left = (time left)/(frame rateper minute)
        total_sec = (self.time_left - (fpm*total_mins))//self.fps  # seconds left = (time left - (frames per minute * minutes left))/(frame rate per second)
        
        # decreases time left
        self.time_left -= 1
        
        # if time is still left, draws how much time is left in minutes:seconds on screen
        if self.time_left > 0:
            # sets the string for the text
            if total_sec < 10:
                # adds a 0 in from of seconds if second are below 10
                t_string = str(total_mins) + ":0" + str(total_sec)
            else:
                t_string = str(total_mins) + ":" + str(total_sec)
            
            # sets the text item based on the text string
            text = self.font.render(t_string, True, (99,99,99))
        
        # once time runs out
        else:
            # sets text item as blank after the time has elapsed
            text = self.font.render("", True, (99,99,99))
            
            # removes all gems that haven't been found from the background
            for gem in self.gems:
                if gem.times_picked_up == 0:
                    self.available_weapons.remove(gem)
                    self.screen.background_obj.remove(gem)
            
            # resets background image
            self.screen.set_background_image()
        
        # draws countdown text on light grey background on screen
        self.countdown.fill((20, 20, 20))
        self.countdown.blit(text, (10,10))
        self.screen.screen.blit(self.countdown, (25,725))
    
    
    ## Level Functions ##
    
    def next_level(self):
        '''
        next_level() advances the game to the next level
        '''
        
        # if the next level isn't the last level and if the current level isn't the beginning tutorial
        if self.level < self.max_levels - 1 and self.level >= 0:
            # gets key that the player wins after killing the monster
            level_key = self.keys[self.level]
            
            # the key's x and y positions are near the center of the killed monster
            level_key.x_bg = self.active_monster.x_bg + 575
            level_key.y_bg = self.active_monster.y_bg + 475
            
            # advances to the next level and retrieves level items
            self.level += 1
            self.levels()
            
            # puts level key and newly available weapon into the background
            self.screen.background_obj.append(level_key)
            self.screen.background_obj.append(self.weapons[self.level])
            
            # removes the new monster from the background object list
            self.screen.background_obj.remove(self.monsters[self.level])
            
            # places the level key into available weapons
            self.available_weapons.append(level_key)
            
            # redraws background
            self.screen.set_background_image()
            
            # sets the new max in the monster's health bar
            self.monster_health_bar.new_max = self.active_monster.health
            
            # releases the next monster by opening the door and retrieves its grid location
            self.screen.door_list[self.level].open_door()
            self.active_monster.get_new_loc(self.screen)
        
        # if the next level is the last level, advances to the final level
        else:
            self.final_level()

    def levels(self):
        '''
        levels() retrieves and sets level-specific variables
        '''
        
        # if the player is past the tutorial
        if self.level >= 0:
            # change monster based on level
            self.active_monster = self.monsters[self.level]
            
            # adds the next weapon to available weapons
            self.available_weapons.append(self.weapons[self.level])
            
            # place the next item in the chest of the previous monster's room
            # only if a monster has already been killed
            if self.level > 0:
                self.chests[self.level-1].place_object(self.weapons[self.level])
    
    def final_level(self):
        '''
        final_level() retrieves the items required for the final level
        '''
        
        # gets key that the player 'wins' after killing the monster
        level_key = self.keys[self.level]
        
        # the key's x and y positions are about the center of the monster
        level_key.x_bg = self.active_monster.x_bg + 575
        level_key.y_bg = self.active_monster.y_bg + 475
        
        # puts level key into the background
        self.screen.background_obj.append(level_key)
        
        # advances the level by 1
        self.level += 1
        
        # gets the key for the final room and places it int othe final monster's chest
        final_key = self.keys[self.level]
        self.chests[self.level-1].place_object(final_key)
        self.screen.background_obj.append(final_key)
        
        # places both keys into available weapons
        self.available_weapons.append(level_key)
        self.available_weapons.append(final_key)
        
        # redraws background
        self.screen.set_background_image()
        
        # final level has no monster
        self.active_monster = None
        
        # final story instructions should be displayed
        self.final_story_instructions = True
    
    
    ## Game Pausing ##
    
    def pause_screen(self):
        '''
        pause_screen() draws the screen of the paused game
        '''
        
        # if the player is not in the beginning tutorial
        if self.level >= 0:
            # places all buttons on screen
            for button in self.buttons:
                # changes pause button frame to paused if it wasn't already
                # this would happen if the menu was opened
                if button.nick == 'pause' and button.frame == 0:
                    button.frame += 1
                
                # places button
                button.place()

                # if the pause button is clicked, unpauses the game
                if button.detectClick(self.events):
                    if button.nick == "pause":
                        self.pause = False
                        self.menu_pause = False
        
        # if the 'esc' key is clicked, exits the game
        if (keyPressed("esc")):
            pygame.quit()
            sys.exit()
        
        # updates the screen
        pygame.display.update()
        self.tick(120, self.events)
    
    
    ## Game Clock ##
    
    def tick(self, fps, events):
        '''
        tick() increments game timer and watches for game exiting
        
        Parameters (required):
            fps - frame rate per second
            events - list of pygame events (e.g., clicks)
        
        Returns:
            clock fps
        '''
        
        # if the 'esc' button is clicked, exits game
        for event in events:
            if (event.type == pygame.KEYDOWN and event.key == keydict["esc"]) or event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # advances game using how many frames per second shoudl be updated
        self.clock.tick(fps)
        return self.clock.get_fps()

    
    ## Game Ending Functions ##
    
    def beat_game(self):
        '''
        beat_game() draws the ending animation for beating the game and achieving immortality
        '''
        
        # draws the background at the last location
        self.screen.screen.blit(self.screen.surface, [-self.screen.stagePosX, -self.screen.stagePosY])
        
        # updates the player's image based on a dictionary of the animation images
        # rate at which images are updates will depend on the previously set frame rate of the animation
        try:
            # updates the image if there is a new image for that frame
            self.player.image = self.player.animation_images[self.c]
        except:
            # since not all frame numbers will be dictionary keys
            # the image from the previous frame will be used
            pass
        
        # draws the player image on screen
        self.screen.screen.blit(self.player.image, [self.player.x, self.player.y])

        # checks for button clicks
        for button in self.buttons:
            if button.detectClick(self.events):
                # if the pause button is clicked, the game is paused
                if button.nick == "pause":
                    self.pause = True

        # draws all buttons on screen
        for button in self.buttons:
            button.place()
        
        # moves to next animation frame
        self.c += 1
        
        # if the 'esc' key is pressed, exits the game
        if (keyPressed("esc")):
            pygame.quit()
            sys.exit()
            
    def win_end_screen(self):
        '''
        win_end_screen() displays the final story screen for when the player wins before the game closes
        '''
        
        # plays story screen
        self.story_display(self.story.win_end_screen,next="[Press enter or click to close game]")

        # quits game and closes window
        pygame.quit()
        sys.exit()
    
    def lose_end_screen(self):
        '''
        lose_end_screen() displays the final story screen for when the player dies before the game restarts
        '''

        # plays story screen
        self.story_display(self.story.lose_end_screen,next="[Press enter or click to restart the game]")
