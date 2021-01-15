# TODO[]: main environment
import os, random, socket
from time import sleep
import random
from equipments import UE, BS
from utils import Com, Display
from scipy.stats import norm
import numpy as np


class Env:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.BSs = []
        self.UEs = []
        self.beams = {}
        self.display = None
        # Note: Simulation Parameters
        self.week_traffic = []
        self.day_of_week = 0
        self.current_time = 0
        self.days_traffic = []
        # TODO[x]: points for poznan map
        self.end_points = [[55.0, 0.5], [64.5, 32.2], [-3, -41.9], [-48.04, -13.38], [15.17, 62.914]]
        self.visit_points = [[11.75, 35.84], [37.92, 32.13], [27.81, -21.57], [0.89, -16.5], [-14.5, -2.5]]
        self.on_display = False
        # TODO[] Connect to server
        self.env_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while not self.connect():
            print("Trying to connect " + str(server_ip) + ":" + str(server_port))
            sleep(3)
        self.com = Com(self.env_sock)

    def connect(self):
        # TODO[] : Connect socket to engine.
        try:
            self.env_sock.connect((self.server_ip, self.server_port))
            self.env_sock.send("Client: Hello Server".encode())
            print(self.env_sock.recv(1024).decode())
            return True
        except:
            return False

    def step(self):
        # Check if new UEs enters
        self.current_time += 1
        # Check incoming UEs

        # Updating existing UEs
        # TODO[]: Update the user groups
        for user in self.UEs:
            # TODO[]: Update group
            user.step()
            print(str(id(user)) + " : " + str(user.position))
            # TODO[]: Calculate rewards
        # TODO[]: Summarize rewards
        reward = None
        return reward

    def open(self, scene_path):
        # TODO[x]: Display the plots
        self.display = Display(scene_path)
        self.on_display = True

    def visualise(self, ues = None, bss = None):
        self.display.run(ues, bss)


    def generate_bs(self, position, rotation, frequency, beam_id):
        # TODO[x]: Create BS
        station = BS(position, rotation, frequency, beam_id)
        self.BSs[id(station)] = station

    def generate_ues(self):
        ue = UE(self)
        self.UEs.append(ue)
        if self.on_display:
            self.display.add_ue(ue)


    def generate_traffic(self):
        week_traffic_param = [[6000, 200], [5000, 400], [4500, 300],
                              [3500, 200], [4000, 300], [7000, 150], [6500, 300]]
        self.week_traffic = []
        for day in range(len(week_traffic_param)):
            mean_day = week_traffic_param[day][0]
            std_day = week_traffic_param[day][1]
            total_ue = np.array(list(map(int, norm(loc=mean_day, scale=std_day).rvs(1))))
            self.week_traffic.append(total_ue)  # TODO[]: change to dynamic daily traffic
            day_traffic = np.array(list(map(int, norm(loc=43200, scale=19000).rvs(total_ue))))
            day_traffic = day_traffic[day_traffic <= 86400]  # Crop exceeded seconds
            day_traffic = day_traffic[day_traffic >= 0]
            self.days_traffic.append(day_traffic)

    # TODO[]: Generate incoming UEs
    def generate_incoming_ue(self):
        today_traffic = self.days_traffic[self.day_of_week]
        today_traffic = today_traffic[today_traffic >= self.current_time]
        while len(today_traffic) > 0 and self.current_time == today_traffic[0]:
            self.generate_ues()
            today_traffic = today_traffic[1:]

    def set_datetime(self, current_time, day_of_week):
        self.current_time = current_time
        self.day_of_week = day_of_week

    def disconnect(self):
        self.env_sock.send("e".encode())
        res = self.env_sock.recv(1024).decode()
        assert res[0:3] == "eok"
        self.env_sock.close()

    def reset(self):
        self.com.reset()
