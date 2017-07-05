#coding: utf-8

import constants
from block import Block
from bullet import Bullet
import pygame

class Alien(Block):

	def __init__(self,x,y,color, targets_group):
		super(Alien, self).__init__(x,y,20,20,color)
		self.dir_x = 1
		self.dir_y = 0
		self.color = color
		if self.color == constants.GREY:
			self.value = 10
		elif self.color == constants.RED:
			self.value = 20
		elif self.color == constants.BLUE:
			self.value = 30
		elif self.color == constants.GREEN:
			self.value = 40
		#Setting the list of target objects
		if isinstance(targets_group, pygame.sprite.Group):
			self.to_destroy= targets_group
		else:
			self.to_destroy= None



	def shooting(self):
		name = Bullet(self.rect.x+ 10, self.rect.y, -1, 1, self.to_destroy)
		return name


	def update(self):
		self.rect.x += self.dir_x
		self.rect.y += self.dir_y
