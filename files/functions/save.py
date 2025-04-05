import sys, datetime, json
from error_handling import error_window

real_time = datetime.datetime.now().strftime("%H:%M:%S")
sorce = "save.py"

try:
    def saveing():
        print("") #remove me (place holder)

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()