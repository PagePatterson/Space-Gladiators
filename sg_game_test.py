import unittest
import sg_game
import random
import pygame

class TimeTester(unittest.TestCase):
    @staticmethod
    def mkTime():
        return sg_game.Time()

    def test_display_time(self): # test that the initial time is zero
        time = TimeTester.mkTime()
        self.assertLess(time.display_time(False), 1)

class LaserTester(unittest.TestCase):
    def test_isenemy(self): # test enemy lasers are enemies and player lasers are not
        l1 = sg_game.Laser((0,0), True)
        l2 = sg_game.Laser((0,0), False)
        self.assertTrue(l1.is_enemy)
        self.assertFalse(l2.is_enemy)

class PewPewTester(unittest.TestCase):
    @staticmethod
    def mkPew():
        return sg_game.PewPew()

    def test_hit(self): # test the health goes down by one when hit
        sprite = PewPewTester.mkPew()
        sprite.health = random.randint(1, 100)
        h1 = sprite.health
        sprite.hit()
        h2 = sprite.health
        self.assertEqual(h2, h1 - 1)
    
    def test_cooldown(self): # test that the cooldown for the hit and shoot go down
        sprite = PewPewTester.mkPew()
        sprite.hit_cooldown = random.randint(1, 10)
        sprite.shoot_cooldown = random.randint(1, 10)
        h1 = sprite.hit_cooldown
        s1 = sprite.shoot_cooldown
        sprite.cooldown()
        h2 = sprite.hit_cooldown
        s2 = sprite.shoot_cooldown
        self.assertEqual(h2, h1 - 1)
        self.assertEqual(s2, s1 - 1)

    def test_move_random(self): # test that the sprite moves 
        sprite = PewPewTester.mkPew()
        sprite.surf = pygame.image.load('images/skin1.png').convert_alpha()
        sprite.surf = pygame.transform.rotozoom(sprite.surf,0,3)
        sprite.posx = random.randint(100,700)
        sprite.posy = random.randint(100,300)
        sprite.rand_move = random.randint(0, 7)
        ps1 = (sprite.posx, sprite.posy)
        sprite.move_random()
        ps2 = (sprite.posx, sprite.posy)
        self.assertNotEqual(ps1, ps2)

    def test_moveLeft(self): # test that the x position of our sprite decreases by 5, which is also left by 5 pixels
        sprite = PewPewTester.mkPew()
        sprite.posx = random.randint(100,700)
        p1 = sprite.posx
        sprite.move_left()
        p2 = sprite.posx
        self.assertEqual(p2, p1-5)

    def test_moveRight(self): # test that the x position of our sprite increases by 5
        sprite = PewPewTester.mkPew()
        sprite.posx = random.randint(100,700)
        p1 = sprite.posx
        sprite.move_right()
        p2 = sprite.posx
        self.assertEqual(p2, p1+5)

    def test_move_up(self): # test that the y position of our sprite decreases by 5, which is also up by 5 pixels
        sprite = PewPewTester.mkPew()
        sprite.posy = random.randint(100,300)
        p1 = sprite.posy
        sprite.move_up()
        p2 = sprite.posy
        self.assertEqual(p2, p1-5)

    def test_moveDown(self): # test that the y position of our sprite increase by 5
        sprite = PewPewTester.mkPew()
        sprite.posy = random.randint(100,300)
        p1 = sprite.posy
        sprite.move_down()
        p2 = sprite.posy
        self.assertEqual(p2, p1+5)

    def test_shoot(self): # test that the shoot cooldown is updated
        sprite = PewPewTester.mkPew()
        sprite.pos = (random.randint(1,799),random.randint(1,399))
        sprite.shoot()
        self.assertEqual(sprite.shoot_cooldown, 10)

    def test_update(self): # test that the position of the sprite will be updated to the x and y position of the sprite
        sprite = PewPewTester.mkPew()
        sprite.surf = pygame.image.load('images/skin1.png').convert_alpha()
        sprite.surf = pygame.transform.rotozoom(sprite.surf,0,3)
        sprite.health = 10
        sprite.pos = (random.randint(100,199),random.randint(1,199))
        sprite.posx = random.randint(200, 300)
        sprite.posy = random.randint(200, 300)
        sprite.update()
        self.assertEqual(sprite.pos, (sprite.posx, sprite.posy))

class PlayerTester(unittest.TestCase):
    def test_player(self): # test that the initial values for the player are correct and it is not classified as an enemy
        p1 = sg_game.Player()
        self.assertEqual(p1.health, 10)
        self.assertFalse(p1.enemy)
    
class EnemyTester(unittest.TestCase):
    def test_enemy(self): # test that the position of the enemy is not outside its range 
        e1 = sg_game.Enemy()
        self.assertEqual(e1.health, 2)
        self.assertLess(e1.pos, (801, 400))
        self.assertTrue(e1.enemy)

class GameMenuTester(unittest.TestCase):
    @staticmethod
    def mkGM():
        return sg_game.GameMenu()

    def test_render(self): # test that the menu text changed based on which button is selected
        gm = GameMenuTester.mkGM()
        t1 = gm.text1
        gm.render()
        t2 = gm.text1
        self.assertNotEqual(t1, t2)

class GameActiveTester(unittest.TestCase):
    @staticmethod
    def mkGA():
        return sg_game.GameActive()

    def test_level_up(self): # test level goes up when level up is called
        GA = GameActiveTester.mkGA()
        sg_game.manager.addedEnemies = True
        lvl_before = sg_game.manager.level
        GA.level_up()
        lvl_after = sg_game.manager.level
        self.assertEqual(lvl_after, lvl_before + 1)
        self.assertFalse(sg_game.manager.addedEnemies)

    def test_level_one(self): # test that the added enemies bool will become true when the enemies have been added
        GA = GameActiveTester.mkGA()
        sg_game.manager.addedEnemies = False
        for i in range(3): # we know that 3 enemies need to be added so we call the function 3 times
            GA.level_one()
        self.assertTrue(sg_game.manager.addedEnemies)

    def test_level_two(self):
        GA = GameActiveTester.mkGA()
        sg_game.manager.addedEnemies = False
        for i in range(6): # we know that 6 enemies need to be added so we call the function 3 times
            GA.level_two()
        self.assertTrue(sg_game.manager.addedEnemies)

    def test_game_over(self): # test that the level variable resets to zero
        GA = GameActiveTester.mkGA()
        sg_game.manager.level = 2
        GA.game_over()
        self.assertEqual(sg_game.manager.level, 0)

class ManagerTester(unittest.TestCase):
    @staticmethod
    def mkMan():
        return sg_game.Manager()

    def test_reset_game(self): # test that the manager button resets to zero
        manage = ManagerTester.mkMan()
        manage.button = 2
        manage.reset_game()
        self.assertEqual(manage.button, 0)

if __name__ == '__main__':
    unittest.main()
