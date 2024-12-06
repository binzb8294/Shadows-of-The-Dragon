# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300,300)
        self.load_data()

    
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.currentMap=0
        self.map_list = []
        self.map_data_L1R1 = []
        self.map_data_L1R2 = []
        self.map_data_L1R3 = []
        with open(path.join(game_folder, 'Maps/L1R1.txt'), 'rt') as f:
            for line in f:
                self.map_data_L1R1.append(line)
        self.map_list.append(self.map_data_L1R1)
        with open(path.join(game_folder, 'Maps/L1R2.txt'), 'rt') as f:
            for line in f:
                self.map_data_L1R2.append(line)
        self.map_list.append(self.map_data_L1R2)
        with open(path.join(game_folder, 'Maps/L1R3.txt'), 'rt') as f:
            for line in f:
                self.map_data_L1R3.append(line)
        self.map_list.append(self.map_data_L1R3)
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.load_data()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.tiles = pg.sprite.Group()
        self.holes = pg.sprite.Group()
        self.players = pg.sprite.Group()
        self.player = Player(self,-1,-1)
        self.enemyList = [];
        self.numEnemies = 0
        self.createMap()
        #self.enemy = Enemy(self, 15, 15, 1, "enemy 1", False)
        #self.enemy2 = Enemy(self, 18, 18, 0, "enemy 2", False)
        


      # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def changeMap(self,mapChange):
        self.currentMap += mapChange
        print('After change')
        print(self.currentMap)
    def createMap(self):
         print('born')
         enemyNumber=1
         self.resetMap()
         XAdjust = (WIDTH/TILESIZE/2)-(len(self.map_list[0][self.currentMap])/2)
         YAdjust = (HEIGHT/TILESIZE/2)-(len(self.map_list[self.currentMap])/2)
         for row, tiles in enumerate(self.map_list[self.currentMap]):
             for col, tile in enumerate(tiles):
                 if tile == ".":
                     floorTile(self,col+XAdjust,row+YAdjust)
                 elif tile == 'P':
                     Hole(self,col+XAdjust,row+YAdjust,-1)
                 elif tile == 'E':
                     floorTile(self,col+XAdjust,row+YAdjust)
                 elif tile == 'H':
                     Hole(self,col+XAdjust,row+YAdjust,1)
                 elif tile == 'M':
                     Wall(self,col+XAdjust,row+YAdjust,tile)
                 elif tile == '\n':
                     pass
                 else:
                     Wall(self,col+XAdjust,row+YAdjust,tile)


         for row, tiles in enumerate(self.map_list[self.currentMap]):
             for col, tile in enumerate(tiles):
                 if tile == 'P':
                      self.player=Player(self,col+XAdjust,row+YAdjust-1,self.player.level,self.player.exp,self.player.health)
                      self.killClones(self.player)
                 elif tile == 'E':
                      self.enemyList.append(Enemy(self,col+XAdjust,row+YAdjust,random.randint(0,1),"Enemy "+str(enemyNumber), False))
                      enemyNumber+=1
                      self.numEnemies+=1
    def quit(self):
        pg.quit()
        sys.exit()
    def killClones(self,myPlayer):
        for Player in self.players:
            if Player != myPlayer:
                Player.kill()
    def resetMap(self):
        for tile in self.tiles:
            tile.kill()
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
                for enemy in self.enemyList:
                    enemy.setDistance()
                for enemy in self.enemyList:
                    enemy.setDiagonal()
                #PLAYER MOVEMENT
                if event.key == pg.K_LEFT:
                    enemyInTheWay = False
                    for enemy in self.enemyList:
                        if (enemy.x < self.player.x and enemy.distance == 0 and enemy.diagonal == False):
                            enemyInTheWay = True
                    if enemyInTheWay == False:
                        self.player.move(dx=-1)
                if event.key == pg.K_RIGHT:
                    enemyInTheWay = False
                    for enemy in self.enemyList:
                        if (enemy.x > self.player.x and enemy.distance == 0 and enemy.diagonal == False):
                            enemyInTheWay = True
                    if enemyInTheWay == False:
                        self.player.move(dx=1)
                    
                if event.key == pg.K_UP:
                    enemyInTheWay = False
                    for enemy in self.enemyList:
                        if (enemy.y < self.player.y and enemy.distance == 0 and enemy.diagonal == False):
                            enemyInTheWay = True
                    if enemyInTheWay == False:
                        self.player.move(dy=-1)
                  
                if event.key == pg.K_DOWN:
                    enemyInTheWay = False
                    for enemy in self.enemyList:
                        if (enemy.y > self.player.y and enemy.distance == 0 and enemy.diagonal == False):
                            enemyInTheWay = True
                    if enemyInTheWay == False:
                        self.player.move(dy=1)
                    

       
                if event.key == pg.K_SPACE:
                    for enemy in self.enemyList:
                        if(enemy.distance == 1 and enemy.diagonal == True) or (enemy.distance == 0 and enemy.diagonal == False):
                            enemy.damage(False)
                 
                    '''
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
                '''
                #Enemy attacks
                #self.enemy.moved = False
                #self.enemy2.moved = False
                for enemy in self.enemyList:
                    enemy.moved=False
          
                for enemy in self.enemyList:
                    enemy.setDistance()
                for enemy in self.enemyList:
                    enemy.setDiagonal()
                for enemy in self.enemyList:
                    self.player.damage(enemy.attack(enemy.distance,enemy.diagonal))
                '''
                if self.enemy.dead == False: 
                    self.player.damage(self.enemy.attack(distance, diagonal))
                if self.enemy2.dead == False: 
                    self.player.damage(self.enemy2.attack(distance2, diagonal2))
                '''
                #Enemy move
                for enemy in self.enemyList:
                    if enemy.dead == False:
                        if enemy.AI == 0:
                            enemy.move_random(enemy.x, enemy.y, self.player.x, self.player.y)
                        if enemy.AI == 1:
                            enemy.move_target(enemy.x, enemy.y, self.player.x, self.player.y)
                '''
                if self.enemy.dead == False:
                    if self.enemy.AI == 0:
                        self.enemy.move_random(self.enemy.x, self.enemy.y, self.player.x, self.player.y)
                    if self.enemy.AI == 1:
                        self.enemy.move_target(self.enemy.x, self.enemy.y, self.player.x, self.player.y)
                '''

                    
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


'''
future bug fixes:
    - enemies disappear randomly
    - enemies move and attack after death
    - enemies and players will overlap
'''
