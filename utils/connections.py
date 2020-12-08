import pandas as pd
import socket

class Com:
    def __init__(self, env_sock):
        self.env_sock = env_sock

    # TODO[]: Get Paths
    def get_path(self, rx_position, tx_positon):
        self.env_sock.send()