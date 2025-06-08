import sys, datetime as dt, os, tkinter, pygame, json
from tkinter import scrolledtext
from functions.error_handling import error_window
from functions import data
from functions.logging import console_output_log


log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
real_time = dt.datetime.now().strftime("%H:%M:%S")

sorce = "console.py"
command_line = None


try:
    def console():

        root = tkinter.Tk()
        root.title("Output Terminal")
        root.geometry("800x400")

        # Grid layout configuration (2 rows: output + input line)
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=0)
        root.grid_columnconfigure(0, weight=1)

        # Output console
        console_output = scrolledtext.ScrolledText(
            root, wrap=tkinter.WORD, state='disabled', bg='black', fg='white'
        )
        console_output.grid(row=0, column=0, sticky='nsew')

        def append_to_console(text):
            console_output.config(state='normal')
            console_output.insert(tkinter.END, text + "\n")
            console_output.config(state = 'disabled')
            console_output.see(tkinter.END)

        def append_to_temp_log(text):
            with open (os.path.join(log_dir, "temp.log"), 'a') as temp_file:
                temp_file.write(f"{text}\n")
                temp_file.close()

        def export_content():
            user_name = os.getlogin()
            file_path = f"C:\\Users\\{user_name}\\Desktop\\export.txt"
            with open(file_path, 'w') as file:
                console_output.config(state='normal')
                file.write(console_output.get("1.0", tkinter.END))
                console_output.config(state='disabled')

        def clear_terminal():
            console_output.config(state='normal')
            console_output.delete("1.0", tkinter.END)
            console_output.config(state='disabled')
            data.copy = True

            with open(os.path.join(log_dir, "temp.log"), 'w') as temp_file:
                temp_file.truncate(0)

        def copy_content():
            root.clipboard_clear()
            console_output.config(state='normal')
            root.clipboard_append(console_output.get("1.0", tkinter.END))
            console_output.config(state='disabled')
            root.update()
        
        def av_reload():
            data.texture_loading_path, data.sound_loading_path = data.load_audiovisual()

            data.test_tank      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))
            data.surface        =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[1]), (data.fov / 2))
            data.orange_shell   =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[2]), (data.fov / 25))
            data.red_shell      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[3]), (data.fov / 25))
            data.green_shell    =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[4]), (data.fov / 25))
            data.shells         =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[5]), (data.fov / 12.5))

            data.shot_sound =    pygame.mixer.Sound(data.sound_loading_path[0])
            data.realod_sound =  pygame.mixer.Sound(data.sound_loading_path[1])
            data.active_engine = pygame.mixer.Sound(data.sound_loading_path[2])
            data.calm_engine =   pygame.mixer.Sound(data.sound_loading_path[3])

            data.calm_engine.set_volume(data.settings["volume"])    
            data.active_engine.set_volume(data.settings["volume"] / 2)  

        def data_reload():
            data.default_data = data.set_default_values()

            data.tank_x =              float(data.default_data["tank_x"])
            data.tank_y =              float(data.default_data["tank_y"])
            data.tank_angle =          float(data.default_data["tank_angle"])
            data.tank_speed =          float(data.default_data["tank_speed"])
            data.tank_rotation_speed = float(data.default_data["tank_rotation_speed"])
            data.tank_hp =             float(data.default_data["tank_hp"])
            data.max_tank_hp =         float(data.default_data["max_tank_hp"])

            data.gs_dmg = float(data.default_data["gs_dmg"])    
            data.gs_pen = float(data.default_data["gs_pen"])    
            data.gs_spd = float(data.default_data["gs_spd"])    

            data.os_dmg = float(data.default_data["os_dmg"])
            data.os_pen = float(data.default_data["os_pen"])
            data.os_spd = float(data.default_data["os_spd"])

            data.rs_dmg = float(data.default_data["rs_dmg"])
            data.rs_pen = float(data.default_data["rs_pen"])
            data.rs_spd = float(data.default_data["rs_spd"])

            data.wave =  int(data.default_data["wave"])
            data.score = int(data.default_data["score"])

        def command_line_execution(command_line):
            command = command_line.split()
            if command[0] == "help":
                append_to_console("Available commands:\n\tset\n\tshow\n\tshutdown")
                append_to_temp_log("Available commands:\n\tset\n\tshow\n\tshutdown")
            elif command[0] == "set":
                if command[1] == "?":
                    append_to_console("variables:\n\ttank_x [value]/default\n\ttank_y [value]/default\n\ttank_angle [value]/default\n\ttank_speed [value]/default\n\ttank_rotation_speed [value]/default\n\ttank_location default\n\tdefault all")
                    append_to_temp_log("variables:\n\ttank_x [value]/default\n\ttank_y [value]/default\n\ttank_angle [value]/default\n\ttank_speed [value]/default\n\ttank_rotation_speed [value]/default\n\ttank_location default\n\tdefault all")
                elif command[2] == "default":
                    if command[1] == "tank_location":
                        data.tank_x, data.tank_y = data.set_tank_location_default(data.default_data)
                    elif command[1] == "tank_speed":
                        data.tank_speed = data.set_tank_speed_default(data.default_data)
                    elif command[1] == "tank_rotation_speed":
                        data.tank_rotation_speed = data.set_tank_rotation_speed_default(data.default_data)
                    elif command[1] == "tank_angle":
                        data.tank_angle = data.set_tank_angle_default(data.default_data)
                    elif command[1] == "fov":
                        data.fov = data.set_fov_default(data.default_data)
                    else:
                        append_to_console(f"Unknown variable: {command[1]} or argument\nUse \"set ?\" for help.")
                        append_to_temp_log(f"Unknown variable: {command[1]} or argument\nUse \"set ?\" for help.")

                elif command[1] == "tank_x":
                    data.tank_x = float(eval(command[2]))
                elif command[1] == "tank_y":
                    data.tank_y = float(eval(command[2]))
                elif command[1] == "tank_angle":
                    data.tank_angle = float(eval(command[2]))
                elif command[1] == "tank_speed":
                    data.tank_speed = float(eval(command[2]))                
                elif command[1] == "tank_rotation_speed":
                    data.tank_rotation_speed = float(eval(command[2]))
                elif command[1] == "fov":
                    if float(command[2]) >= 0.1 and float(command[2]) <= 5:
                        data.fov = float(command[2])
                        av_reload()
                    else:
                        append_to_console("Error: Invalid argument or out of range.")
                        append_to_temp_log("Error: Invalid argument or out of range.")
                elif command[1] == "default" and command[2] == "all":
                    default_data = data.set_default_values()
                    data.tank_x =               float(default_data["tank_x"])
                    data.tank_y =               float(default_data["tank_y"])
                    data.tank_angle =           float(default_data["tank_angle"])
                    data.tank_speed =           float(default_data["tank_speed"])
                    data.tank_rotation_speed =  float(default_data["tank_rotation_speed"])
                    data.fov =                  float(default_data["fov"])
                else:
                    append_to_console(f"Unknown variable: {command[1]} or argument\nUse \"set ?\" for help.")
                    append_to_temp_log(f"Unknown variable: {command[1]} or argument\nUse \"set ?\" for help.")

            elif command[0] == "show" or command[0] == "sh":
                if command[1] == "tank_info":
                    append_to_console(console_output_log(data.tank_x, data.tank_y, data.tank_angle, data.tank_speed, data.tank_rotation_speed, data.tank_hp))
                    append_to_temp_log(console_output_log(data.tank_x, data.tank_y, data.tank_angle, data.tank_speed, data.tank_rotation_speed, data.tank_hp))

                elif command[1] == "time":
                    append_to_console(f"[{real_time}]")
                    append_to_temp_log(f"[{real_time}]")

                elif command[1] == "fps":
                    append_to_console(str(int(data.fps)))
                    append_to_temp_log(str(int(data.fps)))

                elif command[1] == "res":
                    resolution = pygame.display.Info()
                    full_res_x = resolution.current_w
                    full_res_y = resolution.current_h
                    append_to_console(f"{full_res_x}x{full_res_y}")
                    append_to_temp_log(f"{full_res_x}x{full_res_y}")

                elif command[1] == "tank_speed":
                    append_to_console(f"Tank Speed: {data.tank_speed}")
                    append_to_temp_log(f"Tank Speed: {data.tank_speed}")

                elif command[1] == "tank_rotation_speed":
                    append_to_console(f"Tank Rotation Speed: {data.tank_rotation_speed}")
                    append_to_temp_log(f"Tank Rotation Speed: {data.tank_rotation_speed}")

                elif command[1] == "tank_location":
                    append_to_console(f"Tank Location: ({data.tank_x}, {data.tank_y})")
                    append_to_temp_log(f"Tank Location: ({data.tank_x}, {data.tank_y})")

                elif command[1] == "tank_angle":
                    append_to_console(f"Tank Angle: {data.tank_angle}")
                    append_to_temp_log(f"Tank Angle: {data.tank_angle}")

                elif command[1] == "?":
                    append_to_console("variables:\n\ttank_info\n\ttime\n\tfps\n\tres\n\ttank_speed\n\ttank_rotation_speed\n\ttank_location\n\ttank_angle")
                    append_to_temp_log("variables:\n\ttank_info\n\ttime\n\tfps\n\tres\n\ttank_speed\n\ttank_rotation_speed\n\ttank_location\n\ttank_angle")

                else:
                    append_to_console(f"Unknown variable: {command[1]}")
                    append_to_temp_log(f"Unknown variable: {command[1]}")
            
            elif command[0] == "shutdown":
                append_to_console("Shutting down...")
                append_to_temp_log("Shutting down...")
                data.running = False

            elif command[0] == "reload_av":
                append_to_console("Reloading AV data...")
                append_to_temp_log("Reloading AV data...")
                av_reload()
                append_to_console("AV data reloaded successfully.")
                append_to_temp_log("AV data reloaded successfully.")

            elif command[0] == "reload_data":
                append_to_console("Reloading data...")
                append_to_temp_log("Reloading data...")
                data_reload()
                append_to_console("Data reloaded successfully.")
                append_to_temp_log("Data reloaded successfully.")

            else:
                append_to_console(f"Unknown command: {command[0]}")
                append_to_temp_log(f"Unknown command: {command[0]}")
                append_to_console("Use \"help\" for help.")
                append_to_temp_log("Use \"help\" for help.")

        def execute_command():
            command_line = command_entry.get()
            append_to_console(f">>{command_line}")
            append_to_temp_log(f">>{command_line}")
            command_entry.delete(0, tkinter.END)
            command_line_execution(command_line)

        # Command line frame with Execute button on the left
        command_frame = tkinter.Frame(root)
        command_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        command_frame.grid_columnconfigure(1, weight=1)

        execute_button = tkinter.Button(command_frame, text="Execute", command=execute_command)
        execute_button.grid(row=0, column=0, padx=(0, 5))

        command_entry = tkinter.Entry(command_frame, bg='white', fg='black')
        command_entry.grid(row=0, column=1, sticky='ew')

        # Optional buttons frame (can be placed elsewhere or removed if not needed)
        button_frame = tkinter.Frame(root)
        button_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        export_button = tkinter.Button(button_frame, text="Export", command=export_content)
        export_button.grid(row=0, column=0, padx=5, sticky='ew')

        clear_button = tkinter.Button(button_frame, text="Clear", command=clear_terminal)
        clear_button.grid(row=0, column=1, padx=5, sticky='ew')

        copy_button = tkinter.Button(button_frame, text="Copy", command=copy_content)
        copy_button.grid(row=0, column=2, padx=5, sticky='ew')

        # Loading output from a file
        with open(os.path.join(log_dir, "temp.log"), 'r') as temp_file:
            lines = temp_file.readlines()
            for line in lines:
                append_to_console(line.strip())         
        
        root.mainloop()

except Exception as e:
    error_window(e, sorce)
    sys.exit()
