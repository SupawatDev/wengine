# TODO[]: main environment
import k3d
from equipments import UE, BS
from utils import Com

class Env:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_ip = server_ip
        self.BSs = {}
        self.UE_groups = {}
        self.beams = {}
        self.plot = k3d.plot()

    def connect(self):
        # TODO[] : Connect socket to engine.
        return None

    def step(self):
        # TODO[]: Update the user groups
        for UE_group in self.UE_groups:
            # TODO[]: Update group
            None

    def display(self):
        # TODO[]: Display the plots
        self.display()

    def generate_BS(self, position, rotation, frequency, beam_id):
        # TODO[]: Create BS
        station = BS(position, rotation, frequency, beam_id)
        self.BSs[id(station)] = station


def main():
    plot = k3d.plot(camera_auto_fit=True)
    plot.display()