import pygame as pg
import random
import math
from settings import *
from pygame.locals import *
import time
from PIL import Image
#PIL must be installed
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y, level=1, exp=0, health=40, a=1):
        self.file = 'Assets/Knight.png'
        self.flipped = False
        self.knightImage = pg.image.load(self.file)
        self.reversedKnightImage = pg.transform.flip(self.knightImage,True,False)
        self.groups = game.all_sprites
        self.image = self.knightImage
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect.x=-40
        self.rect.y=-40
        self.game.screen.blit(self.image,self.rect)
        self.level=level
        self.exp=exp
        self.health=health
        self.x = x
        self.y = y
        self.atk = a
        self.coordList = []
        self.maxHP=40
  
    def move(self, dx=0, dy=0):
        if(dx==1):
                self.image = self.knightImage
                self.flipped = False
        if(dx==-1):
                self.image = self.reversedKnightImage
                self.flipped = True
        if (not self.collide_with_walls(dx, dy)) and (not self.collide_with_enemy(dx, dy)):
            self.x += dx
          
            self.y += dy
            
   
            self.enterHole(dx,dy)
            self.updateCoordinates()
           
    def damage(self, h):
        if h != 0:
            self.health -= h
            print(f"You lost 1 HP. {self.health} HP remaining!")
            #print(f"health = {self.health}")
        if self.health <= 0:
            print("dead")  
            self.game.gameOver()
    def updateCoordinates(self):
        
        Width = math.ceil(self.rect.width/16)
        Height = math.ceil(self.rect.height/16)
        for coord in self.coordList:
            self.coordList.remove(coord)
        for x in range(0,Width):
            for y in range(0,Height):
                self.coordList.append(coordinate(x+self.x,y+self.y))
       
   
    def enterHole(self, dx=0,dy=0):
        for Hole in self.game.holes:
            if Hole.x == self.x and Hole.y-1 == self.y:
                if Hole.Type == 1:
                    if self.game.currentMap != len(self.game.map_list)-1:
                        self.game.changeMap(Hole.Type)
                        self.game.createMap()
                        #self.game.resetMap()
                    else:
                        self.game.victory()
                        print('victory')
                '''
                if Hole.Type == -1:
                    if self.game.currentMap != 0:
                        self.game.changeMap(Hole.Type)
                        self.game.createMap()
                        #self.game.resetMap()
                 '''   
                        
    def setPosition(self,sx=0,sy=0):        
        self.x=sx
        self.y=sy
        self.game.screen.blit(self.image,self.rect)

    
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy+1:
                return True
        return False
    def collide_with_enemy(self, dx=0, dy=0):
        for enemy in self.game.enemyList:
            for coordS in self.coordList:
                for coordE in enemy.coordList:
                    if coordE.x == coordS.x +dx and coordE.y == coordS.y+dy:
                        return True
        return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        self.updateCoordinates()
        pg.time.wait(10)
        
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
        self.image = pg.image.load('Assets/Animations/Ghoul/Ghoul.png')
        self.rect = self.image.get_rect()
        print(self.rect)
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
        self.coordList = []
        self.updateCoordinates()
    def setDistance(self):
        self.distance = round((abs(self.game.player.x - self.x) + abs(self.game.player.y - self.y))/2)
        #print(f"enemy name: {self.name}. Distance: {self.distance}")
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
            print(f"{self.name} lost 3 points of hp. {self.health} points remaining!")
        else:
            self.health -= 1
            print(f"{self.name} lost 1 point of hp. {self.health} points remaining!")
        if self.health <= 0:
            print(f"{self.name} has been defeated")
            self.image.fill(WHITE)
            self.dead = True
            self.game.enemyList.remove(self)
            self.kill()
            
            
    def updateCoordinates(self):
        for coord in self.coordList:
            self.coordList.remove(coord)
        Width = math.ceil(self.rect.width/16)
        Height = math.ceil(self.rect.height/16)
        for x in range(0,Width):
            for y in range(0,Height):
                self.coordList.append(coordinate(x+self.x,y+self.y))
        '''
        print("post update enemy")
        for coord in self.coordList:
            print(coord.x,coord.y)
        '''
    def move(self, dx=0, dy=0):
        if (not self.collide_with_walls(dx,dy)) and (not self.collide_with_player(dx,dy)):
            self.x += dx
            self.y += dy
        for enemy in self.game.enemyList:
            if not enemy.name == self.name:
                if enemy.x == self.x and enemy.y == self.y:
                    self.move(-1*dx, -1*dy)
        if self.x == self.game.player.x and self.y == self.game.player.y:
            self.move(-1*dx, -1*dx)
        self.updateCoordinates()
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
        self.updateCoordinates()
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            for coordS in self.coordList:
                if wall.x == coordS.x + dx and wall.y == coordS.y + dy:
                    return True
        return False
    def collide_with_player(self, dx=0, dy=0):
        for coordS in self.coordList:
            if self.game.player.x == coordS.x + dx and self.game.player.y == coordS.y + dy:
                return True
        return False
    
    def collide_with_enemy(self, dx=0, dy=0):
        
        for enemy in self.game.enemyList:
            for coordS in self.coordList:
                for coordE in enemy.coordList:
                    if coordE.x == coordS.x +dx and coordE.y == coordS.y+dy:
                        return True
        
        return False
class coordinate():
    def __init__(self,x,y):
        self.x=x
        self.y=y
        
class Background(pg.sprite.Sprite):
    def __init__(self,game,x,y,image):
        self.groups=game.all_sprites,game.tiles
        pg.sprite.Sprite.__init__(self, self.groups)
        
        self.image = image
     
        self.game = game
        
        self.rect = self.image.get_rect()
        self.rect.width = WIDTH
        self.rect.height = HEIGHT
        self.x = x
        self.y = y
        self.rect.x = 0
        self.rect.y = 0
        self.game.screen.blit(self.image,(0,0))
class HealthBar():
    def __init__(self, game):
        self.x = 0
        self.y = 0
        self.w = 1024
        self.h = 32
        self.game=game
        
        self.max_hp = self.game.player.health
        self.hp = self.max_hp
        self.image=Image.new('RGB',(self.w,self.h),'red')
        self.image2=Image.new('RGB',(self.w,self.h),'green')
        
        self.RedPart = pg.image.fromstring(self.image.tobytes(),self.image.size,self.image.mode)
        self.GreenPart = pg.image.fromstring(self.image2.tobytes(),self.image2.size,self.image2.mode)
        self.rect = self.RedPart.get_rect()
        self.rect.center = self.w//2, self.h//2
        self.game.screen.blit(self.RedPart,(0,0))
        self.game.screen.blit(self.GreenPart,(0,0))                   
    def draw(self):
  #calculate health ratio
        
        ratio = self.hp / self.max_hp
        #self.drawing=pg.draw.rect(self.game.screen, RED, (self.x, self.y, self.w*ratio, self.h))
        self.image2 = Image.new('RGB',(int(self.w*ratio),self.h),'green')
        GreenPart = pg.image.fromstring(self.image2.tobytes(),self.image2.size,self.image2.mode)
        
        pg.display.update()
        pg.display.flip()
    def update(self):
        self.hp=self.game.player.health
        self.draw()
        pg.display.flip()
        pg.display.update()
