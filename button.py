import pygame.font

class Button(): #40

	def __init__(self, infrompy_settings, screen, msg):
		"""Initialize button attributes."""
		self.screen = screen
		self.screen_rect = screen.get_rect()

		# Set the dimensions and properties of the button
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont(None, 48)

		# Build the button's rect object and center
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		self.rect.center = self.screen_rect.center

		# The button message needs to be prepped only once.
		self.prep_msg(msg)

	def prep_msg(self, msg):
		"""Turn our msg into a rendered image and center the text."""
		self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center

	def draw_button(self):
		# Draw blank button and then draw message
		self.screen.fill(self.button_color, self.rect) # create the rectangular portion of the button
		self.screen.blit(self.msg_image, self.msg_image_rect) # the blit function draws the text iage on the screen, passing it an image, and then the rect object associated with the image
