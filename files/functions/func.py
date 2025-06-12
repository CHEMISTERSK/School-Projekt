from functions import data
from functions.db.logic.account_logic import login, sign_up
import pygame, os, tkinter as tk, json, threading
from tkinter import messagebox, ttk

game_ms = 0  
last_tick = None
now = 0
delta = 0
minutes = 0
seconds = 0
seconds_total = 0

def ingame_time(exp):
    global game_ms, last_tick, delta, now, minutes, seconds, seconds_total
    if data.playing:
        now = pygame.time.get_ticks()
        if last_tick is not None:
            delta = now - last_tick  
            game_ms += delta
        last_tick = now
    else:
        last_tick = None
    
    seconds_total = game_ms // 1000
    minutes = seconds_total // 60
    seconds = seconds_total % 60

    if exp == True:
        return [game_ms, None, now, delta, seconds_total, minutes, seconds]
    else:
        return f"{minutes:02d}:{seconds:02d}"

def reset_game_time():
    global game_ms, last_tick
    game_ms = 0
    last_tick = None

def fullscreen_toggle(full_res_x, full_res_y):
    if data.fullscreen:
        data.fullscreen = False
        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
        pygame.display.set_mode((res_xy[0], res_xy[1]), pygame.FULLSCREEN)

    elif not data.fullscreen:
        data.fullscreen = True
        res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
        pygame.display.set_mode((res_xy[0], res_xy[1]))
    
def screen_resolution(full_res_x, full_res_y, fullscreen):
    window_res_x = full_res_x
    window_res_y = full_res_y * 0.93 #%

    if fullscreen == False:
        res_x = full_res_x * 1.25 #%
        res_y = full_res_y * 1.25 #%

    elif fullscreen == True:
        res_x = window_res_x
        res_y = window_res_y

    return(res_x, res_y)

def av_reload():
    data.texture_loading_path, data.sound_loading_path = data.load_audiovisual()

    data.test_tank      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))
    data.main_tank      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))  # Hráčský tank
    data.hull           =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[7]), (data.fov / 1))  # Podvozok hráča
    data.turret         =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[8]), (data.fov / 1))  # Veža hráča
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
    data.turret_angle =        0.0  # Reset uhla veže
    data.tank_speed =          float(data.default_data["tank_speed"])
    data.tank_rotation_speed = float(data.default_data["tank_rotation_speed"])
    data.tank_hp =             float(data.default_data["tank_hp"])
    data.max_tank_hp =         float(data.default_data["max_tank_hp"])

    # Shells Data   (gs - green shell;  os - orange shell;  rs - red shell)
    data.gs_dmg = float(data.default_data["gs_dmg"])    # damage
    data.gs_pen = float(data.default_data["gs_pen"])    # penetration
    data.gs_spd = float(data.default_data["gs_spd"])    # speed    data.os_dmg = float(data.default_data["os_dmg"])
    data.os_pen = float(data.default_data["os_pen"])
    data.os_spd = float(data.default_data["os_spd"])

    data.rs_dmg = float(data.default_data["rs_dmg"])
    data.rs_pen = float(data.default_data["rs_pen"])
    data.rs_spd = float(data.default_data["rs_spd"])

    data.wave =  int(data.default_data["wave"])
    data.score = int(data.default_data["score"])
    
    # Reset enemies
    data.enemies = []

