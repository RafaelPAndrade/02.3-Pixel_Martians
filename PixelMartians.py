#coding: utf-8

""" TODO:
    -Use function to fire the shots (Alien)-Alien not done
    -Divide better the Intro from the core game mechanics
    -Backup the pontuation/store points not in Ship class internal status
    -Breakup vertically protections
    -Using visual blocks for life status
    -Random shooting for Aliens
    -Add proper game over+keep high scores between repetitions
    -Better leveling up
    -Types of ammo
    -Ammo counting
    -Scoreboard
    -Bonuses/Random targets
    -Boosts
    -Cooldown
    -Shooting with effects
    -accelaration mechanics [Optional in-game?]+Drag
    -Backing up status to file+Load game from file/last game"""

#imports & inits
import pygame
import random
import constants
from block import Block
from ship import Ship
from alien import Alien
from bullet import Bullet
from printing import words

print('Import done!')

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode([constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT])

done = False


#########################################
#Sprite groups
#########################################

#Universal groups:

##drawables, namely player aliens shots and protections
drawables_list = pygame.sprite.Group() 

##animated stuff, namely player aliens and shots
animated_list = pygame.sprite.Group() 



#Ships POV (behavior of ship's shots regarding certain elements):

##Group of pontuated objects (aliens)
s_point_list = pygame.sprite.Group() 

##Group of not pontuated objects (shields, ?alien_shots?)
s_npoint_list = pygame.sprite.Group() 


#Alien POV

##Group of (not pontuated) objects, player (shields, ?ship shots?)
a_npoint_list = pygame.sprite.Group() 

##walls in left and right of the screen, defined below (aliens only)
limit_list = pygame.sprite.Group() 




###################END PYGAME GROUPS##############################


###########################################
#Game Environment construction
###########################################


