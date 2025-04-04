import pygame as pg

class TilePath(pg.sprite.Sprite):
    """Class representing a tile path in the game."""

    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        """Update the tile path."""
        pass  # No specific update logic for tile paths at the moment
    
    
class TileGrass(pg.sprite.Sprite):
    """Class representing a tile grass in the game."""

    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)

    def update(self):
        """Update the tile grass."""
        pass  # No specific update logic for tile grass at the moment