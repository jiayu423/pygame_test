import pygame as pg
from SpriteSheet import SpriteSheet
import itertools

class Follower(pg.sprite.Sprite):
	def __init__(self, player):
		pg.sprite.Sprite.__init__(self)
		self.image_iter = itertools.cycle(SpriteSheet("graphic/FallingSheep.png",80).load_grid_images(2,1,x_margin =10, x_padding=20, y_margin =15, y_padding =30))
		self.dimension = next(self.image_iter).get_size()
		self.image = pg.Surface([400,700]).convert_alpha()
		self.image.fill((0,0,0,0))
		self.rect = self.image.get_rect(midbottom = (200,800))
		self.player = player

	def update(self):
		numRow = 1
		numColumn = None
		self.clear()
		for i in range(0, self.player.getScore()//10):
			if numColumn == 5:
				numRow +=1
			numColumn = i % 6
			self.image.blit(next(self.image_iter), (numColumn * 60, 700 - numRow * 40))
		self.rect.bottomleft = (pg.mouse.get_pos()[0]+15, 670)
		if self.player.flip:
			self.image = pg.transform.flip(self.image, True, False)
			self.rect.bottomright = (pg.mouse.get_pos()[0]-105, 670)

	def clear(self):
		self.image = pg.Surface([400,700]).convert_alpha()
		self.image.fill((0,0,0,0))
