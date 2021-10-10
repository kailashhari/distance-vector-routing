import pygame as pg


class Packet:
    def __init__(self, source, dest, vector, time):
        self.packet = dict()
        self.packet["source"] = source
        self.packet["dest"] = dest
        self.packet["vector"] = vector
        self.packet["query"] = False

        self.source = source

        self.start_time = time

        self.time = source.links[dest]

        self.speed = [(dest.x - source.x) / self.time, (dest.y - source.y) / self.time]

    def draw(self, screen, time):
        pg.draw.circle(
            screen,
            self.source.color,
            (
                self.source.x + self.speed[0] * (time - self.start_time),
                self.source.y + self.speed[1] * (time - self.start_time),
            ),
            20,
            20,
        )
        pg.draw.circle(
            screen,
            (255, 255, 255),
            (
                self.source.x + self.speed[0] * (time - self.start_time),
                self.source.y + self.speed[1] * (time - self.start_time),
            ),
            20,
            5,
        )
