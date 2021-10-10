import pygame as pg
from RoutingTable import RoutingTable

from Packet import Packet

pkts = dict()
qry = dict()

radius = 50

nodes = list()

max_time = 20


def get_max_time():
    return max_time


def make_query(source, dest, vector):
    packet = dict()
    packet["source"] = source
    packet["dest"] = dest
    return packet


class Router:
    routers = 0

    def __init__(self, x, y, color):
        self.id = Router.routers
        Router.routers += 1
        self.vector = [49] * Router.routers
        self.hops = ["-"] * Router.routers
        self.second = [(49, "-")] * Router.routers
        self.vector[self.id] = 0
        self.hops[self.id] = self.id
        self.second[self.id] = (0, self.id)
        self.links = dict()
        self.active = False
        self.queryPackets = set()
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.rt = RoutingTable(self)

    def add_link(self, router, cost):
        self.vector[router.id] = cost
        self.hops[router.id] = self.id
        self.links[router] = cost

    def new_route(self):
        self.vector.append(49)
        self.hops.append("-")
        self.second.append((49, "-"))

    def send_packet(self, time_now):
        for neighbour in self.links.keys():
            packet = Packet(self, neighbour, self.vector, time_now)
            global max_time
            max_time = max(max_time, time_now + self.links[neighbour] + 2)

            if max_time == time_now + self.links[neighbour]:
                print("Max time updated: ", max_time)

            if (
                time_now + self.links[neighbour] in pkts.keys()
                and packet not in pkts[time_now + self.links[neighbour]]
            ):
                pkts[time_now + self.links[neighbour]].append(packet)
                print("Packet sent from {} to {}".format(self.id, neighbour.id))
            else:
                pkts[time_now + self.links[neighbour]] = [packet]
                print("Packet sent from {} to {}".format(self.id, neighbour.id))

    def recv_packet(self, packet, time_now):
        if packet["query"] and self.active:
            self.queryPackets.add(packet["source"].id)
            print("Query received from {} at {}".format(packet["source"].id, self.id))
            if len(self.queryPackets) == len(self.links):
                self.active = False

        else:
            print("Packet received from {} at {}".format(packet["source"].id, self.id))

        table = self.vector.copy()

        table2 = list()

        distance_dest_source = self.links[packet["source"]]

        for i in packet["vector"]:
            table2.append(i + distance_dest_source)

        for ind in range(len(self.vector)):
            if self.hops[ind] == packet["source"]:
                self.vector[ind] = table2[ind]

            else:
                prev = self.vector[ind]
                self.vector[ind] = min(table2[ind], self.vector[ind])
                if self.vector[ind] != prev:
                    self.hops[ind] = packet["source"].id

                elif (
                    packet["vector"][ind] < self.vector[ind]
                    and table2[ind] != self.vector[ind]
                ):
                    print("Updated second hop of {} at {}".format(ind, self.id))
                    if self.second[ind][0] > table2[ind]:
                        self.second[ind] = (
                            table2[ind],
                            packet["source"].id,
                        )

        if table != self.vector:
            print("Updated routing table for {}".format(self.id))
            self.send_packet(time_now)
            self.print_details()

        else:
            print("No changes in routing table for {}".format(self.id))

    def recv_query(self, packet, time_now):
        if packet["source"] in [neighbour for neighbour in self.links.keys()]:
            print("Query received from {} at {}".format(packet["source"].id, self.id))

            packet = Packet(self, packet["source"], self.vector, time_now)
            packet["query"] = True

            neighbour = packet["source"]

            global max_time
            max_time = max(max_time, time_now + self.links[neighbour] + 2)

            if max_time == time_now + self.links[neighbour]:
                print("Max time updated: ", max_time)

            if (
                time_now + self.links[neighbour] in pkts.keys()
                and packet not in pkts[time_now + self.links[neighbour]]
            ):
                pkts[time_now + self.links[neighbour]].append(packet)
                print("Packet sent from {} to {}".format(self.id, neighbour.id))
            else:
                pkts[time_now + self.links[neighbour]] = [packet]
                print("Packet sent from {} to {}".format(self.id, neighbour.id))

    def send_query(self, time_now):
        self.active = True
        self.queryPackets = set()
        for neighbour in self.links.keys():
            packet = make_query(self, neighbour, self.vector)
            if time_now + self.links[neighbour] in qry.keys():
                qry[time_now + self.links[neighbour]].append(packet)
            else:
                qry[time_now + self.links[neighbour]] = [packet]

    def remove_link(self, router, time_now):
        print("Link removed from {} to {}".format(self.id, router.id))
        self.vector[router.id] = 49
        self.hops[router.id] = "-"
        self.links.pop(router.id)
        self.send_packet(time_now)

    def print_details(self):
        print("Node: {}".format(self.id))
        for i in range(Router.routers):
            print(self.id, "->", i, ":", self.vector[i], "via", self.hops[i])

    def draw_links(self, screen):
        for neighbour in self.links.keys():
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
                str(self.links[neighbour]), True, (240, 242, 245), (0, 2, 5)
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
        for neighbour in node.links.keys():
            packet = Packet(node, neighbour, node.vector, time_now)
            if time_now + node.links[neighbour] in pkts.keys():
                pkts[time_now + node.links[neighbour]].append(packet)
            else:
                pkts[time_now + node.links[neighbour]] = [packet]


def receive_packet(packet, time_now):
    dest = packet["dest"]
    dest.recv_packet(packet, time_now)
