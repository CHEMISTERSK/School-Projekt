import sys, datetime, re, os
from functions.error_handling import error_window, loading_error
from functions import data
from functions import func

sorce = "save.py"


try:
    def saveing():
        global data
        save_data = [
            data.tank_x,
            data.tank_y,
            data.tank_angle,
            data.tank_speed,
            data.tank_rotation_speed,
            data.tank_hp,
            data.max_tank_hp,
            data.gs_dmg,
            data.gs_pen,
            data.gs_spd,
            data.os_dmg,
            data.os_pen,
            data.os_spd,
            data.rs_dmg,
            data.rs_pen,
            data.rs_spd,
            data.wave,
            data.score
        ]

        for data_ in data.time_data:
            save_data.append(data_)

        with open(f"files\\saves\\save_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sav", "w") as save_file:
            for data_ in save_data:
                save_file.write(f"{data_}\n")
            save_file.close()
        
        # Pridaný algoritmus na mazanie najstaršieho save, ak ich je viac ako 5
        save_files = os.listdir("files\\saves")
        if len(save_files) > 5:
            oldest_time = float('inf')
            oldest_file = None
            
            for save in save_files:
                if save.startswith("save_") and save.endswith(".sav"):
                    try:
                        timestamp = int(save[5:-4])
                        if timestamp < oldest_time:
                            oldest_time = timestamp
                            oldest_file = save
                    except ValueError:
                        continue
                        
            if oldest_file:
                try:
                    os.remove(os.path.join("files\\saves", oldest_file))
                    print(f"Removed oldest save file: {oldest_file}")
                except Exception as e:
                    print(f"Error removing oldest save: {e}")

    def loading():
        global data, func
        b = 0
        save_files = os.listdir("files\\saves")
        for save in save_files:
            a = int(save[5:-4])
            if a > b:
                b = a
            else:
                continue
        with open(f"files\\saves\\save_{b}.sav", "r") as save_file:
            loaded_data = save_file.readlines()
            save_file.close()
            
        try:
            if len(loaded_data) < 25:
                raise ValueError("Save file is corrupted or incomplete.")
            
            data.tank_x =                float(loaded_data[0].strip())
            data.tank_y =                float(loaded_data[1].strip())
            data.tank_angle =            float(loaded_data[2].strip())
            data.tank_speed =            float(loaded_data[3].strip())
            data.tank_rotation_speed =   float(loaded_data[4].strip())
            data.tank_hp =               float(loaded_data[5].strip())
            data.max_tank_hp =           float(loaded_data[6].strip())
            data.gs_dmg =                float(loaded_data[7].strip())
            data.gs_pen =                float(loaded_data[8].strip())
            data.gs_spd =                float(loaded_data[9].strip())
            data.os_dmg =                float(loaded_data[10].strip())
            data.os_pen =                float(loaded_data[11].strip())
            data.os_spd =                float(loaded_data[12].strip())
            data.rs_dmg =                float(loaded_data[13].strip())
            data.rs_pen =                float(loaded_data[14].strip())
            data.rs_spd =                float(loaded_data[15].strip())
            data.wave =                    int(loaded_data[16].strip())
            data.score =                   int(loaded_data[17].strip())

            func.game_ms =           int(loaded_data[18].strip())
            func.last_tick =         None
            func.now =               int(loaded_data[20].strip())
            func.delta =             int(loaded_data[21].strip())
            func.seconds_total =     int(loaded_data[22].strip())
            func.minutes =           int(loaded_data[23].strip())
            func.seconds =           int(loaded_data[24].strip())

        except Exception as e:
            loading_error(e, sorce)

except Exception as e:
    error_window(e, sorce)
    sys.exit()