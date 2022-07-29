import pygame as pg
from SpriteSheet import SpriteSheet
import itertools

class Follower(pg.sprite.Sprite):
	numRow = 1
	numColumn = None
	numOfFollower = 0
	def __init__(self, player):
		pg.sprite.Sprite.__init__(self)
		self.image_iter = itertools.cycle(SpriteSheet("graphic/FallingSheep.png",80).load_grid_images(2,1,x_margin =10, x_padding=20, y_margin =15, y_padding =30))
		self.dimension = next(self.image_iter).get_size()
		self.image = pg.Surface([400,700]).convert_alpha()
		self.image.fill((0,0,0,0))
		self.rect = self.image.get_rect(midbottom = (200,800))
		self.player = player
		self.blitImage = self.image

	def update(self):
		if Follower.numOfFollower != self.player.getScore()//10:
			Follower.numOfFollower = self.player.getScore()//10
			Follower.numColumn = Follower.numOfFollower % 8-1
			if Follower.numColumn == 6:
				Follower.numRow +=1
			self.blitImage.blit(next(self.image_iter), (Follower.numColumn * 60, 700 - Follower.numRow * 40))
		if self.player.flip:
			self.image = pg.transform.flip(self.blitImage, True, False)
			self.rect.bottomright = (pg.mouse.get_pos()[0]-105, 670)
		else:
			self.image = self.blitImage
			self.rect.bottomleft = (pg.mouse.get_pos()[0]+15, 670)

	def clear(self):
		self.image = pg.Surface([400,700]).convert_alpha()
		self.image.fill((0,0,0,0))
		self.blitImage = self.image
		Follower.numRow = 1
		Follower.numColumn = None
		Follower.numOfFollower = 0
