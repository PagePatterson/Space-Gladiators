try:
    import pygame
except ModuleNotFoundError:
    print('please install pygame')
    exit()
import shelve
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((800, 800)) # set the size of the screen to 800 x 800 pixels
pygame.mouse.set_visible(False) # the mouse will not be visible in game
pygame.display.set_caption('Space Gladiators') # sets the words on the top of the window
clock = pygame.time.Clock() # we will use this to check the time later
music = 'music/lady-of-the-80s.mp3' # setting the music that will be played in the game
pygame.mixer.init() # we will use this to control if the music is being played
pygame.mixer.music.load(music) # we do this to allow us to play the music later 

# setting the fonts
sub_font = pygame.font.Font('font/body_font.otf', 30)
body_font = pygame.font.Font('font/body_font.otf', 40)
title_font = pygame.font.Font('font/star_font.ttf', 50)

class Time():
    '''
    Used to control the current time.
    '''
    def __init__(self):
        self.current_time = 0 
        self.surf = body_font.render(f'{self.current_time}', True, (64,64,64))
        self.rect = self.surf.get_rect(center = (50,50))

    def display_time(self, display_time = True):
        '''
        Takes a bool. If true, will display the current time on screen. Returns the current time.
        '''
        self.current_time = (pygame.time.get_ticks() - manager.start_time - manager.sub_time) // 1000 # time is given in milliseconds so we convert to seconds
        if display_time:
            self.surf = body_font.render(f'{self.current_time}', True, (64,64,64))
            screen.blit(self.surf,self.rect)
        return self.current_time

class Laser(pygame.sprite.Sprite):
    '''
    Used to create laser objects
    '''
    def __init__(self, pos, enemy = True, direction = 0):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.image.load('images/plaser.png').convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf,0,1.5)
        self.rect = self.surf.get_rect(center = pos)
        self.is_enemy = enemy
        self.direction = direction
        if self.is_enemy:
            self.surf = pygame.image.load('images/olaser.png').convert_alpha() 
            self.surf = pygame.transform.rotozoom(self.surf,0,1.5)
        if self.direction == 1:
            self.surf = pygame.transform.rotate(self.surf, 15)
        if self.direction == 2:
            self.surf = pygame.transform.rotate(self.surf, -15)

class PewPew(pygame.sprite.Sprite):
    '''
    Gives objects a way to shoot lasers and be hit. Updates the location of spaceship objects. Moves objects in a random pattern.
    '''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.hit_cooldown = 0
        self.shoot_cooldown = 0
        self.enemy = True

    def hit(self):
        '''
        Decreases the health of objects by one.
        '''
        if self.hit_cooldown == 0:
            self.health -= 1
            self.hit_cooldown = 10
    
    def cooldown(self):
        '''
        Decreases the cooldown of objects by one
        ''' 
        if self.hit_cooldown > 0: self.hit_cooldown -= 1 
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1

    def move_random(self):
        '''
        Moves game object in a random direction within the top half of the screen. Kind of like a DVD loading screen
        '''
        # checks the position of the sprite and if it is on the edge of the upper half of the game screen it will move away from it
        if self.posx < 1:
            self.rand_move = random.choice([1,5,6]) # the choices are straight or diagonally away from the edge of the screen
        if self.posx > 799:
            self.rand_move = random.choice([0,4,7])
        if self.posy < 1:
            self.rand_move = random.choice([3,4,7])
        if self.posy > 399:
            self.rand_move = random.choice([2,5,6])

        # depending on which random choice was picked above the sprite will move accordingly
        if self.rand_move == 0:
            self.move_left() 
        if self.rand_move == 1:
            self.move_right() 
        if self.rand_move == 2:
            self.move_up() 
        if self.rand_move == 3:
            self.move_down() 
        if self.rand_move == 4:
            self.move_left() 
            self.move_down() 
        if self.rand_move == 5:
            self.move_right() 
            self.move_up() 
        if self.rand_move == 6:
            self.move_up() 
            self.move_right() 
        if self.rand_move == 7:
            self.move_down() 
            self.move_left() 

        #updates the position of the sprite
        self.rect = self.surf.get_rect(center = (self.posx,self.posy))

    def move_left(self):
        '''
        Moves game object left by 5 pixels
        '''
        self.posx -= 5
    
    def move_right(self):
        '''
        Moves game object right by 5 pixels
        '''
        self.posx += 5

    def move_up(self):
        '''
        Moves game object up by 5 pixels
        '''
        self.posy -= 5

    def move_down(self):
        '''
        Moves game object down by 5 pixels
        '''
        self.posy += 5
    
    def shoot(self, direction = 0):
        '''
        Adds new laser to the list of lasers with the initial position being the center of the game object.
        The direction is based on if the sprite is the player or the enemy. 
        '''
        if self.enemy:
            manager.lasers.add(Laser((self.pos)))
            self.shoot_cooldown = 10
        else:
            manager.lasers.add(Laser(self.pos, False, direction))

    def render(self):
        '''
        Draws the game object to the screen
        '''
        screen.blit(self.surf, self.rect)
    
    def update(self):
        '''
        Updates the position of the game object
        '''
        if self.enemy:
            if self.health == 1:
                self.surf = pygame.image.load('images/enemy2.png').convert_alpha()
                self.surf = pygame.transform.rotozoom(self.surf,180,3)  
            self.pos = (self.posx, self.posy)
            self.rect = self.surf.get_rect(center = self.pos)
        else: 
            if pygame.mouse.get_pos()[1] > 445:
                self.posx = pygame.mouse.get_pos()[0]
                self.posy = pygame.mouse.get_pos()[1]
                manager.player.rect = manager.player.surf.get_rect(center = pygame.mouse.get_pos())
            else:
                self.posx = pygame.mouse.get_pos()[0]
                self.posy = 445
                manager.player.rect = manager.player.surf.get_rect(center = (pygame.mouse.get_pos()[0],445))
            self.pos = (self.posx, self.posy)

