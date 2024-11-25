# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
import random
from settings import *
from sprites import *

bg = pg.image.load("/Users/3047266/Downloads/Shadows of the Dragon/map.png")
class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.player = Player(self, 10, 10)
        self.enemy = Enemy(self, 15, 15, 1, "enemy 1", False)
        self.enemy2 = Enemy(self, 18, 18, 0, "enemy 2", False)
        
        for x in range(10, 20):
            Wall(self, x, 5)
            
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                distance = round((abs(self.player.x - self.enemy.x) + abs(self.player.y - self.enemy.y))/2)
                distance2 = round((abs(self.player.x - self.enemy2.x) + abs(self.player.y - self.enemy2.y))/2)
                if self.player.x == self.enemy.x or self.player.y == self.enemy.y:
                    diagonal = False
                else:
                    diagonal = True
                if self.player.x == self.enemy2.x or self.player.y == self.enemy2.y:
                    diagonal2 = False
                else:
                    diagonal2 = True
                #PLAYER MOVEMENT
                if event.key == pg.K_LEFT:
                    if (not(self.enemy.x < self.player.x and distance == 0 and diagonal == False)) and (not(self.enemy2.x < self.player.x and distance2 == 0 and diagonal2 == False)):
                        self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    if (not(self.enemy.x > self.player.x and distance == 0 and diagonal == False)) and (not(self.enemy2.x > self.player.x and distance2 == 0 and diagonal2 == False)):
                        self.player.move(dx=1)
                if event.key == pg.K_UP:
                    if (not(self.enemy.y < self.player.y and distance == 0 and diagonal == False)) and (not(self.enemy2.y < self.player.y and distance2 == 0 and diagonal2 == False)):
                        self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    if (not(self.enemy.y > self.player.y and distance == 0 and diagonal == False)) and (not(self.enemy2.y > self.player.y and distance2 == 0 and diagonal2 == False)):
                        self.player.move(dy=1)

                miss_count = 0 #number of enemies
                if event.key == pg.K_SPACE:
                    if (distance == 1 and diagonal == True) or (distance == 0 and diagonal == False):
                        self.enemy.damage(False)
                    else:
                        miss_count += 1
                    if (distance2 == 1 and diagonal2 == True) or (distance2 == 0 and diagonal2 == False):
                        self.enemy2.damage(False)
                    else:
                        miss_count += 1
                    if miss_count == 2:
                        system.out.print("no enemy nearby")
                print(f"enemy 1 distance away: {distance}\nenemy 2 distance away: {distance2}")
                        
                #Enemy attacks
                self.enemy.moved = False
                self.enemy2.moved = False
                
                distance = round((abs(self.player.x - self.enemy.x) + abs(self.player.y - self.enemy.y))/2)
                distance2 = round((abs(self.player.x - self.enemy2.x) + abs(self.player.y - self.enemy2.y))/2)
                if self.player.x == self.enemy.x or self.player.y == self.enemy.y:
                    diagonal = False
                else:
                    diagonal = True
                if self.player.x == self.enemy2.x or self.player.y == self.enemy2.y:
                    diagonal2 = False
                else:
                    diagonal2 = True

                if self.enemy.dead == False: 
                    self.player.damage(self.enemy.attack(distance, diagonal))
                if self.enemy2.dead == False: 
                    self.player.damage(self.enemy2.attack(distance2, diagonal2))
                
                #Enemy moves
                if self.enemy.dead == False:
                    if self.enemy.AI == 0:
                        self.enemy.move_random(self.enemy.x, self.enemy.y, self.player.x, self.player.y)
                    if self.enemy.AI == 1:
                        self.enemy.move_target(self.enemy.x, self.enemy.y, self.player.x, self.player.y)
                if self.enemy2.dead == False:
                    if self.enemy2.AI == 0:
                        self.enemy2.move_random(self.enemy2.x, self.enemy2.y, self.player.x, self.player.y)
                    if self.enemy2.AI == 1:
                        self.enemy2.move_target(self.enemy2.x, self.enemy2.y, self.player.x, self.player.y)

                    
                if event.key == pg.K_ESCAPE:
                    self.quit()

                #TURN ACTIONS
                    ###

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
