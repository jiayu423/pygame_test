import random
import time

import pygame as pg
from sys import exit
from random import choice
import numpy as np
from song_utils import *
from GIFImage import GIFImage


class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Cagney_transparent.webp")
        self.image = pg.transform.scale(self.image, (153, 276))
        self.rect = self.image.get_rect()
        self.offset = (-100, -50)
        self.originY = 500
        self.score = 0

    def update(self):
        pos = (pg.mouse.get_pos()[0], self.originY)
        self.rect.topleft = pos
        self.rect.move_ip(self.offset)

    def incScore(self, value):
        self.score += value

    def getScore(self):
        return self.score


class Note(pg.sprite.Sprite):
    def __init__(self, start_pos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("Tear_weepy.webp")
        #		self.image = pg.transform.scale(self.image, (50,100))
        self.rect = self.image.get_rect(midbottom=(start_pos[0], start_pos[1]))
        self.speed = 1
        self.y_float = float(self.rect.y)
        self.value = 1

    def update(self):
        """
        The current rhythm system works as follows:
        suppose we have a 60 bpm song, meaning 1 beat per second.
        if each of our note corresponds to 1 beat (1 note : 1 beat, this ratio can change),
        then it means that we need to 'kill' one note per second.
        (The notes are killed when their bottom y touches the top y of the player.)
        So to kill 1 notes/s, we need the note to travel exactly its height each second
        suppose our game is running at 60 fps, meaning that 1/60 s will pass between each frame
        so 33/1 (pixel/notes) * 1/1 (notes/beats) * 60/60 (beats/s) * 1/60 (s/frame) = 33/60 (pixel/frame)
        so after 60 frames (which is 1 s), the note will travel 33 pixel (1 beat), which is what we want
        """
        global dt, bps, note_height
        self.speed = dt * bps * note_height
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


class RedNote(Note):
    def __init__(self, start_pos):
        Note.__init__(self, start_pos)
        self.image = pg.image.load("Parriable_tear.webp")
        self.value = 3


def initNotes(song: Songs, note_size: int, top_player: int):
    """

    :param song: a list of counts
    :param note_size: height of note
    :param top_player: player top y position
    """

    sus = song[1]
    pos_x, pos_y = convertXY(song, note_size, top_player)

    # render notes on screen
    for i in range(len(pos_y)):
        if set(sus).intersection({i}):
            continue
        notes.add(Note([pos_x[i], pos_y[i]]))


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
background = pg.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))

# music
songBase = Songs()
KOKs = songBase.kingOfKings
note_height = 33  # px
bps = KOKs[0]['bpm'] * KOKs[0]['beatRatio'] / 60  # beats / s
dt = 17 / 1000  # ms

bg_music = pg.mixer.Sound('bg5.wav')

# Text
font = pg.font.Font(None, 24)
text = font.render("Click to Start", True, (10, 10, 10))
textpos = text.get_rect(centerx=background.get_width() / 2, y=150)
screen.blit(text, textpos)

pg.display.flip()

# Groups
player = pg.sprite.GroupSingle()
p1 = Player()
player.add(p1)

notes = pg.sprite.Group()

note_timer = pg.USEREVENT + 1
pg.time.set_timer(note_timer, 350)

game_start = True

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            pg.quit()
            exit()
        # if game_active:
        #     if event.type == note_timer:
        #         notes.add(choice([Note(choice([100, 200, 300])), RedNote(choice([100, 200, 300]))]))
        else:
            if event.type == pg.MOUSEBUTTONDOWN:
                game_active = True
                game_start = False
                p1.score = 0
                bg_music.play(loops=-1)
                # 450 is the player top y-pos
                initNotes(KOKs, note_height, 450)

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
            isCaught = note.caught(p1)
            if isCaught:
                pass
                # last_pos = notes.sprites()[-1].rect.topleft[-1]
                # last_pos -= 33
                # notes.add(choice([Note([choice([100, 100, 100]), last_pos]),
                #                   Note([choice([100, 100, 100]), last_pos])]))

            # if not note.caught(p1):
            #     game_active = False
            #     break

    elif not game_start:
        pg.mouse.set_visible(True)
        notes.empty()
        final_score = p1.getScore()
        screen.blit(background, (0, 0))
        score_surf = font.render('Score: {}'.format(final_score), False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(200, 100))
        screen.blit(score_surf, score_rect)
        screen.blit(text, textpos)
    # flower_gif.render(screen,(-50,300))

    pg.display.flip()
    dt = clock.tick(60) / 1000
