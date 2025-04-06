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
        root.title("Console Output")
        root.geometry("600x400")

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

        # Example usage: Append some text
        with open(os.path.join(log_dir, "temp.log"), 'r') as temp_file:
            lines = temp_file.readlines()
            for line in lines:
                append_to_console(line.strip())

        # Start the Tkinter main loop
        root.mainloop()
    #toggle_console()

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()