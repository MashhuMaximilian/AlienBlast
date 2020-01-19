#Refactoring #8
import sys
from time import sleep

import pygame

from bullet import Bullet
from alien import Alien



def check_keydown_events(event, infrompy_settings, screen, ship, bullets):
	"""Respond to keypresses."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		# Create a new bulet and add it to the bullets group.
		new_bullet = Bullet(infrompy_settings, screen, ship)
		bullets.add(new_bullet)

def check_keyup_events(event, ship):
	"""Respond to keyup release."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False

def check_events(infrompy_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	"""Respond to key presses and mouse events."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, infrompy_settings, screen, ship, bullets)
		
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)

		elif event.type == pygame.MOUSEBUTTONDOWN: #42
			mouse_x, mouse_y = pygame.mouse.get_pos()   
			check_play_button(infrompy_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


			#   ship.moving_left = True
			#if event.key == pygame.K_RIGHT:
				#Move ship to the right | ship.rect.centerx += 1 #10
			#   ship.moving_right = True
			#elif event.key == pygame.K_LEFT:
			#   ship.moving_left = True



		#elif event.type == pygame.KEYUP: # For not touching the right key, the ship does nothing #11
		#   if event.key == pygame.K_RIGHT: 
		#       ship.moving_right = False
		#   elif event.key == pygame.K_LEFT:
		#       ship.moving_left = False

def check_play_button(infrompy_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
	"""Start a new game when the play button is clicked."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

	if button_clicked and not stats.game_active:

		# reset the game settings
		infrompy_settings.initialize_dynamic_settings()

		# Hide the mouse
		pygame.mouse.set_visible(False)

		# Reser the game stats
		stats.reset_stats()
		stats.game_active = True

		# Reset the scoreboard images.
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()

	# Empty the list of aliens and bullets
	aliens.empty()
	bullets.empty()

	# Create a new fleet and center the ship
	create_fleet(infrompy_settings, screen, ship, aliens)
	ship.center_ship()

def update_screen(infrompy_settings, screen, stats, sb, ship, aliens, bullets, play_button):
	"""Update the images on the screen and flip the new screen"""

	# Redraw screeen during each pass through the loop #4
	screen.fill(infrompy_settings.bg_color)
	

	#Redraw all bullets behind the ship and aliens.
	for bullet in bullets.sprites():
		bullet.draw_bullet()
	ship.blitme() #7  | The ship appears on the top of the background (as a top layer)
	aliens.draw(screen) #24

	#Draw the score info
	sb.show_score()

	# Draw the play button if the game is inactive
	if not stats.game_active:
		play_button.draw_button()

	# make the most recently drawn screen visible
	pygame.display.flip()

def update_bullets(infrompy_settings, screen, stats, sb, ship, aliens, bullets): #THE ORDER MATTERS!
	"""Update position of bullets and remobe old bullets.""" 
	bullets.update()
	#Remove bullets that have left our main screen.
	for bullet in bullets.copy(): # we make copies of the bullet
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet)
	# print(len(bullets)) | use this to see removed items

	check_bullet_alien_collisions(infrompy_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(infrompy_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to bullet-alien collisions."""
	# Remove any bullets and aliens that have collided.
	collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

	for aliens in collisions.values():
		stats.score += infrompy_settings.alien_points * len(aliens)
		sb.prep_score()
	check_high_score(stats, sb)

	if len(aliens) == 0:
		# if the alien fleet is destroyed move up one level.
		bullets.empty()
		infrompy_settings.increase_speed()

		#Increase level
		stats.level += 1
		sb.prep_level()

		create_fleet(infrompy_settings, screen, ship, aliens)


	# Before refactoring:
	#---------------------------------------------------------------------------------
	#   alien = Alien(infrompy_settings, screen)
	#   alien_width = alien.rect.width
	#   available_space_x = infrompy_settings.screen_width - 2 * alien_width
	#   number_aliens_x = int(available_space_x / (2 * alien_width)) # we use int bc we want an integer number of aliens, not 2.3 aliens or something
	
	#Create first row of aliens #26
	#   for alien_number in range(number_aliens_x):
		#Creating an alien and place it in the row.
	#       alien= Alien(infrompy_settings, screen)
	#       alien.x = alien_width + 2 * alien_width * alien_number
	#       alien.rect.x = alien.x
	#       aliens.add(alien)

def create_fleet(infrompy_settings, screen, ship, aliens):
	"""Create a fleet of aliens."""
	# Create an alien and find the number of aliens in a row.
	alien = Alien(infrompy_settings, screen)
	number_aliens_x = get_number_aliens_x(infrompy_settings, alien.rect.width)
	number_rows = get_number_rows(infrompy_settings, ship.rect.height, alien.rect.height )
	
	#Create the fleet of aliens
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_alien(infrompy_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(infrompy_settings, alien_width):
	"""How many aliens will fit in a row."""
	available_space_x = infrompy_settings.screen_width - alien_width
	number_aliens_x = int(available_space_x / (1.1 * alien_width)) # we use int bc we want an integer number of aliens, not 2.3 aliens or something
	return number_aliens_x

def create_alien(infrompy_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in a row."""
	alien = Alien(infrompy_settings, screen)
	alien_width = alien.rect.width
	alien.x = alien_width + 1.1 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + alien.rect.height * row_number
	aliens.add(alien)

def get_number_rows(infrompy_settings, ship_height, alien_height):
	"""Determine the number of rows of aliens that fit on the screen."""
	available_space_y = (infrompy_settings.screen_height - (3 * alien_height) - ship_height)
	number_rows = int(available_space_y / ( 1.3 * alien_height))
	return number_rows

def check_fleet_edges(infrompy_settings, aliens):
	"""Respond if any aliens have reched the edge of the screen."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(infrompy_settings, aliens)
			break
		#we call change_fleet_direction if check_fleet_edges is True

def change_fleet_direction(infrompy_settings, aliens): #31
	"""Drop the fleet and change the fleet direction."""
	for alien in aliens.sprites(): 
		alien.rect.y += infrompy_settings.fleet_drop_speed
	infrompy_settings.fleet_direction *= -1 #we multiply current value by -1 so it changes direction

def ship_hit(infrompy_settings, screen, stats, sb, ship, aliens, bullets):
	"""Respond to a ship being hit by an alien."""
	if stats.ships_left > 0:

		# Decrement ships_left
		stats.ships_left -= 1

		# Update scoreboard
		sb.prep_ships()

		#Empty scoreboard
		sb.prep_ships()

		# Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		# Create a new fleet and center the ship
		create_fleet(infrompy_settings, screen, ship, aliens)
		ship.center_ship()

		# Pause
		sleep(0.5)

	else:
		stats.game_active = False
		pygame.mouse.set_visible(True)
	#we set the flag to false so the game will not run another fleet of aliens if there are no remaining ships/lives

def check_aliens_bottom(infrompy_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if aliens have reached the bottom of the screen."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			# Treat this the same as if the ship got hit.
			ship_hit(infrompy_settings, screen, stats, sb, ship, aliens, bullets)
			break

def update_aliens(infrompy_settings, screen, stats, sb, ship, aliens, bullets):
	"""Check if the fleet has reached the edge and then update the positions of all aliens."""
	check_fleet_edges(infrompy_settings, aliens)
	aliens.update()

	# look for allien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(infrompy_settings, screen, stats, sb, ship, aliens, bullets)

	# look for aliens hitting the bottom of the screen
	check_aliens_bottom(infrompy_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
	"""Check to see if there is a new high score."""
	if stats.score> stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()