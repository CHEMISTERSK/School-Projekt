import subprocess as sp, sys, datetime as dt, os
from files.functions.error_handling import error_window

real_time = dt.datetime.now().strftime("%H:%M:%S")
sorce = "Signal Bunker.pyw"

base_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(base_dir, 'files\\Signal_Main.py')

try:
    sp.run([sys.executable, script_path])
except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()

    #test