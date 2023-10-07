import os

import pygame

BASE_IMG_PAHT = os.path.join("data", "images")


def load_image(path):
    img = pygame.image.load(os.path.join(BASE_IMG_PAHT, path)).convert()
    img.set_colorkey(pygame.Color("black"))
    return img


def load_images(path):
    images = []
    for img_name in sorted(
        os.listdir(os.path.join(BASE_IMG_PAHT, path)),
        key=lambda el: int(el.split(".")[0]),
    ):
        images.append(load_image(os.path.join(path, img_name)))

    return images
