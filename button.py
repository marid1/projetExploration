import pygame as pg


class Button():
    def __init__(self, x: int, y: int, image: pg.Surface, single_click: bool) -> None:
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.clicked = False
        self.single_click = single_click
        
    def draw(self, surface: pg.Surface) -> bool:
        """Draw the button and check for click events."""
        action = False
        # Get the mouse position
        pos = pg.mouse.get_pos()
        
        # Check mouse hover
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                # If the buttons is type single_click, set clicked to True
                if self.single_click:
                    self.clicked = True
                
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False    
        
        # Draw button
        surface.blit(self.image, self.rect)
        
        return action