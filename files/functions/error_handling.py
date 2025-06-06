import ctypes as ct, datetime as dt, os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

real_time = dt.datetime.now().strftime("%H:%M:%S")

def error_window(e, sorce):
    message = f"An error occurred: {e}"
    ct.windll.user32.MessageBoxW(0, f"{message} in {sorce}. \nPlease check error.log \nIn: School_project\\files\\logs", "Error", 0x10)

    global real_time
    log_file_path = os.path.join(log_dir, "error_log.log")
    log_file_path_temp = os.path.join(log_dir, "temp.log")

    with open(log_file_path, "a") as file:
        file.write(f"[{real_time}]Error in {sorce}: {e}\n")
        file.close()

    with open(log_file_path_temp, "a") as file:
        file.write(f"[{real_time}]\nError in {sorce}: {e}")
        file.close()


def error_window_db(real_time, e, sorce, db):
    log_file_path_temp = os.path.join(log_dir, "temp.log")
    
    if not(db):
        with open(log_file_path_temp, "a") as file:
            file.write(f"[{real_time}]\nDatabase connection error.\n")
            file.write(f"[{real_time}]\nError in {sorce}: {e}")
            file.close()
    else:
        with open(log_file_path_temp, "a") as file:
            file.write(f"[{real_time}]\nDatabase error.\n")
            file.write(f"[{real_time}]\nError in {sorce}: {e}")
            file.close()

def login_sign_error(e, sorce):
    global real_time
    log_file_path_temp = os.path.join(log_dir, "temp.log")
    log_file_path = os.path.join(log_dir, "error_log.log")

    with open(log_file_path_temp, "a") as file:
        file.write(f"[{real_time}]\nLogin/Sign-up error.\n")
        file.write(f"[{real_time}]\nError in {sorce}: {e}")
        file.close()
    
    with open(log_file_path, "a") as file:
        file.write(f"[{real_time}]Error in {sorce}: {e}\n")
        file.close()

def loading_error(e, sorce):
    global real_time
    log_file_path_temp = os.path.join(log_dir, "temp.log")
    log_file_path = os.path.join(log_dir, "error_log.log")

    with open(log_file_path_temp, "a") as file:
        file.write(f"[{real_time}]\nSave loading error.\n")
        file.write(f"[{real_time}]\nError in {sorce}: {e}")
        file.close()
    
    with open(log_file_path, "a") as file:
        file.write(f"[{real_time}]Error in {sorce}: {e}\n")
        file.close()