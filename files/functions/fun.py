from functions import data
import pygame

game_ms = 0  
last_tick = None

def ingame_time():
    global game_ms, last_tick
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