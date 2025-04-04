import pygame as pg

import constants as c


class Turret(pg.sprite.Sprite):
    """Class representing a turret in the game."""

    def __init__(self, image: pg.Surface, tile_x: int, tile_y: int) -> None:
        pg.sprite.Sprite.__init__(self)
        self.tile_x = tile_x
        self.tile_y = tile_y

        # Calculate center coordinates based on tile position
        self.x = (tile_x + 0.5) * c.TILE_SIZE
        self.y = (tile_y + 0.5) * c.TILE_SIZE

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.range = 100  # Example range value for the turret
        self.damage = 10  # Example damage value for the turret
        self.fire_rate = 1  # Example fire rate (shots per second)
        self.last_shot_time = pg.time.get_ticks()  # Time of the last shot

    def update(self):
        """Update the turret's state."""
        pass  # No specific update logic for turrets at the moment
