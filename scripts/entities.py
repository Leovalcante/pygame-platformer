import pygame

MAX_FALL_VEOLICITY = 5


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"top": False, "bottom": False, "right": False, "left": False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=None):
        self.collision = {"top": False, "bottom": False, "right": False, "left": False}

        if movement is None:
            movement = (0, 0)

        fm_x = movement[0] + self.velocity[0]
        fm_y = movement[1] + self.velocity[1]
        self.pos[0] += fm_x
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if fm_x > 0:
                    entity_rect.right = rect.left
                    self.collision["right"] = True
                if fm_x < 0:
                    entity_rect.left = rect.right
                    self.collision["left"] = True

                self.pos[0] = entity_rect.x

        self.pos[1] += fm_y
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if entity_rect.colliderect(rect):
                if fm_y > 0:
                    entity_rect.bottom = rect.top
                    self.collision["bottom"] = True
                if fm_y < 0:
                    entity_rect.top = rect.bottom
                    self.collision["top"] = True

                self.pos[1] = entity_rect.y

        self.velocity[1] = min(MAX_FALL_VEOLICITY, self.velocity[1] + 0.1)

        if self.collision["bottom"] or self.collision["top"]:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets["player"], self.pos)
