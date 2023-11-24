import pygame
from sys import exit

pygame.init()

screen_width = 800
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.mouse.set_visible(False)
pygame.display.set_caption('Space Gladiators')

clock = pygame.time.Clock()

# fonts
pixel = pygame.font.Font('font/pixel_font.ttf', 50)

# images
background = pygame.image.load('images/graph.jpg').convert_alpha()

# shapes
line = pygame.Surface((800,10))

# text
test_text = pixel.render('Spaceship Game', False, 'Black')
score = pixel.render(f'score: 0', False, 'Black')
score_rect = score.get_rect(center = (400, 50)) 

lasers = []

class Laser():
    def __init__(self, pos, enemy = True):
        self._surface =  pygame.Surface((5,30))
        self._rect = self._surface.get_rect(center = pos)
        self._isEnemy = enemy
        if self._isEnemy:
            self._color = 'Red'
        else:
            self._color = 'Green'
        self._surface.fill(self._color)

class Player():
    def __init__(self):
        self.surface = pygame.image.load('images/dude.jpg').convert_alpha()
        self.surface = pygame.transform.scale(self.surface,(80,80))
        self.rect = self.surface.get_rect(center = (400,600))

class Enemy():
    def __init__(self, pos, surface = None):
        self.pos = pos
        self.surface = surface
        self.laser = Laser(self.pos)

player = Player()
    
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # player pushes the x button on the window
            pygame.quit() # close the game
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if pygame.mouse.get_pos()[1] > 440:
                    lasers.append(Laser(pygame.mouse.get_pos(), False))
                else:
                    lasers.append(Laser((pygame.mouse.get_pos()[0], 440), False))

    # draw every surface
    screen.blit(background, (0,0)) # sets coordinate point of top left corner for image
    screen.blit(line, (0,screen_height/2))
    screen.blit(test_text,(screen_width/4,screen_height/6))
    pygame.draw.rect(background, 'Green', score_rect)
    screen.blit(score, score_rect)

    # draw all lasers and checks for collisions
    for item in lasers:
        screen.blit(item._surface, item._rect)
        if item._isEnemy:
            item._rect[1] += 5
            if player.rect.colliderect(item._rect):
                print('collision')
        else:
            if player.rect.colliderect(item._rect):
                print('collision')
            item._rect[1] -= 5

    # ensures the spaceship doesnt go past the midline
    if pygame.mouse.get_pos()[1] > 440:
        player.rect = player.surface.get_rect(center = pygame.mouse.get_pos())
    else:
        player.rect = player.surface.get_rect(center = (pygame.mouse.get_pos()[0],440))

    # draw the spaceship            
    screen.blit(player.surface,(player.rect))

    pygame.display.update() # updates the display
    clock.tick(60) # set maximum frames per second

