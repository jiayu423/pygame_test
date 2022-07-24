import random
import time

import pygame as pg
from sys import exit
from random import choice
import numpy as np
from song_utils import *
from GIFImage import GIFImage
from Player import Player
from Note import Note
import itertools
from SpriteSheet import SpriteSheet

"""
class Note(pg.sprite.Sprite):
    def __init__(self, start_pos, bpm):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("graphic/Tear_weepy.webp")
        #		self.image = pg.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect(midbottom=(start_pos[0], start_pos[1]))
        self.speed = 1
        self.y_float = float(self.rect.y)
        self.value = 1
        self.bpm = bpm

    def update(self):
        
        The current rhythm system works as follows:
        suppose we have a 60 bpm song, meaning 1 beat per second.
        if each of our note corresponds to 1 beat (1 note : 1 beat, this ratio can change),
        then it means that we need to 'kill' one note per second.
        (The notes are killed when their bottom y touches the top y of the player.)
        So to kill 1 notes/s, we need the note to travel exactly its height each second
        suppose our game is running at 60 fps, meaning that 1/60 s will pass between each frame
        so 33/1 (pixel/notes) * 1/1 (notes/beats) * 60/60 (beats/s) * 1/60 (s/frame) = 33/60 (pixel/frame)
        so after 60 frames (which is 1 s), the note will travel 33 pixel (1 beat), which is what we want
        
        global dt, note_height, beatRatio
        self.speed = dt * self.bpm/60 * note_height * beatRatio
        self.y_float += self.speed
        # self.rect.y += self.speed
        self.rect.y = int(self.y_float)

    def caught(self, player):
        if self.rect.colliderect(player.rect):
            player.incScore(self.value)
            self.kill()
            return True
        elif self.rect.y > 450:
            return False
        else:
            return False
"""

def aspect_scale(img, bx,by):
        """ Scales 'img' to fit into box bx/by.
        This method will retain the original image's aspect ratio """
        ix,iy = img.get_size()
        if ix > iy:
            # fit to width
            scale_factor = bx/float(ix)
            sy = scale_factor * iy
            if sy > by:
                scale_factor = by/float(iy)
                sx = scale_factor * ix
                sy = by
            else:
                sx = bx
        else:
            # fit to height
            scale_factor = by/float(iy)
            sx = scale_factor * ix
            if sx > bx:
                scale_factor = bx/float(ix)
                sx = bx
                sy = scale_factor * iy
            else:
                sy = by

        return pg.transform.scale(img, (sx,sy))

def initNotes(song: object, note_size: int, top_player: int):
    """

    :param song: a list of counts
    :param note_size: height of note
    :param top_player: player top y position
    """

    sus = song.ignoredNotes
    pos_x, pos_y = convertXY(song, note_size, top_player)

    # render notes on screen
    for i in range(len(pos_y)):
        if set(sus).intersection({i}):
            continue
        speed = dt * song.bpm[i]/60 * note_height * beatRatio
        notes.add(Note([pos_x[i], pos_y[i]], speed))


# def initNotes_test(notes: object, note_size: float, top_flower: float):
#
#     # value of each rain drop
#     # 1 beat gets a value of 2, 1/2 beat gets a value of 1
#     beats_raw = [np.ones((8,)),
#                  np.ones((4,)) * 2,
#                  np.ones((8,)),
#                  np.ones((3,)) * 2, np.array([0.5, 1, 0.5, 0.5]),
#                  np.array([1.5, 0.5, 1, 0.5, 0.5]),
#                  np.array([1.5, 0.5, 1, 0.5])]
#
#     beats = np.concatenate(beats_raw)
#
#     multiplier = np.zeros((len(beats),))
#
#     for i in range(len(beats) - 1):
#         # 2 times the previous beats + previous multi
#         multiplier[i + 1] = 2 * beats[i] + multiplier[i]
#
#     # generate note pos by cycling through [100, 200, 300]
#     pos_ = np.zeros(beats.shape)
#     col_ = 100
#     start_ = 0
#     for bar in beats_raw:
#         temp_note_len = len(bar)
#         pos_[start_:start_ + temp_note_len] = np.ones((temp_note_len,)) * col_
#         start_ += temp_note_len
#         col_ += 100
#         if col_ > 300: col_ = 100
#
#     note_ys = [(top_flower - 2 * note_size) - multiplier[i] * note_size for i in range(len(beats))]
#
#     for i in range(len(beats)):
#         # pos of silent notes
#         # if i == 26 or i == 31:
#         #     continue
#         notes.add(Note([pos_[i], note_ys[i]]))


pg.init()

# Screen
screen = pg.display.set_mode((400, 800))
pg.display.set_caption('Like a ')
clock = pg.time.Clock()
game_active = False

# Backgrounddsds
background = pg.image.load('graphic/ParkBackground.jpg').convert()
background = aspect_scale(background, 4000, 800)
screen.blit(background, (0, 0))

# music
BYWM = BecauseYouWalkWithMe()
note_height = 60  
# px
beatRatio = BYWM.beatsRatio
# bps = BYWM.bpm * BYWM.beatsRatio / 60  # beats / s
dt = 17 / 1000  # ms

bg_music = pg.mixer.Sound('BGM/Because You Walk With Me.wav')

# Text
font = pg.font.Font(None, 24)
text = font.render("Click to Start", True, (10, 10, 10))
textpos = text.get_rect(centerx=screen.get_width() / 2, y=150)
screen.blit(text, textpos)

pg.display.flip()

# Groups
player = pg.sprite.GroupSingle()
p1 = Player()
player.add(p1)

notes = pg.sprite.Group()

#Game Over Images
rest_sprite_iter = itertools.cycle(SpriteSheet("graphic/Rest Sprite.png", 500, 500).load_grid_images(1,2,x_margin=0,x_padding=0,y_margin=0,y_padding=0))
rest_sprite = next(rest_sprite_iter)
ggTimer = 50

game_start = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
        else:
            if event.type == pg.MOUSEBUTTONDOWN and not game_active:
                # 450 is the player top y-pos
                initNotes(BYWM, note_height, 500)
                bg_music.play(loops=-1)
                p1.score = 0
            if event.type == pg.MOUSEBUTTONDOWN:
                game_active = True
                game_start = False
                
                
            

    if game_active:
        pg.mouse.set_visible(False)
        screen.blit(background, (0, 0))
        player.update()
        player.draw(screen)

        notes.update()
        notes.draw(screen)

        score_cur = p1.getScore()
        score_surf = font.render('Score: {}'.format(score_cur), False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(200, 50))
        screen.blit(score_surf, score_rect)

        for note in notes:
            if not note.caught(p1):
                game_active = False
                break

    elif not game_start:
        bg_music.stop()
        pg.mouse.set_visible(True)
        notes.empty()
        final_score = p1.getScore()
        screen.blit(background, (0, 0))
        #Display Score
        score_surf = font.render('Score: {}'.format(final_score), False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(200, 100))
        screen.blit(score_surf, score_rect)
        screen.blit(text, textpos)
        #Display Images
        if ggTimer <= 0:
            rest_sprite = next(rest_sprite_iter)
            ggTimer = 50
        ggTimer -= 1
        screen.blit(rest_sprite, rest_sprite.get_rect(center = (200,570)))

    pg.display.flip()
    dt = clock.tick(60) / 1000
