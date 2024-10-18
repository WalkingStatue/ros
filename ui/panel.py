import pygame
import os
from ui.image_loader import load_images_panel

class ObstaclesPanel:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.surface = pygame.Surface((width, height))
        self.surface.fill((220, 220, 220))
        self.images = load_images_panel()
        self.draw_obstacles()

    def draw_obstacles(self):
        icon_size = 50
        icon_spacing = 10
        start_x = 10
        start_y = 10
        font = pygame.font.Font(None, int(self.height / 30))

        for category, images in self.images.items():
            title_text = font.render(category.capitalize(), True, (0, 0, 0))
            title_rect = title_text.get_rect(topleft=(start_x, start_y - 20))
            pygame.draw.rect(self.surface, (0, 0, 0), title_rect.inflate(10, 10), 2)
            self.surface.blit(title_text, title_rect)

            num_icons = len(images)
            cols = min(num_icons, 3)
            rows = (num_icons + cols - 1) // cols

            for i, img in enumerate(images):
                col = i % cols
                row = i // cols
                x = start_x + col * (icon_size + icon_spacing)
                y = start_y + row * (icon_size + icon_spacing)
                pygame.draw.rect(self.surface, (0, 0, 0), (x, y, icon_size, icon_size), 2)
                self.surface.blit(img, (x, y))
            start_y += (icon_size + icon_spacing) * rows + 40