def get_registration_data():
    """Zobrazí registračné okno pre zadanie mena a hesla"""
    root = tk.Tk()
    root.title("Registrácia nového účtu")
    root.geometry("420x320")
    root.resizable(False, False)
    
    root.eval('tk::PlaceWindow . center')

    player_name = tk.StringVar()
    password = tk.StringVar()
    confirm_password = tk.StringVar()
    result = {"success": False, "name": "", "password": "", "back_to_login": False}

    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 9))
    
    tk.Label(root, text="Vytvorenie nového účtu", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(root, text="Meno používateľa:", font=("Arial", 10)).pack(pady=5)
    name_entry = tk.Entry(root, textvariable=player_name, font=("Arial", 10), width=25)
    name_entry.pack(pady=5)
    
    tk.Label(root, text="Heslo:", font=("Arial", 10)).pack(pady=5)
    password_entry = tk.Entry(root, textvariable=password, show='*', font=("Arial", 10), width=25)
    password_entry.pack(pady=5)
    
    tk.Label(root, text="Potvrdiť heslo:", font=("Arial", 10)).pack(pady=5)
    confirm_entry = tk.Entry(root, textvariable=confirm_password, show='*', font=("Arial", 10), width=25)
    confirm_entry.pack(pady=5)
    
    def register():
        name = player_name.get().strip()
        pwd = password.get().strip()
        confirm_pwd = confirm_password.get().strip()
        
        if not name or not pwd or not confirm_pwd:
            messagebox.showerror("Chyba", "Všetky polia musia byť vyplnené!")
            return
        
        if pwd != confirm_pwd:
            messagebox.showerror("Chyba", "Heslá sa nezhodujú!")
            return
        
        if len(pwd) < 3:
            messagebox.showerror("Chyba", "Heslo musí mať aspoň 3 znaky!")
            return
        
        if sign_up(data.wave, data.score, name, pwd):
            result["success"] = True
            result["name"] = name
            result["password"] = pwd
            messagebox.showinfo("Úspech", "Registrácia bola úspešná!")
            root.destroy()
        else:
            messagebox.showerror("Chyba", "Registrácia zlyhala! Meno už existuje.")
    
    def back_to_login():
        result["back_to_login"] = True
        root.destroy()
        
    def cancel():
        root.destroy()

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    create_btn = tk.Button(button_frame, text="Vytvoriť účet", command=register, 
                          font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", 
                          width=15, height=2)
    create_btn.pack(pady=5)
    
    back_btn = tk.Button(button_frame, text="Späť na login", command=back_to_login,
                        font=("Arial", 10), bg="#2196F3", fg="white", 
                        width=15, height=1)
    back_btn.pack(pady=3)
    
    cancel_btn = tk.Button(button_frame, text="Zrušiť", command=cancel,
                          font=("Arial", 10), bg="#f44336", fg="white", 
                          width=15, height=1)
    cancel_btn.pack(pady=3)
    
    name_entry.focus()
    
    def on_enter(event):
        register()
    
    root.bind('<Return>', on_enter)
    
    root.mainloop()
    return result

def get_user_credentials():
    """Zobrazí prihlasovanie okno s možnosťou registrácie"""
    while True:
        root = tk.Tk()
        root.title("Prihlásenie")
        root.geometry("300x180")
        root.resizable(False, False)
        
        root.eval('tk::PlaceWindow . center')
        
        player_name = tk.StringVar()
        password = tk.StringVar()
        action_result = {"action": None, "name": "", "password": ""}

        tk.Label(root, text="Meno používateľa:", font=("Arial", 10)).pack(pady=5)
        name_entry = tk.Entry(root, textvariable=player_name, font=("Arial", 10), width=25)
        name_entry.pack(pady=5)
        
        tk.Label(root, text="Heslo:", font=("Arial", 10)).pack(pady=5)
        password_entry = tk.Entry(root, textvariable=password, show='*', font=("Arial", 10), width=25)
        password_entry.pack(pady=5)
        
        def login_action():
            name = player_name.get().strip()
            pwd = password.get().strip()
            
            if not name or not pwd:
                messagebox.showerror("Chyba", "Všetky polia musia byť vyplnené!")
                return
            
            action_result["action"] = "login"
            action_result["name"] = name
            action_result["password"] = pwd
            root.destroy()
        
        def signup_action():
            action_result["action"] = "signup"
            root.destroy()
        
        def cancel_action():
            action_result["action"] = "cancel"
            root.destroy()
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Prihlásiť", command=login_action,
                  font=("Arial", 10), bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Sign Up", command=signup_action,
                  font=("Arial", 10), bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Zrušiť", command=cancel_action,
                  font=("Arial", 10), bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=3)
        name_entry.focus()
        
        root.mainloop()
        
        if action_result["action"] == "cancel":
            return None, None
        elif action_result["action"] == "signup":
            reg_result = get_registration_data()
            if reg_result["success"]:
                return reg_result["name"], reg_result["password"]
            elif reg_result["back_to_login"]:
                continue
        elif action_result["action"] == "login":
            login_success = login(action_result["name"], action_result["password"])
            if login_success:
                return action_result["name"], action_result["password"]
            else:
                messagebox.showerror("Neplatné údaje", "Nesprávne meno alebo heslo. Skúste znova.")

