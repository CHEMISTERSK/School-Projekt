import sys, datetime
from error_handling import error_window

sorce = "save.py"

try:
    def saveing():
        print("") #remove me (place holder)

except Exception as e:
    error_window(e, sorce)
    sys.exit()