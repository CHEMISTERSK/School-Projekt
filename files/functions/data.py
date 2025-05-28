import os, pygame
from functions.error_handling import error_window

try:
    def set_default_values():
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        with open (os.path.join(data_path, "default_data.dat"), "r") as file:
            default_data = file.readlines()
            file.close()
        return default_data

    def set_tank_location_default(default_data):
        tank_x = float(default_data[0])
        tank_y = float(default_data[1])
        return tank_x, tank_y
    
    def set_tank_angle_default(default_data):
        tank_angle = float(default_data[2])
        return tank_angle
    
    def set_tank_speed_default(default_data):
        tank_speed = float(default_data[3])
        return tank_speed

    def set_tank_rotation_speed_default(default_data):
        tank_rotation_speed = float(default_data[4])
        return tank_rotation_speed
    
    def set_fov_default(default_data):
        fov = float(default_data[6])
        return fov

    default_data = set_default_values()

    tank_x = float(default_data[0])
    tank_y = float(default_data[1])
    tank_angle = float(default_data[2])
    tank_speed = float(default_data[3])
    tank_rotation_speed = float(default_data[4])

    fps = float(default_data[5])
    fov = float(default_data[6])
    running = bool(default_data[7])
    fullscreen = bool(default_data[8])
    db = bool(default_data[9])
    copy = bool(default_data[10])


    # Loading Textures and Sounds

    def load_textures():
        texture_loading_path = []
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        with open(os.path.join(data_path, "avdata.dat"), "r") as file:
            texture_data = file.readlines()
        texture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'textures')
        for line in texture_data:
            filename = line.strip()  # Remove whitespace and newlines
            if filename:  # Skip empty lines
                texture_loading_path.append(os.path.join(texture_path, filename))
        return texture_loading_path
    
    texture_loading_path = load_textures()

    test_tank = pygame.transform.scale_by(pygame.image.load(texture_loading_path[1]), fov)
    surface = pygame.transform.scale_by(pygame.image.load(texture_loading_path[2]), (fov / 2))

except Exception as e:
    source = "Data.py"
    error_window(f"Error during file loading: {e}", source)