'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: main.py
Purpose: This file contains the main code for the game and calls classes and functions from other files.
         This file should be run in order to play the game.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
from numpy import place
from background import *
from player import Player
from weapons import *
from monster import *
from plant import *
from additional_func import *
from text import *
from button import *
from game import *
from chest import *

def main():
    # loops game to allow for replaying
    while True:
        # creates Background object for screen
        screen = Background(1000, 800, "images/map.png", (1050, 900), light_switch=(3830, 3870))

        # player and all the items they possess (items_list)
        items_list = []
        player = Player("player", items_list)

        # instructions textbox in the corner of the screen
        text = TextBox(700,530,270,240, top_padding=10, left_padding=10, padding=0)
        
        # story box
        story = Story(150,150)

        # monsters
        lion = Lion(400,1500)
        cerberus = Cerberus(400,3220)
        hydra = Hydra(400,4970)
        cattle = Cattle(6050,1500)
        golden_deer = Golden_Deer(6050,3220)
        boar = Boar(6050,4970)
        monsters = [lion, cerberus, hydra, cattle, golden_deer, boar]

        # weapons
        sword = Sword(None,"ground",x_bg=1300, y_bg=1300)
        shovel = Shovel(player,'hands', x_bg=1300, y_bg=1300)
        boxing_glove = Boxing_Glove(None, 'ground',x_bg=1300, y_bg=1300)
        flame_thrower = Flame_Thrower(None,'ground', x_bg=1300, y_bg=1300)
        trident = Trident(None,'ground',x_bg=1500,y_bg=1500)
        flashlight = Flashlight(None, 'ground', x_bg=1300, y_bg=1400)
        weapons = [shovel, sword, flashlight, boxing_glove, flame_thrower, trident]
        
        # keys for each door
        keys = []
        for n in range(1,9):
            keys.append(Key(None, 'ground', n))

        # flowers throughout the map
        plants = []
        plant_location = [(1980,1170),(2730,2365),(4975,3055),(5535, 5985),(2000,4000),(3000,1800)]
        for location in plant_location:
            plants.append(Plant(location[0],location[1]))

        # chests in monster rooms
        chests = []
        chest_location = [(660,1890), (660,3600), (660,5350), (6950,1890), (6950,3600), (6950,5350)]
        for location in chest_location:
            chests.append(Chest(location[0],location[1]))

        # buttons
        pause_button = Button(900,20,screen.screen,'pause')
        buttons = [pause_button]
        
        # 6 gems throughout labyrinth
        gems = []
        for i in range(0, 6):
            gems.append(Gem(None, 'ground'))

        # elixir/potion of immortality
        potion = Potion(None, 'ground', x_bg=3860, y_bg=7150)
        
        # gets x and y starting positions for the 6 rooms on the sides of the labyrinth
        hor_rooms = []
        for num in range(1,4):
            # gets the top y value for the room
            # this is the wall number from the top * the starting wall x coordinate - 5 * (the wall number from the top - 1)
            # the 5 pixel offset ensures the rooms match up properly with the other walls
            y = 1745*num - 5*(num-1)
            
            # a room on each side of the labyrinth for each y value
            for x in (550, 6600):
                hor_rooms.append((x, y))
        
        # gets x and y starting positions of the single vertical room
        vert_rooms = [(3695,6665)]
        
        # all rooms
        rooms = (hor_rooms, vert_rooms)
        
        # initializes game with above variables
        game = Game(screen, player, weapons, monsters, keys, gems, plants, buttons, text, story, chests, items_list, potion, rooms, level=0)

        # displays initial storyline
        game.story_screen()
        
        # sets up first level of game
        game.setup()

        # displays starting instructions
        game.instruction_screen()

        # loops gameplay while the player is alive
        while player.health > 0:
            # retrieves pygame events (e.g., clicks)
            game.events = pygame.event.get()
            
            # calls regular gameplay if the player hasn't beaten the game
            if not game.complete:
                game.gameplay()
            
            # if the player has beaten the game, gets and plays the beocming immortal animation
            else:
                # gets animation
                if game.c == 0:
                    game.player.held_item.use_potion(game.player)
                
                # plays animation
                if game.c <= 800:
                    game.beat_game()
                
                # shows final end screen informing the user that they won
                else:
                    game.win_end_screen()
            
            # gem countdown while time is still left
            if game.time_left > 0:
                game.gem_countdown()
            
            # pauses game
            while game.pause:
                game.events = pygame.event.get()
                
                game.pause_screen()
                
                # if the game was paused for the menu, displays the menu
                if game.menu_pause:
                    game.menu_display()
            
            # if the player lost, displays the losing screen
            if player.health <= 0:
                game.lose_end_screen()
            
            # updates screen
            pygame.display.update()
            game.tick(game.fps, game.events)

# calls main function
if __name__=="__main__":
    main()