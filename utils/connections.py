import pandas as pd
import socket

class Com:
    def __init__(self, env_sock):
        self.env_sock = env_sock

    # TODO[x][]: Get Paths
    def get_path(self, rx_position, tx_position):
        answers = self.ask(9, input1=rx_position, input2=tx_position)
        answers = answers.split(':')
        records = {'dir': False, 'dif': [], 'ref': []}
        for ans in answers:
            type = ans[:3]
            ans = ans[3:]
            if type == 'dir':
                records['dir'] = True
            elif type == 'ref':
                pos = list(map(float, ans.split(',')))
                records['ref'].append(pos)
            elif type == 'dif':
                pos = list(map(float, ans.split(',')))
                records['diff'].append(pos)
        return records

    # TODO[x][]: Get direct
    def is_direct(self, pos1, pos2):
        if self.ask(7, input1=pos1, input2=pos2)[0] == 't':
            return True
        return False

    # TODO[x][]: Get Outdoor
    def is_outdoor(self, pos):
        if self.ask(6, input1=pos)[0] == 't':
            return True
        return False

    def ask(self, question, input0=None, input1=None, input2=None):
        question = int(question)
        message = 'q{0}'.format(question)
        if input0 is not None:
            message += str(input0)
        if input1 is not None:
            message += ':{0},{1},{2}'.format(input1[0], input1[1], input1[2])

        if input2 is not None:
            message += ':{0},{1},{2}:{3},{4},{5}'.format(input1[0],input1[1],input1[2],
                                                  input2[0],input2[1],input2[2])
        self.env_sock.send(message.encode())
        # Get the answer
        answer = self.env_sock.recv(1024).decode()
        # Confirms that the server sent the answer
        # print(answer)
        assert answer[0] == 'a'
        answer = answer[2:]
        return answer

    def ask_station_info(self, station_number):
        # answer form:
        # (id):(position):(rotation):(frequency):(N of user)&(list of user):(avg loss)
        answer = self.ask(3, input0=station_number)
        answer = answer.split(':')
        if int(answer[0]) == -1:
            return {}  # return an empty struct
        # Structure of a station
        station = {'id': int(answer[0]),
                   'position': list(map(float, answer[1].split(','))),
                   'rotation': list(map(float, answer[2].split(','))),
                   'frequency': float(answer[3]),
                   'transmit_power': float(answer[4]),
                   'users': []}
        user_info = answer[5].split('&')
        if int(user_info[0]) > 0:
            station['users'] = list(map(int, user_info[1].split(',')))
        return station

    def ask_user_info(self, user_id):
        # answer form:
        # (id):(position):(station):(path loss)
        answer = self.ask(4, input0=user_id)
        answer = answer.split(':')
        if int(answer[0]) == -1:
            return {}
        # Structure of a user
        # id: position:
        user = {'id': int(answer[0]),
                'position': list(map(float, answer[1].split(','))),
                'rotation': list(map(float, answer[2].split(','))),
                'station': None,
                'result': {
                    'received_power': None,
                    'total_attenuation': None,
                    'transmit_power': None,
                    'los': None,
                    'direct': {
                        'loss': None,
                        'tx_gain': None,
                        'rx_gain': None,
                        'delay': None},
                    'diffraction': {
                        'loss': None,
                        'tx_gain': None,
                        'rx_gain': None},
                    'reflections': []
                }
                }

        if len(answer) > 3:
            user['station'] = int(answer[3])
        if len(answer) > 4:
            user['result']['received_power'] = float(answer[4])
            user['result']['transmit_power'] = float(answer[5])
            user['result']['total_attenuation'] = float(answer[6])
            is_los = answer[7][0] == 't'
            user['result']['los'] = is_los
            line_data = answer[7].split(',')[1:]
            if is_los:
                user['result']['direct']['loss'] = float(line_data[0])
                user['result']['direct']['tx_gain'] = float(line_data[1])
                user['result']['direct']['rx_gain'] = float(line_data[2])
                user['result']['direct']['delay'] = float(line_data[3])
            else:
                user['result']['diffraction']['loss'] = float(line_data[0])
                user['result']['diffraction']['tx_gain'] = float(line_data[1])
                user['result']['diffraction']['rx_gain'] = float(line_data[2])
                user['result']['diffraction']['delay'] = float(line_data[3])
            # Store reflection result
            ref_n = int(answer[8].split('&')[0])
            if ref_n > 0:
                ref_list = answer[8].split('&')[1:]
                for ref in ref_list:
                    ref_data = ref.split(',')
                    ref_obj = {'loss': float(ref_data[0]),
                               'tx_gain': float(ref_data[1]),
                               'rx_gain': float(ref_data[2]),
                               'delay': float(ref_data[3])}
                    user['result']['reflections'].append(ref_obj)

        return user

    def ask_stations_info(self):  # return list of station IDs.
        answer = self.ask(1)
        # answer form: "(number of stations)&(list of station IDs)"
        answer = answer.split('&')
        station_ids = []
        if int(answer[0]) > 0:
            station_ids = list(map(int, answer[1].split(',')))
        return station_ids

    def ask_users_info(self):  # return list of user IDs.
        answer = self.ask(2)
        # answer form: "(number of users)&(list of user IDs)"
        answer = answer.split('&')
        user_ids = []
        if int(answer[0]) > 0:
            user_ids = list(map(int, answer[1].split(',')))
        return user_ids

    def add_station(self, location, rotation, frequency=2.3e9):
        return self.command(1, location, rotation, frequency)

    def add_user(self, location):
        return self.command(2, location)

    def connect_user_to_station(self, station_id, user_id):
        return self.command(3, station_id=station_id, user_id=user_id)

    def move_station_to(self, station_id, location, rotation):
        return self.command(4, station_id=station_id, location=location, rotation=rotation)

    def remove_station(self, station_id):
        return self.command(5, station_id=station_id)

    def remove_user(self, user_id):
        return self.command(6, user_id=user_id)

    def disconnect_user_from_station(self, station_id, user_id):
        return self.command(7, station_id=station_id, user_id=user_id)

    def move_user_to(self, user_id, location):
        return self.command(8, user_id=user_id, location=location)

    def command(self, command_id, location=None, rotation=None, frequency=2.3e9, station_id=None, user_id=None):
        # Commands:
        # 1: Add a station to the env
        # 2: Add a user to the env
        # 3: Connect a user to a station
        # 4: Move a station
        # 5: Remove a station
        # 6: Remove a user
        # 7: Disconnect a user to a station
        # 8: Move a user
        # Add transmitter and return the transmitter id
        # tx_id = self.env_sock.recv(1024).decode()
        if command_id == 1:
            context = 'c1:%f,%f,%f:%f,%f,%f:%f' % (location[0], location[1], location[2],
                                                   rotation[0], rotation[1], rotation[2],
                                                   frequency)
        elif command_id == 2:
            context = 'c2:%f,%f,%f' % (location[0], location[1], location[2])
        elif command_id == 3:
            context = 'c3:%d,%d' % (station_id, user_id)
        elif command_id == 4:
            context = 'c4:%d:%f,%f,%f:%f,%f,%f' % (station_id,
                                                   location[0], location[1], location[2],
                                                   rotation[0], rotation[1], rotation[2])
        elif command_id == 5:
            context = 'c5:%d' % station_id
        elif command_id == 6:
            context = 'c6:%d' % user_id
        elif command_id == 7:
            context = 'c7:%d:%d' % (station_id, user_id)
        elif command_id == 8:
            context = 'c8:%d:%f,%f,%f' % (user_id,
                                          location[0], location[1], location[2])
        else:
            assert False
        self.env_sock.send(context.encode())
        # to confirm the command was done successfully
        assert self.env_sock.recv(1024).decode()[0:3] == 'suc'

    def get_station_map(self, station_id, resolution):
        # Q5: Get the station map
        context = 'q5'+str(station_id)+','+str(resolution)
        # Send the request
        self.env_sock.send(context.encode())

        assert self.env_sock.recv(1024).decode()[:3] == 'suc'
        self.env_sock.send("ready".encode())
        data_map = []
        x_list, z_list, pl_list = [], [], []
        while True:
            rec_data = self.env_sock.recv(1024).decode()
            if rec_data[:3] == 'end':
                break
            data = rec_data.split(',')
            x, z, avg_pl = float(data[0]), float(data[1]), float(data[2])
            x_list.append(x)
            z_list.append(z)
            pl_list.append(avg_pl)
            data_map.append({'x': x, 'z': z, 'avg_pl': avg_pl})
            self.env_sock.send('ok'.encode())

        # Convert Data to Grid
        data_map = pd.DataFrame(data_map)
        pl_map = data_map.pivot('x', 'z', 'avg_pl')
        return pl_map, data_map

    def reset(self):
        self.env_sock.send("r".encode())
        res = self.env_sock.recv(1024).decode()
        assert res[0:3] == "rok"