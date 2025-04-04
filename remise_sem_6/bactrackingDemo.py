import pygame
import sys
import random
from collections import deque

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tower Defense with Backtracking")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

font = pygame.font.Font(None, 36)

# Grid size
cell_size = 40
cols, rows = width // cell_size, height // cell_size

# Initialize grid (0: empty, 1: blocked)
grid = [[0 for _ in range(cols)] for _ in range(rows)]

# Represent the start and end points
start = (0, 0)
end = (cols - 1, rows - 1)

# Add some random obstacles
for _ in range(20):
    x, y = random.randint(1, cols - 2), random.randint(1, rows - 2)
    grid[y][x] = 1  # Mark the obstacle position as blocked

# Base position
base_x, base_y = 1, 1
grid[base_y][base_x] = 1  # Mark the base position as blocked

# Function to draw the grid
def draw_grid(player, enemies):
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            color = WHITE if grid[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLUE, rect, 2)    
        
    pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, width, height), 40) # Draw black border   
    pygame.draw.rect(screen, YELLOW, (base_x * cell_size, base_y * cell_size, cell_size, cell_size)) # Draw base
    
    for tower, x, y in player.towers:
        tower_rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, GREEN, tower_rect)
    
    for enemy in enemies:
        if enemy.alive:
            enemy.draw()

# Function to check if a move is valid
def is_valid_move(x, y):
    return 0 <= x < cols and 0 <= y < rows and grid[y][x] == 0  # Check bounds and no tower

# Tower Class
class Tower:
    def __init__(self, tower_type, cost, range, power, x=None, y=None):
        self.tower_type = tower_type  # e.g., "Basic", "Advanced", etc.
        self.cost = cost
        self.range = range # number of cells around (ex: 1, 2, 3)
        self.power = power
        self.x = x  # x coordinate of the tower's position on the grid
        self.y = y  # y coordinate of the tower's position on the grid
        self.projectiles = []

    def __repr__(self):
        return f"Tower({self.tower_type}, {self.cost}, {self.range}, {self.power})"

    def is_in_range(self, enemy):
        # Check if the enemy is within the tower's range
        if self.x is None or self.y is None:  # Ensure tower position is defined
            return False
        
        return (abs(enemy.x - self.x) <= self.range) and (abs(enemy.y - self.y) <= self.range)

towers = [
    Tower("Basic Tower", 30, 1 , 10),
    #Tower("Advanced Tower", 60, 2, 20),
    #Tower("Sniper Tower", 80, 3, 30)
]

class Enemy:
    def __init__(self, x, y, speed, color, damage):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.damage = damage
        self.alive = True

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x * cell_size, self.y * cell_size, cell_size, cell_size))

    def hit(self):
        self.alive = False

def generate_random_enemy():
    # Generate random position for enemy
    while True:
        x = random.randint(1, cols-2)  # Avoid base and edges
        y = random.randint(1, rows-2)
        if grid[y][x] == 0:  # Make sure the cell is not blocked
            grid[y][x] = 1
            return x, y

# Player Class
class Player:
    def __init__(self, resources):
        self.resources = resources
        self.towers = []  # List of towers placed by the player

    def can_afford_tower(self, tower):
        return self.resources >= tower.cost

    def place_tower(self, tower, x, y):
        if self.can_afford_tower(tower):
            if is_valid_move(x, y):  # Only place tower if the cell is valid
                self.resources -= tower.cost
                self.towers.append((tower, x, y))
                grid[y][x] = 1  # Block the cell after placing the tower
                return True
        return False

    def gain_resources(self, amount):
        self.resources += amount

def is_tower_in_range(tower, x, y, player):
    """
    Check if a tower is within the range of another tower.
    This checks the surrounding cells based on the tower's range.
    """
    for other_tower, tx, ty in player.towers:
        if tower != other_tower:  # Don't check the tower itself
            # Check all cells within the tower's range (all cells around it)
            for dx in range(-(tower.range + 1), tower.range + 2):
                for dy in range(-(tower.range + 1), tower.range + 2):
                    if 0 <= tx + dx < cols and 0 <= ty + dy < rows:  # Ensure within bounds
                        # Check if (x, y) is in the range of this tower
                        if (tx + dx == x) and (ty + dy == y):
                            return True  # There's another tower within range
    return False