def settings_json(settings):
    if not settings["player_name"] or not settings["password"]:
        player_name, password = get_user_credentials()
        if player_name and password:
            settings["player_name"] = player_name
            settings["password"] = password
            
            data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
            settings_file_path = os.path.join(data_path, 'settings.json')
            
            try:
                with open(settings_file_path, 'w', encoding = 'utf-8') as file:
                    json.dump(settings, file, indent = 4, ensure_ascii = False)
                print(f"Údaje boli úspešne uložené do {settings_file_path}")
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodarilo sa uložiť nastavenia: {e}")
        else:
            messagebox.showwarning("Upozornenie", "Neboli zadané platné prihlasovacie údaje!")
            
# Globálna premenná pre sledovanie stavu okna nastavení
settings_window_open = False

def open_settings_window():
    """Otvorí okno nastavení s možnosťou úpravy FOV, hlasitosti, fullscreen a server IP"""
    global settings_window_open
    
    if settings_window_open:
        return
    
    settings_window_open = True
    
    try:        # Vytvorenie hlavného okna
        root = tk.Tk()
        root.title("Nastavenia Hry")
        root.geometry("600x500")
        root.resizable(False, False)
        
        print("Settings window created successfully")
        
        # Centrovanie okna
        root.update_idletasks()
        width = root.winfo_width()
        height = root.winfo_height()
        x = (root.winfo_screenwidth() // 2) - (width // 2)
        y = (root.winfo_screenheight() // 2) - (height // 2)
        root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Načítanie aktuálnych nastavení
        with open(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'settings.json'), 'r') as f:
            current_settings = json.load(f)
        
        # Hlavný nadpis
        title_label = tk.Label(root, text="Nastavenia Hry", font=("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        # FOV Slider
        fov_frame = tk.Frame(root)
        fov_frame.pack(pady=10, padx=20, fill='x')
        
        fov_label = tk.Label(fov_frame, text="FOV (Field of View):", font=("Arial", 12))
        fov_label.pack(anchor='w')
        
        fov_var = tk.DoubleVar(value=current_settings.get("fov", 1.0))
        fov_value_label = tk.Label(fov_frame, text=f"Hodnota: {fov_var.get():.2f}", font=("Arial", 10))
        fov_value_label.pack(anchor='w')
        
        def update_fov_label(val):
            fov_value_label.config(text=f"Hodnota: {float(val):.2f}")
        
        fov_slider = tk.Scale(fov_frame, from_=0.1, to=5.0, resolution=0.1, orient='horizontal',
                             variable=fov_var, command=update_fov_label, length=400)
        fov_slider.pack(fill='x', pady=5)
        
        # Volume Slider
        volume_frame = tk.Frame(root)
        volume_frame.pack(pady=10, padx=20, fill='x')
        
        volume_label = tk.Label(volume_frame, text="Hlasitosť:", font=("Arial", 12))
        volume_label.pack(anchor='w')
        
        volume_var = tk.DoubleVar(value=current_settings.get("volume", 1.0))
        volume_value_label = tk.Label(volume_frame, text=f"Hodnota: {volume_var.get():.2f}", font=("Arial", 10))
        volume_value_label.pack(anchor='w')
        
        def update_volume_label(val):
            volume_value_label.config(text=f"Hodnota: {float(val):.2f}")
        
        volume_slider = tk.Scale(volume_frame, from_=0.01, to=5.0, resolution=0.01, orient='horizontal',
                                variable=volume_var, command=update_volume_label, length=400)
        volume_slider.pack(fill='x', pady=5)
        
        # Fullscreen Checkbox
        fullscreen_frame = tk.Frame(root)
        fullscreen_frame.pack(pady=10, padx=20, fill='x')
        
        fullscreen_var = tk.BooleanVar(value=current_settings.get("fullscreen", False))
        fullscreen_checkbox = tk.Checkbutton(fullscreen_frame, text="Fullscreen Mode", 
                                           variable=fullscreen_var, font=("Arial", 12))
        fullscreen_checkbox.pack(anchor='w')
          # Server IP Textbox
        ip_frame = tk.Frame(root)
        ip_frame.pack(pady=10, padx=20, fill='x')
        
        ip_label = tk.Label(ip_frame, text="Server IP Adresa:", font=("Arial", 12))
        ip_label.pack(anchor='w')
        
        ip_var = tk.StringVar(value=current_settings.get("server_ip_address", "localhost"))
        ip_entry = tk.Entry(ip_frame, textvariable=ip_var, font=("Arial", 11), width=50)
        ip_entry.pack(fill='x', pady=5)
        def apply_settings():
            """Aplikuje nastavenia bez zatvorenia okna"""
            print("Apply settings clicked!")
            try:
                # Aplikovanie zmien do data module
                data.fov = fov_var.get()
                print(f"Applied FOV: {fov_var.get()}")
                av_reload()  # Znovu načítanie s novou FOV hodnotou
                
                # Nastavenie novej hlasitosti pre zvuky
                volume_value = volume_var.get()
                print(f"Applied Volume: {volume_value}")
                if hasattr(data, 'calm_engine') and data.calm_engine:
                    data.calm_engine.set_volume(volume_value)
                if hasattr(data, 'active_engine') and data.active_engine:
                    data.active_engine.set_volume(volume_value / 2)
                if hasattr(data, 'menu_ambient') and data.menu_ambient:
                    data.menu_ambient.set_volume(volume_value / 3)
                
                messagebox.showinfo("Aplikované", "Nastavenia boli aplikované!")
                
            except Exception as e:
                print(f"Error in apply_settings: {e}")
                messagebox.showerror("Chyba", f"Nepodarilo sa aplikovať nastavenia: {e}")
        
        def save_settings():
            try:
                # Uloženie nových nastavení
                new_settings = current_settings.copy()
                new_settings["fov"] = fov_var.get()
                new_settings["volume"] = volume_var.get()
                new_settings["default_fullscreen"] = fullscreen_var.get()
                new_settings["server_ip_address"] = ip_var.get().strip()
                
                # Zápis do súboru
                settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'settings.json')
                with open(settings_path, 'w') as f:
                    json.dump(new_settings, f, indent=4)
                
                # Aplikovanie zmien
                data.settings = new_settings
                data.fov = new_settings["fov"]
                av_reload()  # Znovu načítanie s novou FOV hodnotou
                
                # Nastavenie novej hlasitosti pre zvuky
                if hasattr(data, 'calm_engine') and data.calm_engine:
                    data.calm_engine.set_volume(volume_var.get())
                if hasattr(data, 'active_engine') and data.active_engine:
                    data.active_engine.set_volume(volume_var.get() / 2)
                if hasattr(data, 'menu_ambient') and data.menu_ambient:
                    data.menu_ambient.set_volume(volume_var.get() / 3)
                
                messagebox.showinfo("Úspech", "Nastavenia boli úspešne uložené!")
                global settings_window_open
                settings_window_open = False
                root.destroy()
                
            except Exception as e:
                messagebox.showerror("Chyba", f"Nepodarilo sa uložiť nastavenia: {e}")
        
        def cancel_settings():
            global settings_window_open
            settings_window_open = False
            root.destroy()
          # Tlačidlá
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        print("Creating buttons...")
        
        apply_btn = tk.Button(button_frame, text="Aplikovať", command=apply_settings,
                             font=("Arial", 11), bg="#2196F3", fg="white", 
                             width=12, height=2)
        apply_btn.pack(side=tk.LEFT, padx=5)
        print("Apply button created")
        
        save_btn = tk.Button(button_frame, text="Uložiť", command=save_settings,
                            font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", 
                            width=12, height=2)
        save_btn.pack(side=tk.LEFT, padx=5)
        print("Save button created")
        
        cancel_btn = tk.Button(button_frame, text="Zrušiť", command=cancel_settings,
                              font=("Arial", 11), bg="#f44336", fg="white", 
                              width=12, height=2)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        print("Cancel button created")
        
        # Spustenie mainloop pre okno nastavení
        root.mainloop()
        
    except Exception as e:
        print(f"Chyba pri vytváraní okna nastavení: {e}")
        settings_window_open = False

def update_high_score(current_score):
    """Aktualizuje high-score v settings.json iba ak je current_score vyšší"""
    try:
        # Načítanie aktuálnych nastavení
        settings_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'settings.json')
        with open(settings_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        
        # Získanie aktuálneho high-score (ak neexistuje, nastaví sa na 0)
        current_high_score = settings.get("heigh-score", 0)
        
        # Aktualizácia iba ak je nové skóre vyšie
        if current_score > current_high_score:
            settings["heigh-score"] = current_score
            
            # Uloženie späť do súboru
            with open(settings_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4, ensure_ascii=False)
                
            print(f"Nový high-score: {current_score} (predchádzajúci: {current_high_score})")
            return True
        else:
            print(f"Skóre {current_score} nie je vyšie ako high-score {current_high_score}")
            return False
            
    except Exception as e:
        print(f"Chyba pri aktualizácii high-score: {e}")
        return False

