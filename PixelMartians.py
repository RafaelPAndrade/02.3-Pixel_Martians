#coding: utf-8

import pygame
import random
import constants
from block import Block
from ship import Ship
from alien import Alien
from bullet import Bullet
import pointing

pygame.init()

clock = pygame.time.Clock()

done = False

drawables_list = pygame.sprite.Group()
animated_list = pygame.sprite.Group()
shot_list = pygame.sprite.Group()
limit_list = pygame.sprite.Group()
shield_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
bomb_list = pygame.sprite.Group()

screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])
#invisible limits
left_wall = Block(0,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
right_wall = Block(constants.SCREEN_WIDTH-1,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
drawables_list.add(left_wall)
drawables_list.add(right_wall)
limit_list.add(left_wall)
limit_list.add(right_wall)


#protections
#left first
for f in range(0,10):
	left_shield = Block(110,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
	drawables_list.add(left_shield)
	shield_list.add(left_shield)
#right
for f in range(0,10):
	right_shield = Block(constants.SCREEN_WIDTH-110-100,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
	drawables_list.add(right_shield)
	shield_list.add(right_shield)
#center
for f in range(0,10):
	center_shield = Block(constants.SCREEN_WIDTH/2-50,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
	drawables_list.add(center_shield)
	shield_list.add(center_shield)



#------------------------Constants/Variables----------------------------
Intro = False
Ready = False


player = False
increase_level = True
invert = False
points = 0
throw = 0
lifes = 3
fired_rounds = 0
#------------------------Game Logic-----------------------------------	
while not done:
	
		
	points = pointing.points
	
	#---------------------------Create aliens------------------------------	
	if increase_level==True:
		aliens=[]
		for b in range(1,11):
			greenalien = Alien(35+40*b,20, constants.GREEN)
			drawables_list.add(greenalien)
			animated_list.add(greenalien)
			shot_list.add(greenalien)
			greenalien.set_value(constants.GREEN)
			aliens.append(greenalien)
		
		
		for c in range (1,11):
			bluealien = Alien(35+40*c,60, constants.BLUE)
			drawables_list.add(bluealien)
			animated_list.add(bluealien)
			shot_list.add(bluealien)
			bluealien.set_value(constants.BLUE)
			aliens.append(bluealien)
		
		
		for d in range (1,11):
			redalien = Alien(35+40*d,100, constants.RED)
			drawables_list.add(redalien)
			animated_list.add(redalien)
			shot_list.add(redalien)
			aliens.append(redalien)
			redalien.set_value(constants.RED)
			
		
		for e in range (1,11):
			greyalien = Alien(35+40*e,140, constants.GREY)
			drawables_list.add(greyalien)
			animated_list.add(greyalien)
			shot_list.add(greyalien)
			greyalien.set_value(constants.GREY)
			aliens.append(greyalien)
		increase_level = False
	#--------------Create player-----------------------------------	
	if player == False: #and lifes > 0
		Player1 = Ship(constants.SCREEN_WIDTH/2-10,constants.BLACK)
		animated_list.add(Player1)
		drawables_list.add(Player1)
		player_list.add(Player1)
		player = True
		lifes -= 1
	#-----------------if there is no more targets, create more, add a life----------------
	if len(shot_list)== 0:
		lifes += 1
		Ready = False
		increase_level = True
		
	#----------------if there is no player, add player--------------------------	
	if len(player_list) == 0:
		player = False		
	
	
	#------if aliens collide with borders, invert horizontal movement and go down------------
	limited_list=pygame.sprite.groupcollide(shot_list, limit_list, False, False)
	if len(limited_list) > 0:
		for i in range(0,40):
			aliens[i].dir_x = aliens[i].dir_x*-1
			aliens[i].rect.y += 40
			
	
	#----------------Aliens retreat when they hit the player, killing him-----
	killing_list = pygame.sprite.spritecollide(Player1,shot_list,False)
	if len(killing_list) > 0:
		Player1.kill()
		for i in range (0,40):
			aliens[i].rect.y -= 240
	#----------Shooting algorithm-----------------		
	for t in range(0,40):	
		throw = random.randrange(0,4500)
		if throw == 6 and aliens[t] in shot_list:
			#---------------if aliens[t] pertence a drawables_list
			Bomb = Bullet(aliens[t].rect.x+5,aliens[t].rect.y+20,-1,1)
			Bomb.set_shot(player_list)
			Bomb.set_shield(shield_list)
			drawables_list.add(Bomb)
			animated_list.add(Bomb)
			bomb_list.add(Bomb)
			fired_rounds += 1
	
	
	#------------------------------get events(key presses)---------------
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True		
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					Player1.move_left()
				elif event.key == pygame.K_RIGHT:
					Player1.move_right()
				elif event.key == pygame.K_d and pointing.gunfired ==False and player == True and Ready == True:
					Proj = Bullet(Player1.rect.x+10,Player1.rect.y,1,5)
					drawables_list.add(Proj)
					animated_list.add(Proj)
					Proj.set_shot(shot_list)
					Proj.set_shield(shield_list)
					Proj.set_bomb(bomb_list)
					pointing.gunfired = True				
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_p:
					if Ready == True:
						Ready = False
					elif Ready == False:
						Ready = True
				
				if event.key == pygame.K_LEFT:
					Player1.dont_move()
					
				elif event.key == pygame.K_RIGHT:
					Player1.dont_move()			
						

	#------------only move if ready------------------
	if Ready == True:
		animated_list.update()	
	
	screen.fill(constants.CFUNDO)		

	drawables_list.draw(screen)
	
	font = pygame.font.Font(None, 40)
	text = font.render(str(points), 5, constants.BLACK)
	textpos = text.get_rect()
	textpos.centerx = 35
	textpos.centery = 15
	screen.blit(text, textpos)	
	
	font = pygame.font.Font(None, 40)
	text = font.render(str(lifes), 5, constants.BLACK)
	textpos = text.get_rect()
	textpos.centerx = constants.SCREEN_WIDTH-35
	textpos.centery = 15
	screen.blit(text, textpos)	
	#for l in range(0,lifes):
		#life_empty = Block(constants.SCREEN_WIDTH-50*(l+1),2, 30,30,constants.BLACK)
		#drawables_list.add(life_empty)	
	
	
	
	
#---------------------------Intro------------------------------	
	if Intro == False:
		font = pygame.font.Font(None, 95)
		text = font.render("Pixel Martians", 5, constants.BLACK)
		textpos = text.get_rect()
		textpos.centerx = constants.SCREEN_WIDTH/2
		textpos.centery = constants.SCREEN_HEIGHT/2
		screen.blit(text, textpos)
	
		font = pygame.font.Font(None, 75)
		text = font.render("Press [D] to continue", 5, constants.BLACK)
		textpos = text.get_rect()
		textpos.centerx = constants.SCREEN_WIDTH/2
		textpos.centery = constants.SCREEN_HEIGHT*5/7
		screen.blit(text, textpos)	
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True		
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_b:
					done = True
				elif event.key == pygame.K_d:
					Intro = True
							
#-----------------------------Ready-------------------------------	

	if Intro == True and Ready == False:
		font = pygame.font.Font(None, 95)
		text = font.render("Get ready...", 5, constants.BLACK)
		textpos = text.get_rect()
		textpos.centerx = constants.SCREEN_WIDTH/2
		textpos.centery = constants.SCREEN_HEIGHT/2
		screen.blit(text, textpos)
		
		font = pygame.font.Font(None, 75)
		text = font.render("Press [D] to continue", 5, constants.BLACK)
		textpos = text.get_rect()
		textpos.centerx = constants.SCREEN_WIDTH/2
		textpos.centery = constants.SCREEN_HEIGHT*5/7
		screen.blit(text, textpos)	
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True		
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_b:
					done = True
				elif event.key == pygame.K_d:
					Ready = True	
	
	pygame.display.flip()

	clock.tick(constants.FPS)

pygame.quit()
