import pygame as pg
from settings import *
import random

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.health = 25
    
    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx,dy):
            self.x += dx
            self.y += dy

    def damage(self, h):
        if h != 0:
            self.health -= h
            print("damaged")
        if self.health <= 0:
            print("dead")
         
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y, AI, n, d):
        self.groups = game.all_sprites
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

    def attack(self, distance, diagonal):
        if (distance == 1 and diagonal == True) or (distance == 0 and diagonal == False):
            self.moved == True
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
            self.dead == True

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
    
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        
