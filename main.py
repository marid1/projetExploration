import random
import pygame as pg
from enemy import Enemy
import constants as c
from tile import TileGrass, TilePath

# Intitialize Pygame
pg.init()

# Create a clock object to control the frame rate
clock = pg.time.Clock()

# Create the game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tour de Défense")

# Load images
path_image = pg.image.load("assets/images/dirt_tile.png").convert_alpha()
grass_image = pg.image.load("assets/images/grass_tile.png").convert_alpha()
enemy_image = pg.image.load("assets/images/enemy.png").convert_alpha()

# Create groups
enemy_group = pg.sprite.Group()
tile_group = pg.sprite.Group()

# Generate random grid using TilePath and TileGrass
for row in range(c.GRID_HEIGHT):
    for col in range(c.GRID_WIDTH):
        tile_x = col * c.TILE_SIZE
        tile_y = row * c.TILE_SIZE
        if random.choice(["path", "grass"]) == "path":
            tile = TilePath(path_image, (tile_x, tile_y))
        else:
            tile = TileGrass(grass_image, (tile_x, tile_y))
        tile_group.add(tile)

waypoints = [(100, 100), (400, 200), (400, 100), (200, 300)]

enemy = Enemy(waypoints, enemy_image)
enemy_group.add(enemy)

# Generate random grid
grid = [[random.choice(["path", "grass"]) for _ in range(c.GRID_WIDTH)] for _ in range(c.GRID_HEIGHT)]


# Game loop
run = True
while run:
    clock.tick(c.FPS)

    screen.fill("white")  # Clear the screen

    # Draw the grid
    tile_group.draw(screen)
    
    # Draw the waypoints
    pg.draw.lines(screen, "black", False, waypoints)

    # Update groups
    enemy_group.update()

    # Draw groups
    enemy_group.draw(screen)

    # Event handler
    for event in pg.event.get():
        # Quit programe when window is closed
        if event.type == pg.QUIT:
            run = False

    # Update the display
    pg.display.flip()

pg.quit()
