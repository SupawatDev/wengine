from collections import OrderedDict
from utils import calculate_total_power, Distance, Direction
import copy
import random
import numpy as np


class UE:
    def __init__(self, env):
        self.env = env;
        position = random.choice(self.env.end_points)
        self.position = [position[0], random.random()*0.5+1.3, position[1]]
        self.direction = []
        self.step_rate = random.random() * 0.5 + 0.9
        self.visit_points = self.generate_visits()
        # TODO[]: Struct the result
        self.connected_result = {}
        self.result = {'P_rx': None, 'BS': None, 'paths': None, 'SNR': None}
        self.paths = []  # TODO[]: Link to line drawing in K3D

    def random_direct(self, position):
        while True:
            # TODO: change range
            random_pos = self.random_outdoor([-150, 1.5, -150], [150, 2, 150])
            if self.env.com.is_direct(position, random_pos) is True:
                return random_pos

    # TODO[x]: Step the UE
    def step(self):
        dest = self.visit_points[0]
        if Distance(dest, self.position) < 3:
            if len(self.visit_points) == 1:
                return False
            else:
                # pop front out, update est
                self.visit_points = self.visit_points[1:]
                dest = self.visit_points[0]
                self.direction = Direction(self.position, dest)

        self.position = np.array(self.position) + self.direction * self.step_rate
        self.update()

    def update(self):
        # TODO[]: Pick up the best signal
        results = OrderedDict()
        noise_power = 0
        for BS in self.env.BSs:
            paths = self.env.com.get_paths(self, self.position, BS.position)
            rev_power = calculate_total_power(self.position, BS, paths)
            noise_power += rev_power
            results[rev_power] = {'P_rx': rev_power, 'BS': BS, 'paths': paths, 'SNR': None};
        # TODO[]: Pick the highest power
        self.result = next(reversed(results))
        # TODO[]: get total_noise
        noise_power -= self.result['P_rx']

    def generate_visits(self):
        visit_n = random.randint(3, 7)
        visit_points = []
        current_pos = self.position
        # Find where to visit
        for i in range(visit_n):
            j = 0
            while True:
                if j < len(self.env.visit_points):
                    # check if visit point is direct
                    j += 1
                    check_pos = self.env.visit_points[j]
                    check_pos = [check_pos[0], 1.5, check_pos[1]]
                    if self.env.com.is_direct(current_pos, check_pos):
                        visit_points.append(check_pos)
                        current_pos = check_pos
                        break
                else:
                    # Get random outdoor position
                    pos = self.random_direct(current_pos)
                    visit_points.append(pos)
                    current_pos = pos
                    break
            # Find exit
        current_pos = visit_points[-1]
        expect_end = random.choice(self.env.end_points)
        expect_end = [expect_end[0], 1.5, expect_end[1]]
        j = 0
        while True:
            if j > len(self.env.visit_points) * 2:
                # go back where comes from
                copy_visits = reversed(copy.deepcopy(visit_points)[:-1])
                visit_points += copy_visits
                break
            elif j < len(self.env.visit_points):
                check_pos = self.env.visit_points[j]
                check_pos = [check_pos[0], 1.5, check_pos[1]]
                if self.env.com.is_direct(current_pos, check_pos) and self.env.com.is_direct(check_pos, expect_end):
                    visit_points.append(check_pos)
                    visit_points.append(expect_end)
                    break
            else:
                # Get random outdoor position
                ps = self.random_direct(current_pos)
                visit_points.append(pos)
                current_pos = pos
            j += 1
        self.direction = Direction(self.position, visit_points[0])
        return visit_points
