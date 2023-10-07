import os
import sys

import pygame

from scripts.entities import PhysicsEntity
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images


class Game:
    def __init__(self, width: int = 640, height: int = 480):
        pygame.init()
        pygame.display.set_caption("Ninja game")
        self.screen = pygame.display.set_mode((width, height))
        self.display = pygame.Surface((width / 2, height / 2))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            "decor": load_images(os.path.join("tiles", "decor")),
            "large_decor": load_images(os.path.join("tiles", "large_decor")),
            "grass": load_images(os.path.join("tiles", "grass")),
            "stone": load_images(os.path.join("tiles", "stone")),
            "player": load_image(os.path.join("entities", "player.png")),
        }
        self.player = PhysicsEntity(self, "player", (50, 50), (8, 15))
        self.tilemap = Tilemap(self)

    def run(self):
        while True:
            self.display.fill((14, 219, 248))

            self.tilemap.render(self.display)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3
                    if (
                        event.key == pygame.K_c
                        and pygame.key.get_mods() & pygame.K_LCTRL
                    ):
                        pygame.quit()
                        sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False

            self.screen.blit(
                pygame.transform.scale(self.display, self.screen.get_size()), (0, 0)
            )
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Game().run()
