import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

class Game:
    """
    Initializes the game for the main file to run and update through.



    param screen_width: The width of the game window
    param screen_height:  The height of the game window
    param offset: The offset used in addition to the hieght and width for the full game window
    
    
    """
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.aliens_laser_color = (255, 165, 0)
        self.aliens_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.levels = 1
        self.run = True
        self.score = 0
        self.highscore = 0
        self.load_highscore()
        self.alien_explosion_sound = pygame.mixer.Sound("Sound/invaderkilled.wav")
        self.spaceship_explosion_sound = pygame.mixer.Sound("Sound/explosion.wav")
        pygame.mixer.music.load("Sound/bgm.wav")
        pygame.mixer.music.play(-1)


    """     
    Creates the obstacles and the gaps between them based
    on the size of the and obstacles using the offset and screen size to
    correctly place them in game.
    
    """
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles


    """ 
    Create the a 5 x 11 set of aliens for the game
    where we have 3 types of aliens to be created for the set
    
    """
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x =  75 + column * 55
                y = 110 + row * 55

                if row == 0:
                    alien_type = 3
                elif row in (1, 2):
                    alien_type = 2
                else:
                    alien_type = 1

                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)


    """
    How we move the aliens in the game 
    while keeping them in the constraint of the game space
    
    """
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)

        alien_sprites = self.aliens_group.sprites()
        for alien in alien_sprites:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)


    """
    A seperate function to move the group of aliens down
    for the alien movement function

    """
    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance



    """
    How we decide which alien to shoot the laser down
    towards the player

    """
    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height, self.aliens_laser_color)
            self.aliens_lasers_group.add(laser_sprite)



    """
    Function for the whenever it is called to create
    the mystery ship

    """
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))


    def check_for_collisions(self):
        #Spaceship laser collision
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:

                    self.alien_explosion_sound.play()

                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()

                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):

                    self.alien_explosion_sound.play()

                    self.score += 500
                    self.check_for_highscore()
                    laser_sprite.kill()

                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()

        #Alien laser collision
        if self.aliens_lasers_group:
            for alien_laser_sprite in self.aliens_lasers_group:
                if pygame.sprite.spritecollide(alien_laser_sprite, self.spaceship_group, False):
                    alien_laser_sprite.kill()
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over()

                for obstacle in self.obstacles:
                        if pygame.sprite.spritecollide(alien_laser_sprite, obstacle.blocks_group, True):
                            alien_laser_sprite.kill()

        #Collision for the aliens against the other sprites in game
        if self.aliens_group:
            for alien in self.aliens_group:

                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)

                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()


    """
    Function to play once game is ended in a loss of lives
    or aliens have touched the spaceship

    """
    def game_over(self):
        self.run = False
        self.spaceship_explosion_sound.play()
        print("Game Over")


    """
    To reset the game back to the start to play again
    if player decides to replay after their loss.
    Resets all the sprites and variables
    """
    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.aliens_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0


    """
    To check if the score is higher than the highscore 
    in which case, we update the high score to the newest score
    and write it to a file.
    """
    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score

            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))


    """
    To load a text file that has the high score from
    a previous session if there was one.

    """
    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0


    """
    To start the next level in the game once all
    the aliens are defeated. Recreates the alien group
    and increase the level count.
    """
    def next_level(self):
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.aliens_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.levels += 1