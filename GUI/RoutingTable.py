import pygame as pg

width = 450

height = 200

color = (0, 0, 0)


class RoutingTable:
    def __init__(self, node):
        if node.x == 650:
            self.x = 50
        else:
            self.x = 1400
        self.y = node.y - 100
        self.color = node.color

    def draw(self, screen, node):
        pg.draw.rect(screen, self.color, pg.Rect(self.x, self.y, width, height), 5)
        for i in range(1, 6):
            pg.draw.line(
                screen,
                self.color,
                (self.x + width / 6 * i, self.y),
                (self.x + width / 6 * i, self.y + height),
                3,
            )
        for i in range(1, 3):
            pg.draw.line(
                screen,
                self.color,
                (self.x, self.y + height / 3 * i),
                (self.x + width, self.y + height / 3 * i),
                1,
            )
        font = pg.font.Font("freesansbold.ttf", 22)
        for i in range(0, 6):
            text = font.render(str(i), True, self.color, (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (self.x + width / 6 * i + width / 12, self.y + height / 6)
            screen.blit(text, textRect)

        for i in range(0, 6):
            val = node.vector[i]
            if val == 49:
                val = "Inf"
            text = font.render(str(val), True, self.color, (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 6 * i + width / 12,
                self.y + 3 * height / 6,
            )
            screen.blit(text, textRect)

        for i in range(0, 6):
            text = font.render(str(node.hops[i]), True, self.color, (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 6 * i + width / 12,
                self.y + 5 * height / 6,
            )
            screen.blit(text, textRect)
