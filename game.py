import math
import random
import os
import sys

import pygame

from scripts.clouds import Clouds
from scripts.entities import Player
from scripts.particles import Particle
from scripts.tilemap import Tilemap
from scripts.utils import load_image, load_images, Animation


class Game:
    def __init__(self, width: int = 640, height: int = 480):
        pygame.init()
        pygame.display.set_caption("Ninja game")
        self.screen = pygame.display.set_mode((width, height))
        self.display = pygame.Surface((width // 2, height // 2))

        self.clock = pygame.time.Clock()
        self.movement = [False, False]

        self.assets = {
            "decor": load_images(os.path.join("tiles", "decor")),
            "large_decor": load_images(os.path.join("tiles", "large_decor")),
            "grass": load_images(os.path.join("tiles", "grass")),
            "stone": load_images(os.path.join("tiles", "stone")),
            "player": load_image(os.path.join("entities", "player.png")),
            "background": load_image("background.png"),
            "clouds": load_images("clouds"),
            "player/idle": Animation(
                load_images(os.path.join("entities", "player", "idle")), img_dur=6
            ),
            "player/run": Animation(
                load_images(os.path.join("entities", "player", "run")), img_dur=4
            ),
            "player/jump": Animation(
                load_images(os.path.join("entities", "player", "jump"))
            ),
            "player/slide": Animation(
                load_images(os.path.join("entities", "player", "slide"))
            ),
            "player/wall_slide": Animation(
                load_images(os.path.join("entities", "player", "wall_slide"))
            ),
            "particle/leaf": Animation(
                load_images(os.path.join("particles", "leaf")), img_dur=20, loop=False
            ),
        }
        self.clouds = Clouds(self.assets["clouds"], count=16)
        self.player = Player(self, (50, 50), (8, 15))
        self.tilemap = Tilemap(self, tile_size=16)
        try:
            self.tilemap.load("map.json")
        except FileNotFoundError:
            raise

        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 2)], keep=True):
            self.leaf_spawners.append(
                pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13)
            )

        self.particles = []

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (
                self.player.rect().centerx
                - self.display.get_width() / 2
                - self.scroll[0]
            ) / 30

            self.scroll[1] += (
                self.player.rect().centery
                - self.display.get_height() / 2
                - self.scroll[1]
            ) / 30

            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (
                        rect.x + random.random() * rect.width,
                        rect.y + random.random() * rect.height,
                    )
                    self.particles.append(
                        Particle(
                            self,
                            "leaf",
                            pos,
                            velocity=[-0.1, 0.2],
                            frame=random.randint(0, 20),
                        )
                    )

            self.clouds.update()
            self.clouds.render(self.display, render_scroll)

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset=render_scroll)
                if particle.p_type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.jump()
                    if (
                        event.key == pygame.K_c
                        and pygame.key.get_mods() & pygame.K_LCTRL
                    ) or event.key == pygame.K_ESCAPE:
                        self.quit()
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

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run()
