#!/usr/bin/python
#
# -------------------------------------------------------------
# template - a template to start pygame programs
# 2012-10-01 Javier Cantero <jcantero@escomposlinux.org>
#
# LICENSE:
# Public Domain - Use what/where/how you like and remove this
# -------------------------------------------------------------

import pygame
import drawings
import gridmap
import bot
import controls



# general constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
NSQUARES = 15;
ARESTA = 30;
ARESTA_CONTROL = 40;
X_CONTROL = 600;
Y_CONTROL = 100;
MARGIN = 6;
D = ARESTA+MARGIN;
STOP_COUNTER = D/18;
FRAME_RATE = 30
'''KEYS'''
LEFT_KEY = pygame.K_LEFT
RIGHT_KEY = pygame.K_RIGHT
UP_KEY = pygame.K_UP
DOWN_KEY = pygame.K_DOWN
Q_KEY = pygame.K_q
KEY1 = pygame.K_1
KEY2 = pygame.K_2
KEY3 = pygame.K_3
KEY4 = pygame.K_4
A_KEY = pygame.K_a
S_KEY = pygame.K_s
W_KEY = pygame.K_w
D_KEY = pygame.K_d

DIRECTION_CONTROLLER = [LEFT_KEY,RIGHT_KEY,UP_KEY,DOWN_KEY]
MOVEMENT_CONTROLLER = {A_KEY:(-1,0),W_KEY:(0,-1),S_KEY:(0,1),D_KEY:(1,0)}
BUILDER_CONTROLLER = [KEY1,KEY2,KEY3,KEY4]


 
class Game():
    def __init__(self):
    	self.GRID_MAP = gridmap.grid_map(ARESTA,NSQUARES)
    	self.CONTROL = controls.control_panel(X_CONTROL,Y_CONTROL,ARESTA_CONTROL);
    	self.robot_is_on = False;
    	self.builder = "arrow"
    	self.builderSelector = {KEY1:"simple",KEY2:"arrow",KEY3:"selector"}
    	self.builderTable = {"simple":gridmap.simple_builder(), "arrow":gridmap.arrow_builder(),"selector":gridmap.selector_builder()};
    def start_robot(self,sequence):
    	self.rob = bot.robot(273,21,sequence);
    	self.robot_is_on = True;
    def loop(self, screen):
        clock = pygame.time.Clock()
        last_clicked_grid = gridmap.grid_square(1);
        last_clicked_grid_X = 900;
        last_clicked_grid_Y = 900;
        while True:
            delta_t = clock.tick( FRAME_RATE )

            # handle input events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return # closing the window, end of the game loop
                elif event.type == pygame.MOUSEBUTTONDOWN:
                	pos = pygame.mouse.get_pos()
                	column = pos[1] // (ARESTA + MARGIN)
                	row = pos[0] // (ARESTA + MARGIN)
                	if( column < 15 and row < 15):
                		last_clicked_grid.selected();
                		last_clicked_grid = self.GRID_MAP.grid[row][column];
                		last_clicked_grid_X = row;
                		last_clicked_grid_Y = column;
                		self.GRID_MAP.grid[row][column].selected();
                elif event.type == pygame.KEYDOWN:
                    if (event.key in DIRECTION_CONTROLLER):
                    	grid_maker = self.builderTable[self.builder];
                    	self.GRID_MAP.grid[last_clicked_grid_X][last_clicked_grid_Y] = grid_maker.makegrid(event.key)
                    elif event.key == Q_KEY:
                    	T = 0;
                    	self.start_robot([0,1,1,0]);
                    elif (event.key in BUILDER_CONTROLLER):
                    	self.builder = self.builderSelector[event.key]
                    elif (event.key in MOVEMENT_CONTROLLER):
                    	movement = MOVEMENT_CONTROLLER[event.key]
                    	last_clicked_grid.selected();
                    	last_clicked_grid_X += movement[0];
                    	last_clicked_grid_Y += movement[1];
                    	last_clicked_grid = self.GRID_MAP.grid[last_clicked_grid_X][last_clicked_grid_Y];
                    	last_clicked_grid.selected();
            # render game screen
            screen.fill( (255, 255, 255) ) # black background
            self.GRID_MAP.drawmap(screen);
            self.CONTROL.draw(screen)

            if(self.robot_is_on):
            	self.rob.draw(screen)
            	(X,Y) = self.rob.get_coords()
            	x = X// (ARESTA + MARGIN)
            	y = Y// (ARESTA + MARGIN)
            	actual_grid = self.GRID_MAP.grid[x][y];
            	self.rob.move()
            	self.rob.change_speed(actual_grid)
          
            pygame.display.update()
            # or pygame.display.flip()

    def quit(self):
        pass


def main():
    pygame.init()
    screen = pygame.display.set_mode( (SCREEN_WIDTH, SCREEN_HEIGHT) )
    pygame.display.set_caption( 'Example' )
    #pygame.mouse.set_visible( False )
    game = Game()
    game.loop( screen )
    game.quit()

    pygame.quit()

if __name__ == '__main__':
    main()
