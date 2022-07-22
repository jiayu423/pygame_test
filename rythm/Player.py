# This is the Player class
# It loads Player images and keeps track of the score

import pygame as pg
from SpriteSheet import SpriteSheet
import itertools

class Player(pg.sprite.Sprite):
		def __init__(self):
			pg.sprite.Sprite.__init__(self)
			self.player_images_iter = self._load_images()
			self.image = next(self.player_images_iter)
			self.rect = self.image.get_rect()
			self.pre_x_pos = pg.mouse.get_pos()[0]
			self.offset = (-100, -50)

			#Y position of Player
			self.originY = 550
			self.score = 0
			
		def _load_images(self):
			"""Loads images from the sprite sheet"""
			filename = 'WalkSprite.png'

			#Modify this to scale the images
			images_ss = SpriteSheet('WalkSprite.png', bx=153)
			player_images = images_ss.load_grid_images(7,1, x_margin = 20, y_margin = 20, y_padding = 40)
			return itertools.cycle(player_images)
		
		def update(self):
			pos = (pg.mouse.get_pos()[0], self.originY)
			self._walk(pos[0]-self.pre_x_pos)
			self.pre_x_pos = pos[0]
			self.rect.topleft = pos
			self.rect.move_ip(self.offset)
			
		def _walk(self, change):
			if change < -3:
				self.image = next(self.player_images_iter)
			elif change > 3:
				self.image = pg.transform.flip(next(self.player_images_iter), True, False)
				
		def incScore(self, value):
			self.score += value
			
		def getScore(self):
			return self.score
