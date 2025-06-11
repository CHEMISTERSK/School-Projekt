# Importing External Functions
import pygame, sys, time as t, os, random as r, datetime, math, threading
from pygame.locals import *

# Importing Internal Functions
from functions.error_handling import error_window
from functions.logging import *
from functions.db.db import get_connection
from functions.console import console
from functions.func import *
from functions import data
from functions.save import *
from functions.db.logic.account_logic import *
from functions.db.logic.saveing_logic import *

# Importing Mechanics
from mechanics import generation as gen
from mechanics.menu import *
from mechanics.enemy import Enemy
from mechanics.player_shooting import *


# Game Initialization
pygame.init()
pygame.mixer.init()
pygame.display.set_caption("SP")

# Initialize player shooting after pygame init
player_shooting = PlayerShooting()

resolution = pygame.display.Info()
full_res_x = resolution.current_w
full_res_y = resolution.current_h

screen = pygame.display.set_mode((full_res_x, full_res_y * 0.93))

epoch = t.time()
last_log = int(epoch)

clock = pygame.time.Clock()

real_time = datetime.datetime.now().strftime("%H:%M:%S")

log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')

font_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fonts', 'impact.ttf')
font = pygame.font.Font(font_path, 15)

last_fps_log = int(epoch)
fps_text = f"FPS: "
text_surface = font.render(fps_text, True, (255, 255, 255))

d_x = full_res_x * 0.5
d_y = full_res_y * 0.5

# Functions Calling
res_xy = screen_resolution(full_res_x, full_res_y, data.fullscreen)
main_log_clear()
connection = get_connection()
main_log(real_time, resolution, res_xy[0], res_xy[1], clock, pygame.time.get_ticks(), epoch, data.db, connection)
fullscreen_toggle(full_res_x, full_res_y)
settings_json(data.settings)

