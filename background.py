'''
Names: Spencer Lyudovyk, Amanda Lin, Jue Gong
Date: 05/09/22
Project: Labors of Hercules (Choose Your Own Adventure Game)
File: background.py
Purpose: This file contains the classes and methods for the Background and Doors of the game.
Task Description: Design a school-appropriate game allowing for user interaction/input.
'''

# imports
import pygame
from additional_func import *
from monster import Monster
from button import *
from weapons import *

class Background():
    '''
    The Background() class represents the labyrinth with the background image and all items on it that shift behind the player to make the player move through the map.
    It also contains all the wall collision points to prevent characters from moving through walls.
    '''
    
    def __init__(self, sizex, sizey, bg_img, stagePos, offset=(505, 390), light_switch=(0,0)):
        '''
        __init__() initializes a Background() object
        
        Parameters (required):
            sizex - window width
            sizey - window height
            bg_img - filename of background image to be used
            stagePos - tuple of the x and y coordinates the player starts at
        
        Parameters (optional):
            offset - tuple of x and y offsets when drawing items like walls; used to ensure proper placement in background; set to (505, 390) by default
            light_switch - tuple of light switch x and y coordinates in labyrinth; set to (0,0) by default
        '''
        
        # size of screen
        self.sizex = sizex
        self.sizey = sizey
        self.screen = pygame.display.set_mode([self.sizex, self.sizey])
        
        # walls and doors
        self.wall_list = set()  # set of wall points
        self.wall_cells = {}  # dictionary of which cells have which walls (north, east, south, and/or west) in the labyrinth grid
        self.door_list = []  # list of all door objects in the background
        
        # list of all objects in the background
        self.background_obj = []
        
        # starting center point position
        # this will be the player's position at the beginning of the game
        self.stagePosX = stagePos[0]
        self.stagePosY = stagePos[1]
        
        # offsets for background object placement
        self.offset_x = offset[0]
        self.offset_y = offset[1]
        
        # gets background image from filename
        if type(bg_img) is str:
            self.image = loadImage(bg_img)
        
        # width and height of background image
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
        # surface to draw on, same size as image
        self.surface = pygame.surface.Surface([self.width,self.height])
        
        # image for the dark sections of the labyrinth
        self.dark = loadImage('images/dark.png')
        
        # light switch button that can be clicked on to turn on all lights in the labyrinth
        self.light_switch = BackgroundButton(light_switch[0], light_switch[1], self.surface, 'switch')
        self.background_obj.append(self.light_switch)  # light switch starts as a background object

    def one_wall(self, x_left, y_top, x_right, y_bottom):
        '''
        one_wall() creates a single wall at the specified inputs by adding its coordinates to the wall_list
        
        Parameters (required):
            x_left - left x value of wall with respect to the background
            y_top - top y value of wall with respect to the background
            x_right - right x value of wall with respect to the background
            y_bottom - bottom x value of wall with respect to the background
        '''
        
        # loops through the x and y coordinates in multiples of 5 and adds all points to the wall_list
        # offests ensure placement in the correct location
        for x in range(x_left - self.offset_x, x_right - self.offset_x + 1, 5):
            for y in range(y_top - self.offset_y, y_bottom - self.offset_y + 1, 5):
                self.wall_list.add((x,y))
    
    def place_walls(self, h=405, w=630, hor_rooms=None, vert_rooms=None, corridor_room=None, corridor_length=265):
        '''
        place_walls() creates the walls in the background and adds them to the wall_list to ensure the players/characters do not move through them
        
        Parameters (optional):
            h - pixel height of horizontal rooms or pixel width of vertical rooms; default value is 405
            w - pixel width of horizontal rooms or pixel height of vertical rooms; default value is 630
            hor_rooms - a list containing all the horizontally oriented rooms; by default, set to None
            vert_rooms - a list containing all the vertically oriented rooms; by default, set to None
            corridor_room - a tuple containing the top x and y coordinates of the corridor room; used to add two walls to extend the corridor at the room's entrance; by default, set to None
            corridor_length - length of corridor near corridor room in pixels; set to 265 by default
        '''
        
        # dictionary for each cell in the labyrinth grid and where walls should be placed in that grid
        # each cell may get a north (N), west (W), east (E), and/or south (S) wall
        self.wall_cells = {1: {1:('N', 'W'), 2:('N', 'S'), 3:('N', 'S'), 4:('N', 'S'), 5:('N'), 6:('N', 'S'), 7:('N', 'S'), 8:('N', 'S'), 9:('N', 'E')},
                      2: {1:('W', 'E'), 2:('N', 'W'), 3:('N', 'S'), 4:('N', 'E', 'S'), 5:('W'), 6:('N', 'E'), 7:('N', 'W', 'S'), 8:('N', 'E'), 9:('W', 'E')},
                      3: {1:('W', 'E'), 2:('W', 'S'), 3:('N', 'E'), 4:('W', 'N'), 5:('E'), 6:('W'), 7:('N', 'S'), 8:('S', 'E'), 9:('W', 'E')},
                      4: {1:('W', 'E'), 2:('W', 'N'), 3:('S'), 4:('S', 'E'), 5:('W', 'E'), 6:('W', 'S', 'E'), 7:('W', 'N'), 8:('N', 'E'), 9:('W', 'E')},
                      5: {1:('W', 'E'), 2:('W', 'E'), 3:('W', 'N'), 4:('N', 'S'), 5:('S'), 6:('N', 'S'), 7:('S', 'E'), 8:('W', 'E'), 9:('W', 'E')},
                      6: {1:('W', 'E'), 2:('W', 'S', 'E'), 3:('W', 'E'), 4:('W', 'N'), 5:('N', 'E', 'S'), 6:('W', 'N'), 7:('N', 'S'), 8:('S', 'E'), 9:('W', 'E')},
                      7: {1:('W', 'E'), 2:('W', 'N'), 3:('S', 'E'), 4:('W', 'S'), 5:('N', 'S'), 6:('E'), 7:('W', 'N', 'S'), 8:('N', 'E'), 9:('W', 'E')},
                      8: {1:('W', 'E'), 2:('W', 'S'), 3:('N', 'S'), 4:('N', 'S'), 5:('N', 'E'), 6:('W', 'S'), 7:('N', 'S'), 8:('S', 'E'), 9:('W', 'E')},
                      9: {1:('W', 'S'), 2:('N', 'S'), 3:('N', 'S'), 4:('N', 'S'), 5:('S'), 6:('N', 'S'), 7:('N', 'S'), 8:('N', 'S'), 9:('S', 'E')}}
        
        # loops through each cell in the 9x9 grid of the labyrinth
        # checks which kind of wall each of the cells wants (based on dictionary) and creates it
        for col in range(0,9):  # 9 columns
            for row in range(0,9):  # 9 rows
                if 'N' in self.wall_cells[row+1][col+1]:
                    self.one_wall(1245+540*col+60*col-60, (1050+540*row+60*row)-60, 1245+540*(col+1)+60*(col+1), 1050+540*row+60*row)
                if 'S' in self.wall_cells[row+1][col+1]:
                    self.one_wall(1245+540*col+60*col-60, (1050+540*(row+1)+60*(row+1))-60, 1245+540*(col+1)+60*(col+1), 1050+540*(row+1)+60*(row+1))
                if 'W' in self.wall_cells[row+1][col+1]:
                    self.one_wall((1245+540*col+60*col)-60, 1050+540*row+60*row-60, 1245+540*col+60*col, 1050+540*(row+1)+60*(row+1))                
                if 'E' in self.wall_cells[row+1][col+1]:
                    self.one_wall((1245+540*(col+1)+60*(col+1))-60, 1050+540*row+60*row-60, 1245+540*(col+1)+60*(col+1), 1050+540*(row+1)+60*(row+1))
        
        # creates the walls of the 6 cells on the left and right sides of the labyrinth
        if hor_rooms:
            for (start_x, start_y) in hor_rooms:
                self.one_wall(start_x,start_y,start_x+w+60,start_y+60)  # top wall
                self.one_wall(start_x,start_y,start_x+60,start_y+h+60)  # left wall
                self.one_wall(start_x,start_y+h,start_x+w+60,start_y+h+60)  # bottom wall
                self.one_wall(start_x+w,start_y,start_x+w+60,start_y+h+60)  # right wall
         
        # creates the vertical rooms using the same mathematical inputs as the previous rooms
        # height and width are flipped for vertical rooms
        if vert_rooms:
            for (start_x, start_y) in vert_rooms:
                self.one_wall(start_x,start_y,start_x+h+60,start_y+60)  # top wall
                self.one_wall(start_x,start_y,start_x+60,start_y+w+60)  # left wall
                self.one_wall(start_x,start_y+w,start_x+h+60,start_y+w+60)  # bottom wall
                self.one_wall(start_x+h,start_y,start_x+h+60,start_y+w+60)  # right wall
        
        # corridor walls for the final room
        if corridor_room:
            start_x = corridor_room[0]
            start_y = corridor_room[1]
            self.one_wall(start_x, start_y-corridor_length, start_x+60, start_y+w+60)
            self.one_wall(start_x+h, start_y-corridor_length, start_x+h+60, start_y+w+60)

    def set_background_image(self):        
        '''
        set_background_image() creates the background image of the game and places it onto the screen with an offest
        '''
        
        # pastes background image to screen
        self.surface.blit(self.image, [0,0])
        
        # draws all doors
        self.place_doors()
        
        # draws all objects that are not monsters on the background image
        for object in self.background_obj:
            if isinstance(object, BackgroundButton):  # places background buttons using their own function
                object.place()
            elif not isinstance(object, Monster):  # places all other non-monsters with their specified frame number and background coordinates
                self.surface.blit(object.images[object.frame], [object.x_bg, object.y_bg])
        
        # draws the background onto the screen at the specified offset based on the player's location
        self.screen.blit(self.surface, [-self.stagePosX, -self.stagePosY])
    
    def scroll(self, x, y, player, item=None):
        '''
        scroll() redraws the background if the player moves on screen
        
        Parameters (required):
            x - pixels moved in the x direction; negative means left; positive means right
            y - pixels moved in the y direction; negative means up; positive means down
            player - player object
        
        Parameters (optional):
            item - the object the player is holding, if any; by default, set to None (i.e., player isn't holding an object)
        '''
        
        # increment center point position
        self.stagePosX += x
        self.stagePosY += y
        
        # calculate new top left corner x position
        if self.stagePosX > 0 and self.stagePosX < self.width:  # allows the player to move if they are in the the background
            xOff = (0 - self.stagePosX % self.width)
        elif self.stagePosX > self.width:  # stops the player from moving if they try to move off the background too far right
            xOff = (-self.width - self.stagePosX % self.width)
        else:  # stops the player from moving if they try to move off the background too far left
            xOff = (0 + abs(self.stagePosX) % self.width)
        
        # calculate new top left corner y position
        if self.stagePosY > 0 and self.stagePosY < self.height:  # allows the player to move if they are in the the background
            yOff = (0 - self.stagePosY % self.height)
        elif self.stagePosY > self.height:  # stops the player from moving if they try to move off the background too far up
            yOff = (-self.height - self.stagePosY % self.height)
        else:  # stops the player from moving if they try to move off the background too far down
            yOff = (0 + abs(self.stagePosY) % self.height)
        
        # by default, the background image itself is not redrawn
        redraw = False
        
        # esures that the player is in the background and has not collided with any walls; if so, will redraw the background
        if not self.detect_wall_collision(player) and self.stagePosX > -self.offset_x and self.stagePosY > -self.offset_y and self.stagePosX < (self.width-self.offset_x) and self.stagePosY < (self.height-self.offset_y):
            redraw = True
        
        # if any items the player isn't allowed to walk over are being touched, doesn't redraw the background
        for object in self.background_obj:
            if item != None and object.walk_over == False and item.touching(object, self):
                redraw = False
            elif object.walk_over == False and isinstance(object, Monster) and player.touching(object, self,monster=True): # if object is monster
                redraw = False
            elif object.walk_over == False and not isinstance(object, Monster) and player.touching(object, self,monster=False): # if object is not monster
                redraw = False
        
        # redraws the background if specified
        if redraw == True:
            self.screen.blit(self.surface, [xOff, yOff])
        
        # if redrawing not specified, does not move and resets previous position
        else:
            self.stagePosX -= x
            self.stagePosY -= y
            self.screen.blit(self.surface, [-self.stagePosX, -self.stagePosY])
    
    def detect_wall_collision(self, player):
        '''
        detect_wall_collision() detects if select player x and y points are in a wall to determine if it was collided with a wall
        
        Parameter (required):
            player - player object
        
        Returns:
            Boolean - True if the player has collided with a wall; False if the player has not
        '''
        
        # retrieves the left, middle, and right x coordinates of the player with reference to the background grid based on the center position and the player width
        x_left = self.stagePosX - (player.width//2) - 5
        x_mid = self.stagePosX
        x_right = self.stagePosX + (player.width//2) + 5
        
        # retrieves the top, middle, and bottom y coordinates of the player with reference to the background grid based on the center position and the player height
        y_top = self.stagePosY - (player.height//2) - 5
        y_mid = self.stagePosY
        y_bottom = self.stagePosY + (player.height//2) + 5
        
        # set of all player points using x and y coordinates above
        player_points = {(x_left, y_top), (x_left, y_mid), (x_left, y_bottom),
                         (x_mid, y_top), (x_mid, y_bottom),
                         (x_right, y_top), (x_right, y_mid), (x_right, y_bottom)}
        
        # gets a set of all points both in the walls and in the player
        intersection = player_points.intersection(self.wall_list)
        
        # if there are any points both in the walls and the player, returns True (i.e., player has collided with the wall)
        if intersection:
            return True
        
        # if the player is holding an item, checks if that item has collided with a wall
        # returns True if it has
        if player.held_item != None:
            return self.item_detect_wall_collision(player.held_item)
        
        # returns False if no collisions were detected
        return False
    
    def monster_detect_wall_collision(self, monster):
        '''
        monster_detect_wall_collision() detects if select monster x and y points are in a wall to determine if it was collided with a wall
        
        Parameter (required):
            monster - monster object
        
        Returns:
            Boolean - True if the monster has collided with a wall; False if the monster has not
        '''
        
        # retrieves the left (0/3), left middle (1/3), right middle (2/3), and right (3/3) x coordinates of the monster with reference to the background grid based on the center position and the monster width
        x_left = monster.x_bg
        x_l_mid = monster.x_bg + (monster.width//3)
        x_r_mid = monster.x_bg + 2*(monster.width//3)
        x_right = monster.x_bg + (monster.width)
        
        # retrieves the top (0/3), top middle (1/3), bottom middle (2/3), and bottom (3/3) y coordinates of the monster with reference to the background grid based on the center position and the monster height
        y_top = monster.y_bg 
        y_t_mid = monster.y_bg + (monster.height//3)
        y_b_mid = monster.y_bg + 2*(monster.height//3)
        y_bottom = monster.y_bg + (monster.height)

        # set of all monster points using x and y coordinates above
        monster_points = {(x_left, y_top), (x_left, y_t_mid), (x_left, y_b_mid), (x_left, y_bottom),
                         (x_l_mid, y_top), (x_l_mid, y_t_mid), (x_l_mid, y_b_mid),(x_l_mid, y_bottom), 
                         (x_r_mid, y_top), (x_r_mid, y_t_mid), (x_r_mid, y_b_mid),(x_r_mid, y_bottom),
                         (x_right, y_top), (x_right, y_t_mid), (x_right, y_b_mid),(x_right, y_bottom)}
        
        # gets a set of all points both in the walls and in the monster
        intersection = monster_points.intersection(self.wall_list)

        # if there are any points both in the walls and the monster, returns True (i.e., monster has collided with the wall)
        if intersection:
            return True
    
        # returns False if no collisions were detected
        return False

    def item_detect_wall_collision(self, item):
        '''
        item_detect_wall_collision() detects if select item x and y points are in a wall to determine if it was collided with a wall
        
        Parameter (required):
            item - holdable item object
        
        Returns:
            Boolean - True if the item has collided with a wall; False if the item has not
        '''
        
        # retrieves the left, middle, and right x coordinates of the item with reference to the background grid based on the center position and the item width
        x_left = self.stagePosX - 500 + item.x - 10
        x_mid = self.stagePosX - 500 + item.x + (item.width//2)
        x_right = self.stagePosX - 500 + item.x + item.width + 10
        
        # retrieves the top, middle, and bottom y coordinates of the item with reference to the background grid based on the center position and the item height
        y_top = self.stagePosY - 400 + item.y - 10
        y_mid = self.stagePosY - 400 + item.y + (item.height//2)
        y_bottom = self.stagePosY - 400 + item.y + item.height + 10
            
        # set of all item points using x and y coordinates above
        item_points = {(x_left, y_top), (x_left, y_mid), (x_left, y_bottom),
                            (x_mid, y_top), (x_mid, y_bottom),
                            (x_right, y_top), (x_right, y_mid), (x_right, y_bottom)}
            
        # gets a set of all points both in the walls and in the item
        intersection = item_points.intersection(self.wall_list)
            
        # if there are any points both in the walls and the item, returns True (i.e., item has collided with the wall)
        if intersection:
            return True
        
        # returns False if no collisions were detected
        return False

    def get_new_loc(self, object, corridor_width=620):
        '''
        get_new_loc() retrieves an object's grid row and grid column coordinates in the 9x9 labyrinth grid
        
        Parameter (required):
            object - the object that the grid position will be retrieves fo
        
        Parameter (optional):
            corridor_width - width of each corridor in the labyrinth; set to 620 by default
        '''
        
        # x and y positions of the object with respect to the background image
        if 'x_bg' in object.__dict__:
            x_bg = object.x_bg
            y_bg = object.y_bg
        else:
            x_bg = self.stagePosX
            y_bg = self.stagePosY
        
        # gets new grid cell row and column position of object
        # position = (background coordinate - starting center position + offset)//corridor width
        object.pos_col = (x_bg - 1050 + 450)//corridor_width 
        object.pos_row = (y_bg - 900 + 395)//corridor_width

    def make_doors(self, main_x=(1093,6584), main_y_top=1824, door_dist=1740, corridor_doors=[(3756, 6392), (3756, 6664)]):
        '''
        make_doors() creates all the doors in the background
        
        Parameters (optional):
            main_x - x coordinates of the walls on either side of the labyrinth; left doors will be at x=1093 and right doors will be at x=6584 by default
            main_y_top - top y coordinate of side walls in labyrinth
            room_dist - distances between each of the doors at the side of the labyrinth
            corridor_doors - list of x and y starting coordinates of doors in cooridor; doors will be drawn by default at (3756, 6392) and (3756, 6664)
        '''
        
        # door index counter
        index = 1
        
        # creates the 3 vertical walls on each side of the labyrinth
        for x in range(1,4):
            self.door_list.append(Door(self, main_x[0], main_y_top + door_dist*(x-1), index))
            index += 1
        for x in range(1,4):
            self.door_list.append(Door(self, main_x[1], main_y_top + door_dist*(x-1), index))
            index += 1
        
        # creates the two corridor walls at the bottom of the labyrinth before the last room
        for door in corridor_doors:
            self.door_list.append(Door(self, door[0], door[1], index))
            index += 1
    
    def place_doors(self):
        '''
        place_doors() draws all doors from the door list
        '''
        
        # loops through and places doors
        for door in self.door_list:
            door.place()
    
    def place_dark(self, player, all=False):
        '''
        place_dark() draws dark squares on the labyrinth to decrease player visibility
        
        Parameter (required):
            player - player object
        
        Parameter (optional):
            all - Boolean; True if all grid squares should be darkened; False if not; default value is False
        '''
        
        # darkens all cells if needed
        if all==True:
            for row in range(2,9):
                for col in range(2,9):
                    self.place_one_dark(row,col)
        
        # if the player is in the labyrinth, darkens the grid squares directly around them
        else:
            # grid row and column position of player
            row = player.pos_row
            col = player.pos_col
            
            # darkens square to north of player if not in the top labyrinth square
            if row > 2:
                self.place_one_dark(row-1, col)
            
            # darkens square to northeast of player if not in the top or rightmost labyrinth square
            if row > 2 and col < 8:
                self.place_one_dark(row-1, col+1)
            
            # darkens square to southwest of player if not in the bottom leftmost labyrinth square
            if row < 8 and col > 2:
                self.place_one_dark(row+1, col-1)
            
            # darkens square to west of player if not in the leftmost labyrinth square
            if col > 2:
                self.place_one_dark(row, col-1)
            
            # darkens square to northwest of player if not in the top leftmost labyrinth square
            if row > 2 and col > 2:
                self.place_one_dark(row-1, col-1)
            
            # darkens square to south of player if not in the bottom labyrinth square
            if row < 8:
                self.place_one_dark(row+1, col)
            
            # darkens square to southeast of player if not in the bottom rightmost labyrinth square
            if row < 8 and col < 8:
                self.place_one_dark(row+1, col+1)
            
            # darkens square to east of player if not in the rightmost labyrinth square
            if col < 8:
                self.place_one_dark(row, col+1)
    
    def place_one_dark(self, row, col):
        '''
        place_one_dark() places a single dark square in the specified grid location
        
        Parameters (required):
            row - row position of dark square in grid
            col - column position of dark square in grid
        '''
        
        # gets x and y positions of dark square with respect to background based on center posiiton
        x = -self.stagePosX + 1245 + 540*(col - 1) + 60*(col - 2)
        y = -self.stagePosY + 1045 + 540*(row - 1) + 60*(row - 2)
        
        # draws dark square
        self.screen.blit(self.dark, [x, y])

class Door():
    '''
    The Door() class represents a single door in the labyrinth.
    '''
    
    def __init__(self, screen, x, y, id, frame=0):
        '''
        ___init___() initializes a Door() object
        
        Parameters (required):
            screen - the screen that the door will be drawn to
            x - x position of the door with respect to the screen
            y - y position of the door with repsect to the screen
            id - door number; used to get the correct door images
        
        Parameter (optional):
            frame - frame number of the door (i.e., what to draw it as out of the several frame options)
        '''
        
        # retrieves open and closed door images and places them into a list
        self.images = []
        for n in range(1,3):
            img = loadImage('images/door' + str(id) + str(n) + '.png')
            self.images.append(img)
        
        # door width and height (slightly larger than sprite width/height to allow for collision detection)
        self.width = self.images[0].get_width() + 20
        self.height = self.images[0].get_height() + 20
        
        self.screen = screen  # Background object that the door is a part of
        self.frame = frame  # starting frame number of door; 0 is closed; 1 is open
        
        # x and y position of door
        self.x_bg = x  # x position of door with respect to the background
        self.y_bg = y  # y position of door with respect to the background
        self.x = self.x_bg - (self.x_bg%5) - self.screen.stagePosX - self.screen.sizex//2  # x position of the door with repsect to the pygame window
        self.y = self.y_bg - (self.x_bg%5) - self.screen.stagePosY - self.screen.sizey//2  # y position of the door with repsect to the pygame window
        
        # set of the points of the door that should be removed from the labyrinth walls if opened and the points that should be added if closed
        # starts of empty and is populated as needed
        self.passable = set()
    
    def place(self):
        '''
        place() draws the door onto the screen wither open or closed depending on frame number
        '''
        
        self.screen.surface.blit(self.images[self.frame], [self.x_bg, self.y_bg])
    
    def get_passable(self, open=True):
        '''
        get_passable() retrieves
        
        Parameters (optional):
            open - Boolean representing whether the door should be opened or closed; set to True by default
        '''
        
        # top left x and y positions of door rounded to the lower multiple of 5
        start_x = self.x_bg - (self.x_bg%5)
        start_y = self.y_bg - (self.y_bg%5)
        
        # if the door should be opened, searches a larger area of points to remove from the wall list
        # larger area is needed to ensure all closed points are removed
        if open:
            # searches through door points by multiples of 5 and removes them from the background wall_list if found
            # subtracting 15 and adding 15 ensures a larger area is searched
            for x in range(start_x - self.screen.offset_x - 15, start_x - self.screen.offset_x + self.width + 15 + 1, 5):
                for y in range(start_y - self.screen.offset_y - 15, start_y - self.screen.offset_y + self.height + 15 + 1, 5):
                    if (x,y) in self.screen.wall_list:
                        self.screen.wall_list.remove((x,y))
        
        # if the door should be closed, searches a smaller area of points
        # smaller area is needed to ensure that, if reopened, all points will be fully removed
        if not open:
            # searches through door points by multiples of 5 and adds them to the background wall_list if not found
            # adding 15 and subtracting 25 ensures a larger area is searched
            for x in range(start_x - self.screen.offset_x + 15, start_x - self.screen.offset_x + self.width - 15 + 1, 5):
                for y in range(start_y - self.screen.offset_y + 15, start_y - self.screen.offset_y + self.height - 15 + 1, 5):
                    if (x,y) not in self.screen.wall_list:
                        self.screen.wall_list.add((x,y))
    
    def open_door(self):
        '''
        open_door() opens the door
        '''
        
        self.frame = 1  # changes frame to open (i.e., 1)
        self.get_passable()  # opens door by removing door points from background wall_list
        self.place()  # redraws the door with the new frame number
    
    def close_door(self):
        '''
        close_door() closes the door
        '''
        
        self.frame = 0  # changes frame to closed (i.e., 0)
        self.get_passable(open=False)  # closes door by adding door points to background wall_list
        self.place()  # redraws the door with the new frame number
    
    def open_with_items(self, items_list, min_num, game, corridor_length=310):
        '''
        open_with_items() opens a door if the correct number of gems has been collected and placed in front of the door
        
        Parameters (required):
            items_list - list of collected items to check if they match the needed item type (Gem)
            min_num - minimum number of Gems needed to open door
            game - game object that the door is a part of
        
        Parameters (optional):
            corridor_length - how long the corridor in front of the room is (i.e., how far away from the room to search for the items)
        '''
        
        # counter of number of items collected
        counter = 0
        
        if items_list != None:
            # if the item is a Gem and is placed in front of the door, increments counter by 1
            for item in items_list:
                if isinstance(item, Gem) and item.in_space(self.x_bg - item.width, self.x_bg + self.width + item.width, self.y_bg - corridor_length, self.y_bg + item.height) and item.loc == 'ground':
                    counter += 1
        
            # if enough gems have been placed, opens the door and redraws the background
            if counter >= min_num:
                self.open_door()
                self.screen.set_background_image()
            
            # if not enough gems have been placed, informs the user of how many more gems they need
            elif (game.player.pos_col > 0 and game.player.pos_col < 9) and game.player.pos_row > 9:
                game.error = True
                game.error_msg.update_text("You need {x} more gems to open the door".format(x=str(min_num-counter)))
