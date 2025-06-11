from functions import data
from functions.db.logic.account_logic import login, sign_up
import pygame, os, tkinter as tk, json
from tkinter import simpledialog, messagebox, ttk

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
    data.hull           =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))  # Podvozok hráča
    data.turret         =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[0]), (data.fov / 1))  # Veža hráča
    data.surface        =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[1]), (data.fov / 2))
    data.orange_shell   =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[2]), (data.fov / 25))
    data.red_shell      =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[3]), (data.fov / 25))
    data.green_shell    =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[4]), (data.fov / 25))
    data.shells         =       pygame.transform.scale_by(pygame.image.load(data.texture_loading_path[5]), (data.fov / 12.5))

    data.shot_sound =    pygame.mixer.Sound(data.sound_loading_path[0])
    data.realod_sound =  pygame.mixer.Sound(data.sound_loading_path[1])
    data.active_engine = pygame.mixer.Sound(data.sound_loading_path[2])
    data.calm_engine =   pygame.mixer.Sound(data.sound_loading_path[3])

    data.calm_engine.set_volume(0.5)    # %
    data.active_engine.set_volume(0.2)  # %

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
    
    # Centrovanie okna
    root.eval('tk::PlaceWindow . center')
    
    # Premenné pre vstupné polia
    player_name = tk.StringVar()
    password = tk.StringVar()
    confirm_password = tk.StringVar()
    result = {"success": False, "name": "", "password": "", "back_to_login": False}
    
    # Štýlovanie
    style = ttk.Style()
    style.configure("TLabel", font=("Arial", 10))
    style.configure("TButton", font=("Arial", 9))
    
    # Vytvorenie vstupných polí
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
        
        # Pokus o registráciu v databáze
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
      # Tlačidlá s lepším rozložením
    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)
    
    # Každé tlačidlo v vlastnom riadku pre lepšiu viditeľnosť
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
    
    # Focus na prvé pole
    name_entry.focus()
    
    # Bind Enter key to register
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
        
        # Centrovanie okna
        root.eval('tk::PlaceWindow . center')
        
        # Premenné
        player_name = tk.StringVar()
        password = tk.StringVar()
        action_result = {"action": None, "name": "", "password": ""}
        
        # Vstupné polia
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
        
        # Tlačidlá
        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)
        
        tk.Button(button_frame, text="Prihlásiť", command=login_action,
                  font=("Arial", 10), bg="#2196F3", fg="white", width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Sign Up", command=signup_action,
                  font=("Arial", 10), bg="#FF9800", fg="white", width=10).pack(side=tk.LEFT, padx=3)
        tk.Button(button_frame, text="Zrušiť", command=cancel_action,
                  font=("Arial", 10), bg="#f44336", fg="white", width=10).pack(side=tk.LEFT, padx=3)
          # Focus na prvé pole
        name_entry.focus()
        
        root.mainloop()
        
        if action_result["action"] == "cancel":
            return None, None
        elif action_result["action"] == "signup":
            # Otvorenie registračného okna
            reg_result = get_registration_data()
            if reg_result["success"]:
                return reg_result["name"], reg_result["password"]
            elif reg_result["back_to_login"]:
                # Používateľ sa chce vrátiť na login, pokračuj v slučke
                continue
            # Ak registrácia zlyhala alebo bola zrušená, pokračuj v slučke
        elif action_result["action"] == "login":
            # Overenie prihlásenia
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
        
    