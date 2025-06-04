import pygame, os
from pygame.locals import *
from functions import data

def menu_buttons(full_res_x, full_res_y, screen):
    screen.blit(data.game_menu, (full_res_x * 0.0586, 0))

def play_button(mouse_x, mouse_y, full_res_x, full_res_y):
    if mouse_x in range(int(full_res_x * 0.5664), int(full_res_x * 0.7878)) and mouse_y in range(int(full_res_y * 0.1993), int(full_res_y * 0.3487)):
        if pygame.mouse.get_pressed()[0]:
            data.playing = True
    
def exit_button(mouse_x, mouse_y, full_res_x, full_res_y):
    if mouse_x in range(int(full_res_x * 0.5664), int(full_res_x * 0.7878)) and mouse_y in range(int(full_res_y * 0.8275), int(full_res_y * 0.9722)):
        if pygame.mouse.get_pressed()[0]:
            log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),'..', 'logs')
            os.remove(os.path.join(log_dir, "temp.log"))
            data.running = False