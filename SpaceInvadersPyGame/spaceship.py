import pygame
from laser import Laser

class Spaceship(pygame.sprite.Sprite):

    """
    Initializes the Spaceship and position it at the bottom
    middle of the game.

    param screen_width: Takes the width for the game boundry to calculate
    position for Spaceship
    param screen_height: Takes the height for the game boundry to calculate
    position for Spaceship
    param offset: Takes the offset to combine with width or height to accurately
    position the Spaceship in the game boundry
    """
    def __init__(self, screen_width, screen_height, offset):
        super().__init__()
        self.offset = offset
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.image = pygame.image.load("Graphics/player.png")
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2,self.screen_height))
        self.speed = 5
        self.laser_color = (0, 200, 200)
        self.lasers_group = pygame.sprite.Group()
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 600
        self.laser_sound = pygame.mixer.Sound("Sound/shoot.wav")
        

    """
    Takes the key inputs to understand what the spaceship
    needs to do which is its movement and firing of the laser
    """
    def get_user_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            laser = Laser(self.rect.center, 5, self.screen_height, self.laser_color)
            self.lasers_group.add(laser)
            self.laser_time = pygame.time.get_ticks()
            self.laser_sound.play()

    """
    The main update function to be called by the loop.
    """
    def update(self):
        self.get_user_input()
        self.constraint_movement()
        self.lasers_group.update()
        self.recharge_laser()
     

    """
    To constrain the spaceship within the boundry
    of the game when it is moving using the screen_width
    and offset to indicate the left and right boundry.
    """
    def constraint_movement(self):
        if self.rect.right > self.screen_width:
            self.rect.right = self.screen_width

        if self.rect.left < self.offset:
            self.rect.left = self.offset


    """
    To add a delay of shooting the laser from the
    spaceship.
    """
    def recharge_laser(self):
        if not self.laser_ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_delay:
                self.laser_ready = True



    """
    To reset the position of the spaceship and remove any lasers fired
    when the game needs to reset.
    """
    def reset(self):
        self.rect = self.image.get_rect(midbottom = ((self.screen_width + self.offset)/2, self.screen_height))
        self.lasers_group.empty()


