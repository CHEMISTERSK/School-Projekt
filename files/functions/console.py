import sys, datetime as dt, os, tkinter
from tkinter import scrolledtext
from functions.error_handling import error_window

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
real_time = dt.datetime.now().strftime("%H:%M:%S")

sorce = "console.py"

console_process = None

try:
    def console():
        root = tkinter.Tk()
        root.title("Output Terminal")
        root.geometry("800x400")

        # Grid layout configuration (2 rows: output + buttons)
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
            console_output.insert(tkinter.END, text + '\n')
            console_output.config(state='disabled')
            console_output.see(tkinter.END)

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
                temp_file.write(" ")

        def copy_content():
            root.clipboard_clear()
            console_output.config(state='normal')
            root.clipboard_append(console_output.get("1.0", tkinter.END))
            console_output.config(state='disabled')
            root.update()

        # Button frame
        button_frame = tkinter.Frame(root)
        button_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        # Buttons
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
