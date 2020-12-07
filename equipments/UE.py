from collections import OrderedDict

class UE:
    def __init__(self, env, position):
        self.env = env;
        self.position = position
        # TODO[]: Struct the result
        self.connected_result = {}
        self.result = {'P_rx': None, 'BS': None, 'SNR': None}
        self.paths = []# TODO[]: Link to line drawing in K3D

    def update(self):
        # TODO[]: Pick up the best signal
        results = OrderedDict()
        for BS in self.env.BSs:
            total_power = self.calculate_power(BS)
            results[total_power] = BS.get_id();
        self.result = {'P_rx': results}

    def calculate_power(self, BS):
        # TODO[]: Calculate the result
        #   TODO[]: Trace path
        paths = self.env.com.get_paths(self, self.position, BS.position)
        #
        return total_power


    def get_connected_BS(self):
        return None