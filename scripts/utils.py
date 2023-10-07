import os

import pygame

BASE_IMG_PAHT = os.path.join("data", "images")


def load_image(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PAHT, path)).convert()
    img.set_colorkey(pygame.Color("black"))
    return img
