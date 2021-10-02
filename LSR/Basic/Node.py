from RoutingTable import RoutingTable
from djs import Graph

import pygame as pg

from Packet import Packet

max_time = 100
expiry = 30

nodes = list()

pkts = dict()

radius = 50


def get_max_time():
    return max_time


def send_packet(node, packet: Packet, time_now, start_time, source, delay):
    if time_now in pkts.keys():
        pkts[time_now].append((packet, node, start_time, source, delay))
    else:
        pkts[time_now] = [(packet, node, start_time, source, delay)]


class Router:
    """
    Router
    """

    count = 0

    def __init__(self, x, y, color):
        self.sequence_number = 0
        self.id = Router.count
        Router.count += 1
        self.neighbors = dict()
        self.fullData = dict()
        self.packets_received = set()
        self.expiry = expiry
        self.latest = dict()
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.distance = list()
        self.rt = RoutingTable(self)

    def add_link(self, neighbour, cost):
        """
        Link Routers
        """
        print("Router {} connected to: {}".format(self.id, neighbour.id))
        self.neighbors[neighbour] = cost
        # self.compute_table()

    def remove_link(self, neighbour, time_now):
        """
        Remove Link
        """
        print("Router {} disconnected from: {}".format(self.id, neighbour.id))
        self.neighbors.pop(neighbour)
        # self.send_packet(time_now)
        # self.compute_table()

    def compute_table(self):
        g = Graph(Router.count)
        print("Computing table for {}".format(self.id))

        for node in self.neighbors.keys():
            g.add_edge(self.id, node.id, self.neighbors[node])

        for item in self.fullData.keys():
            for node in self.fullData[item].data.keys():
                g.add_edge(item.id, node.id, self.fullData[item].data[node])

        self.distance = g.dijkstra(self.id)

        print(self.distance)

    def delete_data(self, time_now):
        """
        Delete Data
        """
        for i in range(Router.count):
            if i != self.id and i in self.latest.keys() and time_now > self.latest[i]:
                print("Deleting data from {} at {}".format(i, self.id))
                self.fullData.pop(nodes[i])
                self.latest.pop(i)
                self.compute_table()

    def forward_packet(self, packet: Packet, time_now):
        """
        Forward Packet
        """
        print("Forwarding packet from {} at {}".format(packet.source.id, self.id))
        for neighbour in self.neighbors.keys():
            if neighbour.id not in packet.received:
                print("Forwarding packet {} to {}".format(packet.id, neighbour.id))
                send_packet(
                    neighbour,
                    packet,
                    time_now + self.neighbors[neighbour],
                    time_now,
                    self,
                    self.neighbors[neighbour],
                )

    def send_packet(self, time_now):
        """
        Send Packet
        """
        print("Sending packets from {}".format(self.id))
        packet = Packet(self.sequence_number, self.neighbors.copy(), self)
        for neighbour in self.neighbors.keys():
            send_packet(
                neighbour,
                packet,
                time_now + self.neighbors[neighbour],
                time_now,
                self,
                self.neighbors[neighbour],
            )
        self.sequence_number += 1

    def receive_pkt(self, packet: Packet, time_now):
        """
        Receive Packet
        """
        print("Received packet from {} at {}".format(packet.source.id, self.id))
        packet.received.add(self.id)

        data = self.fullData.copy()

        if packet.id not in self.packets_received:
            self.packets_received.add(packet.id)
            if packet.source in self.fullData.keys():
                if (
                    packet.sequence_number
                    > self.fullData[packet.source].sequence_number
                ):
                    self.fullData[packet.source] = packet
                    self.fullData[packet.source].expiry = time_now + self.expiry
                    self.latest[packet.source.id] = time_now + self.expiry

            else:
                self.fullData[packet.source] = packet
                self.fullData[packet.source].expiry = time_now + self.expiry
                self.latest[packet.source.id] = time_now + self.expiry

            self.forward_packet(packet, time_now)

        if data != self.fullData:
            self.compute_table()

    def draw_links(self, screen):
        for neighbour in self.neighbors:
            pg.draw.line(
                screen,
                (240, 242, 245),
                (self.x, self.y),
                (
                    neighbour.x,
                    neighbour.y,
                ),
                10,
            )
            font = pg.font.Font("freesansbold.ttf", 32)
            text = font.render(
                str(self.neighbors[neighbour]), True, (240, 242, 245), (0, 2, 5)
            )
            textRect = text.get_rect()
            textRect.center = (
                (self.x + neighbour.x) / 2 + 25,
                (self.y + neighbour.y) / 2 + 25,
            )
            screen.blit(text, textRect)

    def draw(self, screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.radius, 0)
        pg.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 5)
        font = pg.font.Font("freesansbold.ttf", 40)
        text = font.render(str(self.id), True, (255, 255, 255), self.color)
        textRect = text.get_rect()
        textRect.center = (self.x, self.y)
        screen.blit(text, textRect)
        self.rt.draw(screen, self)


def link_nodes(node1: Router, node2: Router, cost):
    node1.add_link(node2, cost)
    node2.add_link(node1, cost)


def remove_link(node1: Router, node2: Router, time_now):
    node1.remove_link(node2, time_now)
    node2.remove_link(node1, time_now)

    print("Router {} disconnected from: {}".format(node1.id, node2.id))

    print([k[0].id for k in pkts[23]])

    for t in pkts.keys():
        pk = pkts[t].copy()
        for pack in pk:
            if t == 23:
                print(pack[0].id)
            if pack[3] == node1 and pack[1] == node2:
                pkts[t].remove(pack)

            elif pack[3] == node2 and pack[1] == node1:
                pkts[t].remove(pack)


colors = [
    (10, 74, 240, 0.8),
    (14, 229, 21, 0.8),
    (103, 10, 240, 0.8),
    (240, 161, 10, 0.8),
    (240, 31, 10, 0.8),
    (210, 60, 138, 0.8),
]

position = [
    (650, 150),
    (650, 450),
    (1250, 450),
    (1250, 150),
    (1250, 750),
    (650, 750),
]

# Initialise routers
def init_nodes():
    for i in range(6):
        nodes.append(Router(position[i][0], position[i][1], colors[i]))

    def link_nodes(node1, node2, cost):
        node1.add_link(node2, cost)
        node2.add_link(node1, cost)

    link_nodes(nodes[0], nodes[1], 5)
    link_nodes(nodes[1], nodes[2], 23)
    link_nodes(nodes[2], nodes[5], 6)
    link_nodes(nodes[2], nodes[4], 4)
    link_nodes(nodes[2], nodes[3], 7)
    link_nodes(nodes[3], nodes[1], 30)
    link_nodes(nodes[0], nodes[3], 10)

    for node in nodes:
        node.compute_table()


def receive_packet(packetpack: dict, time_now):
    packet = packetpack[0]
    node = packetpack[1]
    node.receive_pkt(packet, time_now)
