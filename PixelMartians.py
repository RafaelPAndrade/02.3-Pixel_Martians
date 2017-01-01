#coding: utf-8
""" TODO:
    -Use function to fire the shots (Ship and Alien)-Done
    -Backup the pontuation/store not in Ship class internal status
    -Divide better the Intro from the core game mechanics
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


#drawables, namely player aliens shots and protections
drawables_list = pygame.sprite.Group() 

#animated stuff, namely player aliens and shots
animated_list = pygame.sprite.Group() 

#Group of pontuated objects (aliens)
point_list = pygame.sprite.Group() 

#Group of not pontuated objects (shields)
npoint_list = pygame.sprite.Group() 

#--->(invisible) walls in left and right of the screen, defined below
limit_list = pygame.sprite.Group() 


#invisible limits
left_wall = Block(0,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
right_wall = Block(constants.SCREEN_WIDTH-1,0,1,constants.SCREEN_HEIGHT,constants.BLACK)
limit_list.add(left_wall)
limit_list.add(right_wall)


def gen_protections():
	#protections
	#TODO: break up, independent sections in each protection
	#left first
	for f in range(0,10):
		left_shield = Block(110,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(left_shield)
		npoint_list.add(left_shield)
	#right
	for f in range(0,10):
		right_shield = Block(constants.SCREEN_WIDTH-110-100,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(right_shield)
		npoint_list.add(right_shield)
	#center
	for f in range(0,10):
		center_shield = Block(constants.SCREEN_WIDTH/2-50,constants.SCREEN_HEIGHT-80-2*f,100,2,constants.LBLUE)
		drawables_list.add(center_shield)
		npoint_list.add(center_shield)

gen_protections()


def gen_aliens(list_aliens):
	for b in range(1,11):
		greenalien = Alien(35+40*b,20, constants.GREEN)
		drawables_list.add(greenalien)
		animated_list.add(greenalien)
		point_list.add(greenalien)
		list_aliens.append(greenalien)


	for c in range (1,11):
		bluealien = Alien(35+40*c,60, constants.BLUE)
		drawables_list.add(bluealien)
		animated_list.add(bluealien)
		point_list.add(bluealien)
		list_aliens.append(bluealien)



	for d in range (1,11):
		redalien = Alien(35+40*d,100, constants.RED)
		drawables_list.add(redalien)
		animated_list.add(redalien)
		point_list.add(redalien)
		list_aliens.append(redalien)


	for e in range (1,11):
		greyalien = Alien(35+40*e,140, constants.GREY)
		drawables_list.add(greyalien)
		animated_list.add(greyalien)
		point_list.add(greyalien)
		list_aliens.append(greyalien)
	return True

def gen_player(life):
	name = Ship(constants.SCREEN_WIDTH/2-10,constants.BLACK, life, npoint_list, point_list)
	animated_list.add(name)
	drawables_list.add(name)
	
	return name

	


#------------------------Constants/Variables----------------------------
Intro = False
Ready = False
player = False
increase_level = True
points=0	#keeps pontuation when killing Player1
life=3		#keeps lifes number when killing Player1
#------------------------Game Logic-----------------------------------
print('Starting cicle...')
while not done:


	#---------------------------Create aliens------------------------------
	if increase_level==True:
		aliens=[] #list of aliens 
		gen_aliens(aliens)
		increase_level = False

	#--------------Create player-----------------------------------
	if player == False or Player1 not in drawables_list:
		Player1=gen_player(life)
		Player1.lifes -= 1
		Player1.pontuation=points
		del points
		del life
		print(Player1.t_w_points)
		player = True


	#-----------------if there is no more targets/aliens, create more, add a life----------------
	if len(point_list)== 0:
		Player1.lifes += 1
		Ready = False
		increase_level = True


	#------if aliens collide with borders, invert horizontal movement and go down------------
	limited_list=pygame.sprite.groupcollide(point_list, limit_list, False, False)
	if len(limited_list) > 0:
		for i in range(0,40):
			aliens[i].dir_x = aliens[i].dir_x*-1
			aliens[i].rect.y += 40


	#----------------Aliens retreat when they hit the player, killing him-----
	killing_list = pygame.sprite.spritecollide(Player1, point_list,False)
	if len(killing_list) > 0:
		points=Player1.pontuation
		life= Player1.lifes
		Player1.kill()
		player= False
		for i in range (0,40):
			aliens[i].rect.y -= 240

	'''#----------Shooting algorithm-----------------
	for t in range(0,40):
		throw = random.randrange(0,4500)
		if throw == 6 and aliens[t] in shot_list:
			#---------------if aliens[t] pertence a drawables_list
			Bomb = Bullet(aliens[t].rect.x+5,aliens[t].rect.y+20,-1,1)
			drawables_list.add(Bomb)
			animated_list.add(Bomb)
			fired_rounds += 1'''


	#------------------------------get events(key presses)---------------
	for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					Player1.move_left()
				elif event.key == pygame.K_RIGHT:
					Player1.move_right()
				elif event.key == pygame.K_d:
					Proj =Player1.shooting()
					drawables_list.add(Proj)
					animated_list.add(Proj)
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

	words(35,15,constants.BLACK, 40, str(Player1.pontuation), screen)

	words(constants.SCREEN_WIDTH-35, 15, constants.BLACK, 40, str(Player1.lifes), screen)


#---------------------------Intro------------------------------
	if Intro == False:

		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT/2, constants.BLACK, 95, "Pixel Martians", screen)

		words(constants.SCREEN_WIDTH/2, constants.SCREEN_HEIGHT*5/7, constants.BLACK, 75, "Press [D] to continue", screen)


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