try:
    # Main Loop
    while data.running:

        # Screen Resolution
        screen.fill((0, 0, 0))

        real_time = datetime.datetime.now().strftime("%H:%M:%S")
        epoch = t.time()
        keys = pygame.key.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_clicked = False

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                os.remove(os.path.join(log_dir, "temp.log"))
                data.running = False

            # Mouse click detection
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_clicked = True

        # Key Binding
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    data.time_data = ingame_time(True)
                    data.playing = False

                # Save Game
                elif event.key == pygame.K_F5:
                    cloud_save(data.settings["player_name"])
                    saveing()

                # Switching Between Fullscreen And Windowed Mode
                elif event.key == pygame.K_F11:
                    fullscreen_toggle(full_res_x, full_res_y)

                # Console
                elif event.key == pygame.K_F12:
                    threading.Thread(target = console, daemon = True).start()
          #   Menu Buttons
        if data.playing == False:
            play_button(mouse_x, mouse_y, full_res_x, full_res_y, mouse_clicked)
            continue_button(mouse_x, mouse_y, full_res_x, full_res_y, mouse_clicked)
            settings_button(mouse_x, mouse_y, full_res_x, full_res_y, mouse_clicked)
            exit_button(mouse_x, mouse_y, full_res_x, full_res_y, mouse_clicked)

        elif data.playing == True:
            gen.generation(screen)
            data.menu_ambient.stop()

            # Game Loop
            current_time = pygame.time.get_ticks()

            # Movement Logic
            if keys[pygame.K_a]:
                data.tank_angle += data.tank_rotation_speed

            elif keys[pygame.K_d]:
                data.tank_angle -= data.tank_rotation_speed

            if data.tank_angle > 360:
                data.tank_angle -= 360

            if data.tank_angle < 0:
                data.tank_angle += 360

            angle_radians = math.radians(data.tank_angle)

            if keys[pygame.K_w]:
                data.tank_x -= (data.tank_speed * math.sin(angle_radians)) * data.fov
                data.tank_y -= (data.tank_speed * math.cos(angle_radians)) * data.fov

            elif keys[pygame.K_s]:
                data.tank_x += (data.tank_speed * math.sin(angle_radians)) * data.fov
                data.tank_y += (data.tank_speed * math.cos(angle_radians)) * data.fov
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Calculate angle from turret center to mouse cursor
            dx = mouse_x - d_x
            dy = mouse_y - (d_y + 10)
            # Try different angle calculation
            data.turret_angle = -math.degrees(math.atan2(dy, dx)) + 90
            
            # Normalize angle to 0-360 degrees
            while data.turret_angle < 0:
                data.turret_angle += 360
            while data.turret_angle >= 360:
                data.turret_angle -= 360

            # Engine Sounds
            if (keys[pygame.K_s] or keys[pygame.K_w]) or (keys[pygame.K_a] or keys[pygame.K_d]):
                if data.active_engine.get_num_channels() == 0:
                    data.active_engine.play()
                data.calm_engine.stop()

            else:
                if data.calm_engine.get_num_channels() == 0:
                    data.calm_engine.play()
                data.active_engine.stop()            
            # Render hull (follows tank movement)
            rotated_hull = pygame.transform.rotate(pygame.transform.scale_by(data.hull, 0.5), data.tank_angle)
            rotated_hull_rect = rotated_hull.get_rect(center = (d_x, d_y))
            screen.blit(rotated_hull, rotated_hull_rect.topleft)            
            turret_center_x = d_x
            turret_center_y = d_y
            
            # Scale and rotate turret
            scaled_turret = pygame.transform.scale_by(data.turret, 0.5)
            rotated_turret = pygame.transform.rotate(scaled_turret, data.turret_angle)
            
            # Center the rotated turret on the desired position
            turret_rect = rotated_turret.get_rect(center=(turret_center_x, turret_center_y))
            screen.blit(rotated_turret, turret_rect)
            
            # Enemy Logic
            # Enemies spawn every 5 seconds if there are less than 5 enemies
            if len(data.enemies) < 5 and current_time % 5000 < 16:  # 16ms tolerance for 240fps
                # Spawn enemy around the player
                spawn_distance = 1000
                attempts = 0
                while attempts < 10:  # Max 10 attempts to spawn an enemy
                    angle = r.uniform(0, 2 * math.pi)
                    enemy_x = data.tank_x + math.cos(angle) * spawn_distance
                    enemy_y = data.tank_y + math.sin(angle) * spawn_distance
                    new_enemy = Enemy(enemy_x, enemy_y, speed = 2)
                    # check for collision with existing enemies
                    collision = False
                    for existing_enemy in data.enemies:
                        if math.hypot(new_enemy.x - existing_enemy.x, new_enemy.y - existing_enemy.y) < (100 * data.fov):
                            collision = True
                            break
                    
                    if not collision:
                        data.enemies.append(new_enemy)
                        break
                    attempts += 1
                    
            # actualization of enemies
            player_pos = (data.tank_x, data.tank_y)
            total_hits = 0
            
            # Player shooting mechanics            
            player_shooting.shoot(data.tank_x, data.tank_y, mouse_x, mouse_y, mouse_clicked)
            player_shooting.update_projectiles()
            killed_enemies = player_shooting.check_enemy_collisions(data.enemies)
            
            for enemy in data.enemies:
                # actualization of enemies
                enemy.update(player_pos)
                
                # check for collision with other enemies
                enemy.check_collision_with_others(data.enemies)
                
                # check for collision of shot with player
                hits = enemy.check_projectile_collision_with_player(data.tank_x, data.tank_y)
                total_hits += hits
                
                # draw enemy
                enemy.draw(screen, data.tank_x, data.tank_y)            # Draw player projectiles
            player_shooting.draw_projectiles(screen, data.tank_x, data.tank_y)
            
            # damage to player
            if total_hits > 0:
                damage = total_hits * 13
                data.tank_hp -= damage
                if data.tank_hp < 0:
                    data.tank_hp = 0
            
        # Top Info Bar
            if int(epoch) - last_log == 240:
                last_log = int(epoch)
                data.db, connection = get_connection()
                main_log(real_time, resolution, res_xy[0], res_xy[1], clock, current_time, epoch, data.db, connection)

            pygame.draw.rect(screen, (0, 0, 0), (0, 0, res_xy[0], 35), 100)

            if not data.db:
                screen.blit(font.render("No Connection To The Server", True, (219, 17, 4)), (full_res_x * 0.0651, full_res_y * 0.0087))
            else:
                screen.blit(font.render("Connected To The Server", True, (5, 199, 2)), (full_res_x * 0.0651, full_res_y * 0.0087))

            screen.blit(font.render(f"Score: {data.score}", True, (226, 226, 10)), (full_res_x * 0.9309, full_res_y * 0.0087))
            screen.blit(font.render(f"Wave:  {data.wave}" , True, (226, 226, 10)), (full_res_x * 0.8789, full_res_y * 0.0087))
            screen.blit(font.render(f"HP:  {int((data.tank_hp / data.max_tank_hp)*100)}%", True, (219, 17, 4)), (full_res_x * 0.6510, full_res_y * 0.0087))            # Weapon cooldown indicator
            cooldown_progress = player_shooting.get_cooldown_progress()
            if cooldown_progress < 1.0:
                cooldown_text = f"Reloading... {int((1.0 - cooldown_progress) * 100)}%"
                screen.blit(font.render(cooldown_text, True, (255, 100, 100)), (full_res_x * 0.5500, full_res_y * 0.0087))
            else:
                screen.blit(font.render("Ready to fire!", True, (100, 255, 100)), (full_res_x * 0.5500, full_res_y * 0.0087))
        
        screen.blit(font.render(f"{ingame_time(False)}", True, (255, 255, 255)), (full_res_x * 0.4883, full_res_y * 0.0087))

        if data.playing == False:
            menu_buttons(full_res_x, screen)
            if data.menu_ambient.get_num_channels() == 0:
                    data.menu_ambient.play()
            data.calm_engine.stop()
            data.active_engine.stop()

        # development tool
        #screen.blit(pygame.transform.scale_by(pygame.image.load("files\\textures\\red_dot.png"), 0.25), (900, 650))        

        # # FPS Counter
        if int(epoch) - last_fps_log >= 1:
            last_fps_log = int(epoch)
            data.fps = clock.get_fps()
            fps_text = f"FPS: {int(data.fps)}"
            # Používame už definovaný font namiesto vytvárania nového
            text_surface = font.render(fps_text, True, (255, 255, 255))
        screen.blit(text_surface, (full_res_x * 0.0065, full_res_y * 0.0087))

        pygame.display.update()
        clock.tick(240)

    pygame.quit()
    sys.exit()

# Error Handling
except Exception as e:
    error_window(e, "Main.py")
    os.remove(os.path.join(log_dir, "temp.log"))
    pygame.quit()
    sys.exit()