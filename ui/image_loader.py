import pygame
import os

def load_images_grid(icon_size=70): #Function for grid images
    image_categories = {
        "buildings": os.path.join(os.path.dirname(__file__), 'images', 'buildings'),
        "ruins": os.path.join(os.path.dirname(__file__), 'images', 'ruins'),
        "trees": os.path.join(os.path.dirname(__file__), 'images', 'trees')
    }
    images = {}
    for category, dir_path in image_categories.items():
        category_images = []
        for filename in os.listdir(dir_path):
            if filename.endswith(".png"):
                img_path = os.path.join(dir_path, filename)
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (icon_size, icon_size))
                    category_images.append(img)
                except pygame.error as e:
                    print(f"Error loading image {img_path}: {e}")
        images[category] = category_images
    return images

def load_images_panel(icon_size=50): #Function for panel images
    image_categories = {
        "buildings": os.path.join(os.path.dirname(__file__), 'images', 'buildings'),
        "ruins": os.path.join(os.path.dirname(__file__), 'images', 'ruins'),
        "trees": os.path.join(os.path.dirname(__file__), 'images', 'trees')
    }
    images = {}
    for category, dir_path in image_categories.items():
        category_images = []
        for filename in os.listdir(dir_path):
            if filename.endswith(".png"):
                img_path = os.path.join(dir_path, filename)
                try:
                    img = pygame.image.load(img_path).convert_alpha()
                    img = pygame.transform.scale(img, (icon_size, icon_size))
                    category_images.append(img)
                except pygame.error as e:
                    print(f"Error loading image {img_path}: {e}")
        images[category] = category_images
    return images
