import pygame as pg
from enemy import Enemy
import constants as c

# Intitialize Pygame
pg.init()

# Create a clock object to control the frame rate
clock = pg.time.Clock()

# Create the game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
pg.display.set_caption("Tour de Défense")

# Load images
enemy_image = pg.image.load("assets/images/enemy.png").convert_alpha()

# Create groups
enemy_group = pg.sprite.Group()

enemy = Enemy((200,300), enemy_image)
enemy_group.add(enemy)

# Game loop
run = True
while run:
    clock.tick(c.FPS)
    
    screen.fill("white")  # Clear the screen
    
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