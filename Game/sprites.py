import pygame as pg
from settings import *
from pygame.locals import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.file = 'Assets/Knight.png'
        self.image = pg.image.load(self.file)
        self.groups = game.all_sprites
        self.rect = self.image.get_rect()
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        
        self.game.screen.blit(self.image,self.rect)
  
        self.x = x
        self.y = y
     
    
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy
            if(dx!=0)and(dy==0):
            {
                self.image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            }

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy+1:
                return True
        print("tilecords")
        print(self.x+dx,self.y+dy)
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
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
       
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.game.screen.blit(self.image,self.rect)

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y, wallType):
        self.groups = game.all_sprites, game.walls
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
            self.image = pg.image.load('Assets/Top Right Upper Wall.png')
        if wallType == '5':
            self.image = pg.image.load('Assets/Top Left Upper Wall.png')
        if wallType == '6':
            self.image = pg.image.load('Assets/Top Right Upper Wall.png')
        if wallType == '7':
            self.image = pg.image.load('Assets/Left Wall.png')
        if wallType == '8':
            self.image = pg.image.load('Assets/Right Wall.png')
        if wallType == 'm':
            self.image = pg.image.load('Assets/Bottom Wall.png')
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.game.screen.blit(self.image,self.rect)
#class tile(self,TileName,x,y):
  
