#coding: latin-1

import pygame
import constants
from block import Block
from bullet import Bullet


class Ship(Block):
    def __init__(self,x,color):
        super(Ship, self).__init__ (x,constants.SCREEN_HEIGHT-60,30,30,color)
        self.dir_x = 0
    
    def move_left(self):
        self.dir_x = -constants.VEL
        
    def move_right(self):
        self.dir_x = constants.VEL
    
    def shooting (self,Proj):
        Proj = Bullet(self.rect.x-13,constants.SCREEN_HEIGHT-60,1)
        
    def dont_move(self):
        self.dir_x = constants.NULL        
        
    
    def update(self):
        self.rect.x += self.dir_x
        if self.rect.x >= constants.SCREEN_WIDTH-30:
            self.rect.x = constants.SCREEN_WIDTH-30
        elif self.rect.x <= 0:
            self.rect.x = 0
        
    
    