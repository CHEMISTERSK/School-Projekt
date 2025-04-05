import sys, os, datetime, psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'files')))
from functions.error_handling import error_window


real_time = datetime.datetime.now().strftime("%H:%M:%S")
sorce = "db.py"

try:
    def get_connection():
        return psycopg2.connect(
            host = "localhost",
            port = 5432,
            database = "", #name of database
            user = "postgres",
            password = "50028082"
    )

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()