class Player(PewPew):
    '''
    Represents the player.
    '''
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('images/skin1.png').convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf,0,3)
        self.rect = self.surf.get_rect(center = (400,600))
        self.health = 10
        self.pos = pygame.mouse.get_pos()
        self.enemy = False # PewPew has self.enemy initially set to true so we need to change it

class Enemy(PewPew):
    '''
    Represents the enemy spaceships
    '''
    def __init__(self):
        super().__init__()
        self.surf = pygame.image.load('images/enemy1.png').convert_alpha()
        self.surf = pygame.transform.rotozoom(self.surf,180,3)  
        self.posy = random.randint(0,399)
        self.posx = random.randint(0,800)
        self.pos = (self.posx, self.posy)
        self.rect = self.surf.get_rect(center = self.pos)
        self.rand_move = random.randint(0,3)
        self.health = 2 

class GameMenu():
    '''
    Represents the game menu
    '''
    def __init__(self):
        # image
        self.background = pygame.image.load('images/background.png').convert_alpha()

        # text
        self.title = title_font.render('space gladiators', True, 'Purple')
        self.title_rect = self.title.get_rect(center = (400,200))
        self.text1 = body_font.render('start', True, 'Purple')
        self.text1_rect = self.text1.get_rect(center = (400,300))
        self.text2 = body_font.render('tutorial', True, 'Purple')
        self.text2_rect = self.text2.get_rect(center = (400,400))
        self.text3 = body_font.render('credit', True, 'Purple')
        self.text3_rect = self.text3.get_rect(center = (400,500))
        self.score = sub_font.render(f'highscore:{manager.highscore}', True, (64, 64, 64))
        self.score_rect = self.score.get_rect(center = (400, 750))
        self.credit1 = title_font.render('Credit', True, 'Purple')
        self.credit1_rect = self.credit1.get_rect(center = (400,200))
        self.credit2 = body_font.render('Creator: Page Patterson', True, 'Purple')
        self.credit2_rect = self.credit2.get_rect(center = (400,400))
        self.credit3 = body_font.render('Art: Ryan Patterson', True, 'Purple')
        self.credit3_rect = self.credit3.get_rect(center = (400,500))
        self.to_nav1 = sub_font.render(f'use the arrow keys to navigate', True, (64,64,64))
        self.to_nav1_rect = self.to_nav1.get_rect(center = (400, 650))
        self.to_nav2 = sub_font.render(f'press enter to continue', True, (64,64,64))
        self.to_nav2_rect = self.to_nav2.get_rect(center = (400, 700))
        self.space = sub_font.render(f'press space to continue', True, (64,64,64))
        self.space_rect = self.to_nav2.get_rect(center = (400, 750))

    def render(self):
        '''
        This draws the game menu to the screen
        '''
        self.score = sub_font.render(f'highscore:{manager.highscore}', True, (64, 64, 64))
        # sets color of button depending on which is selected
        if manager.button == 0:
            self.text1 = body_font.render('start', True, 'Pink')
        if manager.button == 1:
            self.text2 = body_font.render('tutorial', True, 'Pink')
        elif manager.button == 2:
            self.text3 = body_font.render('credit', True, 'Pink')

        # draws everything to screen
        screen.blit(self.background, (0,0))
        screen.blit(self.title,self.title_rect)
        screen.blit(self.text1,self.text1_rect)
        screen.blit(self.text2,self.text2_rect)
        screen.blit(self.text3,self.text3_rect)
        screen.blit(self.score, self.score_rect)
        if manager.highscore == 'None':
            screen.blit(self.to_nav1,self.to_nav1_rect)
            screen.blit(self.to_nav2,self.to_nav2_rect)

    def credit(self):
        screen.blit(self.background, (0,0))
        screen.blit(self.credit1, self.credit1_rect)
        screen.blit(self.credit2, self.credit2_rect)
        screen.blit(self.credit3, self.credit3_rect)
        screen.blit(self.space, self.space_rect)

