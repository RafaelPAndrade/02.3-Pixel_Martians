#coding: utf-8

import pygame
import constants
from block import Block
from bullet import Bullet


class Ship(Block):
	"""
	Class of objects that are players.

	Caractheristics:
	-Controlable (move_left/right/dont_move)+Move horizontaly only
	-Generate objects of the class Bullet in upward side of square(shooting):
		-Contain Group of objects that do and do not attribute points
	"""

	def __init__(self,x,color, lifes, targets_nopoints=None, targets_points=None):
		super(Ship, self).__init__ (x,constants.SCREEN_HEIGHT-60,30,30,color)
		self.dir_x = 0
		self.lifes=lifes
		self.pontuation=0
		#Setting the list of target objects
		if isinstance(targets_nopoints, pygame.sprite.Group):
			self.t_n_points= targets_nopoints
		else:
		
			self.t_n_points= None
		if isinstance(targets_points, pygame.sprite.Group):
			self.t_w_points= targets_points #must have self.value...
		else:	
			self.t_w_points= None



	def move_left(self):
		self.dir_x = -constants.VEL

	def move_right(self):
		self.dir_x = constants.VEL

	def dont_move(self):
		self.dir_x = constants.NULL
		
	def change_points_by(self,value):
		self.pontuation+= value

	def shooting(self):
		name = Bullet(self.rect.x + 10, self.rect.y - 10, 1, 5, self.t_n_points, self.t_w_points, self)
		#name = Bullet(constants.SCREEN_WIDTH//2, constants.SCREEN_HEIGHT//2, 1, 5)
		return name


	def update(self):
		self.rect.x += self.dir_x
		if self.rect.x >= constants.SCREEN_WIDTH-30:
			self.rect.x = constants.SCREEN_WIDTH-30
		elif self.rect.x <= 0:
			self.rect.x = 0



