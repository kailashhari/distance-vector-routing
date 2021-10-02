import pygame as pg
import time, math

import threading

from pygame.constants import K_SPACE


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


from Node import (
    add_link,
    nodes,
    sendpkt_initial,
    get_max_time,
    receive_packet,
    pkts,
    init_nodes,
    remove_link,
)

# initialise game engine
pg.init()

# set screen size
screen_width = 1920
screen_height = 1080
screen = pg.display.set_mode([screen_width, screen_height])

# frames per second setting
FPS = 60
fpsClock = pg.time.Clock()

# set window caption and logo
pg.display.set_caption("Networks Theory")
icon = pg.image.load("./assets/logo.jpg")
pg.display.set_icon(icon)

running = True

# for delay start
l = 0

slow_down = 1
times = set()

# start time
t_start = None

# initialise nodes
init_nodes()

sendpkt_initial(0)

# pause
is_paused = True
t_start = time.time()
elapsed_time = 0

# game loop
while running:
    if not is_paused:
        elapsed_time = time.time() - t_start

    else:
        t_start = time.time() - elapsed_time

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == 768:
            is_paused = not is_paused

    # empty screen
    screen.fill((0, 2, 5))

    # draw nodes
    [node.draw_links(screen) for node in nodes]

    # draw links
    [node.draw(screen) for node in nodes]

    # check start
    time_now_ms = (time.time() - t_start) / slow_down
    time_now = math.floor(time.time() - t_start) / slow_down

    # draw timer
    font = pg.font.Font("freesansbold.ttf", 40)
    text = font.render(str(round(time_now_ms, 1)), True, (240, 242, 245), (0, 2, 5))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, 50)
    screen.blit(text, textRect)

    # draw packets
    if not is_paused or elapsed_time != 0:
        for i in pkts.keys():
            if i >= time_now:
                for pk in pkts[i]:
                    pk.draw(screen, time_now_ms)

    # receive packets
    if math.floor(time_now) not in times:
        # to check once in every second
        times.add(math.floor(time_now))
        if time_now in pkts.keys():
            for k in pkts[time_now]:
                receive_packet(k.packet, time_now)

            pkts.pop(time_now)

        if time_now == 2:
            remove_link(nodes[1], nodes[2], time_now)

        # end of simulation
        if t_start + get_max_time() * slow_down + 5 / slow_down < time.time():
            print(
                "At time {} all packets are sent and stabity established".format(
                    get_max_time()
                )
            )
            break

    font = pg.font.Font("freesansbold.ttf", 40)
    flex = "A Project By"
    text = font.render(flex, True, (10, 74, 240, 0.8), (0, 2, 5))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, 760)
    screen.blit(text, textRect)

    text = font.render("H.Kailash - 106119050", True, (14, 229, 21, 0.8), (0, 2, 5))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, 810)
    screen.blit(text, textRect)

    text = font.render("&", True, (240, 161, 10, 0.8), (0, 2, 5))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, 860)
    screen.blit(text, textRect)

    text = font.render("Indresh.P - 106119052", True, (240, 31, 10, 0.8), (0, 2, 5))
    textRect = text.get_rect()
    textRect.center = (screen_width / 2, 910)
    screen.blit(text, textRect)

    # update screen
    pg.display.flip()
    fpsClock.tick(FPS)

# quit game
pg.quit()
