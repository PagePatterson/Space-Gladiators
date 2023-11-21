import pygame
from sys import exit

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Space Gladiators')

clock = pygame.time.Clock()

# fonts
pixel = pygame.font.Font('font/pixel_font.ttf', 50)

# images
background = pygame.image.load('images/graph.jpg').convert_alpha()
player_ship = pygame.image.load('images/dude.jpg').convert_alpha()
player_ship = pygame.transform.scale(player_ship,(80,80))

# shapes
line = pygame.Surface((800,10))
laser = pygame.Surface((5,30))
laser.fill('Red')

# text
test_text = pixel.render('Spaceship Game', False, 'Black')

# rectangles - used to place the surface and detect collisions
player_ship_rect = player_ship.get_rect(midbottom = (50,500))
laser_rect = laser.get_rect(center = (50,50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # player pushes the x button on the window
            pygame.quit() # close the game
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            print('mouse down')

    # draw every surface
    screen.blit(background, (0,0)) # sets coordinate point of top left corner for image
    screen.blit(line, (0,screen_height/2))
    screen.blit(test_text,(screen_width/4,screen_height/6))
    
    # move the laser down
    laser_rect.y += 1
    if laser_rect.y > screen_height:
        laser_rect.y = 0
    screen.blit(laser,(laser_rect))

    player_ship_rect.move(pygame.mouse.get_pos())

    screen.blit(player_ship,(player_ship_rect))

    #if player_ship_rect.colliderect(laser_rect):
     #   print('collision')

    pygame.display.update() # updates the display
    clock.tick(60) # set maximum frames per second

