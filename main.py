import random
import pygame as pg
from enemy import Enemy
from turret import Turret
from tile import Tile
from button import Button
import constants as c

# Intitialize Pygame
pg.init()

# Create a clock object to control the frame rate
clock = pg.time.Clock()

# Create the game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANNEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tour de Défense")

# Game variables
placing_turrets = False
selected_turret = None

# Load images
path_image = pg.image.load("assets/images/dirt_tile.png").convert_alpha()
grass_image = pg.image.load("assets/images/grass_tile.png").convert_alpha()
# Enemies
enemy_images = {
    "weak": pg.image.load("assets/images/enemy_1.png").convert_alpha(),
    "medium": pg.image.load("assets/images/enemy_2.png").convert_alpha(),
    "strong": pg.image.load("assets/images/enemy_3.png").convert_alpha(),
    "elite": pg.image.load("assets/images/enemy_4.png").convert_alpha()
}
cursor_turret_image = pg.image.load("assets/images/cursor_turret.png").convert_alpha()
# Turret spritesheets
turret_spritesheets = []
for x in range(1, c.TURRET_LEVELS + 1):
    turret_sheet = pg.image.load(f'assets/images/base_turret_{x}.png').convert_alpha()
    turret_spritesheets.append(turret_sheet)
rock_image = pg.image.load("assets/images/small_rock.png").convert_alpha()
# Buttons images
add_turret_image = pg.image.load("assets/images/add_button.png").convert_alpha()
cancel_image = pg.image.load("assets/images/cancel_button.png").convert_alpha()
upgrade_turret_image = pg.image.load("assets/images/upgrade_turret_button.png").convert_alpha()

# Create groups
enemy_group = pg.sprite.Group()
tile_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Generate random grid using TilePath and TileGrass
for row in range(c.GRID_HEIGHT):
    for col in range(c.GRID_WIDTH):
        tile_x = col * c.TILE_SIZE
        tile_y = row * c.TILE_SIZE
        # Use weighted random choice for path and grass
        tile_type = random.choices(["path", "grass"], weights=[65, 35], k=1)[0]
        if tile_type == "path":
            tile = Tile(path_image, tile_type, (tile_x, tile_y))
        else:
            tile = Tile(grass_image, tile_type, (tile_x, tile_y))
            add_obstacle = random.choices([True, False], weights=[15, 85], k=1)[0]
            if add_obstacle:
                tile.add_obstacles(rock_image)
        tile_group.add(tile)


# Create a turret and add it to the turret group
def create_turret(mouse_pos) -> None:
    mouse_tile_X = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_Y = mouse_pos[1] // c.TILE_SIZE

    for tile in tile_group:
        # Check if the mouse position is within the tile's rect
        if tile.rect.collidepoint(mouse_pos):
            if not tile.blocked:
                turret = Turret(turret_spritesheets, mouse_tile_X, mouse_tile_Y)
                turret_group.add(turret)
                tile.blocked = True
            else:
                print("Cannot place turret here. Tile is blocked.")
            return

def select_turret(mouse_pos):
    mouse_tile_X = mouse_pos[0] // c.TILE_SIZE
    mouse_tile_Y = mouse_pos[1] // c.TILE_SIZE
    for turret in turret_group:
        if (mouse_tile_X, mouse_tile_Y) == (turret.tile_x, turret.tile_y):
            return turret

def clear_selection():
    for turret in turret_group:
        turret.selected = False

# Define waypoints for the enemy to follow
waypoints = [(100, 100), (400, 200), (400, 100), (200, 300)]

# Create an enemy and add it to the enemy group
enemy_type = "weak"
enemy = Enemy(enemy_type, waypoints, enemy_images)
enemy_group.add(enemy)

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, add_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 30, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 120, 120, upgrade_turret_image, True)

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
    turret_group.update(enemy_group)

    # Highlight selected turret
    if selected_turret:
        selected_turret.selected = True

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    # Draw buttons
    if turret_button.draw(screen):
        placing_turrets = True
        
    if placing_turrets:
        cursor_pos = pg.mouse.get_pos()
        cursor_rect = cursor_turret_image.get_rect(center=cursor_pos)
        if cursor_pos[0] <= c.SCREEN_WIDTH:
            screen.blit(cursor_turret_image, cursor_rect)
        if cancel_button.draw(screen):
            placing_turrets = False

    # If turret selected, show upgrade button
    if selected_turret:
        if selected_turret.upgrade_level < c.TURRET_LEVELS:
            if upgrade_button.draw(screen):
                selected_turret.upgrade()

    # Event handler
    for event in pg.event.get():
        # Quit program when window is closed
        if event.type == pg.QUIT:
            run = False
        # Check for mouse clicks to place turrets
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pg.mouse.get_pos()
            # Check if mouse is in grid bounds
            if mouse_pos[0] < c.SCREEN_WIDTH and mouse_pos[1] < c.SCREEN_HEIGHT:
                # Clear selected turrets
                selected_turret = None
                clear_selection()
                if placing_turrets:
                    create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    # Update the display
    pg.display.flip()

pg.quit()