#invisible limits, avoiding aliens from exiting the screen (in swarm)
left_wall = Block(0,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
right_wall = Block(constants.SCREEN_WIDTH-1,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
limit_list.add(left_wall)
limit_list.add(right_wall)


#player protections
def gen_protections():
	#protections
	#TODO: break up, independent sections in each protection
	#left first
	for f in range(0,10):
		left_shield = Block(110,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(left_shield)
		s_npoint_list.add(left_shield)
		a_npoint_list.add(left_shield)
	#right
	for f in range(0,10):
		right_shield = Block(constants.SCREEN_WIDTH-110-100,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(right_shield)
		s_npoint_list.add(right_shield)
		a_npoint_list.add(right_shield)
	#center
	for f in range(0,10):
		center_shield = Block(constants.SCREEN_WIDTH/2-50,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(center_shield)
		s_npoint_list.add(center_shield)
		a_npoint_list.add(center_shield)

gen_protections()


#aliens
def gen_aliens(list_aliens):
	for b in range(1,11):
		greenalien = Alien(35+40*b,20, constants.GREEN, a_npoint_list)
		drawables_list.add(greenalien)
		animated_list.add(greenalien)
		s_point_list.add(greenalien)
		list_aliens.append(greenalien)


	for c in range (1,11):
		bluealien = Alien(35+40*c,60, constants.BLUE, a_npoint_list)
		drawables_list.add(bluealien)
		animated_list.add(bluealien)
		s_point_list.add(bluealien)
		list_aliens.append(bluealien)



	for d in range (1,11):
		redalien = Alien(35+40*d,100, constants.RED, a_npoint_list)
		drawables_list.add(redalien)
		animated_list.add(redalien)
		s_point_list.add(redalien)
		list_aliens.append(redalien)


	for e in range (1,11):
		greyalien = Alien(35+40*e,140, constants.GREY, a_npoint_list)
		drawables_list.add(greyalien)
		animated_list.add(greyalien)
		s_point_list.add(greyalien)
		list_aliens.append(greyalien)
	return True

def gen_player(life):
	name1 = Ship(constants.SCREEN_WIDTH/2-10,constants.BLACK, life, s_npoint_list, s_point_list)
	animated_list.add(name1)
	drawables_list.add(name1)
	a_npoint_list.add(name1)
	return name1

	
#------------------------Constants/Variables----------------------------
Intro = False
Ready = False
player = False
increase_level = True
points=0	#keeps pontuation when killing Player1
life=3		#keeps lifes number when killing Player1
Proj=None
#------------------------Game Logic-----------------------------------
print('Starting cicle...')
while not done:




	#--------------Create player-----------------------------------
	if player == False or Player1 not in drawables_list:
		print("Generating player... because:", player == False)
		Player1=gen_player(life)
		Player1.lifes -= 1
		Player1.pontuation=points
		#del points
		#del life
		#print(Player1.t_w_points)
		print("Player Generated!")
		player = True	


	#---------------------------Create aliens------------------------------
	if increase_level==True:
		aliens=[] #list of aliens 
		gen_aliens(aliens)
		print(aliens[39].to_destroy)
		increase_level = False


	#-----------------if there is no more targets/aliens, create more, add a life----------------
	if len(s_point_list)== 0:
		Player1.lifes += 1
		Ready = False
		increase_level = True


	#------if aliens collide with borders, invert horizontal movement and go down------------
	limited_list=pygame.sprite.groupcollide(s_point_list, limit_list, False, False)
	if len(limited_list) > 0:
		for i in range(0,40):
			aliens[i].dir_x = aliens[i].dir_x*-1
			aliens[i].rect.y += 40


	#----------------Aliens retreat when they hit the player, killing him-----
	collision_sprite = pygame.sprite.spritecollideany(Player1, s_point_list)
	if collision_sprite is not None:
		print("Got collision!")
		points=Player1.pontuation
		life= Player1.lifes
		Player1.kill()
		player= False
		for i in range (0,40):
			aliens[i].rect.y -= 240
		del collision_list
	
	#----------Shooting algorithm-----------------
	#for t in range(0,40):
	#	throw = random.randrange(0,4500)
	#	if throw == 6 and aliens[t] in drawables_list:
	#		Bomb = aliens[t].shooting()
	#		drawables_list.add(Bomb)
	#		animated_list.add(Bomb)
	#		s_npoint_list.add(Bomb)


	#------------------------------get events(key presses)---------------
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					Player1.move_left()
				elif event.key == pygame.K_RIGHT:
					Player1.move_right()
				elif event.key == pygame.K_d and Ready == True:
					print("Before,", len(animated_list))
					Proj = Player1.shooting()
					print(id(Proj))
					drawables_list.add(Proj)
					animated_list.add(Proj)
					a_npoint_list.add(Proj)
					print('Shots fired!!')
					print("After,", len(animated_list))
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_p:
					if Ready == True:
						print("Paused...")
						Ready = False
					elif Ready == False:
						Ready = True
						print("Resumed!")

				if event.key == pygame.K_LEFT:
					Player1.dont_move()

				elif event.key == pygame.K_RIGHT:
					Player1.dont_move()

	#------------only move if ready------------------
	if Ready == True:
		animated_list.update()

	screen.fill(constants.CFUNDO)

	drawables_list.draw(screen)


	words(35,15,constants.BLACK, 40, str(Player1.pontuation), screen)

	words(constants.SCREEN_WIDTH-35, 15, constants.BLACK, 40, str(Player1.lifes), screen)


#---------------------------Intro------------------------------
	if Intro == False:

		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2, constants.BLACK, 95, "Pixel Martians", screen)

		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT*5/7, constants.BLACK, 75, "Press [D] to continue", screen)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
				print("Exiting...")
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_b:
					print("Exiting...")
					done = True
				elif event.key == pygame.K_d:
					Intro = True

#-----------------------------Ready-------------------------------

	if Intro == True and Ready == False:

		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2, constants.BLACK, 95, "Get ready...", screen)


		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT*5/7, constants.BLACK, 75, "Press [D] to continue", screen)


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
