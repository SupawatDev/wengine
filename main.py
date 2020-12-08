# TODO[]: main environment
import os
import random
from equipments import UE, BS
from utils import Com, Display
from scipy.stats import norm

class Env:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.BSs = {}
        self.UEs = {}
        self.beams = {}
        self.display = None
        # Note: Simulation Parameters
        self.week_traffic = [[6000, 200], [5000, 400], [4500, 300], [3500,200], [4000, 300], [7000, 150], [6500, 300] ]
        self.day_of_week = 0
        self.current_time = 0
        self.day_traffic = None

    def connect(self):
        # TODO[] : Connect socket to engine.
        return None

    def step(self):
        # Check if new UEs enters
        self.time += 1
        # Check incoming UEs

        # Updating existing UEs
        # TODO[]: Update the user groups
        for UE_group in self.UEs:
            # TODO[]: Update group
            None
            # TODO[]: Calculate rewards
        # TODO[]: Summarize rewards

    def display(self, scene_path):
        # TODO[]: Display the plots
        self.display = Display(scene_path)

    def generate_BS(self, position, rotation, frequency, beam_id):
        # TODO[x]: Create BS
        station = BS(position, rotation, frequency, beam_id)
        self.BSs[id(station)] = station

    def generate_ues(self, start_points):
        ue = UE(position=random.choice(start_points))
        self.UEs[id(ue)] = ue

    def generate_ues_traffic(self):
        mean_day = self.week_traffic[self.day_of_week][0]
        std_day = self.week_traffic[self.day_of_week][1]
        self.day_traffic = norm(loc=mean_day, scale=std_day).rvs(1)

    def set_datetime(self, time, day_of_week):
        self.time = time
        self.day_of_week = day_of_week

