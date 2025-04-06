#Importing external functions
import pygame, sys, time as t, os, random as r, datetime, ctypes, subprocess
from pygame.locals import *

#Importing internal functions
from functions.error_handling import error_window
from functions.logging import main_log, main_log_clear
from functions.db.db import get_connection




#Game Initialization
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
running = True

sorce = "Signal_Main.py"
console_process = None
fullscreen = False

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files', 'logs')
log_path = os.path.join(log_dir, "running_log.log")


#Default Value Settings (New Game later in .dat file)




#Loading Files




#Functions calling
res_xy = screen_resolution(full_res_x, full_res_y, fullscreen)
main_log_clear()
main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch)
get_connection()


#Functions
def toggle_console():
    global console_process
    if console_process is None:
        # Open a new console window
        console_process = subprocess.Popen("python", creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # Close the console window
        console_process.terminate()
        console_process = None




try:
#Main Loop
    while running:

        #Screen Resolution
        screen.fill((0, 0, 0))

        #FPS Counter
        fps = clock.get_fps()
        fps_text = f"FPS: {int(fps)}"
        font = pygame.font.Font(None, 18)
        text_surface = font.render(fps_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        #Game Loop
        clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()

        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        epoch = t.time()

        keys = pygame.key.get_pressed()

        if(int(epoch) - last_log == 60):
            last_log = int(epoch)
            main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Key Binding
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                #Switching Between Fullscreen And Windowed Mode
                elif event.key == pygame.K_F11:
                    if not fullscreen:
                        fullscreen = True
                        res_xy = screen_resolution(full_res_x, full_res_y, fullscreen)
                        screen = pygame.display.set_mode((res_xy[0], res_xy[1]), pygame.FULLSCREEN)
                    
                    elif fullscreen:
                        fullscreen = False
                        res_xy = screen_resolution(full_res_x, full_res_y, fullscreen)
                        screen = pygame.display.set_mode((res_xy[0], res_xy[1]))
                
                elif event.key == pygame.K_F12:
                    toggle_console()



         

















        

        pygame.display.update()
        clock.tick(180)

    pygame.quit()
    sys.exit()

#Error Handling
except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    pygame.quit()
    sys.exit()