import pygame as pg
import math
from pygame.math import Vector2


class Enemy(pg.sprite.Sprite):
    """Class representing an enemy in the game."""

    def __init__(self, waypoints, image) -> None:
        pg.sprite.Sprite.__init__(self)
        self.waypoints = waypoints
        self.pos = Vector2(self.waypoints[0])
        self.target_waypoint = 1
        self.speed = 2
        self.angle = 0

        self.orinal_image = image
        self.image = pg.transform.rotate(self.orinal_image, self.angle)

        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self) -> None:
        """Update the enemy's position."""
        self.move()
        self.rotate()

    def move(self) -> None:
        """Move the enemy towards the target waypoint."""
        # Define a target waypoint
        if self.target_waypoint < len(self.waypoints):
            self.target = Vector2(self.waypoints[self.target_waypoint])
            self.movement = self.target - self.pos
        else:
            # Enemy has reached the end of the path
            self.kill()

        # Calculate distance to target
        dist = self.movement.length()
        # Check if remaining distance is greater than speed
        if dist >= self.speed:
            self.pos += self.movement.normalize() * self.speed
        else:
            if dist != 0:
                self.pos += self.movement.normalize() * dist
            self.target_waypoint += 1

    def rotate(self) -> None:
        """Rotate the enemy towards the target waypoint."""
        # Calculate the distance to the next waypoint
        dist = self.target - self.pos

        # Use the distance to calculate the angle
        self.angle = math.degrees(math.atan2(-dist[1], dist[0]))

        # Rotate the image and update the rect
        self.image = pg.transform.rotate(self.orinal_image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
