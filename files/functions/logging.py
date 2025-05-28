import os, pygame, sys, datetime as dt
from datetime import date
from functions.error_handling import error_window
from functions import data

real_time = dt.datetime.now().strftime("%H:%M:%S")
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
sorce = "logging.py"

try:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def main_log(real_time, resolution, res_x, res_y, clock, current_time, epoch, db, connection):
        log_path_r = os.path.join(log_dir, "running_log.log")
        
        with open(log_path_r, "a") as file:
            file.write("\n")
            file.write(f"[{real_time}]\n")
            file.write(f"Resolution:\n\t{resolution}\n")
            file.write(f"Resolution X:\t{res_x} px\n")
            file.write(f"Resolution Y:\t{int(res_y)} px\n")
            file.write(f"PyClock:\t{clock}\n")
            file.write(f"CurrentTime:\t{current_time}\n")
            file.write(f"Epoch:\t\t{epoch}\n")
            file.write(f"PyGame Version:\t{pygame.version.ver}\n")
            file.write(f"Database connection status: {db}, Connection object: {connection}")
            file.close()

    def main_log_clear():
        log_path_t = os.path.join(log_dir, "temp.log")
        log_path = os.path.join(log_dir, "running_log.log")
        
        with open(log_path, "w") as file:
            file.write(" ")     
            file.close()

        if data.copy == True:
            with open(log_path_t, "w") as file:
                file.write("Signal_Bunker game console all rights reserved (C)\n")
                file.close()
            data.copy = False
    
    def console_output_log(tank_x, tank_y, tank_angle, tank_speed, tank_rotation_speed):
        return f"Tank X:\t\t\t{tank_x}\n" \
               f"Tank Y:\t\t\t{tank_y}\n" \
               f"Tank Angle:\t\t\t{tank_angle}\n" \
               f"Tank Speed:\t\t\t{tank_speed}\n" \
               f"Tank Rotation Speed:\t\t\t{tank_rotation_speed}\n"
        

except Exception as e:
    error_window(e, sorce)
    sys.exit()