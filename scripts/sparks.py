import math

import pygame


class Spark:
    def __init__(self, pos, angle, speed) -> None:
        self.pos = list(pos)
        self.angle = angle
        self.speed = speed

    def update(self):
        self.pos[0] += math.cos(self.angle) * self.speed
        self.pos[1] += math.sin(self.angle) * self.speed

        self.speed = max(0, self.speed - 0.1)

        return not self.speed

    def render(self, surf: pygame.Surface, offset=None):
        if offset is None:
            offset = (0, 0)
        render_points = [
            (
                self.pos[0] + math.cos(self.angle) * self.speed * 3 - offset[0],
                self.pos[1] + math.sin(self.angle) * self.speed * 3 - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle + math.pi / 2) * self.speed * 0.5
                - offset[0],
                self.pos[1]
                + math.sin(self.angle + math.pi / 2) * self.speed * 0.5
                - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle + math.pi) * self.speed * 3
                - offset[0],
                self.pos[1]
                + math.sin(self.angle + math.pi) * self.speed * 3
                - offset[1],
            ),
            (
                self.pos[0]
                + math.cos(self.angle - math.pi / 2) * self.speed * 0.5
                - offset[0],
                self.pos[1]
                + math.sin(self.angle - math.pi / 2) * self.speed * 0.5
                - offset[1],
            ),
        ]
        pygame.draw.polygon(surf, pygame.Color("white"), render_points)
