import math
import pygame
import time
from functions import data

class PlayerProjectile:
    def __init__(self, x, y, angle, speed=10):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = speed
        self.creation_time = time.time()
        self.lifetime = 20
        self.size = 8
        
    def update(self):
        # Use standard math coordinates - angle is calculated from tank to mouse cursor
        self.x += math.cos(self.angle) * self.speed * data.fov
        self.y += math.sin(self.angle) * self.speed * data.fov
        
    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime
        
    def draw(self, screen, camera_x, camera_y):
        screen_width, screen_height = screen.get_size()
        draw_x = self.x - camera_x + screen_width // 2
        draw_y = self.y - camera_y + screen_height // 2
        
        pygame.draw.circle(screen, (255, 255, 0), (int(draw_x), int(draw_y)), self.size)
        
    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

class PlayerShooting:
    def __init__(self):
        self.projectiles = []
        self.last_shot_time = 0
        self.cooldown = 3000
        self.reload_sound_played = False
        
    def shoot(self, tank_x, tank_y, mouse_x, mouse_y, mouse_clicked):
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_shot_time >= self.cooldown:
            if mouse_clicked:
                # Calculate angle from tank position to mouse cursor
                # Tank is always at the center of the screen
                screen_width, screen_height = pygame.display.get_surface().get_size()
                tank_screen_x = screen_width // 2
                tank_screen_y = screen_height // 2
                
                # Calculate direction from tank to mouse cursor
                dx = mouse_x - tank_screen_x
                dy = mouse_y - tank_screen_y
                angle_radians = math.atan2(dy, dx)
                
                new_projectile = PlayerProjectile(tank_x, tank_y, angle_radians)
                self.projectiles.append(new_projectile)
                data.shot_sound.play()
                self.last_shot_time = current_time
                self.reload_sound_played = False
                
        elif current_time - self.last_shot_time >= self.cooldown - 100 and not self.reload_sound_played:
            data.reload_sound.play()
            self.reload_sound_played = True
            
    def update_projectiles(self):
        for projectile in self.projectiles[:]:
            projectile.update()
            if projectile.is_expired():
                self.projectiles.remove(projectile)
                
    def check_enemy_collisions(self, enemies):
        hits = 0
        for projectile in self.projectiles[:]:
            projectile_rect = projectile.get_rect()
            for enemy in enemies[:]:
                enemy_rect = enemy.get_rect()
                if projectile_rect.colliderect(enemy_rect):
                    self.projectiles.remove(projectile)
                    enemies.remove(enemy)
                    hits += 1
                    break
        if hits > 0:
            data.score += hits * 100
        return hits
        
    def draw_projectiles(self, screen, camera_x, camera_y):
        for projectile in self.projectiles:
            projectile.draw(screen, camera_x, camera_y)
            
    def get_cooldown_progress(self):
        current_time = pygame.time.get_ticks()
        time_since_shot = current_time - self.last_shot_time
        if time_since_shot >= self.cooldown:
            return 1.0
        else:
            return time_since_shot / self.cooldown

player_shooting = PlayerShooting()
