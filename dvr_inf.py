import time
import math

pkts = dict()
nodes = list()

max_time = 20


def make_packet(source, dest, vector):
    packet = dict()
    packet["source"] = source
    packet["dest"] = dest
    packet["vector"] = vector
    return packet


class Router:
    routers = 0

    def __init__(self):
        self.id = Router.routers
        Router.routers += 1
        self.vector = [49] * Router.routers
        self.hops = ["-"] * Router.routers
        self.vector[self.id] = 0
        self.hops[self.id] = self.id
        self.neighbors = list()
        self.links = dict()
        self.packets = dict()

    def init_again(self):
        self.vector = [49] * Router.routers
        self.vector[self.id] = 0
        self.hops = ["-"] * Router.routers
        self.hops[self.id] = self.id
        self.links = dict()
        self.neighbors = list()

    def add_link(self, router, cost):
        self.vector[router.id] = cost
        self.hops[router.id] = self.id
        self.neighbors.append(router)
        self.links[router.id] = cost

    def new_route(self):
        self.vector.append(49)
        self.hops.append("-")

    def send_packet(self, time_now):
        for neighbour in self.neighbors:
            id = neighbour.id
            packet = make_packet(self.id, id, self.vector)
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
        self.vector[router.id] = 49
        self.hops[router.id] = "-"
        self.neighbors.remove(router)
        self.links.pop(router.id)
        self.packets.pop(router.id)
        self.send_packet(time_now)

    def print_details(self):
        print("Node: {}".format(self.id))
        for i in range(Router.routers):
            print(self.id, "->", i, ":", self.vector[i], "via", self.hops[i])


def link_nodes(node1, node2, cost):
    node1.add_link(node2, cost)
    node2.add_link(node1, cost)


def remove_link(node1, node2, time_now):
    node1.remove_link(node2, time_now)
    node2.remove_link(node1, time_now)


def link_cost(node1, node2):
    return node1.vector[node2.id]


def main():

    # Initialise routers
    for i in range(6):
        [node.new_route() for node in nodes]
        nodes.append(Router())

    # Add links
    link_nodes(nodes[0], nodes[1], 5)
    link_nodes(nodes[1], nodes[2], 3)
    link_nodes(nodes[2], nodes[5], 6)
    link_nodes(nodes[2], nodes[4], 4)
    link_nodes(nodes[2], nodes[3], 7)

    t_start = time.time()

    def receive_packet(packet, time_now):
        dest = packet["dest"]
        node = nodes[dest]
        node.recv_packet(packet, time_now)

    def sendpkt_initial(time_now):
        for node in nodes:
            for neighbour in node.neighbors:
                packet = make_packet(node.id, neighbour.id, node.vector)
                if time_now + node.links[neighbour.id] in pkts.keys():
                    pkts[time_now + node.links[neighbour.id]].append(packet)
                else:
                    pkts[time_now + node.links[neighbour.id]] = [packet]

    sendpkt_initial(0)

    print("Packet Sent to all routers from their neighbours")

    times = set()

    while 1:
        time_now = time.time() - t_start
        if math.floor(time_now) not in times:
            times.add(math.floor(time_now))
            if time_now in pkts.keys():
                print("At time {}".format(time_now))
                for k in pkts[time_now]:
                    receive_packet(k, time_now)
            if time_now == 10:
                remove_link(nodes[2], nodes[1], time_now)

            if t_start + max_time < time.time():
                print(
                    "At time {} all packets are sent and stabity established".format(
                        time_now - 2
                    )
                )
                break

    for node in nodes:
        node.print_details()


if __name__ == "__main__":
    main()