class GameActive():
    '''
    Holds all of the levels in the game and the tutorial.
    '''
    def __init__(self):
        # images
        self.background = pygame.image.load('images/background.png').convert_alpha()

        # shapes
        self.line = pygame.Surface((800,5))
        self.line.fill('Black')

        # text
        self.score = body_font.render(f'level {manager.level}', True, 'Purple')
        self.score_rect = self.score.get_rect(center = (400, 50)) 
        self.pause = title_font.render(f'paused', True, 'Purple')
        self.pause_rect = self.pause.get_rect(center = (400, 200))
        self.pause1 = sub_font.render(f'press space to exit game', True, (64,64,64))
        self.pause1_rect = self.pause1.get_rect(center = (400, 300))
        self.game_over_img = body_font.render(f'Game Over', True, 'Purple')
        self.game_over_img_rect = self.game_over_img.get_rect(center = (400, 400))
        self.game_won_img = body_font.render(f'Congratulations!', True, 'Purple')
        self.game_won_img_rect = self.game_won_img.get_rect(center = (400, 300))
        self.health = body_font.render(f'HP {manager.player.health}', True, 'Purple')
        self.health_rect = self.health.get_rect(center = (700, 50))
        self.space = sub_font.render(f'press space to continue', True, (64,64,64))
        self.space_rect = self.space.get_rect(center = (400, 750))

    def render_background(self, shooting = True, over = False):
        '''
        Draws the background to the screen. Also updates the position of the lasers. 
        '''
        screen.blit(self.background, (0,0)) # sets coordinate point of top left corner for image

        if not over:
            screen.blit(self.score, self.score_rect)
            screen.blit(self.line, (0,400))
            manager.time.display_time()
            screen.blit(self.health, self.health_rect)

        if shooting:
            # draw all lasers and checks for collisions
            for item in manager.lasers:
                if item.surf: 
                    screen.blit(item.surf, item.rect)
                if item.is_enemy:
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

    def render_player(self):
        '''
        Draws player to the screen and updates the position of the player. Ends the game when the player health is zero.
        '''
        manager.player.update()
        manager.player.render()
        if manager.player.health == 0:
            manager.game_isover = True
        manager.player.pos = pygame.mouse.get_pos()

    def render_enemy(self):
        '''
        Draws the enemy sprite to the screen, moves the enemy, and creates new laser sprites periodically. 
        '''
        for enemy in manager.enemy:
            enemy.move_random()
            enemy.update()
            if random.randint(0,10) < 7:
                if enemy.shoot_cooldown < 1:
                    enemy.shoot()
            enemy.cooldown()
            screen.blit(enemy.surf,(enemy.rect))

    def level_up(self):
        '''
        When called, the level will go up by one.  
        '''
        manager.level += 1
        manager.addedEnemies = False

    def level_one(self):
        '''
        Holds all of the game logic for level one of the game. 
        '''
        manager.enemy_count = 3
        if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
            manager.enemy.add(Enemy())
        if len(manager.enemy) == manager.enemy_count:
            manager.addedEnemies = True
        if len(manager.enemy) == 0 and manager.addedEnemies:
            self.level_up()
        self.render_background()
        self.render_player()
        self.render_enemy()
        manager.player.cooldown()

    def update_highscore(self):
        '''
        Update the highscore by storing the highest score the player has made on the disk
        and changes the score variable in manager to the score
        '''
        with shelve.open('space_gladiators.txt') as sg:
            try:
                if sg['highscore'] > manager.score: # if the new score is lower than the saved one 
                    sg['highscore'] = manager.score # update the highscore in the file
            except KeyError: # this happens when the file has not been created yet, like on the first run of the game
                sg['highscore'] = manager.score 
            manager.highscore = sg['highscore']
            sg.close()

    def level_two(self):
        '''
        Holds all of the game logic for level two of the game. 
        '''
        manager.enemy_count = 6
        if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
            manager.enemy.add(Enemy())
        if len(manager.enemy) == manager.enemy_count:
            manager.addedEnemies = True
        if len(manager.enemy) == 0 and manager.addedEnemies:
            manager.score = (pygame.time.get_ticks() - manager.start_time - manager.sub_time) // 1000 # store the time when the game ended 
            self.update_highscore()
            manager.game_iswon = True
        self.render_background()
        self.render_player()
        self.render_enemy()
        manager.player.cooldown()

    def tutorial(self):
        '''
        Holds all of the game logic for the tutorial of the game
        '''
        space = False
        manager.level = 0
        if manager.tutorial_point == 0:
            display = body_font.render(f'welcome to the tutorial!', True, ('Purple'))
            space = True
        elif manager.tutorial_point == 1:
            space = False
            display = body_font.render(f'use the mouse to move', True, ('Purple'))
            if not manager.tutorial_pos_check == pygame.mouse.get_pos():
                manager.tutorial_point += 1
        elif manager.tutorial_point == 2:
            display = body_font.render(f'left click to shoot', True, ('Purple'))
        elif manager.tutorial_point == 3:
            display = body_font.render(f'hold down "a" or "d" to aim', True, ('Purple'))
        elif manager.tutorial_point == 4:
            display = body_font.render(f'shoot the enemies', True, ('Purple'))
            manager.enemy_count = 1
            if len(manager.enemy) < manager.enemy_count and not manager.addedEnemies:
                manager.enemy.add(Enemy())
            elif len(manager.enemy) == manager.enemy_count:
                manager.addedEnemies = True
            elif not (len(manager.enemy) and manager.addedEnemies):
                manager.tutorial_point += 1
        elif manager.tutorial_point == 5:
            display = body_font.render(f'tutorial complete!', True, ('Purple'))
            space = True
        else:
            manager.in_menu = True
            manager.in_tutorial = False

        display_rect = display.get_rect(center = (400, 200))
        self.render_background()
        self.render_player()
        self.render_enemy()
        screen.blit(display, display_rect)
        if space: screen.blit(self.space, self.space_rect)
        manager.tutorial_pos_check = pygame.mouse.get_pos()
        manager.player.cooldown()

    def game_over(self):
        '''
        Draws the game over image to the screen
        '''
        manager.level = 0
        self.render_background(False, True)
        screen.blit(self.game_over_img, self.game_over_img_rect)
        screen.blit(self.space, self.space_rect)

    def game_won(self):
        '''
        Draws the ending time and game won image to the screen
        '''
        manager.sub_time += clock.get_time()
        self.game_won_score = body_font.render(f'Time: {manager.score}', True, 'Purple')
        self.game_won_score_rect = self.game_won_score.get_rect(center = (400, 400))
        self.render_background(False, True)
        screen.blit(self.game_won_img, self.game_won_img_rect)
        screen.blit(self.game_won_score, self.game_won_score_rect)
        screen.blit(self.space, self.space_rect)
    
    def pause_game(self):
        '''
        Stops the clock, the laser, player, and enemy sprites, and draws the pause image to the screen
        '''
        manager.sub_time += clock.get_time()
        self.render_background(False)
        screen.blit(self.pause, self.pause_rect)
        screen.blit(self.pause1, self.pause1_rect)

