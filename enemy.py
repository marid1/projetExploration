import pygame as pg

class Enemy(pg.sprite.Sprite):
    """Class representing an enemy in the game."""
    def __init__(self, pos, image):
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        
    def update(self):
        """Update the enemy's position."""
        self.move()
        
    def move(self):
        self.rect.x += 1