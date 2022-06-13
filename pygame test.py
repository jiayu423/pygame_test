import pygame as pg
from sys import exit
import pygame.time
from random import randint


# functions
def displayScore():
    current_time = int(pg.time.get_ticks()/1000 - startTime)
    score_surface = text_font.render(f'{current_time}', False, (64, 64, 64))
    score_rect = score_surface.get_rect(center=(int(screen_x / 2), 140))
    screen.blit(score_surface, score_rect)


def obsMovement(obsList):

    if obsList:
        for rect in obsList:
            rect.x -= 5
            screen.blit(stone, rect)

        obsList = [obs for obs in obsList if obs.x > -100]

    return obsList


def collisions(player, obstacles):

    if obstacles:
        for obs in obstacles:
            if player.colliderect(obs): return False
    return True


# variables
screen_x, screen_y = 641, 611  # size of the game screen
game_active = False
startTime = 0

# init game screen
pg.init()
screen = pg.display.set_mode((screen_x, screen_y))
pg.display.set_caption('wilderness')
clock = pygame.time.Clock()

# load image
bg = pg.image.load('graphics/wilderness.png')
sheep = pg.image.load('graphics/sheep2.png')
ground = pg.image.load('graphics/ground.png')
stone = pg.image.load('graphics/stone.png')
fly = pg.image.load('graphics/stone.png')
sheep1 = pg.image.load('graphics/sheep3.png')
sheep2 = pg.image.load('graphics/sheep4.png')

# sheep animation
sheep_list = [sheep1, sheep2, sheep]
swap = 0

# scaling and rotation
sheep_intro = pg.transform.rotozoom(sheep, 0, 2)

# text options
text_font = pg.font.Font(None, 50)  # (font type , font size)

# player
sheep_rect = sheep_list[-1].get_rect(midbottom=(100, 557))
sheep_rect_intro = sheep_intro.get_rect(center=(int(screen_x/2), int(screen_y/2)))
isJump = False

# obstacle
stone_rect_init = stone.get_rect(midbottom=(screen_x, 557))
obstacle_rect_list = [stone_rect_init]

# gravity!
sheep_gravity = 0

# timer
# this event will be auto triggered with user input
obstacle_timer = pg.USEREVENT + 1
pg.time.set_timer(obstacle_timer, 900)
sheep_timer = pg.USEREVENT + 2
pg.time.set_timer(sheep_timer, 120)

while True:

    for event in pg.event.get():
        # event loop to check user input
        # get() contains all events
        if event.type == pg.QUIT:
            pg.quit()
            exit()

        # if event.type == pg.MOUSEMOTION:
        #     # only trigger if mouse moved
        #     print(event.pos)

        if event.type == pg.KEYDOWN:
            # activate jump only when space pressed and touching the floor
            if event.key == pg.K_SPACE and sheep_rect.bottom == 557 and game_active:
                sheep_gravity = -15
                sheep = sheep_list[-1]
                sheep_rect = sheep.get_rect(midbottom=(100, 557))
                isJump = True
            elif event.key == pg.K_SPACE and not game_active != False:
                obstacle_rect_list = [stone_rect_init]
                startTime = int(pg.time.get_ticks()/1000)
                game_active = True

        if event.type == obstacle_timer and game_active:
            if randint(0, 2):
                obstacle_rect_list.append(stone.get_rect(midbottom=(randint(screen_x, screen_x+200), 557)))
            else:
                obstacle_rect_list.append(stone.get_rect(midbottom=(randint(screen_x, screen_x + 200), 500)))

        if event.type == sheep_timer and game_active and not isJump:
            sheep = sheep_list[swap]
            sheep_rect = sheep.get_rect(midbottom=(100, 557))
            if swap == 0: swap = 1
            else: swap = 0

    if game_active:
        # bg
        screen.blit(bg, (0, 0))  # block image transfer: place one surface over the display surface at location (second arg)
        screen.blit(ground, (0, 557))

        # # obstacles
        obstacle_rect_list = obsMovement(obstacle_rect_list)

        # score
        displayScore()

        # player
        sheep_gravity += 1
        sheep_rect.y += sheep_gravity
        if sheep_rect.bottom >= 557:
            sheep_rect.bottom = 557
            isJump = False
        screen.blit(sheep, sheep_rect)

        # # collision detection
        game_active = collisions(sheep_rect, obstacle_rect_list)
        # if stone_rect.colliderect(sheep_rect):
        #     game_active = False

    else:

        screen.fill((94, 129, 162))
        screen.blit(sheep_intro, sheep_rect_intro)
        obstacle_rect_list.clear()

    # keys = pg.key.get_pressed()
    # if keys[pg.K_SPACE]:
    #     print('caonima')

    # # detect collisions between two rects
    # if stone_rect.colliderect(sheep_rect):
    #     print('collision')

    # # check if mounse collides with stone
    # mouse_pos = pg.mouse.get_pos()
    # if stone_rect.collidepoint(mouse_pos):
    #     print(pg.mouse.get_pressed())

    pg.display.update()
    clock.tick(60)  # set max frame rate to 60 (so that the each iteration waits 1/60 s before proceeds)
