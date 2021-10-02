from djs import Graph
import time, math

max_time = 30
expiry = 10

nodes = list()

pkts = dict()


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


def send_packet(node, packet: Packet, time_now):
    if time_now in pkts.keys():
        pkts[time_now].append((packet, node))
    else:
        pkts[time_now] = [(packet, node)]


class Router:
    """
    Router
    """

    count = 0

    def __init__(self):
        self.sequence_number = 0
        self.id = Router.count
        Router.count += 1
        self.neighbors = dict()
        self.fullData = dict()
        self.packets_received = set()
        self.expiry = expiry
        self.latest = dict()

    def add_link(self, neighbour, cost):
        """
        Link Routers
        """
        print("Router {} connected to: {}".format(self.id, neighbour.id))
        self.neighbors[neighbour] = cost

    def remove_link(self, neighbour, time_now):
        """
        Remove Link
        """
        print("Router {} disconnected from: {}".format(self.id, neighbour.id))
        self.neighbors.pop(neighbour)
        self.send_packet(time_now)

    def compute_table(self):
        g = Graph(Router.count)
        print("Computing table for {}".format(self.id))

        for node in self.neighbors.keys():
            g.add_edge(self.id, node.id, self.neighbors[node])

        for item in self.fullData.keys():
            for node in self.fullData[item].data.keys():
                g.add_edge(item.id, node.id, self.fullData[item].data[node])

        g.dijkstra(self.id)

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
                send_packet(neighbour, packet, time_now + self.neighbors[neighbour])

    def send_packet(self, time_now):
        """
        Send Packet
        """
        print("Sending packets from {}".format(self.id))
        packet = Packet(self.sequence_number, self.neighbors, self)
        for neighbour in self.neighbors.keys():
            send_packet(neighbour, packet, time_now + self.neighbors[neighbour])
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


def link_nodes(node1: Router, node2: Router, cost):
    node1.add_link(node2, cost)
    node2.add_link(node1, cost)


def remove_link(node1: Router, node2: Router, time_now):
    node1.remove_link(node2, time_now)
    node2.remove_link(node1, time_now)


def main():
    # Initialise routers
    for _ in range(6):
        nodes.append(Router())

    # Add links
    link_nodes(nodes[0], nodes[1], 5)
    link_nodes(nodes[1], nodes[2], 3)
    link_nodes(nodes[2], nodes[5], 6)
    link_nodes(nodes[2], nodes[4], 4)
    link_nodes(nodes[2], nodes[3], 7)

    t_start = time.time()

    def receive_packet(packetpack: dict, time_now):
        packet = packetpack[0]
        node = packetpack[1]
        node.receive_pkt(packet, time_now)

    times = set()

    while 1:
        time_now = math.floor(time.time() - t_start)
        if math.floor(time_now) not in times:

            print("At time {}".format(time_now))

            times.add(math.floor(time_now))

            if time_now % 5 == 0:
                for node in nodes:
                    node.send_packet(time_now)

            if time_now == 10:
                remove_link(nodes[2], nodes[1], time_now)

            [node.delete_data(math.floor(time_now)) for node in nodes]

            if time_now in pkts.keys():
                for k in pkts[time_now]:
                    receive_packet(k, time_now)

            if t_start + max_time < time.time():
                print("At time {} process is stopped".format(time_now))
                break


if __name__ == "__main__":
    main()
