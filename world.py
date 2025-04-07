import pygame as pg
import random
from tile import Tile
from enemy_data import ENEMY_SPAWN_DATA

class World:
    def __init__(self, grass_img, path_img, rock_img, grid_width, grid_height, tile_size):
        self.grass_img = grass_img
        self.path_img = path_img
        self.rock_img = rock_img
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.tile_size = tile_size
        self.tile_group = pg.sprite.Group()
        self.waypoints = []

        self.level = 1
        self.enemy_list = []
        self.spawned_enemies = 0

    def generate_map(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                x = col * self.tile_size
                y = row * self.tile_size
                tile_type = random.choices(["path", "grass"], weights=[65, 35])[0]

                if tile_type == "path":
                    tile = Tile(self.path_img, tile_type, (x, y))
                else:
                    tile = Tile(self.grass_img, tile_type, (x, y))
                    if random.choices([True, False], weights=[15, 85])[0]:
                        tile.add_obstacles(self.rock_img)
                self.tile_group.add(tile)

    def process_enemies(self):
        enemies = ENEMY_SPAWN_DATA[self.level - 1]
        for enemy_type in enemies:
            enemies_to_spawn = enemies[enemy_type]
            for enemy in range(enemies_to_spawn):
                self.enemy_list.append(enemy_type)

        # Randomize list of enemies
        random.shuffle(self.enemy_list)

    def draw(self, surface):
        self.tile_group.draw(surface)
