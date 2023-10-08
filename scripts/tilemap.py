import itertools
import json

import pygame
from pygame.math import Vector2

NEIGHBOR_OFFSETS = list(itertools.product([-1, 0, 1], repeat=2))
PHYSICS_TILES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tile_size=16):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}
        self.offgrid_tiles = []

    def tiles_around(self, pos):
        tiles = []
        tile_loc = (int(pos[0] // self.tile_size), int(pos[1] // self.tile_size))
        for offset in NEIGHBOR_OFFSETS:
            check_loc = (
                str(tile_loc[0] + offset[0]) + ";" + str(tile_loc[1] + offset[1])
            )
            if check_loc in self.tilemap:
                tiles.append(self.tilemap[check_loc])

        return tiles

    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile["type"] in PHYSICS_TILES:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tile_size,
                        tile["pos"][1] * self.tile_size,
                        self.tile_size,
                        self.tile_size,
                    )
                )

        return rects

    def render(self, surf, offset=(0, 0)):
        for off_tile in self.offgrid_tiles:
            surf.blit(
                self.game.assets[off_tile["type"]][off_tile["variant"]],
                (off_tile["pos"][0] - offset[0], off_tile["pos"][1] - offset[1]),
            )

        # Only render tiles within the screen
        for x in range(
            offset[0] // self.tile_size,
            (offset[0] + surf.get_width()) // self.tile_size + 1,
        ):
            for y in range(
                offset[1] // self.tile_size,
                (offset[1] + surf.get_height()) // self.tile_size + 1,
            ):
                loc = f"{x};{y}"
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surf.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        Vector2(tile["pos"]) * self.tile_size - Vector2(offset),
                    )

    def save(self, path):
        try:
            fout = open(path, "w")
            json.dump(
                {
                    "tilemap": self.tilemap,
                    "tile_size": self.tile_size,
                    "offgrid": self.offgrid_tiles,
                },
                fout,
                separators=(",", ":"),
            )
        finally:
            if fout:
                fout.close()

    def load(self, path):
        try:
            fin = open(path)
            map_data = json.load(fin)
        finally:
            if fin:
                fin.close()

        self.tilemap = map_data["tilemap"]
        self.tile_size = map_data["tile_size"]
        self.offgrid_tiles = map_data["offgrid"]
