# Basic code stuctures #3

import sys
import pygame
from pygame.sprite import Group
import cv2 

from settings import Settings #5
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button #41
from ship import Ship #drawing the ship screen #7
from alien import Alien #23
import game_functions as gf # (this is an alias) #8
 



def run_game(specimen=None, doRender=True):
	"""Initialize game and create a screen object."""
	specimen = specimen
	doRender = doRender

    # Create a game surface if we chose to render
	if doRender:
		renderSurface = pygame.display.get_surface()      

  
	pygame.init()
	infrompy_settings = Settings()
	screen = pygame.display.set_mode((infrompy_settings.screen_width, infrompy_settings.screen_height))
	pygame.display.set_caption("Invaders from Python")

	#Make a play button
	play_button = Button(infrompy_settings, screen, "Play")

	#create an instance to store game stats and create a scoreboard.
	stats = GameStats(infrompy_settings)
	sb = Scoreboard(infrompy_settings, screen, stats)

	# Make a ship, a group of bullets and a group of aliens #25

	#Create a ship
	ship = Ship(infrompy_settings, screen) #7 | make instance of ship before the main loop so we don't make an entry of the ship at each loop
	# Make a group to store bullets in.
	bullets = Group()
	# Make an alien #23
	aliens = Group()


	#Create a fleet of aliens
	gf.create_fleet(infrompy_settings, screen, ship, aliens)
	

	# Start main loop for the game.
	while True:
		#gf.check_events(infrompy_settings, screen, ship, bullets) #8 #10the argument 'ship' enters the scene
		#ship.update() #11 will check for any updates of our ship
		#gf.update_bullets(infrompy_settings, screen, ship, aliens, bullets) #aliens added in 32
		#gf.update_aliens(infrompy_settings, stats, screen, ship, aliens, bullets)
		#gf.update_screen(infrompy_settings, screen, ship, aliens, bullets) #Creates an instance of an alien #23
		gf.check_events(infrompy_settings, screen, stats, sb, play_button, ship, aliens, bullets)

		if specimen and not doRender:
			dt = 0.05
		if stats.game_active: #39
			ship.update() #11 will check for any updates of our ship
			gf.update_bullets(infrompy_settings, screen, stats, sb, ship, aliens, bullets) #aliens added in 32
			gf.update_aliens(infrompy_settings,screen, stats, sb, ship, aliens, bullets)
		gf.update_screen(infrompy_settings, screen, stats, sb, ship, aliens, bullets, play_button) #Creates an instance of an alien #23 | insert stats and play_button in #41

run_game(specimen=None, doRender=True)



