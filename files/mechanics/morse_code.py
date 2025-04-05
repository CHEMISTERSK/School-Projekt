import sys, os, datetime, winsound as ws, time as t, pygame
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'files')))

from functions.error_handling import error_window

real_time = datetime.datetime.now().strftime("%H:%M:%S")
sorce = "morse_code.py"

try:
    MORSE_CODE = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',  
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...',
    '8': '---..', '9': '----.', '0': '-----'
    }

    FREQ = 800  # Frequncy(Hz)
    DOT = 150   # dot duration (ms)
    DASH = 450  # desh duration (ms)

    def play_morse(text):
        last_epoch = pygame.time.get_ticks()

        for char in text.upper():
            if char == ' ':
                while pygame.time.get_ticks() - last_epoch < 75:    #pause between words
                    pass
                last_epoch = pygame.time.get_ticks()  
                continue

            if char in MORSE_CODE:
                for symbol in MORSE_CODE[char]:
                    current_epoch = pygame.time.get_ticks() 

                    pause_duration = current_epoch - last_epoch
                    if pause_duration < DOT:
                        pygame.time.delay(DOT - pause_duration)
                    
                    if symbol == '.':
                        ws.Beep(FREQ, DOT)  # dot
                    elif symbol == '-':
                        ws.Beep(FREQ, DASH)  # dash

                    last_epoch = pygame.time.get_ticks()    #Reset the epoch for each symbol

                pygame.time.delay(1)  #pause between letters
        pygame.time.delay(100)  #last letter pause

except Exception as e:
    error_window(f"An error occurred: {e}", real_time, e, sorce)
    sys.exit()