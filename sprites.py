import pygame as pg
import random
from settings import *
from pygame.locals import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, level=1, exp=0, health=25, a=1):
        self.file = 'Assets/Knight.png'
        self.image = pg.image.load(self.file)
        self.groups = game.all_sprites
        
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.game.screen.blit(self.image,self.rect)
        self.level=level
        self.exp=exp
        self.health=health
        self.x = x
        self.y = y
        self.atk = a
        
    def damage(self, h):
        if h != 0:
            self.health -= h
            print("damaged")
            print(f"health = {self.health}")
        if self.health <= 0:
            print("dead")  
            self.game.quit()
            
    def move(self, dx=0, dy=0):
        if (not self.collide_with_walls(dx, dy)) and (not self.collide_with_enemy(dx, dy)):
            self.x += dx
            self.y += dy
            self.enterHole(dx,dy)
            
    def enterHole(self, dx=0,dy=0):
        for Hole in self.game.holes:
            if Hole.x == self.x and Hole.y-1 == self.y:
                if Hole.Type == 1:
                    if self.game.currentMap != len(self.game.map_list)-1:
                        self.game.changeMap(Hole.Type)
                        self.game.createMap()
                        #self.game.resetMap()
                        for enemy in self.game.enemyList:
                            print(enemy.name)
                if Hole.Type == -1:
                    if self.game.currentMap != 0:
                        self.game.changeMap(Hole.Type)
                        self.game.createMap()
                        #self.game.resetMap()
                        for enemy in self.game.enemyList:
                            print(enemy.name)
                        
    def setPosition(self,sx=0,sy=0):        
        self.x=sx
        self.y=sy
        self.game.screen.blit(self.image,self.rect)
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy+1:
                return True
    def collide_with_enemy(self, dx=0, dy=0):
        for enemy in self.game.enemyList:
            if enemy.x == self.x + dx and enemy.y == self.y + dy+1:
                return True
        '''
        print("tilecords")
        print(self.x,self.y)
        '''
        return False
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
       
class floorTile(pg.sprite.Sprite):
    def __init__(self,game,x,y):
        self.file = 'Assets/Floor Tile.png'
        self.image = pg.image.load(self.file)
        self.groups = game.all_sprites, game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
       
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #self.game.screen.blit(self.image,self.rect)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, wallType):
        self.groups = game.all_sprites, game.walls, game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        if wallType == '1':
            self.image = pg.image.load('Assets/Top Wall.png')
        if wallType == '2':
            self.image = pg.image.load('Assets/Upper Wall.png')
        if wallType == '3':
            self.image = pg.image.load('Assets/Top Left Corner.png')
        if wallType == '4':
            self.image = pg.image.load('Assets/Top Right Corner.png')
        if wallType == '5':
            self.image = pg.image.load('Assets/Top Left Upper Wall.png')
        if wallType == '6':
            self.image = pg.image.load('Assets/Top Right Upper Wall.png')
        if wallType == '7':
            self.image = pg.image.load('Assets/Left Wall.png')
        if wallType == '8':
            self.image = pg.image.load('Assets/Right Wall.png')
        if wallType == '9':
            self.image = pg.image.load('Assets/Bottom Left Corner.png')
        if wallType == '0':
            self.image = pg.image.load('Assets/Bottom Right Corner.png')
        if wallType == 'M':
            self.image = pg.image.load('Assets/Bottom Wall.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        #self.game.screen.blit(self.image,self.rect)
class Hole(pg.sprite.Sprite):
    def __init__(self, game, x, y, Type):
          self.groups = game.all_sprites, game.holes, game.tiles
          pg.sprite.Sprite.__init__(self, self.groups)
          self.game = game
          self.image = pg.image.load('Assets/Hole.png')
          self.rect = self.image.get_rect()
          self.Type=Type
          self.x = x
          self.y = y
          '''
          print('holecords')
          print(x)
          print(y)
          '''
          self.rect.x = x * TILESIZE
          self.rect.y = y * TILESIZE
class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, AI, n, d, a=1):
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y 
        self.AI = AI
        self.name = n
        self.health = 5
        self.dead = d
        self.moved = False
        self.diagonal = False
        self.distance = 0
        self.atk = a
        
    def setDistance(self):
        self.distance = round((abs(self.game.player.x - self.x) + abs(self.game.player.y - self.y))/2)

    def setDiagonal(self):
        if self.game.player.x == self.x or self.game.player.y == self.y:
            self.diagonal = False
        else:
            self.diagonal = True
            
    def attack(self, distance, diagonal):
        if (distance == 1 and diagonal == True) or (distance == 0 and diagonal == False):
            self.moved = True
            return 1
        else:
            return 0
    
    def damage(self, crit):
        if crit == True:
            self.health -= 3
        else:
            self.health -= 1
        if self.health <= 0:
            print(f"{self.name} has been defeated")
            self.image.fill(WHITE)
            self.dead = True

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy
            
    #ex = enemy.x, ey = enemy.y, px = player.x, py = player.y
    def move_random(self, ex, ey, px, py):
        if self.moved == False:
            enemy_movement_direction = random.randint(1,4)
            if enemy_movement_direction == 1:
                if not (ex == px+1):
                    self.move(dx=-1)
            if enemy_movement_direction == 2:
                if not (ex == px-1):
                    self.move(dx=1)
            if enemy_movement_direction == 3:
                if not (ey == py+1):
                    self.move(dy=-1)
            if enemy_movement_direction == 4:
                if not (ey == py-1):
                    self.move(dy=1)
        self.moved = True
        
                
    def move_target(self, ex, ey, px, py):
        if self.moved == False:
            enemy_movement_direction = random.randint(1,2)

            #if player to the left
            if px < ex:
                #if player above
                if py < ey:
                    if enemy_movement_direction == 1:
                        self.move(dx=-1)
                    else:
                        self.move(dy=-1)
                #if player below
                elif py > ey:
                    if enemy_movement_direction == 1:
                        self.move(dx=-1)
                    else:
                        self.move(dy=1)
                #if y values are equal
                else:
                    self.move(dx=-1)
            #if player to the right
            elif px > ex:
                #if player above
                if py < ey:
                    if enemy_movement_direction == 1:
                        self.move(dx=1)
                    else:
                        self.move(dy=-1)
                #if player below
                elif py > ey:
                    if enemy_movement_direction == 1:
                        self.move(dx=1)
                    else:
                        self.move(dy=1)
                #if y values are equal
                else:
                    self.move(dx=1)
            #if x values are equal
            else:
                #if player above
                if py < ey:
                    self.move(dy=-1)
                #if player below
                elif py > ey:
                    self.move(dy=1)
                #if y values are equal
                else:
                    print("error: enemy and player are on the same tile")
        self.moved = True
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
