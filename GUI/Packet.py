import pygame as pg


class Packet:
    def __init__(self, source, dest, vector, time):
        self.packet = dict()
        self.packet["source"] = source.id
        self.packet["dest"] = dest.id
        self.packet["vector"] = vector

        self.source = source

        self.start_time = time

        self.time = source.links[dest.id]

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
