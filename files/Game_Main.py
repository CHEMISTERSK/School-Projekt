# Importing External Functions
import pygame, sys, time as t, os, random as r, datetime, math, threading
from pygame.locals import *

# Importing Internal Functions
from functions.error_handling import error_window
from functions.logging import *
from functions.db.db import get_connection
from functions.console import console
from functions.func import *
from functions import data
from functions.save import *
from functions.db.logic.account_logic import *
from functions.db.logic.saveing_logic import *

# Importing Mechanics
from mechanics import generation as gen
from mechanics.menu import *


# Game Initialization
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("SP")

resolution = pygame.display.Info()
full_res_x = resolution.current_w
full_res_y = resolution.current_h

screen = pygame.display.set_mode((full_res_x, full_res_y * 0.93))

epoch = t.time()
last_log = int(epoch)

clock = pygame.time.Clock()

real_time = datetime.datetime.now().strftime("%H:%M:%S")

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'impact.ttf')
font = pygame.font.Font(font_path, 15)

last_fps_log = int(epoch)
fps_text = f"FPS: "
text_surface = font.render(fps_text, True, (255, 255, 255))

d_x = full_res_x * 0.5
d_y = full_res_y * 0.5

# Functions Calling
res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
main_log_clear()
connection = get_connection()
main_log(real_time, resolution, res_xy[0], res_xy[1], clock, pygame.time.get_ticks(), epoch, data.db, connection)
fullscreen_toggle(full_res_x, full_res_y)
settings_json(data.settings)

try:
    # Main Loop
    while data.running:

        # Screen Resolution
        screen.fill((0, 0, 0))

        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        epoch = t.time()
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(os.path.join(log_dir, "temp.log"))
                data.running = False

        # Key Binding
            # Back To Menu
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    data.time_data = ingame_time(True)
                    data.playing = False

                # Save Game
                elif event.key == pygame.K_F5:
                    cloud_save(data.settings["player_name"])
                    saveing()

                # Switching Between Fullscreen And Windowed Mode
                elif event.key == pygame.K_F11:
                    fullscreen_toggle(full_res_x, full_res_y)

                # Console
                elif event.key == pygame.K_F12:
                    threading.Thread(target = console, daemon = True).start()
        
        #   Menu Buttons
        if data.playing == False:
            play_button(mouse_x, mouse_y, full_res_x, full_res_y)
            continue_button(mouse_x, mouse_y, full_res_x, full_res_y)
            settings_button(mouse_x, mouse_y, full_res_x, full_res_y)
            exit_button(mouse_x, mouse_y, full_res_x, full_res_y)

        elif data.playing == True:
            gen.generation(screen)
            data.menu_ambient.stop()

            # Game Loop
            current_time = pygame.time.get_ticks()

            # Movement Logic
            if keys[pygame.K_a]:
                data.tank_angle += data.tank_rotation_speed

            elif keys[pygame.K_d]:
                data.tank_angle -= data.tank_rotation_speed

            if data.tank_angle > 360:
                data.tank_angle -= 360

            if data.tank_angle < 0:
                data.tank_angle += 360

            angle_radians = math.radians(data.tank_angle)

            if keys[pygame.K_w]:
                data.tank_x -= (data.tank_speed * math.sin(angle_radians)) * data.fov
                data.tank_y -= (data.tank_speed * math.cos(angle_radians)) * data.fov

            elif keys[pygame.K_s]:
                data.tank_x += (data.tank_speed * math.sin(angle_radians)) * data.fov
                data.tank_y += (data.tank_speed * math.cos(angle_radians)) * data.fov

            # Engine Sounds
            if (keys[pygame.K_s] or keys[pygame.K_w]) or (keys[pygame.K_a] or keys[pygame.K_d]):
                if data.active_engine.get_num_channels() == 0:
                    data.active_engine.play()
                data.calm_engine.stop()

            else:
                if data.calm_engine.get_num_channels() == 0:
                    data.calm_engine.play()
                data.active_engine.stop()

            # Tank Mobility
            rotated_tank = pygame.transform.rotate(pygame.transform.scale_by(data.test_tank, 0.5), data.tank_angle)
            rotated_tank_rect = rotated_tank.get_rect(center = (d_x, d_y))
            screen.blit(rotated_tank, rotated_tank_rect.topleft)
            
        # Top Info Bar
            if int(epoch) - last_log == 240:
                last_log = int(epoch)
                data.db, connection = get_connection()
                main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, data.db, connection)

            pygame.draw.rect(screen, (0, 0, 0), (0, 0, res_xy[0], 35), 100)

            if not data.db:
                screen.blit(font.render("No Connection To The Server", True, (219, 17, 4)), (full_res_x * 0.0651, full_res_y * 0.0087))
            else:
                screen.blit(font.render("Connected To The Server", True, (5, 199, 2)), (full_res_x * 0.0651, full_res_y * 0.0087))

            screen.blit(font.render(f"Score: {data.score}", True, (226, 226, 10)), (full_res_x * 0.9309, full_res_y * 0.0087))
            screen.blit(font.render(f"Wave:  {data.wave}" , True, (226, 226, 10)), (full_res_x * 0.8789, full_res_y * 0.0087))
            screen.blit(font.render(f"HP:  {int((data.tank_hp / data.max_tank_hp)*100)}%", True, (219, 17, 4)), (full_res_x * 0.6510, full_res_y * 0.0087))
        
        screen.blit(font.render(f"{ingame_time(False)}", True, (255, 255, 255)), (full_res_x * 0.4883, full_res_y * 0.0087))

        if data.playing == False:
            menu_buttons(full_res_x, screen)
            if data.menu_ambient.get_num_channels() == 0:
                    data.menu_ambient.play()
            data.calm_engine.stop()
            data.active_engine.stop()

        # development tool
        #screen.blit(pygame.transform.scale_by(pygame.image.load("files\\textures\\red_dot.png"), 0.25), (900, 650))        # FPS Counter
        if int(epoch) - last_fps_log >= 1:
            last_fps_log = int(epoch)
            data.fps = clock.get_fps()
            fps_text = f"FPS: {int(data.fps)}"
            # Používame už definovaný font namiesto vytvárania nového
            text_surface = font.render(fps_text, True, (255, 255, 255))
        screen.blit(text_surface, (full_res_x * 0.0065, full_res_y * 0.0087))

        pygame.display.update()
        clock.tick(240)

    pygame.quit()
    sys.exit()

# Error Handling
except Exception as e:
    error_window(e, "Main.py")
    os.remove(os.path.join(log_dir, "temp.log"))
    pygame.quit()
    sys.exit()