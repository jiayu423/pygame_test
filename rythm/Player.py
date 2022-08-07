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
			self.catchLeft = SpriteSheet.aspect_scale(self, pg.image.load("graphic/CatchLeft.png"), 120, 1000)
			self.catchLeft.set_colorkey(pg.Color("black"), pg.RLEACCEL)
			self.catchCount = 0
			self.walkCount = 0
			self.flip = False

			#Y position of Player
			self.originY = 560
			self.score = 0
			
		def _load_images(self):
			"""Loads images from the sprite sheet"""
			filename = 'WalkSprite.png'

			#Modify this to scale the images
			images_ss = SpriteSheet('graphic/WalkSprite.png', bx=153)
			player_images = images_ss.load_grid_images(7,1, x_margin = 20, y_margin = 30, y_padding = 60)
			return itertools.cycle(player_images)
		
		def update(self):
			# if self.catchCount != 0:
			# 	self.image = self.catchLeft
			# 	pos = (pg.mouse.get_pos()[0], 510)
			# 	self.catchCount -= 1
			# 	self.walkCount = 0
			#
			# else:
			self._walk(pg.mouse.get_pos()[0]-self.pre_x_pos)
			pos = (pg.mouse.get_pos()[0], self.originY)
			self.pre_x_pos = pos[0]
			self.rect.topleft = pos
			self.rect.move_ip(self.offset)
			# print(self.rect.topright)
			
		def _walk(self, change):
			if change < 0 and self.walkCount == 0:
				self.image = next(self.player_images_iter)
				self.walkCount = 15
				self.flip = False
			elif self.walkCount == 0 :
				self.flip = True
				self.image = pg.transform.flip(next(self.player_images_iter), True, False)
				self.walkCount = 15
			
			self.walkCount -= 1
				
		def incScore(self, value):
			self.score += value
			self.catchCount = 10


			
		def getScore(self):
			return self.score
			