def is_enemy_near_base(enemies, base_x, base_y, base_range=5):
    """
    Check if any enemy is near the base (within a defined range).
    """
    for enemy in enemies:
        if enemy.alive and abs(enemy.x - base_x) <= base_range and abs(enemy.y - base_y) <= base_range:
            # Check all cells within the base's range (all cells around it)
            for dx in range(-(base_range + 1), base_range + 2):
                for dy in range(-(base_range + 1), base_range + 2):
                    if 0 <= base_x + dx < cols and 0 <= base_y + dy < rows:  # Ensure within bounds
                        if (base_x + dx == x) and (base_y + dy == y):
                            return True  # There's an enemy near the base
    return False

# Backtracking to find best tower placement
def backtrack_tower_placement(tower, enemies, player):
    best_position = None
    max_enemy_damage = 0
    
    # First, check if there are enemies near the base to prioritize defense
    if is_enemy_near_base(enemies, base_x, base_y):
        print("Enemies near base! Prioritizing base defense.")
    
    for y in range(rows):
        for x in range(cols):
            if is_valid_move(x, y) and not is_tower_in_range(tower, x, y, player):
                tower.x, tower.y = x, y
                total_damage = 0
                
                # Calculate how many enemies this tower can hit
                for enemy in enemies:
                    if tower.is_in_range(enemy):
                        total_damage += 1  # Add 1 for each enemy within range
                
                # Prioritize tower placement closer to the base if there are enemies nearby
                if is_enemy_near_base(enemies, base_x, base_y) and (abs(x - base_x) + abs(y - base_y)) <= 3:
                    total_damage += 50  # Bonus damage for towers close to base
                
                # Keep track of the best position (max damage)
                if total_damage > max_enemy_damage:
                    max_enemy_damage = total_damage
                    best_position = (x, y)

    return best_position

def show_tower_popup(player):
    # Create pop-up background
    popup_rect = pygame.Rect(200, 150, 400, 300)
    pygame.draw.rect(screen, (50, 50, 50), popup_rect)  # Dark background
    pygame.draw.rect(screen, WHITE, popup_rect, 5)  # Border

    # Text to display
    popup_text = font.render("Choose a tower", True, WHITE)
    screen.blit(popup_text, (250, 160))

    # Display towers the player can afford
    y_offset = 200
    for tower in towers:
        if player.can_afford_tower(tower):
            tower_text = font.render(f"{tower.tower_type} - {tower.cost} resources", True, WHITE)
            screen.blit(tower_text, (220, y_offset))
            y_offset += 40

    # Display a close button
    close_button = pygame.Rect(500, 420, 100, 40)
    pygame.draw.rect(screen, (200, 0, 0), close_button)
    close_text = font.render("Place", True, WHITE)
    screen.blit(close_text, (510, 430))
    
    return close_button

# Main Game Loop with Automatic Mode
def main():
    player = Player(resources=20)
    popup_visible = False
    
    selected_type_tower = 0
    
    enemies = [Enemy(*generate_random_enemy(), 1, RED, 10) for _ in range(10)]
    last_resource_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill(BLACK)

        if player.resources >= min(tower.cost for tower in towers) and not popup_visible:
            popup_visible = True
            
        # Draw grid and towers
        draw_grid(player, enemies)

        for enemy in enemies:
            if enemy.alive:
                enemy.draw()

        current_time = pygame.time.get_ticks()
        if current_time - last_resource_time >= 10000:  # 10 seconds passed
            player.gain_resources(15)
            last_resource_time = current_time
            print(player.resources)            
            
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN and popup_visible:
                mouse_pos = pygame.mouse.get_pos()
                close_button = show_tower_popup(player)

                # Check if the player clicked the close button
                if close_button.collidepoint(mouse_pos):
                    print("close")
                    popup_visible = False
                    
                    selected_tower = Tower(
                        towers[selected_type_tower].tower_type,
                        towers[selected_type_tower].cost,
                        towers[selected_type_tower].range,
                        towers[selected_type_tower].power
                    )
                    
                    best_position = backtrack_tower_placement(selected_tower, enemies, player)
                    
                    if best_position:
                        player.place_tower(selected_tower, best_position[0], best_position[1])
                        print(f"Tower placed at {best_position}")

        resources_text = font.render(f"Resources: {player.resources}", True, WHITE)
        screen.blit(resources_text, (10, 10))
        
        if popup_visible:
            show_tower_popup(player)        
        
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Run the game
if __name__ == "__main__":
    main()
