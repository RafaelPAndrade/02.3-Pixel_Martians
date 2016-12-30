#coding: utf-8

import constants
from block import Block
import pygame
import pointing

class Alien(Block):
    
    def __init__(self,x,y,color):
        super(Alien, self).__init__(x,y,20,20,color)
        self.dir_x = 1
        self.dir_y = 0
        self.value = 0
        self.Bomb = None
        
    def set_value(self,color):
        self.color = color
        if self.color == constants.GREY:
            self.value = 10
        elif self.color == constants.RED:
            self.value = 20
        elif self.color == constants.BLUE:
            self.value = 30
        elif self.color == constants.GREEN:
            self.value = 40
            

                
    def update(self):
        self.rect.x += self.dir_x
        self.rect.y += self.dir_y