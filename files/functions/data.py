import os, pygame
from functions.error_handling import error_window

try:
    pygame.mixer.init()

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

    # Numerical and Logical values loading
    default_data = set_default_values()

    tank_x =              float(default_data[0])
    tank_y =              float(default_data[1])
    tank_angle =          float(default_data[2])
    tank_speed =          float(default_data[3])
    tank_rotation_speed = float(default_data[4])
    tank_hp =             float(default_data[11])

    fps =        float(default_data[5])
    fov =        float(default_data[6])
    running =    bool(default_data[7])
    fullscreen = bool(default_data[8])
    db =         bool(default_data[9])
    copy =       bool(default_data[10])

    gs_dmg = float(default_data[12])
    gs_pen = float(default_data[13])
    gs_spd = float(default_data[14])
    os_dmg = float(default_data[15])
    os_pen = float(default_data[16])
    os_spd = float(default_data[17])
    rs_dmg = float(default_data[18])
    rs_pen = float(default_data[19])
    rs_spd = float(default_data[20])


    # Loading Textures and Sounds

    def load_audiovisual():
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        with open(os.path.join(data_path, "avdata.dat"), "r") as file:
            av_data = file.read()

        texture_loading_path = []
        sound_loading_path = []
        namespace = {}
        exec(av_data, {}, namespace)

        textures = namespace.get("textures", [])
        sounds = namespace.get("sounds", [])

        texture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'textures')
        sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sounds')

        for texture in textures:
            filename = texture.strip()  
            if filename:  
                texture_loading_path.append(os.path.join(texture_path, filename))

        for sound in sounds:
            filename = sound.strip()  
            if filename:  
                sound_loading_path.append(os.path.join(sound_path, filename))
        return texture_loading_path, sound_loading_path
    
    texture_loading_path, sound_loading_path = load_audiovisual()


    # Textures
    test_tank = pygame.transform.scale_by(pygame.image.load(texture_loading_path[0]), fov)
    surface =   pygame.transform.scale_by(pygame.image.load(texture_loading_path[1]), (fov / 2))

    orange_shell =  pygame.transform.scale_by(pygame.image.load(texture_loading_path[2]), (fov / 25))
    red_shell =     pygame.transform.scale_by(pygame.image.load(texture_loading_path[3]), (fov / 25))
    green_shell =   pygame.transform.scale_by(pygame.image.load(texture_loading_path[4]), (fov / 25))

    shells = pygame.transform.scale_by(pygame.image.load(texture_loading_path[5]), (fov / 5))

    #Sounds
    shot_sound =    pygame.mixer.Sound(sound_loading_path[0])
    realod_sound =  pygame.mixer.Sound(sound_loading_path[1])
    active_engine = pygame.mixer.Sound(sound_loading_path[2])
    calm_engine =   pygame.mixer.Sound(sound_loading_path[3])
    
    # Volume setting
    calm_engine.set_volume(0.4)    # %
    active_engine.set_volume(0.2)  # %

except Exception as e:
    source = "Data.py"
    error_window(f"Error during file loading: {e}", source)