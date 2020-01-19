			# Creating a settings module for our game. #5
class Settings():
	"""A class to store our games settings."""

	def __init__(self):
		"""Initialize our games settings and screen settings."""
		self.screen_width = 1200
		self.screen_height = 760
		self.bg_color = (140, 82, 255)


		# Ship settings
		self.ship_limit =0


		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = 34,34,34


		#alien settings
		self.fleet_drop_speed = 30

		



		#How quickly the game speeds up
		self.speedup_scale = 1.5
		#How quickly the alien point values increases
		self.score_scale =1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change during the game."""
		self.ship_speed = 3.8
		self.bullet_speed = 5.6
		self.alien_speed_factor = 0.314159265358979323846

		#fleet_direction of 1 represents right; and -1 represents left
		self.fleet_direction = 1

		#Scoring
		self.alien_points = 107

	def increase_speed(self):
		"""Increase speed settings and alien point values."""
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale


		self.alien_points = float(self.alien_points * self.score_scale)
