#coding: latin-1

import pygame

class Block(pygame.sprite.Sprite):
	""" Classe para representar blocos coloridos-todos os objetos, neste jogo, sao subclasses deste """
	def __init__(self, x, y, width, height, color):
		super(Block, self).__init__()
		self.image = pygame.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
