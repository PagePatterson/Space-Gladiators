import pygame
import fonts
'''
This file contains all of the surfaces and graphical elements used in the game
'''

# images
graph = pygame.image.load('images/graph.jpg').convert_alpha()
dude = pygame.image.load('images/dude.jpg').convert_alpha()
dude = pygame.transform.scale(dude,(80,80))

# shapes
line = pygame.Surface((800,10))
laser = pygame.Surface((5,30))
laser.fill('Red')

# text
test_text = fonts.pixel.render('Spaceship Game', False, 'Black')

# rectangles - used to place the surface and detect collisions
def dude_rect(x,y):
    rect = dude.get_rect(midbottom = (x,y))
    return rect
