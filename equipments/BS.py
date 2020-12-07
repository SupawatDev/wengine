
class BS:
    # TODO[]: Basic BS parameters
    def __init__(self, position, rotation, frequency, beam=0):
        self.position = position
        self.rotation = rotation
        self.frequency = frequency
        self.beam = beam

    def get_gain(self, nearest_position):
        # TODO: calculate gain
        None