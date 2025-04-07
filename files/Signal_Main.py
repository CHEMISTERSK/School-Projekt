#Importing external functions
import pygame, sys, time as t, os, random as r, datetime
from pygame.locals import *

#Importing internal functions
from functions.error_handling import error_window
from functions.logging import main_log, main_log_clear
from functions.db.db import get_connection
from functions.console import console




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

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

db = False


#Default Value Settings (New Game later in .dat file)




#Loading Files




#Functions calling
res_xy = screen_resolution(full_res_x, full_res_y, fullscreen)
main_log_clear()
db, connection = get_connection()
main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, db, connection)




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
        screen.blit(text_surface, (10, 28))

        #Game Loop
        clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()

        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        epoch = t.time()

        keys = pygame.key.get_pressed()

        if(int(epoch) - last_log == 60):
            last_log = int(epoch)
            db, connection = get_connection()
            main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, db, connection)
            

        if not db:
            screen.blit(font.render("No Connection", True, (255, 255, 255)), (10, 10))
        else:
            screen.blit(font.render("Connected", True, (255, 255, 255)), (10, 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(os.path.join(log_dir, "temp.log"))
                running = False

            #Key Binding
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    os.remove(os.path.join(log_dir, "temp.log"))
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
                    console()



         
















        

        pygame.display.update()
        clock.tick(180)

    pygame.quit()
    sys.exit()

#Error Handling
except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    os.remove(os.path.join(log_dir, "temp.log"))
    pygame.quit()
    sys.exit()