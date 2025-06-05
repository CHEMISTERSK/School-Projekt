from functions import data
import pygame

game_ms = 0  
last_tick = None
now = None
delta = 0
minutes = 0
seconds = 0
seconds_total = 0

def ingame_time(exp):
    global game_ms, last_tick, delta, now, minutes, seconds, seconds_total
    if data.playing:
        now = pygame.time.get_ticks()
        if last_tick is not None:
            delta = now - last_tick  
            game_ms += delta
        last_tick = now
    else:
        last_tick = None
    
    seconds_total = game_ms // 1000
    minutes = seconds_total // 60
    seconds = seconds_total % 60

    if exp == True:
        return [game_ms, None, now, delta, seconds_total, minutes, seconds]
    else:
        return f"{minutes:02d}:{seconds:02d}"

def reset_game_time():
    global game_ms, last_tick
    game_ms = 0
    last_tick = None

def fullscreen_toggle(full_res_x, full_res_y):
    if not data.fullscreen:
        data.fullscreen = True
        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
        pygame.display.set_mode((res_xy[0], res_xy[1]), pygame.FULLSCREEN)

    elif data.fullscreen:
        data.fullscreen = False
        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
        pygame.display.set_mode((res_xy[0], res_xy[1]))
    
def screen_resolution(full_res_x, full_res_y, fullscreen):
    window_res_x = full_res_x
    window_res_y = full_res_y * 0.93 #%

    if fullscreen == True:
        res_x = full_res_x * 1.25 #%
        res_y = full_res_y * 1.25 #%

    elif fullscreen == False:
        res_x = window_res_x
        res_y = window_res_y

    return(res_x, res_y)

def av_reload():
    data.texture_loading_path, data.sound_loading_path = data.load_audiovisual()

    data.test_tank      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))
    data.surface        =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[1]), (data.fov / 2))
    data.orange_shell   =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[2]), (data.fov / 25))
    data.red_shell      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[3]), (data.fov / 25))
    data.green_shell    =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[4]), (data.fov / 25))
    data.shells         =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[5]), (data.fov / 12.5))

    data.shot_sound =    pygame.mixer.Sound(data.sound_loading_path[0])
    data.realod_sound =  pygame.mixer.Sound(data.sound_loading_path[1])
    data.active_engine = pygame.mixer.Sound(data.sound_loading_path[2])
    data.calm_engine =   pygame.mixer.Sound(data.sound_loading_path[3])

    data.calm_engine.set_volume(0.5)    # %
    data.active_engine.set_volume(0.2)  # %

def data_reload():
    data.default_data = data.set_default_values()

    data.tank_x =              float(data.default_data[0])
    data.tank_y =              float(data.default_data[1])
    data.tank_angle =          float(data.default_data[2])
    data.tank_speed =          float(data.default_data[3])
    data.tank_rotation_speed = float(data.default_data[4])
    data.tank_hp =             float(data.default_data[11])
    data.max_tank_hp =         float(data.default_data[11])

    # Shells Data   (gs - green shell;  os - orange shell;  rs - red shell)
    data.gs_dmg = float(data.default_data[12])    # damage
    data.gs_pen = float(data.default_data[13])    # penetration
    data.gs_spd = float(data.default_data[14])    # speed

    data.os_dmg = float(data.default_data[15])
    data.os_pen = float(data.default_data[16])
    data.os_spd = float(data.default_data[17])

    data.rs_dmg = float(data.default_data[18])
    data.rs_pen = float(data.default_data[19])
    data.rs_spd = float(data.default_data[20])

    data.wave =  int(data.default_data[21])
    data.score = int(data.default_data[22])