import pygame as pg
from RoutingTable import RoutingTable

from Packet import Packet

scale_down = 0.7
pkts = dict()

radius = int(50 * scale_down)

nodes = list()

max_time = 20


def get_max_time():
    return max_time


class Router:
    routers = 0

    def __init__(self, x, y, color):
        self.id = Router.routers
        Router.routers += 1
        self.vector = [25] * Router.routers
        self.hops = ["-"] * Router.routers
        self.vector[self.id] = 0
        self.hops[self.id] = self.id
        self.neighbors = list()
        self.links = dict()
        self.packets = dict()
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.rt = RoutingTable(self)

    def init_again(self):
        self.vector = [25] * Router.routers
        self.vector[self.id] = 0
        self.hops = ["-"] * Router.routers
        self.hops[self.id] = self.id
        self.links = dict()
        self.neighbors = list()

    def add_link(self, router, cost):
        self.vector[router.id] = cost
        self.hops[router.id] = router.id
        self.neighbors.append(router)
        self.links[router.id] = cost

    def new_route(self):
        self.vector.append(25)
        self.hops.append("-")

    def send_packet(self, time_now):
        for neighbour in self.neighbors:
            id = neighbour.id
            packet = Packet(self, neighbour, self.vector, time_now)
            global max_time
            max_time = max(max_time, time_now + self.links[id] + 2)

            if max_time == time_now + self.links[id]:
                print("Max time updated: ", max_time)

            if (
                time_now + self.links[id] in pkts.keys()
                and packet not in pkts[time_now + self.links[id]]
            ):
                pkts[time_now + self.links[id]].append(packet)
                print("Packet sent from {} to {}".format(self.id, id))
            else:
                pkts[time_now + self.links[id]] = [packet]
                print("Packet sent from {} to {}".format(self.id, id))

    def recv_packet(self, packet, time_now):
        if packet["source"] in [neighbour.id for neighbour in self.neighbors]:
            print("Packet received from {} at {}".format(packet["source"], self.id))
            self.packets[packet["source"]] = packet["vector"]
            if len(self.packets) == len(self.neighbors):
                print("All packets received by {}".format(self.id))

                table = self.vector

                links = self.links.copy()
                self.init_again()
                for neighbour in links.keys():
                    self.add_link(nodes[neighbour], links[neighbour])

                for neighbour in self.packets.keys():
                    for j in range(Router.routers):
                        if j != self.id:
                            self.vector[j] = min(
                                self.vector[j],
                                self.packets[neighbour][j] + self.links[neighbour],
                            )
                            if (
                                self.vector[j]
                                == self.packets[neighbour][j] + self.links[neighbour]
                            ):
                                self.hops[j] = neighbour

                if table != self.vector:
                    print("Updated routing table for {}".format(self.id))
                    self.send_packet(time_now)
                    self.print_details()

                else:
                    print("No changes in routing table for {}".format(self.id))

    def remove_link(self, router, time_now):
        print("Link removed from {} to {}".format(self.id, router.id))
        self.vector[router.id] = 25
        self.hops[router.id] = "-"
        self.neighbors.remove(router)
        self.links.pop(router.id)
        if router.id in self.packets.keys():
            self.packets.pop(router.id)
        self.send_packet(time_now)

    def print_details(self):
        print("Node: {}".format(self.id))
        for i in range(Router.routers):
            print(self.id, "->", i, ":", self.vector[i], "via", self.hops[i])

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
                str(self.links[neighbour.id]), True, (240, 242, 245), (0, 2, 5)
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


colors = [
    (10, 74, 240, 0.8),
    (14, 229, 21, 0.8),
    (103, 10, 240, 0.8),
    (240, 161, 10, 0.8),
    (240, 31, 10, 0.8),
    (210, 60, 138, 0.8),
]

position = [
    (int(650 * scale_down), int(150 * scale_down)),
    (int(650 * scale_down), int(450 * scale_down)),
    (int(1250 * scale_down), int(450 * scale_down)),
    (int(1250 * scale_down), int(150 * scale_down)),
    (int(1250 * scale_down), int(750 * scale_down)),
    (int(650 * scale_down), int(750 * scale_down)),
]

# Initialise routers
def init_nodes():
    for i in range(6):
        [node.new_route() for node in nodes]
        nodes.append(Router(position[i][0], position[i][1], colors[i]))

    def link_nodes(node1, node2, cost):
        node1.add_link(node2, cost)
        node2.add_link(node1, cost)

    link_nodes(nodes[0], nodes[1], 5)
    link_nodes(nodes[1], nodes[2], 3)
    link_nodes(nodes[2], nodes[5], 6)
    link_nodes(nodes[2], nodes[4], 4)
    link_nodes(nodes[2], nodes[3], 7)


def remove_link(node1, node2, time_now):
    node1.remove_link(node2, time_now)
    node2.remove_link(node1, time_now)

    for t in pkts.keys():
        pk = pkts[t].copy()
        for packet in pk:
            if (
                packet.packet["source"] == node1.id
                and packet.packet["dest"] == node2.id
            ):
                pkts[t].remove(packet)
            if (
                packet.packet["source"] == node2.id
                and packet.packet["dest"] == node1.id
            ):
                pkts[t].remove(packet)


def add_link(node1, node2, cost, time_now):
    node1.add_link(node2, cost)
    node2.add_link(node1, cost)
    node1.send_packet(time_now)
    node2.send_packet(time_now)


def sendpkt_initial(time_now):
    for node in nodes:
        for neighbour in node.neighbors:
            packet = Packet(node, neighbour, node.vector, 0)
            if time_now + node.links[neighbour.id] in pkts.keys():
                pkts[time_now + node.links[neighbour.id]].append(packet)
            else:
                pkts[time_now + node.links[neighbour.id]] = [packet]


def receive_packet(packet, time_now):
    dest = packet["dest"]
    node = nodes[dest]
    node.recv_packet(packet, time_now)
