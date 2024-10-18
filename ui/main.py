import pygame
import os
from .panel import ObstaclesPanel
from .grid import Grid

pygame.init()

# Window dimensions
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Rescue Operation Simulator")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
light_blue = (173, 216, 230)


# Game objects
obstacles_panel = ObstaclesPanel(200, 800)
grid = Grid(20, 15, 20)

# Title screen
title_font = pygame.font.Font(None, 74)
title_text = title_font.render("Rescue Operation Simulator", True, white)
title_rect = title_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))

# Game loop variables
running = True
scroll_y = 0
scroll_speed = 5
show_title_screen = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and show_title_screen:
                show_title_screen = False
            if event.key == pygame.K_UP:
                scroll_y = max(scroll_y - scroll_speed, 0)
            if event.key == pygame.K_DOWN:
                max_scroll = max(0, obstacles_panel.height - screen_height)
                scroll_y = min(scroll_y + scroll_speed, max_scroll)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Mouse wheel up
                scroll_y = max(scroll_y - scroll_speed, 0)
            if event.button == 5:  # Mouse wheel down
                max_scroll = max(0, obstacles_panel.height - screen_height)
                scroll_y = min(scroll_y + scroll_speed, max_scroll)
        if event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Drawing
    screen.fill(light_blue) # Changed background color
    if show_title_screen:
        screen.blit(title_text, title_rect)
    else:
        screen.blit(obstacles_panel.surface, (0, -scroll_y))
        screen.blit(grid.surface, (obstacles_panel.width, -scroll_y))
    pygame.display.flip()
