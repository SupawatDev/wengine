# TODO[]: main environment
import os
import random
from equipments import UE, BS
from utils import Com, Display
from scipy.stats import norm
import numpy as np


class Env:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.BSs = {}
        self.UEs = {}
        self.beams = {}
        self.display = None
        # Note: Simulation Parameters
        self.week_traffic = []
        self.day_of_week = 0
        self.current_time = 0
        self.days_traffic = []
        # TODO[] points for poznan map
        self.end_points = [[55.0, 0.5], [64.5, 32.2], [-3, -41.9], [-48.04, -13.38], [15.17, 62.914]]
        self.visit_points = [[11.75, 35.84], [37.92, 32.13], [27.81, -21.57], [0.89, -16.5], [-14.5, -2.5]]
        self.on_display = False
        # TODO[] Socket
        self.com = Com()

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
        reward = None
        return reward

    def display(self, scene_path):
        # TODO[x]: Display the plots
        self.display = Display(scene_path)
        self.display.show()
        self.on_display = True

    def generate_bs(self, position, rotation, frequency, beam_id):
        # TODO[x]: Create BS
        station = BS(position, rotation, frequency, beam_id)
        self.BSs[id(station)] = station

    def generate_ues(self):
        ue = UE(self, position=random.choice(self.start_points))
        self.UEs[id(ue)] = ue

    def generate_traffic(self):
        week_traffic_param = [[6000, 200], [5000, 400], [4500, 300], [3500, 200], [4000, 300], [7000, 150], [6500, 300]]
        self.week_traffic = []
        for day in range(len(week_traffic_param)):
            mean_day = self.week_traffic[day][0]
            std_day = self.week_traffic[day][1]
            total_ue = np.array(list(map(int, norm(loc=mean_day, scale=std_day).rvs(1))))
            self.week_traffic.append(total_ue)  # TODO[]: change to dynamic daily traffic
            day_traffic = np.array(list(map(int, norm(loc=43200, scale=19000).rvs(total_ue))))
            self.days_traffic.append(day_traffic)

    # TODO[]: Generate incoming UEs
    def generate_incoming_ue(self):
        today_traffic = self.days_traffic[self.day_of_week]
        today_traffic = today_traffic[today_traffic >= self.current_time]
        while self.current_time == today_traffic[0]:
            self.generate_ues()
            today_traffic = today_traffic[1:]

    def set_datetime(self, current_time, day_of_week):
        self.current_time = current_time
        self.day_of_week = day_of_week
