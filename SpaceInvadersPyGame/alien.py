import pygame, random

class Alien(pygame.sprite.Sprite):

    """
    To intialize the alien sprite.

    param type: THe type of alien to create and image file to grab
    param x: The x coordinate in which used for the rect of the sprite
    param y: The y coordinate in which used for the rect of the sprite
    """
    def __init__(self, type, x, y):
        super().__init__()
        self.type = type
        path = f"Graphics/alien_{type}.png"
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect(topleft = (x, y))



    """
    How to update the movement of the alien

    param direction: Which way the alien would move on the x posistion
    """
    def update(self, direction):
        self.rect.x += direction


class MysteryShip(pygame.sprite.Sprite):

    """
    How to initalize the Mystery Ship with its movement speed and spawn position.

    param screen_width: Takes in the screen_width of the game to understand the boundry and spawn
    of the Mystery Ship.
    param offset: Also used to understand the boundry of the game for the spawning of the Mystery Ship.
    """
    def __init__(self, screen_width, offset):
        super().__init__()
        self.screen_width = screen_width
        self.offset = offset
        self.image = pygame.image.load("Graphics/mystery.png")

        x = random.choice([self.offset/2, self.screen_width - self.offset - self.image.get_width()])
        if x == self.offset/2:
            self.speed = 3
        else:
            self.speed = -3

        self.rect = self.image.get_rect(topleft = (x,90))



    """
    How to call for the movement of the Mystery Ship
    dependent on whether it spawned on the left side or right side.
    """
    def update(self):
        self.rect.x += self.speed
        if self.rect.right  > self.screen_width + self.offset/2:
            self.kill()
        elif self.rect.left < self.offset/2:
            self.kill()


