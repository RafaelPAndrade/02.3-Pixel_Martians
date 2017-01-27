#coding: utf-8

import pygame
from block import Block
import constants

#insert this class in ship method gen_shoot()
class Bullet(Block):
	def __init__(self,x,y, sign, speed, targets_nopoints= None, targets_points=None, point_receptor=None):
		super(Bullet, self).__init__(x,y,10,10,constants.YELLOW)
		self.dir_x = 0
		self.dir_y = -1*sign*speed
		#Next 2 shall be pygame.sprite.Group()...
		if isinstance(targets_nopoints, pygame.sprite.Group):
			self.t_n_points= targets_nopoints
		else:
		
			self.t_n_points= None
		if isinstance(targets_points, pygame.sprite.Group):
			self.t_w_points= targets_points		#must have self.value...
			self.point_receptor=point_receptor	#must have change_points_by(x) method
		else:	
			self.t_w_points= None
		
		

	def update(self):
		#always go up
		self.rect.y += self.dir_y
		#verify if within bounds
		if self.rect.y < 0 or self.rect.y >= constants.SCREEN_HEIGHT:
			self.kill() #removes from ALL the pygame's Groups
			del self
			return
			
		if self.t_n_points != None:
			collision_list = pygame.sprite.spritecollide(self, self.t_n_points, True)
			#Having spritecollide set to True destroys obstacles 
			if len(collision_list)>0:
				self.kill()

		if self.t_w_points != None:
			collision_list = pygame.sprite.spritecollide(self, self.t_w_points, True)
			#Having spritecollide set to True destroys obstacles 
			if len(collision_list)>0:
				self.kill()
				for el in collision_list:
					self.point_receptor.change_points_by(el.value)
