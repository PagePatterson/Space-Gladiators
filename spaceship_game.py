import pygame
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 800))
pygame.mouse.set_visible(False)
pygame.display.set_caption('Space Gladiators')
clock = pygame.time.Clock()
RunGameLoop = True

# fonts
body_font = pygame.font.Font('font/body_font.otf', 40)
title_font = pygame.font.Font('font/star_font.ttf', 50)

class Time():
    def __init__(self):
        self.current_time = 0
        self.surf = body_font.render(f'{self.current_time}', True, (64,64,64))
        self.rect = self.surf.get_rect(center = (50,50))

    def displayTime(self, display_time = True):
        self.current_time = (pygame.time.get_ticks()- manager.start_time - manager.sub_time) // 1000
        if display_time:
            self.surf = body_font.render(f'{self.current_time}', True, (64,64,64))
            screen.blit(self.surf,self.rect)
        return self.current_time

class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, enemy = True, direction = 0):
        pygame.sprite.Sprite.__init__(self)
        self.surface = pygame.image.load('images/plaser.png').convert_alpha()
        self.surface = pygame.transform.rotozoom(self.surface,0,1.5)
        self.rect = self.surface.get_rect(center = pos)
        self.isEnemy = enemy
        self.direction = direction
        if self.isEnemy:
            self.surface = pygame.image.load('images/olaser.png').convert_alpha()
            self.surface = pygame.transform.rotozoom(self.surface,0,1.5)
        if self.direction == 1:
            self.surface = pygame.transform.rotate(self.surface, 15)
        if self.direction == 2:
            self.surface = pygame.transform.rotate(self.surface, -15)

