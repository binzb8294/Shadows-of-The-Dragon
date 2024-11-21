# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()

        
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data =[]
        with open(path.join(game_folder, 'Maps/map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.createMap()
       


      # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
            
    def createMap(self):
         XAdjust = (WIDTH/TILESIZE/2)-(len(self.map_data[0])/2)
         YAdjust = (HEIGHT/TILESIZE/2)-(len(self.map_data)/2)
         for row, tiles in enumerate(self.map_data):
             for col, tile in enumerate(tiles):
                 if tile == ".":
                     floorTile(self,col+YAdjust,row+XAdjust)
                 elif tile == 'P':
                     floorTile(self,col+YAdjust,row+XAdjust)
                 else:
                     Wall(self,col+YAdjust,row+XAdjust,tile)
           
         for row, tiles in enumerate(self.map_data):
             for col, tile in enumerate(tiles):
                 if tile == 'P':
                     self.player = Player(self,col+XAdjust,row+YAdjust)
    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    

    def draw(self):
        self.screen.fill(BGCOLOR)
    
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx=1)
                if event.key == pg.K_UP:
                    self.player.move(dy=-1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy=1)

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
