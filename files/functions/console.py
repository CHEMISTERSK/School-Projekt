import sys, datetime as dt, os, tkinter
from tkinter import scrolledtext
from functions.error_handling import error_window

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
real_time = dt.datetime.now().strftime("%H:%M:%S")
sorce = "console.py"

console_process = None

try:
    def toggle_console():
        # Create a new Tkinter window
        root = tkinter.Tk()
        root.title("Output Terminal")
        root.geometry("800x400")

        # Add a scrolled text widget for output with a black background and white text
        console_output = scrolledtext.ScrolledText(
            root, wrap=tkinter.WORD, state='disabled', bg='black', fg='white'
        )
        console_output.pack(expand=True, fill='both')

        # Function to append text to the console
        def append_to_console(text):
            console_output.config(state='normal')  # Enable editing
            console_output.insert(tkinter.END, text + '\n')  # Add text
            console_output.config(state='disabled')  # Disable editing
            console_output.see(tkinter.END)  # Scroll to the end

        # Export content of the terminal to a file
        def export_content():
            user_name = os.getlogin()
            file_path = f"C:\\users\\{user_name}\\desktop\\export.txt"
            
            if file_path:
                with open(file_path, 'w') as file:
                    console_output.config(state='normal')
                    file.write(console_output.get("1.0", tkinter.END))
                    console_output.config(state='disabled')

        # Clear the terminal content
        def clear_terminal():
            console_output.config(state='normal')
            console_output.delete("1.0", tkinter.END)
            console_output.config(state='disabled')

        # Copy content of the terminal to clipboard
        def copy_content():
            root.clipboard_clear()
            console_output.config(state='normal')
            root.clipboard_append(console_output.get("1.0", tkinter.END))
            console_output.config(state='disabled')
            root.update()  # Update the clipboard

        # Add buttons at the bottom of the terminal
        button_frame = tkinter.Frame(root)
        button_frame.pack(fill='x', side='bottom')

        export_button = tkinter.Button(button_frame, text="Export", command=export_content)
        export_button.pack(side='left', padx=5, pady=5)

        clear_button = tkinter.Button(button_frame, text="Clear", command=clear_terminal)
        clear_button.pack(side='left', padx=5, pady=5)

        copy_button = tkinter.Button(button_frame, text="Copy", command=copy_content)
        copy_button.pack(side='left', padx=5, pady=5)

        # Example usage: Append some text
        with open(os.path.join(log_dir, "temp.log"), 'r') as temp_file:
            lines = temp_file.readlines()
            for line in lines:
                append_to_console(line.strip())

        # Start the Tkinter main loop
        root.mainloop()

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()