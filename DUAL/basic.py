import time
import math

pkts = dict()
qry = dict()
nodes = list()

max_time = 20
expiry = 20


def make_packet(source, dest, vector, time_now):
    packet = dict()
    packet["source"] = source
    packet["dest"] = dest
    packet["vector"] = vector
    packet["query"] = False
    return packet


class Router:
    routers = 0

    def __init__(self):
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
        self.neighboursPacket = dict()
        self.expiry = expiry

    def add_link(self, router, cost):
        self.vector[router.id] = cost
        self.hops[router.id] = router.id
        self.links[router] = cost

    def new_route(self):
        self.vector.append(49)
        self.hops.append("-")
        self.second.append((49, "-"))

    def delete_packet(self, time_now):
        packets = self.neighboursPacket.copy()
        for key in self.neighboursPacket.keys():
            if self.neighboursPacket[key][0] < time_now:
                packets.pop(key)

        self.neighboursPacket = packets

    def send_packet(self, time_now):
        for neighbour in self.links.keys():
            packet = make_packet(self, neighbour, self.vector, time_now)
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
            if self.hops[ind] == packet["source"].id:
                self.vector[ind] = table2[ind]
                if self.vector[ind] > self.second[ind][0]:
                    self.vector[ind] = self.second[ind][0]
                    self.hops[ind] = self.second[ind][1]
                    if self.vector[ind] < 49:
                        self.second[ind] = (self.vector[ind], self.hops[ind])
                    else:
                        self.second[ind] = (49, "-")

            else:
                prev = self.vector[ind]
                prevhop = self.hops[ind]
                self.vector[ind] = min(table2[ind], self.vector[ind])
                if self.vector[ind] != prev:
                    self.hops[ind] = packet["source"].id
                    if prev < self.second[ind][0]:
                        self.second[ind] = (prev, prevhop)

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

        self.neighboursPacket[packet["source"]] = (
            time_now + self.expiry,
            packet["vector"],
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

            pkt = make_packet(self, packet["source"], self.vector, time_now)
            pkt["query"] = True

            neighbour = packet["source"]

            global max_time
            max_time = max(max_time, time_now + self.links[neighbour] + 2)

            if max_time == time_now + self.links[neighbour]:
                print("Max time updated: ", max_time)

            if (
                time_now + self.links[neighbour] in pkts.keys()
                and pkt not in pkts[time_now + self.links[neighbour]]
            ):
                pkts[time_now + self.links[neighbour]].append(pkt)
                print("Packet sent from {} to {}".format(self.id, neighbour.id))
            else:
                pkts[time_now + self.links[neighbour]] = [pkt]
                print("Packet sent from {} to {}".format(self.id, neighbour.id))

    def send_query(self, time_now):
        self.active = True
        self.queryPackets = set()
        for neighbour in self.links.keys():
            packet = make_packet(self, neighbour, self.vector, time_now)
            packet["query"] = True
            if time_now + self.links[neighbour] in qry.keys():
                qry[time_now + self.links[neighbour]].append(packet)
            else:
                qry[time_now + self.links[neighbour]] = [packet]
            print("Query sent from {} to {}".format(self.id, neighbour.id))

    def remove_link(self, router, time_now):
        print("Link removed from {} to {}".format(self.id, router.id))
        self.vector[router.id] = 49
        self.hops[router.id] = "-"
        self.links.pop(router)

        for i in range(len(self.vector)):
            if self.hops[i] == router.id:
                self.vector[i] = 49
                self.hops[i] = "-"

        self.send_packet(time_now)

    def print_details(self):
        print("Node: {}".format(self.id))
        for i in range(Router.routers):
            print(self.id, "->", i, ":", self.vector[i], "via", self.hops[i])
            print("Secondhop", self.id, "->", i, ":", self.second[i])


def link_nodes(node1, node2, cost):
    node1.add_link(node2, cost)
    node2.add_link(node1, cost)


def remove_link(node1, node2, time_now):
    node1.remove_link(node2, time_now)
    node2.remove_link(node1, time_now)


def main():

    # Initialise routers
    for _ in range(6):
        [node.new_route() for node in nodes]
        nodes.append(Router())

    # Add links
    link_nodes(nodes[0], nodes[3], 10)
    link_nodes(nodes[0], nodes[4], 12)
    link_nodes(nodes[0], nodes[1], 5)
    link_nodes(nodes[1], nodes[2], 3)
    link_nodes(nodes[2], nodes[5], 6)
    link_nodes(nodes[2], nodes[4], 4)
    link_nodes(nodes[2], nodes[3], 7)

    t_start = time.time()

    def receive_packet(packet, time_now):
        dest = packet["dest"]
        dest.recv_packet(packet, time_now)

    def sendpkt_initial(time_now):
        for node in nodes:
            for neighbour in node.links.keys():
                packet = make_packet(node, neighbour, node.vector, time_now)
                if time_now + node.links[neighbour] in pkts.keys():
                    pkts[time_now + node.links[neighbour]].append(packet)
                else:
                    pkts[time_now + node.links[neighbour]] = [packet]

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

            if t_start + max_time < time.time():
                print(
                    "At time {} all packets are sent and stabity established".format(
                        time_now
                    )
                )
                break

    for node in nodes:
        node.print_details()


if __name__ == "__main__":
    main()
