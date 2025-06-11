import math
import pygame
import time
from functions import data

class Projectile:
    def __init__(self, x, y, angle, speed=10):
        self.x = x
        self.y = y
        self.angle = angle  # uhol v radiánoch
        self.speed = speed
        self.creation_time = time.time()
        self.lifetime = 20  # 20 sekúnd
        
    def update(self):
        # Pohyb strely v smere jej uhla
        self.x += math.cos(self.angle) * self.speed * data.fov
        self.y += math.sin(self.angle) * self.speed * data.fov
        
    def is_expired(self):
        return time.time() - self.creation_time > self.lifetime
        
    def draw(self, screen, camera_x, camera_y):
        # Vykreslenie strely relatívne k hráčovi
        screen_width, screen_height = screen.get_size()
        draw_x = self.x - camera_x + screen_width // 2
        draw_y = self.y - camera_y + screen_height // 2
        
        # Rotácia strely podľa jej uhla + 90 stupňov doprava
        rotated_shell = pygame.transform.rotate(data.red_shell, math.degrees(-self.angle) + 90)
        rotated_shell_rect = rotated_shell.get_rect(center=(draw_x, draw_y))
        screen.blit(rotated_shell, rotated_shell_rect.topleft)
    
    def get_rect(self):
        # Získanie obdĺžnika pre detekciu kolízií
        shell_size = 20
        return pygame.Rect(self.x - shell_size//2, self.y - shell_size//2, shell_size, shell_size)

class Enemy:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.target_distance = 500
        self.shooting = False
        self.cooldown = 0
        self.angle = 0  # uhol otočenia tanku
        self.size = 50  # veľkosť nepriateľa
        self.projectiles = []  # zoznam striel
        
    def update(self, player_pos):
        px, py = player_pos
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)
        
        # Výpočet uhla smerom k hráčovi
        self.angle = math.atan2(dy, dx)
        
        if distance > self.target_distance:
            # Pohyb smerom k hráčovi
            self.x += math.cos(self.angle) * self.speed * data.fov
            self.y += math.sin(self.angle) * self.speed * data.fov
        else:
            self.shooting = True
            self.shoot()
            
        # Aktualizácia striel
        self.update_projectiles()
        
    def shoot(self):
        if self.cooldown <= 0:
            # Vytvorenie novej strely
            projectile = Projectile(self.x, self.y, self.angle)
            self.projectiles.append(projectile)
            
            # Prehranie zvuku
            data.shot_sound.play()
            
            # Nastavenie cooldownu (480 frames = 2 sekundy pri 240 FPS)
            self.cooldown = 480
        else:
            self.cooldown -= 1
            
    def update_projectiles(self):        # Aktualizácia všetkých striel a odstránenie expirovaných
        self.projectiles = [proj for proj in self.projectiles if not proj.is_expired()]
        for projectile in self.projectiles:
            projectile.update()

    def draw(self, screen, camera_x, camera_y):
        screen_width, screen_height = screen.get_size()
        
        # Vykreslenie nepriateľa relatívne k hráčovi
        draw_x = self.x - camera_x + screen_width // 2
        draw_y = self.y - camera_y + screen_height // 2
        
        # Rotácia nepriateľa podľa uhla + 180 stupňov
        rotated_tank = pygame.transform.rotate(pygame.transform.scale_by(data.test_tank, 0.4), math.degrees(-self.angle) + 180)
        rotated_tank_rect = rotated_tank.get_rect(center=(draw_x, draw_y))
        screen.blit(rotated_tank, rotated_tank_rect.topleft)
        
        # Vykreslenie striel
        for projectile in self.projectiles:
            projectile.draw(screen, camera_x, camera_y)
    
    def get_rect(self):
        # Získanie obdĺžnika pre detekciu kolízií
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
    
    def check_collision_with_others(self, others):
        # Kontrola kolízie s ostatnými nepriateľmi
        my_rect = self.get_rect()
        for other in others:
            if other != self:
                other_rect = other.get_rect()
                if my_rect.colliderect(other_rect):
                    # Odtiahni sa od druhého nepriateľa
                    dx = self.x - other.x
                    dy = self.y - other.y
                    distance = math.hypot(dx, dy)
                    if distance > 0:
                        # Normalizuj vektor a posun sa o malú vzdialenosť
                        dx /= distance
                        dy /= distance
                        self.x += dx * 10
                        self.y += dy * 10

    def check_projectile_collision_with_player(self, player_x, player_y, player_size=40):
        # Kontrola kolízie striel s hráčom
        player_rect = pygame.Rect(player_x - player_size//2, player_y - player_size//2, player_size, player_size)
        hit_projectiles = []
        
        for projectile in self.projectiles:
            projectile_rect = projectile.get_rect()
            if player_rect.colliderect(projectile_rect):
                hit_projectiles.append(projectile)
        
        # Odstráň strely ktoré zasiahli hráča
        for projectile in hit_projectiles:
            self.projectiles.remove(projectile)
            
        return len(hit_projectiles)  # Počet zásahov