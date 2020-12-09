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

    def ask(self, question, input1=None, input2=None):
        question = int(question)
        message = 'q{0}'.format(question)
        if input1 is not None:
            message += ':{0},{1},{2}'.format(input1[0], input1[1], input1[2])

        if input2 is not None:
            message += ':{0},{1},{2}:{3},{4},{5}'.format(input1[0],input1[1],input1[2],
                                                  input2[0],input2[1],input2[2])
        self.env_sock.send(message.encode())
        # Get the answer
        answer = self.env_sock.recv(1024).decode()
        # Confirms that the server sent the answer
        assert answer[0] == 'a'
        answer = answer[2:]
        return answer
