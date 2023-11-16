import pygame
from sys import exit

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
import surfaces

pygame.display.set_caption('Spaceship Game')
clock = pygame.time.Clock()
laser_y_pos = 50
dude_rect = surfaces.dude_rect(400,400)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # player pushes the x button on the window
            pygame.quit() # close the game
            exit()
    # draw every surface
    screen.blit(surfaces.graph, (0,0)) # sets coordinate point of top left corner for image
    screen.blit(surfaces.line, (0,screen_height/2))
    screen.blit(surfaces.test_text,(screen_width/4,screen_height/6))
    
    # move the laser down
    laser_y_pos += 1
    if laser_y_pos > screen_height:
        laser_y_pos = 0
    screen.blit(surfaces.laser,(50,laser_y_pos))
    screen.blit(surfaces.dude,(dude_rect))
    dude_rect.left += 1

    pygame.display.update() # updates the display
    clock.tick(60) # set maximum frames per second
