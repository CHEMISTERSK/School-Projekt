import math
import pygame

class Enemy:
    def __init__(self, x, y, speed=2):
        self.x = x
        self.y = y
        self.speed = speed
        self.target_distance = 500
        self.shooting = False
        self.size = 40  # veľkosť nepriateľa
        self.cooldown = 0  # cooldown

    def update(self, player_pos):
        px, py = player_pos
        dx = px - self.x
        dy = py - self.y
        distance = math.hypot(dx, dy)

        if distance > self.target_distance:
            # Pohyb smerom k hráčovi
            angle = math.atan2(dy, dx)
            self.x += math.cos(angle) * self.speed
            self.y += math.sin(angle) * self.speed
        else:
            self.shooting = True
            self.shoot(player_pos)

    def shoot(self, player_pos):
        if self.cooldown == 0:
            print(f"Nepriateľ na ({int(self.x)}, {int(self.y)}) strieľa na hráča na {player_pos}!")
            self.cooldown = 60  # Cooldown na 1 sekundu (pri 60 FPS)
        else:
            self.cooldown -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.size, self.size))