import os, pygame, json
from functions.error_handling import error_window

try:
    pygame.mixer.init()

    def set_default_values():
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        with open(os.path.join(data_path, "default_data.json"), "r", encoding="utf-8") as file:
            default_data = json.load(file)
            file.close()
        return default_data

    def set_tank_location_default(default_data):
        tank_x = float(default_data["tank_x"])
        tank_y = float(default_data["tank_y"])
        return tank_x, tank_y
    
    def set_tank_angle_default(default_data):
        tank_angle = float(default_data["tank_angle"])
        return tank_angle
    
    def set_tank_speed_default(default_data):
        tank_speed = float(default_data["tank_speed"])
        return tank_speed

    def set_tank_rotation_speed_default(default_data):
        tank_rotation_speed = float(default_data["tank_rotation_speed"])
        return tank_rotation_speed
    
    def set_fov_default(default_data):
        fov = float(default_data["fov"])
        return fov    # Numerical and Logical values loading
    default_data = set_default_values()

    tank_x =              float(default_data["tank_x"])
    tank_y =              float(default_data["tank_y"])
    tank_angle =          float(default_data["tank_angle"])
    turret_angle =        0.0  # Uhol veže (bude sa nastavovať podľa myši)
    tank_speed =          float(default_data["tank_speed"])
    tank_rotation_speed = float(default_data["tank_rotation_speed"])
    tank_hp =             float(default_data["tank_hp"])
    max_tank_hp =         float(default_data["max_tank_hp"])

    fps =        float(default_data["fps"])
    fov =        float(default_data["fov"])
    running =    default_data["running"]
    fullscreen = default_data["fullscreen"]
    db =         default_data["db"]
    copy =       default_data["copy"]

    # Shells Data   (gs - green shell;  os - orange shell;  rs - red shell)
    gs_dmg = float(default_data["gs_dmg"])    # damage
    gs_pen = float(default_data["gs_pen"])    # penetration
    gs_spd = float(default_data["gs_spd"])    # speed

    os_dmg = float(default_data["os_dmg"])
    os_pen = float(default_data["os_pen"])
    os_spd = float(default_data["os_spd"])

    rs_dmg = float(default_data["rs_dmg"])
    rs_pen = float(default_data["rs_pen"])
    rs_spd = float(default_data["rs_spd"])

    wave =  int(default_data["wave"])
    score = int(default_data["score"])

    playing = default_data["playing"]

    # Time Data
    time_data = []

    # Enemies Data
    enemies = []

    # Settings loading
    def settings_loading():
        settings_data = {}
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        while True:
            try:
                with open(os.path.join(data_path, "settings.json"), "r", encoding = "utf-8") as file:
                    settings_data = json.load(file)
                    file.close()
                return settings_data
            except FileNotFoundError:
                settings_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
                with open(os.path.join(settings_dir, 'settings.json'), 'w') as settings_file:
                    default_settings = {
                        "player_name": "",
                        "password": "",
                        "fov": 0.75,
                        "volume": 0.5,
                        "default_fullscreen": False,
                        "server_ip_address": "localhost",
                        "server_port": 5432,
                    }
                    json.dump(default_settings, settings_file, indent=4)
                    settings_file.close()
    
    settings = settings_loading()


    # Loading Textures and Sounds
    def load_audiovisual():
        data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        with open(os.path.join(data_path, "avdata.json"), "r", encoding="utf-8") as file:
            av_data = json.load(file)

        textures = av_data.get("textures", [])
        sounds = av_data.get("sounds", [])

        texture_loading_path = []
        sound_loading_path = []

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
    
    texture_loading_path, sound_loading_path = load_audiovisual()    # Textures
    test_tank = pygame.transform.scale_by(pygame.image.load(texture_loading_path[0]), fov)
    main_tank = pygame.transform.scale_by(pygame.image.load(texture_loading_path[0]), fov)
    hull = pygame.transform.scale_by(pygame.image.load(texture_loading_path[7]), fov)
    turret = pygame.transform.scale_by(pygame.image.load(texture_loading_path[8]), fov)
    surface =   pygame.transform.scale_by(pygame.image.load(texture_loading_path[1]), (fov / 2))

    orange_shell =  pygame.transform.scale_by(pygame.image.load(texture_loading_path[2]), (fov / 25))
    red_shell =     pygame.transform.scale_by(pygame.image.load(texture_loading_path[3]), (fov / 25))
    green_shell =   pygame.transform.scale_by(pygame.image.load(texture_loading_path[4]), (fov / 25))

    shells = pygame.transform.scale_by(pygame.image.load(texture_loading_path[5]), (fov / 5))

    game_menu = pygame.transform.scale_by(pygame.image.load(texture_loading_path[6]), (fov / 1.125))

    #Sounds
    shot_sound =    pygame.mixer.Sound(sound_loading_path[0])
    reload_sound =  pygame.mixer.Sound(sound_loading_path[1])
    active_engine = pygame.mixer.Sound(sound_loading_path[2])
    calm_engine =   pygame.mixer.Sound(sound_loading_path[3])
    menu_ambient =  pygame.mixer.Sound(sound_loading_path[4])
    
    # Volume setting
    calm_engine.set_volume(settings["volume"])    
    active_engine.set_volume(settings["volume"] / 2)
    shot_sound.set_volume(settings["volume"])

except Exception as e:
    source = "Data.py"
    error_window(f"Error during file loading: {e}", source)