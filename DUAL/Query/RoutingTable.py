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
        for i in range(1, 7):
            pg.draw.line(
                screen,
                self.color,
                (self.x + width / 7 * i, self.y),
                (self.x + width / 7 * i, self.y + height),
                1,
            )
        for i in range(1, 4):
            pg.draw.line(
                screen,
                self.color,
                (self.x, self.y + height / 4 * i),
                (self.x + width, self.y + height / 4 * i),
                3,
            )
        font = pg.font.Font("freesansbold.ttf", 32)
        text = font.render("N", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + height / 8)
        screen.blit(text, textRect)
        for i in range(1, 7):
            text = font.render(str(i - 1), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (self.x + width / 7 * i + width / 14, self.y + height / 8)
            screen.blit(text, textRect)

        text = font.render("D", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + 3 * height / 8)
        screen.blit(text, textRect)
        for i in range(1, 7):
            val = node.vector[i - 1]
            if val == 49:
                val = "Inf"
            text = font.render(str(val), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 7 * i + width / 14,
                self.y + 3 * height / 8,
            )
            screen.blit(text, textRect)

        text = font.render("H", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + 5 * height / 8)
        screen.blit(text, textRect)
        for i in range(1, 7):
            text = font.render(str(node.hops[i - 1]), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 7 * i + width / 14,
                self.y + 5 * height / 8,
            )
            screen.blit(text, textRect)

        text = font.render("S", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + 7 * height / 8)
        screen.blit(text, textRect)
        for i in range(1, 7):
            text = font.render(
                str(node.second[i - 1][1]), True, (255, 255, 255), (0, 2, 5)
            )
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 7 * i + width / 14,
                self.y + 7 * height / 8,
            )
            screen.blit(text, textRect)
