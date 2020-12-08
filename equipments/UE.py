from collections import OrderedDict
from utils.propagation_models import calculate_total_power
class UE:
    def __init__(self, env, position):
        self.env = env;
        self.position = position
        # TODO[]: Struct the result
        self.connected_result = {}
        self.result = {'P_rx': None, 'BS': None,'paths': None,'SNR': None}
        self.paths = []# TODO[]: Link to line drawing in K3D

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
