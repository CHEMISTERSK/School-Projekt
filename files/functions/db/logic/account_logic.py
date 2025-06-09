import os, sys, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from functions.db.db import get_connection
from functions.error_handling import *
from functions import data
from functions.logging import append_to_temp_log

real_time = datetime.datetime.now().strftime("%H:%M:%S")

def sign_up(wave, score, player_name, password):
    conn = get_connection()
    cur = conn.cursor()
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    try:
        cur.execute('''
            SELECT player_name FROM player_data WHERE player_name = %s AND softdelete = %s
        ''', (player_name, False))
        
        result = cur.fetchone()
        if result:
            login_sign_error("Username already exists", "account_logic.py")
            append_to_temp_log("Sign up failed: Username already exists")
            return False
        
        else:
            cur.execute('''
                INSERT INTO player_data (wave, score, player_name, password, timestemp, softdelete) 
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (wave, score, player_name, password, timestamp, False))
            append_to_temp_log("Sign up successful")
            conn.commit()
            return True
        
    except Exception as e:
        error_window_db(real_time, e, "account_logic.py", data.db)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

def login(player_name, password):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute('''
            SELECT * FROM player_data WHERE player_name = %s AND password = %s AND softdelete = %s
        ''', (player_name, password, False))

        result = cur.fetchone()
        if result:
            append_to_temp_log("Login successful")
            return True
        
        else:
            append_to_temp_log("Login failed: Invalid credentials or account deleted")
            return False
        
    except Exception as e:
        error_window_db(real_time, e, "account_logic.py", data.db)
        return False
    
    finally:
        cur.close()
        conn.close()

