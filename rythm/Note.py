import pygame as pg
from SpriteSheet import SpriteSheet
import itertools
from random import choice

class Note(pg.sprite.Sprite):
	def __init__(self, start_pos, speed):
		pg.sprite.Sprite.__init__(self)
		imageFile = choice(['graphic/FallingSheepUpsideDown.png', 'graphic/FallingSheep.png', 'graphic/FallingSheepRotating.png'])

		#Modify this to change the scale of the SpriteSheet
		self.image_iter = itertools.cycle(SpriteSheet(imageFile,150, 150).load_grid_images(2,1,x_margin =10, x_padding=25, y_margin =10, y_padding =25))

		self.image = next(self.image_iter)
		self.rect = self.image.get_rect(midbottom = (start_pos[0],start_pos[1]))
		self.speed = speed
		self.value = 1
		self.counter = 0
		self.y_float = float(self.rect.y)

	def update(self):
		self.y_float += self.speed
		self.rect.y = int(self.y_float)
		self.counter += 1

		#Counter to change to the next image
		if self.counter > 8:
			self.image = next(self.image_iter)
			self.counter = 0

	def caught(self, player):
		if self.rect.colliderect(player.rect):
			player.incScore(self.value)
			self.kill()
			return True
		#Kill condition for notes
		if self.rect.y > 500:
			return False
		else:
			return True
