import pygame


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]

    def update(self, movement=None):
        if movement is None:
            movement = (0, 0)

        fm_x = movement[0] + self.velocity[0]
        fm_y = movement[1] + self.velocity[1]
        self.pos[0] += fm_x
        self.pos[1] += fm_y

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
