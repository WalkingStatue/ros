import pygame
import numpy as np
from src.grid import create_grid, place_obstacles, creates_maze
from src.agent import ObstacleType, place_survivors, place_agent
from ui.image_loader import load_images_grid

class Grid:
    def __init__(self, width, height, cell_size=70):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid = create_grid(height, width)
        self.images = load_images_grid()
        self.surface = self.create_surface()
        self.draw_grid()

    def create_surface(self):
        surface = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        surface.fill((220, 220, 220)) #Light Grey Background
        return surface

    def draw_grid(self):
        num_obstacles = 50
        num_survivors = 5
        place_obstacles(self.grid, num_obstacles)
        place_survivors(self.grid, num_survivors)
        place_agent(self.grid)
        creates_maze(self.grid, 0, 0)

        for row in range(self.height):
            for col in range(self.width):
                cell_value = self.grid[row, col]
                x = col * self.cell_size
                y = row * self.cell_size
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                if cell_value == 0:
                    pygame.draw.rect(self.surface, (100, 255, 100), rect) #Lighter Green
                elif cell_value == -1:
                    pygame.draw.rect(self.surface, (0, 50, 255), rect) #Darker Blue
                elif cell_value == 2:
                    pygame.draw.rect(self.surface, (255, 0, 0), rect) #Brighter Red
                elif cell_value == -2:
                    pygame.draw.rect(self.surface, (255, 255, 0), rect) #Yellow
                elif cell_value == ObstacleType.BUILDING.value:
                    self.draw_image(self.images["buildings"][0], x, y)
                elif cell_value == ObstacleType.RUBBLE.value:
                    self.draw_image(self.images["ruins"][0], x, y)
                elif cell_value == ObstacleType.FALLEN_TREE.value:
                    self.draw_image(self.images["trees"][0], x, y)
                else:
                    pygame.draw.rect(self.surface, (255, 255, 255), rect) #Default

                #Grid Overlay
                pygame.draw.rect(self.surface, (100,100,100), rect, 1)

    def draw_image(self, image, x, y):
        if image:
            self.surface.blit(image, (x, y))
        else:
            print("Warning: Image not loaded correctly.")
