import pygame
from pygame.math import Vector2

MAX_FALL_VEOLICITY = 5


class PhysicsEntity:
    def __init__(self, game, e_type, pos, size):
        self.game = game
        self.e_type = e_type
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "right": False, "left": False}

        self.action = ""
        self.anim_offset = (-3, -3)
        self.flip = False
        self.set_action("idle")

        self.last_movement = [0, 0]

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[f"{self.e_type}/{self.action}"].copy()

    def update(self, tilemap, movement=None):
        self.collision = {"up": False, "down": False, "right": False, "left": False}

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
                    self.collision["down"] = True
                if fm_y < 0:
                    entity_rect.top = rect.bottom
                    self.collision["up"] = True

                self.pos[1] = entity_rect.y

        # This is not an if else as i don't want flip
        # the animation if the character is still
        if movement[0] > 0:
            self.flip = False
        elif movement[0] < 0:
            self.flip = True

        self.last_movement = movement

        self.velocity[1] = min(MAX_FALL_VEOLICITY, self.velocity[1] + 0.1)

        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0

        self.animation.update()

    def render(self, surf, offset=(0, 0)):
        # surf.blit(self.game.assets["player"], Vector2(self.pos) - Vector2(offset))
        surf.blit(
            pygame.transform.flip(self.animation.img(), self.flip, False),
            Vector2(self.pos) - Vector2(offset) + Vector2(self.anim_offset),
        )


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, "player", pos, size)
        self.air_time = 0
        self.jumps = 3
        self.wall_slide = False

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        self.air_time += 1
        if self.collision["down"]:
            self.air_time = 0
            self.jumps = 3

        self.wall_slide = False

        in_air = self.air_time > 4
        if in_air and self.collision["left"] or self.collision["right"]:
            self.wall_slide = True
            self.velocity[1] = min(self.velocity[1], 0.5)

            self.set_action("wall_slide")

        if not self.wall_slide:
            if in_air:
                self.set_action("jump")
            elif movement[0] != 0:
                self.set_action("run")
            else:
                self.set_action("idle")

        if self.velocity[0] > 0:
            self.velocity[0] = max(self.velocity[0] - 0.1, 0)
        else:
            self.velocity[0] = min(self.velocity[0] + 0.1, 0)

    def jump(self):
        if self.wall_slide:
            if self.last_movement[0] < 0:
                self.velocity[0] = 3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
            elif self.last_movement[0] > 0:
                self.velocity[0] = -3.5
                self.velocity[1] = -2.5
                self.air_time = 5
                self.jumps = max(0, self.jumps - 1)
                return True
        elif self.jumps:
            self.jumps -= 1
            self.velocity[1] = -3
            self.air_time = 5
            return True
