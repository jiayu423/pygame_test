import random
import time

import pygame as pg
from sys import exit
from random import choice
import numpy as np
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


def initNotes(notes: object, note_size: float, top_flower: float):
    """

    :param speed: falling speed of notes
    :param notes: a pg.sprite.Group object that contains notes
    :param note_size: height of the note
    :param top_flower: the y coord of flower top rect
    """

    # number of notes at the start of the game
    n_notes = int(np.floor((top_flower - note_size) / note_size))

    # create some hidden notes
    n_notes = n_notes + 5

    # list of notes y pos (the bottom of rect)
    note_ys = [(top_flower) - i * note_size * 2 for i in range(n_notes)]

    # render notes on screen
    for i in range(n_notes):
        notes.add(choice([Note([choice([100, 100, 100]), note_ys[i]]),
                          Note([choice([100, 100, 100]), note_ys[i]])]))


def initNotes_test(notes: object, note_size: float, top_flower: float):

    beats = [np.ones((8, )),
             np.ones((4, ))*2,
             np.ones((8, )),
             np.ones((3, ))*2, np.array([0.5, 1, 0.5]),
             np.array([0.5, 1.5, 0.5, 1, 0.5, 0.5, 1.5, 0.5, 1, 0.5])]

    beats = np.concatenate(beats)

    multiplier = np.zeros((len(beats), ))

    for i in range(len(beats)-1):
        # 2 times the previous beats + previous multi
        multiplier[i+1] = 2 * beats[i] + multiplier[i]

    # h = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 20, 24, 28])
    note_ys = [(top_flower-2*note_size) - multiplier[i] * note_size for i in range(len(beats))]
    print(note_ys)

    for i in range(len(beats)):
        notes.add(choice([Note([choice([100, 100, 100]), note_ys[i]]),
                          Note([choice([100, 100, 100]), note_ys[i]])]))


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
note_height = 33  # px
bps = 280 / 60  # beats / s
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

# flower_gif = GIFImage("resized_flower.gif")

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
                initNotes_test(notes, 33, 450)

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
