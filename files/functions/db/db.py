import sys, os, datetime, psycopg2
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'files')))
from functions.error_handling import error_window

#Variables For except Exception
real_time = datetime.datetime.now().strftime("%H:%M:%S")
sorce = "db.py"

try:
    def get_connection():
        #Variables For except psycopg2.OperationalError
        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        sorce = "db.py"
        try:
            return psycopg2.connect(
                host = "localhost",
                port = 5432,
                database = "", #name of database
                user = "postgres",
                password = "50028082"
            )
        #Connection error handling
        except psycopg2.OperationalError as e:
            error_window("Database connection error.", real_time, e, sorce)
            return None

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()