# Importing external functions
import pygame, sys, time as t, os, random as r, datetime, math, threading
from pygame.locals import *

# Importing internal functions
from functions.error_handling import error_window
from functions.logging import main_log, main_log_clear
from functions.db.db import get_connection
from functions.console import console
from functions import data



# Game Initialization
pygame.init()
pygame.display.set_caption("Signal")

resolution = pygame.display.Info()
full_res_x = resolution.current_w
full_res_y = resolution.current_h

screen = pygame.display.set_mode((full_res_x, full_res_y * 0.93))

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


epoch = t.time()
last_log = int(epoch)

clock = pygame.time.Clock()
current_time = pygame.time.get_ticks()

real_time = datetime.datetime.now().strftime("%H:%M:%S")

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

font = pygame.font.Font(None, 18)

last_fps_log = int(epoch)
fps_text = f"FPS: "
font = pygame.font.Font(None, 18)
text_surface = font.render(fps_text, True, (255, 255, 255))


# Functions Calling
res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
main_log_clear()
db, connection = get_connection()
main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, data.db, connection)
data.set_default_values()



try:
# Main Loop
    while data.running:

        # Screen Resolution
        screen.fill((0, 0, 0))

        # Game Loop
        current_time = pygame.time.get_ticks()

        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        epoch = t.time()
        keys = pygame.key.get_pressed()
        

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(os.path.join(log_dir, "temp.log"))
                data.running = False

            # Key Binding
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os.remove(os.path.join(log_dir, "temp.log"))
                    data.running = False

                # Switching Between Fullscreen And Windowed Mode
                elif event.key == pygame.K_F11:
                    if not data.fullscreen:
                        data.fullscreen = True
                        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
                        screen = pygame.display.set_mode((res_xy[0], res_xy[1]), pygame.FULLSCREEN)

                    elif data.fullscreen:
                        data.fullscreen = False
                        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
                        screen = pygame.display.set_mode((res_xy[0], res_xy[1]))

                elif event.key == pygame.K_F12:
                    threading.Thread(target=console, daemon=True).start()

        # Movement Logic
        if keys[pygame.K_a]:
            data.tank_angle += data.tank_rotation_speed

        if keys[pygame.K_d]:
            data.tank_angle -= data.tank_rotation_speed

        if data.tank_angle > 360:
            data.tank_angle -= 360

        if data.tank_angle < 0:
            data.tank_angle += 360

        angle_radians = math.radians(data.tank_angle)

        if keys[pygame.K_w]:
            data.tank_x -= data.tank_speed * math.sin(angle_radians)
            data.tank_y -= data.tank_speed * math.cos(angle_radians)

        if keys[pygame.K_s]:
            data.tank_x += data.tank_speed * math.sin(angle_radians)
            data.tank_y += data.tank_speed * math.cos(angle_radians)



        rotated_tank = pygame.transform.rotate(data.test_tank, data.tank_angle)
        rotated_tank_rect = rotated_tank.get_rect(center = (data.tank_x, data.tank_y))
        screen.blit(rotated_tank, rotated_tank_rect.topleft)



















        
        if int(epoch) - last_log == 60:
            last_log = int(epoch)
            data.db, connection = get_connection()
            main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, data.db, connection)

        if not db:
            screen.blit(font.render("No Connection", True, (219, 17, 4)), (10, 7))
        else:
            screen.blit(font.render("Connected", True, (5, 199, 2)), (10, 7))

        # FPS Counter
        if int(epoch) - last_fps_log >= 1:
            last_fps_log = int(epoch)
            data.fps = clock.get_fps()
            fps_text = f"FPS: {int(data.fps)}"
            font = pygame.font.Font(None, 18)
            text_surface = font.render(fps_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 25))

        pygame.display.update()
        clock.tick(240)

    pygame.quit()
    sys.exit()

#Error Handling
except Exception as e:
    error_window(e, "Signal_Main.py")
    os.remove(os.path.join(log_dir, "temp.log"))
    pygame.quit()
    sys.exit()