class Manager():
    '''
    This represents all of the game states that the game might be in. This will be used to switch between each game state.
    '''
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
        self.game_isover = False
        self.game_iswon = False
        self.score = 'None'
        self.credit = False

        try: # updates the highscore using a file stored on the computer so that scores can be saved after exiting the game
            with shelve.open('space_gladiators.txt') as sg:
                self.highscore = sg['highscore']
                sg.close()
        except KeyError: # this occurs when the file containing the game information does not exist yet. like when first opening the game
            self.highscore = 'None'

    def reset_game(self):
        '''
        Resets all of the variables regarding the game
        '''
        self.button = 0
        self.addedEnemies = False
        self.lasers.empty()
        self.enemy.empty()
        self.player = Player()
        self.start_time = pygame.time.get_ticks()
        self.pause = False
        self.in_menu = False
        self.sub_time = 0
        self.tutorial_pos_check = pygame.mouse.get_pos()
        self.enemy_count = 1
        self.game_over = False
        self.game_won = False
        self.credit = False

    def play_music(self):
        '''
        Starts the music in game
        '''
        pygame.mixer.music.play()

    def stop_music(self):
        '''
        Stops the music in game
        '''
        pygame.mixer.music.stop()
        
manager = Manager() # we will use the manager to control the game state and store important variables

