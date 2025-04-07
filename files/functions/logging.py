import os, pygame, sys, datetime as dt
from datetime import date
from functions.error_handling import error_window

real_time = dt.datetime.now().strftime("%H:%M:%S")
log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
sorce = "logging.py"

try:
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    def main_log(real_time, resolution, res_x, res_y, clock, current_time, epoch, db, connection):
        log_path_a = os.path.join(log_dir, "running_log.log")
        log_path_b = os.path.join(log_dir, "epoch_running_log.log")
        log_path_c = os.path.join(log_dir, "temp.log")
        
        with open(log_path_a, "a") as file:
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
            file.write("\n")
            file.close()

        with open(log_path_b, "a") as file:
            file.write("\n")
            file.write(f"[{date.today()}] [{real_time}]\n")
            file.write(f"Resolution:\n\t{resolution}\n")
            file.write(f"Resolution X:\t{res_x} px\n")
            file.write(f"Resolution Y:\t{int(res_y)} px\n")
            file.write(f"PyClock:\t{clock}\n")
            file.write(f"CurrentTime:\t{current_time}\n")
            file.write(f"Epoch:\t{epoch}\n")
            file.write(f"PyGame Version:\t{pygame.version.ver}\n")
            file.write("\n")
            file.close()

        with open(log_path_c, "a") as file:
            file.write(f"[{real_time}]\n")
            file.write(f"Resolution X:\t{res_x} px\n")
            file.write(f"Resolution Y:\t{int(res_y)} px\n")
            file.write(f"PyClock:\t{clock}\n")
            file.write(f"CurrentTime:\t{current_time}\n")
            file.write(f"Epoch:\t{epoch}\n")
            file.write(f"PyGame Version:\t{pygame.version.ver}\n")
            file.write(f"[{real_time}]\nDatabase connection status: {db}, Connection object: {connection}\n")
            file.close()

    def main_log_clear():
        log_path = os.path.join(log_dir, "running_log.log")
        with open(log_path, "w") as file:
            file.write(" ")     
            file.close()

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()