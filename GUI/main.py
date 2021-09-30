import pygame as pg
import time, math

from Node import (
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

FPS = 300  # frames per second setting
fpsClock = pg.time.Clock()


# set window caption and logo
pg.display.set_caption("Networks Theory")
icon = pg.image.load("./assets/logo.jpg")
pg.display.set_icon(icon)

running = True

l = 0

slow_down = 1

times = set()

t_start = None

init_nodes()

# game loop
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 2, 5))

    [node.draw_links(screen) for node in nodes]

    [node.draw(screen) for node in nodes]

    if t_start is not None:
        time_now_ms = (time.time() - t_start) / slow_down
        time_now = math.floor(time.time() - t_start) / slow_down
        font = pg.font.Font("freesansbold.ttf", 40)
        text = font.render(str(round(time_now_ms, 2)), True, (240, 242, 245), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (screen_width / 2, 100)
        screen.blit(text, textRect)

        for i in pkts.keys():
            if i >= time_now:
                for pk in pkts[i]:
                    pk.draw(screen, time_now_ms)

        if math.floor(time_now) not in times:
            times.add(math.floor(time_now))
            if time_now in pkts.keys():
                for k in pkts[time_now]:
                    receive_packet(k.packet, time_now)

                pkts.pop(time_now)

            # if time_now == 10:
            #     remove_link(nodes[2], nodes[1], time_now)

            if t_start + get_max_time() * slow_down + 5 / slow_down < time.time():
                print(
                    "At time {} all packets are sent and stabity established".format(
                        get_max_time()
                    )
                )
                break

    l += 1

    if l == 400:
        t_start = time.time()
        sendpkt_initial(0)

    pg.display.update()
    fpsClock.tick(FPS)


pg.quit()
