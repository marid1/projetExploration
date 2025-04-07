import random
import pygame as pg
from enemy import Enemy
from turret import Turret
from tile import Tile
from button import Button
import constants as c
from world import World

# Intitialize Pygame
pg.init()

# Create a clock object to control the frame rate
clock = pg.time.Clock()

# Create the game window
screen = pg.display.set_mode((c.SCREEN_WIDTH + c.SIDE_PANNEL, c.SCREEN_HEIGHT))
pg.display.set_caption("Tour de Défense")

# Game variables
level_started = False
last_enemy_spawn = pg.time.get_ticks()
placing_turrets = False
selected_turret = None
game_over = False
game_outcome = 0 # -1 is loss & 1 is win

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
start_button = pg.image.load("assets/images/start_button.png").convert_alpha()
restart_button = pg.image.load("assets/images/restart_button.png").convert_alpha()

# Load fonts for display text
text_font = pg.font.SysFont("Consolas", 24, bold = True)
large_font = pg.font.SysFont("Consolas", 36)

# Function for outputting text onto screenç
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# Create groups
enemy_group = pg.sprite.Group()
tile_group = pg.sprite.Group()
turret_group = pg.sprite.Group()

# Initialize world
world = World(grass_image, path_image, rock_image, c.GRID_WIDTH, c.GRID_HEIGHT, c.TILE_SIZE)
world.generate_map()
tile_group = world.tile_group
world.process_enemies()

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
                world.money -= c.BUY_COST
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

# Create buttons
turret_button = Button(c.SCREEN_WIDTH + 30, 120, add_turret_image, True)
cancel_button = Button(c.SCREEN_WIDTH + 30, 180, cancel_image, True)
upgrade_button = Button(c.SCREEN_WIDTH + 120, 120, upgrade_turret_image, True)
start_button = Button(c.SCREEN_WIDTH + 60, 300, start_button, True)
restart_button = Button(310, 300, restart_button, True)

# Game loop
run = True
while run:
    clock.tick(c.FPS)

    screen.fill("white")  # Clear the screen

    # Draw the grid
    tile_group.draw(screen)

    # Draw the waypoints
    pg.draw.lines(screen, "black", False, waypoints)

    if game_over == False:
        # Check if player lost
        if world.health <= 0:
            game_over = True
            game_outcome = -1 # Loss
        # Check if player won
        if world.level > c.TOTAL_LEVELS:
            game_over = True
            game_outcome = 1 # Loss
        # Update groups
        enemy_group.update(world)
        turret_group.update(enemy_group)

        # Highlight selected turret
        if selected_turret:
            selected_turret.selected = True

    # Draw groups
    enemy_group.draw(screen)
    for turret in turret_group:
        turret.draw(screen)

    draw_text("Vie " + str(world.health), text_font, "grey100", 0, 0)
    draw_text("Argent: " + str(world.money), text_font, "grey100", 0, 30)
    draw_text("Vague: " + str(world.level), text_font, "grey100", 0, 60)

    if game_over == False:
        # Check if level started
        if level_started == False:
            if start_button.draw(screen):
                level_started = True
        else:
            # Spawn enemies
            if pg.time.get_ticks() - last_enemy_spawn > c.SPAWN_COOLDOWN:
                if world.spawned_enemies < len(world.enemy_list):
                    enemy_type = world.enemy_list[world.spawned_enemies]
                    enemy = Enemy(enemy_type, waypoints, enemy_images)
                    enemy_group.add(enemy)
                    world.spawned_enemies += 1
                    last_enemy_spawn = pg.time.get_ticks()

        # Check if wave finished
        if world.check_level_complete():
            world.money += c.LEVEL_COMPLETE_REWARD
            world.level += 1
            level_started = False
            last_enemy_spawn = pg.time.get_ticks()
            world.reset_level()
            world.process_enemies()

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
                    if world.money >= c.UPGRADE_COST:
                        selected_turret.upgrade()
                        world.money -= c.UPGRADE_COST
    else:
        # GAME OVER!!!
        pg.draw.rect(screen, "dodgerblue", (200, 200, 400, 200), border_radius = 30)
        if game_outcome == -1:
            draw_text("GAME OVER", large_font, "grey0", 310, 230)
        elif game_outcome == 1:
            draw_text("GAGNÉ!", large_font, "grey0", 340, 230)
        if restart_button.draw(screen):
            game_over = False
            level_started = False
            placing_turrets = False
            selected_turret = None
            last_enemy_spawn = pg.time.get_ticks()
            world = World(grass_image, path_image, rock_image, c.GRID_WIDTH, c.GRID_HEIGHT, c.TILE_SIZE)
            world.generate_map()
            tile_group = world.tile_group
            world.process_enemies()

            # Empty groups
            enemy_group.empty()
            turret_group.empty()

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
                    # Check if enough money to buy
                    if world.money >= c.BUY_COST:
                        create_turret(mouse_pos)
                else:
                    selected_turret = select_turret(mouse_pos)

    # Update the display
    pg.display.flip()

pg.quit()
