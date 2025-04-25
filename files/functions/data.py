import os

def default_values():
    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
    with open (os.path.join(data_path, "default_data.dat"), "r") as file:
        default_data = file.readlines()
        file.close()
    return default_data

default_data = default_values()

tank_x = float(default_data[0])
tank_y = float(default_data[1])
tank_angle = float(default_data[2])
tank_speed = float(default_data[3])
tank_rotation_speed = float(default_data[4])

fps = float(default_data[5])
running = bool(default_data[6])