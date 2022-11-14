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
from Follower import Follower


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
    bpm = song.bpm[song.introEndPoint+1:]

    # render notes on screen
    for i in range(len(pos_y)):
        if set(sus).intersection({i}):
            continue

        speed = 16/1000 * bpm[i]/60 * note_height * beatRatio
        notes.add(Note([pos_x[i], pos_y[i]], speed))


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
note_height = 50
# px
beatRatio = BYWM.beatsRatio
# bps = BYWM.bpm * BYWM.beatsRatio / 60  # beats / s
# dt = 17 / 1000  # ms

bg_music = pg.mixer.Sound('BGM/Because You Walk With Me.wav')

# Text
font = pg.font.Font(None, 24)
text = font.render("Click to Start", True, (10, 10, 10))
textpos = text.get_rect(centerx=screen.get_width() / 2, y=150)
screen.blit(text, textpos)

pg.display.flip()

# Groups
player = pg.sprite.Group()
p1 = Player()
# followers = Follower(p1)
# player.add(followers)
player.add(p1)

notes = pg.sprite.Group()

#Game Over Images
rest_sprite_iter = itertools.cycle(SpriteSheet("graphic/Rest Sprite.png", 500, 500).load_grid_images(1,2,x_margin=0,x_padding=0,y_margin=0,y_padding=0))
rest_sprite = next(rest_sprite_iter)
ggTimer = 50

game_start = True

while True:

    st = time.time()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
        elif event.type == pg.MOUSEBUTTONDOWN and not game_active:
                # 450 is the player top y-pos
                initNotes(BYWM, note_height, 510)
                bg_music.play(loops=-1)
                p1.score = 0
                game_active = True
                game_start = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_r:
                game_active = False

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
        # followers.clear()
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
        screen.blit(rest_sprite, rest_sprite.get_rect(center = (200, 570)))

    pg.display.flip()

    dt = time.time() - st
    if (16/1000 - dt) <= 0:
        time.sleep(16/1000)

    else:
        time.sleep(16/1000 - dt)
