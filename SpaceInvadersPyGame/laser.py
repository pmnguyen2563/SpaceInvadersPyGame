import pygame

class Laser(pygame.sprite.Sprite):

    """
    The initialization of a Laser to be used in game by
    the aliens or the player spaceship

    param position: Where it would come out, aka the player
    or the alien
    param speed: The speed of the laser where it would go up or down
    param screen_height: To take into account of when to destroy the laser
    if it hits the boundry of the game.
    param color: The color for the laser dependent on who is firing
    """
    def __init__(self,position, speed, screen_height, color):
        super().__init__()
        self.image = pygame.Surface((4,15))
        self.image.fill(color)
        self.rect = self.image.get_rect(center = position)
        self.speed = speed
        self.screen_height = screen_height


    """
    To update the position of the laser dependent on its speed
    and whether it has reached the boundry of the game to destroy
    it.
    """
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > self.screen_height + 15 or self.rect.y < 10:
            self.kill()