class PewPew(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hit_cooldown = 0
        self.shoot_cooldown = 0
        self.enemy = True

    def hit(self):
        if self.hit_cooldown == 0:
            self.health -= 1
            self.hit_cooldown = 10
    
    def cooldown(self):
        if self.hit_cooldown > 0: self.hit_cooldown -= 1 
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

    def moveRandom(self):
        if self.posx < 1:
            self.wtf = random.choice([1,5,6])
        if self.posx > 799:
            self.wtf = random.choice([0,4,7])
        if self.posy < 1:
            self.wtf = random.choice([3,4,7])
        if self.posy > 399:
            self.wtf = random.choice([2,5,6])

        if self.wtf == 0:
            self.moveLeft() 
        if self.wtf == 1:
            self.moveRight() 
        if self.wtf == 2:
            self.moveUp() 
        if self.wtf == 3:
            self.moveDown() 
        if self.wtf == 4:
            self.moveLeft() 
            self.moveDown() 
        if self.wtf == 5:
            self.moveRight() 
            self.moveUp() 
        if self.wtf == 6:
            self.moveUp() 
            self.moveRight() 
        if self.wtf == 7:
            self.moveDown() 
            self.moveLeft() 

        self.rect = self.surface.get_rect(center = (self.posx,self.posy))

    def moveLeft(self):
        self.posx -= 5
    
    def moveRight(self):
        self.posx += 5

    def moveUp(self):
        self.posy -= 5

    def moveDown(self):
        self.posy += 5
    
    def shoot(self, direction = 0):
        if self.enemy:
            manager.lasers.add(Laser((self.pos)))
            self.shoot_cooldown = 10
        else:
            manager.lasers.add(Laser(self.pos, False, direction))

    def render(self):
        screen.blit(self.surface, self.rect)
    
    def update(self):
        if self.enemy:
            self.pos = (self.posx, self.posy)
            self.rect = self.surface.get_rect(center = self.pos)
        else: 
            if pygame.mouse.get_pos()[1] > 445:
                self.posx = pygame.mouse.get_pos()[0]
                self.posy = pygame.mouse.get_pos()[1]
                manager.player.rect = manager.player.surface.get_rect(center = pygame.mouse.get_pos())
            else:
                self.posx = pygame.mouse.get_pos()[0]
                self.posy = 445
                manager.player.rect = manager.player.surface.get_rect(center = (pygame.mouse.get_pos()[0],445))
            self.pos = (self.posx, self.posy)

class Player(PewPew):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load('images/skin1.png').convert_alpha()
        self.surface = pygame.transform.rotozoom(self.surface,0,3)
        self.rect = self.surface.get_rect(center = (400,600))
        self.health = 10
        self.pos = pygame.mouse.get_pos()
        self.enemy = False

class Enemy(PewPew):
    def __init__(self):
        super().__init__()
        self.surface = pygame.image.load('images/enemy1.png').convert_alpha()
        self.surface = pygame.transform.rotozoom(self.surface,180,3)  
        self.posy = random.randint(0,399)
        self.posx = random.randint(0,800)
        self.pos = (self.posx, self.posy)
        self.rect = self.surface.get_rect(center = self.pos)
        self.wtf = random.randint(0,3)
        self.health = 1

class GameMenu():
    def __init__(self):
        self.background = pygame.image.load('images/background.png').convert_alpha()
        self.title = title_font.render('space gladiators', True, 'Purple')
        self.title_rect = self.title.get_rect(center = (400,200))
        self.text1 = body_font.render('start', True, 'Purple')
        self.text_rect1 = self.text1.get_rect(center = (400,300))
        self.text2 = body_font.render('tutorial', True, 'Purple')
        self.text_rect2 = self.text2.get_rect(center = (400,400))
    
    def render(self):
        if manager.button == 0:
            self.text1 = body_font.render('start', True, 'Pink')
        elif manager.button == 1:
            self.text2 = body_font.render('tutorial', True, 'Pink')
        screen.blit(self.background, (0,0))
        screen.blit(self.title,self.title_rect)
        screen.blit(self.text1,self.text_rect1)
        screen.blit(self.text2,self.text_rect2)

class GameActive():
    def __init__(self):
        # images
        self.background = pygame.image.load('images/background.png').convert_alpha()

        # shapes
        self.line = pygame.Surface((800,5))
        self.line.fill('Black')

        # text
        self.score = body_font.render(f'level {manager.level}', True, 'Purple')
        self.score_rect = self.score.get_rect(center = (400, 50)) 
        self.pause = title_font.render(f'paused', True, 'Pink')
        self.pause_rect = self.pause.get_rect(center = (400, 200))
        self.pause1 = body_font.render(f'press space to exit game', True, 'Pink')
        self.pause1_rect = self.pause1.get_rect(center = (400, 300))
        self.game_over = body_font.render(f'Game Over', True, 'Purple')
        self.game_over_rect = self.game_over.get_rect(center = (400, 400))
        self.game_won = body_font.render(f'Congratulations!', True, 'Purple')
        self.game_won_rect = self.game_won.get_rect(center = (400, 300))
        self.health = body_font.render(f'HP {manager.player.health}', True, 'Purple')
        self.health_rect = self.health.get_rect(center = (700, 50))

        self.tutorial_point = 0

    def renderBackground(self, shooting = True, over = False):
        screen.blit(self.background, (0,0)) # sets coordinate point of top left corner for image

        if not over:
            screen.blit(self.score, self.score_rect)
            screen.blit(self.line, (0,400))
            manager.time.displayTime()
            screen.blit(self.health, self.health_rect)

        if shooting:
            # draw all lasers and checks for collisions
            for item in manager.lasers:
                if item.surface: 
                    screen.blit(item.surface, item.rect)
                if item.isEnemy:
                    item.rect[1] += 20
                    if manager.player.rect.colliderect(item.rect):
                        manager.player.hit()
                else:
                    if item.direction == 0:
                        item.rect[1] -= 20
                    elif item.direction == 1:
                        item.rect[1] -= 19
                        item.rect[0] -= 5
                    elif item.direction == 2:
                        item.rect[1] -= 19
                        item.rect[0] += 5
                    for enemy in manager.enemy:
                        if enemy.rect.colliderect(item.rect):
                            enemy.hit()
                            if enemy.health < 1: pygame.sprite.Sprite.kill(enemy)
                if item.rect[1] < 0 or item.rect[1] > 800:
                    pygame.sprite.Sprite.kill(item)

    def renderPlayer(self):
        manager.player.update()
        manager.player.render()
        if manager.player.health == 0:
            manager.game_over = True
        manager.player.pos = pygame.mouse.get_pos()

    def renderEnemy(self):
        for enemy in manager.enemy:
            enemy.moveRandom()
            enemy.update()
            if random.randint(0,10) < 7:
                if enemy.shoot_cooldown < 1:
                    enemy.shoot()
            enemy.cooldown()
            screen.blit(enemy.surface,(enemy.rect))

    def levelUp(self):
        manager.level += 1
        manager.addedEnemies = False

    def levelOne(self):
        manager.enemy_count = 3
        if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
            manager.enemy.add(Enemy())
        if len(manager.enemy) == manager.enemy_count:
            manager.addedEnemies = True
        if len(manager.enemy) == 0 and manager.addedEnemies:
            self.levelUp()
        self.renderBackground()
        self.renderPlayer()
        self.renderEnemy()
        manager.player.cooldown()

    def levelTwo(self):
        manager.enemy_count = 6
        if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
            manager.enemy.add(Enemy())
        if len(manager.enemy) == manager.enemy_count:
            manager.addedEnemies = True
        if len(manager.enemy) == 0 and manager.addedEnemies:
            manager.game_won = True
        self.renderBackground()
        self.renderPlayer()
        self.renderEnemy()
        manager.player.cooldown()

    def tutorial(self):
        manager.level = 0
        if manager.tutorial_point == 0:
            display = body_font.render(f'welcome to the tutorial!', True, ('Pink'))
        elif manager.tutorial_point == 1:
            display = body_font.render(f'use the mouse to move', True, ('Pink'))
            if not manager.tutorial_pos_check == pygame.mouse.get_pos():
                manager.tutorial_point += 1
        elif manager.tutorial_point == 2:
            display = body_font.render(f'left click to shoot', True, ('Pink'))
        elif manager.tutorial_point == 3:
            display = body_font.render(f'hold down "a" or "d" to aim', True, ('Pink'))
        elif manager.tutorial_point == 4:
            display = body_font.render(f'shoot the enemies', True, ('Pink'))
            manager.enemy_count = 1
            if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
                manager.enemy.add(Enemy())
            elif len(manager.enemy) == manager.enemy_count:
                manager.addedEnemies = True
            elif not (len(manager.enemy) and manager.addedEnemies):
                manager.tutorial_point += 1
        elif manager.tutorial_point == 5:
            display = body_font.render(f'tutorial complete!', True, ('Pink'))
        else:
            manager.in_menu = True
            manager.in_tutorial = False
        display_rect = display.get_rect(center = (400, 200))
        self.renderBackground()
        self.renderPlayer()
        self.renderEnemy()
        screen.blit(display, display_rect)
        manager.tutorial_pos_check = pygame.mouse.get_pos()
        manager.player.cooldown()

    def gameOver(self):
        self.level = 0
        self.renderBackground(False, True)
        screen.blit(self.game_over, self.game_over_rect)

    def gameWon(self):
        manager.sub_time += clock.get_time()
        self.game_won_score = body_font.render(f'Time: {manager.time.displayTime()}', True, 'Purple')
        self.game_won_score_rect = self.game_won_score.get_rect(center = (400, 400))
        self.renderBackground(False, True)
        screen.blit(self.game_won, self.game_won_rect)
        screen.blit(self.game_won_score, self.game_won_score_rect)
    
    def pauseGame(self):
        manager.sub_time += clock.get_time()
        self.renderBackground(False)
        screen.blit(self.pause, self.pause_rect)
        screen.blit(self.pause1, self.pause1_rect)

class Manager():
    def __init__(self):
        self.in_menu = True
        self.button = 0
        self.lasers = pygame.sprite.Group()
        self.enemy = pygame.sprite.Group()
        self.start_time = 0
        self.player = Player()
        self.time = Time()
        self.addedEnemies = False
        self.level = 0
        self.tutorial_point = 0
        self.pause = False
        self.sub_time = 0
        self.tutorial_pos_check = pygame.mouse.get_pos()
        self.enemy_count = 1
        self.game_over = False
        self.game_won = False

    def resetGame(self):
        self.button = 0
        self.addedEnemies = False
        self.lasers.empty()
        self.enemy.empty()
        self.player = Player()
        self.start_time = pygame.time.get_ticks()
        self.pause = False
        self.in_menu = False
        if self.level == 0: self.tutorial_active = True
        else: self.game_active = True
        self.sub_time = 0
        self.tutorial_pos_check = pygame.mouse.get_pos()
        self.enemy_count = 1
        self.game_over = False
        self.game_won = False
    
    def gameOver(self):
        self.in_menu = True
        self.game_active = False

manager = Manager()

while RunGameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # player pushes the x button on the window
            pygame.quit() # close the game
            exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            if manager.pause == True: 
                manager.pause = False
            else: manager.pause = True
        if manager.in_menu:
            if event.type == pygame.KEYUP and manager.button < 1 and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                manager.button += 1
            if event.type == pygame.KEYUP and manager.button > 0 and (event.key == pygame.K_UP or event.key == pygame.K_w):
                manager.button -= 1
            if event.type == pygame.KEYUP and manager.button == 0 and event.key == pygame.K_RETURN:
                manager.level = 1
                manager.resetGame()
            if event.type == pygame.KEYUP and manager.button == 1 and event.key == pygame.K_RETURN:
                manager.resetGame()
                manager.tutorial_point = 0
                manager.level = 0
                manager.in_menu = False
        elif manager.pause:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                manager.resetGame()
                manager.in_menu = True
                manager.pause = False
        elif manager.game_over or manager.game_won:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                manager.in_menu = True
                manager.game_won = True
                manager.game_over = False
        else:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.mouse.get_pos()[1] > 440: 
                    if keys[pygame.K_a]:
                        manager.player.shoot(1)
                    elif keys[pygame.K_d]:
                        manager.player.shoot(2)
                    else:
                        manager.player.shoot()
                else:
                    manager.lasers.add(Laser((pygame.mouse.get_pos()[0], 440), False))
        if manager.level == 0:
            if manager.tutorial_point == 0:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    manager.tutorial_point += 1
            elif manager.tutorial_point == 2:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    manager.tutorial_point += 1
            elif manager.tutorial_point == 3:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if keys[pygame.K_a]:
                        manager.tutorial_point += 1
                    elif keys[pygame.K_d]:
                        manager.tutorial_point += 1
            elif manager.tutorial_point == 5:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                    manager.in_menu = True

    keys = pygame.key.get_pressed()

    if manager.in_menu:
        GameMenu().render()
    elif manager.game_over:
        GameActive().gameOver()
    elif manager.game_won:
        GameActive().gameWon()
    elif manager.pause:
        GameActive().pauseGame()
    elif manager.level == 2:
        GameActive().levelTwo()
    elif manager.level == 1:
        GameActive().levelOne()
    elif manager.level == 0:
        GameActive().tutorial()
 
    pygame.display.update() # updates the display
    clock.tick(60) # set maximum frames per second
