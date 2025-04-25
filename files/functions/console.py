import sys, datetime as dt, os, tkinter
from tkinter import scrolledtext
from functions.error_handling import error_window
from functions import data
from functions.logging import console_output_log

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
real_time = dt.datetime.now().strftime("%H:%M:%S")

sorce = "console.py"
console_process = None
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

            with open(os.path.join(log_dir, "temp.log"), 'w') as temp_file:
                temp_file.truncate(0)

        def copy_content():
            root.clipboard_clear()
            console_output.config(state='normal')
            root.clipboard_append(console_output.get("1.0", tkinter.END))
            console_output.config(state='disabled')
            root.update()

        def default_values():
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
            with open (os.path.join(data_path, "default_data.dat"), "r") as file:
                default_data = file.readlines()
                file.close()
            return default_data

        def command_line_execution(command_line):
            command = command_line.split()
            if command[0] == "set":
                if command[1] == "tank_x":
                    data.tank_x = float(command[2])
                elif command[1] == "tank_y":
                    data.tank_y = float(command[2])
                elif command[1] == "tank_angle":
                    data.tank_angle = float(command[2])
                elif command[1] == "tank_speed":
                    data.tank_speed = float(command[2])
                elif command[1] == "tank_rotation_speed":
                    data.tank_rotation_speed = float(command[2])
                elif command[1] == "?":
                    append_to_console("variables:\n\ttank_x [value]\n\ttank_y [value]\n\ttank_angle [value]\n\ttank_speed [value]\n\ttank_rotation_speed [value]")
                elif command[1] == "default" and command[2] == "all":
                    default_data = default_values()
                    data.tank_x = float(default_data[0])
                    data.tank_y = float(default_data[1])
                    data.tank_angle = float(default_data[2])
                    data.tank_speed = float(default_data[3])
                    data.tank_rotation_speed = float(default_data[4]) 
                else:
                    append_to_console(f"Unknown variable: {command[1]}")

            elif command[0] == "show" or command[0] == "sh":
                if command[1] == "tank_info":
                    append_to_console(console_output_log(data.tank_x, data.tank_y, data.tank_angle, data.tank_speed, data.tank_rotation_speed))
                elif command[1] == "time":
                    append_to_console(f"[{real_time}]")
                elif command[1] == "fps":
                    append_to_console(str(int(data.fps)))
                elif command[1] == "?":
                    append_to_console("variables:\n\ttank_info\n\ttime\n\tfps")
                else:
                    append_to_console(f"Unknown variable: {command[1]}")
            elif command[0] == "shutdown":
                append_to_console("Shutting down...")
                data.running = False

        def execute_command():
            command_line = command_entry.get()
            append_to_console(f">>{command_line}")
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

    #console()

except Exception as e:
    error_window(e, sorce)
    sys.exit()
