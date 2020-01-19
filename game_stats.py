
class GameStats():
	"""Track stats for invaders from python"""
	def __init__(self, infrompy_settings):
		"""Initialize stats."""
		self.infrompy_settings = infrompy_settings
		self.reset_stats()

		#start Invaders from python in an active state.
		self.game_active = False
		#start the game in an inactive state
		#self.game_active = True

		#high score should never be reset
		self.high_score = 0 #we initialize high score in the init method, instead of the reset stats
		

	def reset_stats(self):
		"""Initialize stats that can change during the game."""
		self.ships_left = self.infrompy_settings.ship_limit
		self.score = 0
		self.level = 1
