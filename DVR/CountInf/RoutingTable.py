import pygame as pg

scale_down = 0.7
width = int(450 * scale_down)

height = int(200 * scale_down)

color = (0, 0, 0)


class RoutingTable:
    def __init__(self, node):
        if node.x == int(650 * scale_down):
            self.x = int(50 * scale_down)
        else:
            self.x = int(1400 * scale_down)
        self.y = node.y - int(100 * scale_down)
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
        for i in range(1, 3):
            pg.draw.line(
                screen,
                self.color,
                (self.x, self.y + height / 3 * i),
                (self.x + width, self.y + height / 3 * i),
                3,
            )
        font = pg.font.Font("freesansbold.ttf", int(32 * scale_down))
        text = font.render("N", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + height / 6)
        screen.blit(text, textRect)
        for i in range(1, 7):
            text = font.render(str(i - 1), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (self.x + width / 7 * i + width / 14, self.y + height / 6)
            screen.blit(text, textRect)

        text = font.render("D", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + 3 * height / 6)
        screen.blit(text, textRect)
        for i in range(1, 7):
            val = node.vector[i - 1]
            if val == 49:
                val = "Inf"
            text = font.render(str(val), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 7 * i + width / 14,
                self.y + 3 * height / 6,
            )
            screen.blit(text, textRect)

        text = font.render("H", True, (255, 255, 255), (0, 2, 5))
        textRect = text.get_rect()
        textRect.center = (self.x + width / 14, self.y + 5 * height / 6)
        screen.blit(text, textRect)
        for i in range(1, 7):
            text = font.render(str(node.hops[i - 1]), True, (255, 255, 255), (0, 2, 5))
            textRect = text.get_rect()
            textRect.center = (
                self.x + width / 7 * i + width / 14,
                self.y + 5 * height / 6,
            )
            screen.blit(text, textRect)
