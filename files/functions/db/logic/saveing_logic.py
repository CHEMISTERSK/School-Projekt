import os, sys, datetime, pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))
from functions.db.db import get_connection
from functions.error_handling import *
from functions import data, console as cons, func

def cloud_save(player_name):
    conn = get_connection()
    cur = conn.cursor()
    real_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    try:
        cur.execute('''
            SELECT id FROM player_data 
            WHERE player_name = %s
        ''', (player_name,))
        
        player_result = cur.fetchone()
        if not player_result:
            cons.append_to_console(f"Player '{player_name}' not found")
            return False
            
        player_id = player_result[0] 
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        
        cur.execute('''
            UPDATE player_data
            SET wave = %s, score = %s, timestemp = %s
            WHERE id = %s
        ''', (data.wave, data.score, timestamp, player_id))
        
        cur.execute('''
            INSERT INTO tank_data 
            (player_id, tank_x, tank_y, tank_angle, tank_speed, tank_rotation_speed, tank_hp, max_tank_hp, timestemp, softdelete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (player_id, data.tank_x, data.tank_y, data.tank_angle, data.tank_speed, data.tank_rotation_speed, data.tank_hp, data.max_tank_hp, timestamp, False))
        
        cur.execute('''
            INSERT INTO shell_data
            (player_id, gs_dmg, gs_pen, gs_spd, os_dmg, os_pen, os_spd, rs_dmg, rs_pen, rs_spd, timestemp, softdelete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (player_id, data.gs_dmg, data.gs_pen, data.gs_spd, data.os_dmg, data.os_pen, data.os_spd, data.rs_dmg, data.rs_pen, data.rs_spd, timestamp, False))

        cur.execute('''
            INSERT INTO time_data
            (player_id, game_ms, last_tick, now, delta, seconds_total, minutes, seconds, timestemp, softdelete)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (player_id, func.game_ms, func.last_tick, func.now, func.delta, func.seconds_total, func.minutes, func.seconds, timestamp, False))
        
        conn.commit()
        cons.append_to_console(f"Game data saved to cloud")
        cons.append_to_temp_log(f"Game data saved to cloud")
        return True
        
    except Exception as e:
        error_window_db(real_time, e, "saveing_logic.py", data.db)
        conn.rollback()
        return False
    
    finally:
        cur.close()
        conn.close()

def clound_load(player_name):
    conn = get_connection()
    cur = conn.cursor()
    real_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    try:
        cur.execute('''
        SELECT 
            tank_data.tank_x,
            tank_data.tank_y,
            tank_data.tank_angle,
            tank_data.tank_speed,
            tank_data.tank_rotation_speed,
            tank_data.tank_hp,
            tank_data.max_tank_hp,

            shell_data.gs_dmg,
            shell_data.gs_pen,
            shell_data.gs_spd,
            shell_data.os_dmg,
            shell_data.os_pen,
            shell_data.os_spd,
            shell_data.rs_dmg,
            shell_data.rs_pen,
            shell_data.rs_spd,

            time_data.game_ms,
            time_data.last_tick,
            time_data.now,
            time_data.delta,
            time_data.seconds_total,
            time_data.minutes,
            time_data.seconds,

            player_data.id AS player_id,
            player_data.wave,
            player_data.score,
            player_data.player_name,
            player_data.timestemp AS player_timestemp
                    
        FROM player_data
        LEFT JOIN tank_data 
		    ON player_data.id = tank_data.player_id 
		    AND player_data.timestemp = tank_data.timestemp
		
		LEFT JOIN shell_data 
		    ON player_data.id = shell_data.player_id 
		    AND player_data.timestemp = shell_data.timestemp
		
		LEFT JOIN time_data 
		    ON player_data.id = time_data.player_id 
		    AND player_data.timestemp = time_data.timestemp
		
		WHERE player_data.player_name = %s
		ORDER BY player_data.timestemp DESC
		LIMIT 1;
        ''', (player_name,))

        result = cur.fetchone()
        return result

    except Exception as e:
        error_window_db(real_time, e, "saveing_logic.py", data.db)
        conn.rollback()
        return False