while __name__ == '__main__':
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # player pushes the x button on the window
            pygame.quit() # close the game
            exit()
        if event.type == pygame.KEYUP and event.key == pygame.K_e:
            if manager.pause == True: 
                manager.pause = False
            else: manager.pause = True
        if manager.in_menu: # updating the selected button in the menu based on what the player has pressed, w or up arrow for up and s or down arrow for down
            if event.type == pygame.KEYUP and manager.button < 2 and (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                manager.button += 1
            if event.type == pygame.KEYUP and manager.button > 0 and (event.key == pygame.K_UP or event.key == pygame.K_w):
                manager.button -= 1
            if event.type == pygame.KEYUP and manager.button == 0 and event.key == pygame.K_RETURN:
                manager.level = 1
                manager.play_music()
                manager.reset_game()
            if event.type == pygame.KEYUP and manager.button == 1 and event.key == pygame.K_RETURN:
                manager.reset_game()
                manager.tutorial_point = 0
                manager.level = 0
                manager.in_menu = False
            if event.type == pygame.KEYUP and manager.button == 2 and event.key == pygame.K_RETURN:
                manager.credit = True
                manager.in_menu = False
        if manager.credit:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                manager.in_menu = True
                manager.credit = False
        elif manager.pause:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE: # added a way to exit the game from the pause menu
                manager.reset_game()
                manager.in_menu = True
                manager.pause = False
                manager.stop_music()
        elif manager.game_isover or manager.game_iswon:
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                manager.in_menu = True
                manager.game_iswon = False 
                manager.game_isover = False
                manager.stop_music() 
        else: # when the player is not in the menu, paused, game over, or game won screen 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if pygame.mouse.get_pos()[1] > 440: 
                    if keys[pygame.K_a]:
                        manager.player.shoot(1) # shoot a laser traveling on a leftward diagonal
                    elif keys[pygame.K_d]:
                        manager.player.shoot(2) # shoot a laser traveling on a right diagonal
                    else:
                        manager.player.shoot() # shoot a laser traveling straight upwards
                else:
                    manager.lasers.add(Laser((pygame.mouse.get_pos()[0], 440), False))
        if manager.level == 0: # level zero is the tutorial screen
            if manager.tutorial_point == 0:
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE: # true when the player pushes space
                    manager.tutorial_point += 1
            elif manager.tutorial_point == 2: 
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # true when the player pushes left click
                    manager.tutorial_point += 1
            elif manager.tutorial_point == 3:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # true when the player pushes left click
                    if keys[pygame.K_a]: # true if the player is holding down the 'a' key
                        manager.tutorial_point += 1
                    elif keys[pygame.K_d]: # true if the player is holding down the 'd' key
                        manager.tutorial_point += 1
            elif manager.tutorial_point == 5: 
                if event.type == pygame.KEYUP and event.key == pygame.K_SPACE: 
                    manager.in_menu = True

    keys = pygame.key.get_pressed() # stores a string of bools of which keys are pressed in keys 

    # these are checking bools in the manager to see which state the game is in
    # depending on which is true it will show the game screen that represents the true bool
    if manager.in_menu:
        GameMenu().render()
    elif manager.credit:
        GameMenu().credit()
    elif manager.game_isover:
        GameActive().game_over()
    elif manager.game_iswon:
        GameActive().game_won()
    elif manager.pause:
        GameActive().pause_game()
    elif manager.level == 2:
        GameActive().level_two()
    elif manager.level == 1:
        GameActive().level_one()
    elif manager.level == 0:
        GameActive().tutorial()
 
    pygame.display.update() # updates the display
    clock.tick(60) # set maximum frames per second
