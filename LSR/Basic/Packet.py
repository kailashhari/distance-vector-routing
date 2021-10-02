import pygame as pg


class Packet:
    """
    Packets
    """

    count = 0

    def __init__(self, seq_no, data, source):
        self.sequence_number = seq_no
        self.id = Packet.count
        Packet.count += 1
        self.data = data
        self.source = source
        self.received = set()
        self.received.add(source.id)


def drawPacket(screen, packet: Packet, source, dest, start_time, time, delay):

    speed = [(dest.x - source.x) / delay, (dest.y - source.y) / delay]
    pg.draw.circle(
        screen,
        packet.source.color,
        (
            source.x + speed[0] * (time - start_time),
            source.y + speed[1] * (time - start_time),
        ),
        20,
        20,
    )
    pg.draw.circle(
        screen,
        (255, 255, 255),
        (
            source.x + speed[0] * (time - start_time),
            source.y + speed[1] * (time - start_time),
        ),
        20,
        5,
    )
    font = pg.font.Font("freesansbold.ttf", 10)
    text = font.render(str(packet.id), True, (255, 255, 255), packet.source.color)
    textRect = text.get_rect()
    textRect.center = (
        source.x + speed[0] * (time - start_time),
        source.y + speed[1] * (time - start_time),
    )
    screen.blit(text, textRect)
