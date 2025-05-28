from functions import data
import pygame

def generation_4(screen):
    block_size = 1024 * data.fov / 2
    screen_width, screen_height = screen.get_size()
    
    tank_block_x = data.tank_x // block_size
    tank_block_y = data.tank_y // block_size

    blocks_x = (screen_width // block_size) + 2
    blocks_y = (screen_height // block_size) + 2

    start_x = int(tank_block_x - blocks_x // 2)
    end_x = int(tank_block_x + blocks_x // 2)
    start_y = int(tank_block_y - blocks_y // 2)
    end_y = int(tank_block_y + blocks_y // 2)

    for j in range(start_x, end_x + 1):
        for k in range(start_y, end_y + 1):
            pos_x = j * block_size
            pos_y = k * block_size

            draw_x = pos_x - data.tank_x + screen_width // 2
            draw_y = pos_y - data.tank_y + screen_height // 2
            screen.blit(data.surface, (draw_x, draw_y))