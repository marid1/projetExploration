import pygame as pg

class Tile(pg.sprite.Sprite):
    """Class representing a tile path in the game."""

    def __init__(self, image: pg.Surface, type: str, pos: tuple[int]) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
        
        self.blocked = False
        self.type = type

    def add_obstacles(self, obstacle_image: pg.Surface) -> None:
        """Add obstacles to the tile."""
        if not self.blocked:
            self.blocked = True
            # Create a new surface to combine the tile and obstacle
            new_image = self.image.copy()
            new_image.blit(obstacle_image, (0, 0))
            self.image = new_image
        
    def update(self):
        """Update the tile path."""
        pass  # No specific update logic for tile paths at the moment
