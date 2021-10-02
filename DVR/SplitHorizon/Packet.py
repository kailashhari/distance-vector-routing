import pygame as pg

inf = 49


class Packet:
    def __init__(self, source, dest, vector, hops, time):
        self.packet = dict()
        self.packet["source"] = source.id
        self.packet["dest"] = dest.id

        new_vector = vector.copy()

        for i in range(len(hops)):
            if hops[i] == dest.id:
                new_vector[i] = inf

        self.packet["vector"] = new_vector

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
