#coding: utf-8

import pygame
from block import Block
import constants
import pointing


class Bullet(Block):
    def __init__(self,x,y,sign,speed):
        super(Bullet, self).__init__(x,y,10,10,constants.YELLOW)
        self.dir_x = 0
        self.dir_y = -1*sign*speed
        self.shot = None
        self.shield = None
        self.bomb = None
        self.points = 0
        self.sign = 0
        self.destroy = False
        
        if self.dir_y < 0:
            self.destroy = True
        
        
    def set_shot(self, shot):
        self.shot=shot
    
    def set_shield(self, shield):
        self.shield = shield
        
    def set_bomb(self, bomb):
        self.bomb = bomb   
        
    def update(self):
        self.rect.y += self.dir_y
        if self.rect.y < 0 or self.rect.y >= constants.SCREEN_HEIGHT:
            self.kill()
            pointing.gunfired = False
        
        shotted_list = pygame.sprite.spritecollide(self, self.shot, True)
        if len(shotted_list)>0 and self.dir_y < 0:
            self.kill()
            pointing.gunfired = False
            if shotted_list[0].dir_y ==0:
                pointing.points += shotted_list[0].value
        elif len(shotted_list)>0 and self.dir_y > 0:
            self.kill()
        
        shotted_list2 = pygame.sprite.spritecollide(self,self.shield, True)
        if len(shotted_list2)>0:
            self.kill()
            pointing.gunfired = False
        
        if self.destroy == True:
            shotted_list3 = pygame.sprite.spritecollide(self,self.bomb,self.destroy)
            if len(shotted_list3)>0:
                self.kill()
                pointing.gunfired = False
                                                    
