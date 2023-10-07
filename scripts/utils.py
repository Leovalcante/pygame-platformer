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


class Animation:
    def __init__(self, images, img_dur=5, loop=True) -> None:
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True

    def img(self):
        return self.images[int(self.frame / self.img_duration)]
