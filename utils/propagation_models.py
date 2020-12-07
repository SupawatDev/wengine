
# TODO[]: Direct path loss calculation
def direct_path(rx_position, BS):
    receive_power = None
    gain = calculate_gain(rx_position, BS)
    return receive_power

# TODO[]: Reflection loss calculation
def reflection_path(rx_position, BS, reflection_point):
    reflection_power = None
    gain = calculate_gain(reflection_point, BS)
    # TODO[]: Reflection coefficient calculation
    return reflection_power

# TODO[]: Diffraction loss calculation
def diffracted_path(rx_position, BS, diffracted_points):
    diff_power = None
    nearest_tx_pos = get_nearest_position_to(BS.position, diffracted_points)
    gain = calculate_gain(nearest_tx_pos, BS)
    return diff_power

# TODO[] Get nearest point
def get_nearest_position_to(position, points):
    nearest = None
    for point in points:
        None
    return nearest

# TODO[]: Calculate the gain
def calculate_gain(near_tx_pos, BS):
    return None

# TODO[]: Calculate total power
def calculate_total_power(ue_position, BS, records):
    total_power = 0
    for record in records:
        if record.type == 'direct':
            total_power += direct_path(ue_position, BS)
        if record.type == 'reflect':
            total_power += reflection_path(ue_position, BS, record)
        if record.type == 'diffract':
            total_power += diffracted_path(ue_position, BS, record)
    return total_power
