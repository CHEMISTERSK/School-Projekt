import ctypes as ct, datetime as dt, os

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

real_time = dt.datetime.now().strftime("%H:%M:%S")

def error_window(message, real_time, e, sorce):
    print(f"\n[{real_time}]Error in {sorce}:\t{e}\n")
    ct.windll.user32.MessageBoxW(0, f"{message} in {sorce}. \nPlease check error.log \nIn: Signal\\files\\logs", "Error", 0x10)

    log_file_path = os.path.join(log_dir, "error_log.log")

    with open(log_file_path, "a") as file:
        file.write(f"[{real_time}]Error in {sorce}: {e}")


def error_window_db(real_time, e, sorce):
    print("Database connection error.\n")
    print(f"[{real_time}]Error in {sorce}:\t{e}\n")

    log_file_path = os.path.join(log_dir, "error_log.log")

    with open(log_file_path, "a") as file:
        file.write(f"[{real_time}]Error in {sorce}: {e}")