import pygame as pg


class Packet:
    def __init__(self, source, dest, vector, time):
        self.packet = dict()
        self.packet["source"] = source
        self.packet["dest"] = dest
        new_vector = vector.copy()

        # split horizon
        for i in range(len(source.hops)):
            if source.hops[i] == dest.id:
                new_vector[i] = 49  # Poison reverse

        self.packet["vector"] = new_vector
        self.packet["query"] = False

        self.source = source

        self.start_time = time

        self.time = source.links[dest]

        self.speed = [(dest.x - source.x) / self.time, (dest.y - source.y) / self.time]

    def draw(self, screen, time, size):
        pg.draw.circle(
            screen,
            self.source.color,
            (
                self.source.x + self.speed[0] * (time - self.start_time),
                self.source.y + self.speed[1] * (time - self.start_time),
            ),
            size,
            size,
        )
        pg.draw.circle(
            screen,
            (255, 255, 255),
            (
                self.source.x + self.speed[0] * (time - self.start_time),
                self.source.y + self.speed[1] * (time - self.start_time),
            ),
            size,
            size // 4,
        )
