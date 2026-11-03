import pygame, sys, random
from game import Game

pygame.init()

#SCREEN SIZE WITH OFFSET FOR UI
SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

#COLOR
GREY = (29, 29, 27)
YELLOW = (243, 216 ,63)


#UI variables
font = pygame.font.Font("Font/monogram.ttf", 40)
level_surface = font.render("LEVEL ", False, YELLOW)
game_over_surface = font.render("GAME OVER", False, YELLOW)
restart_surface = font.render("PRESS R TO RESTART", False, YELLOW)
score_text_surface = font.render("SCORE", False, YELLOW)
highscore_text_surface = font.render("HIGH SCORE", False ,YELLOW)

#Set up Game window
screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Python Space Invaders")

#Set game frame rate
clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

#DELAY FOR ALIEN'S LASER
SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 500)


#TIMER FOR MYSTERY SHIP APPEARANCE
MYSTERY_SHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERY_SHIP, random.randint(4000, 8000))


#GAME LOOP
while True:
    for event in pygame.event.get():
        #CHECK FOR CLOSING OF APPLICATION
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #CHECK TO SEE IF ALIEN LASER IS AVAILABLE TO SHOOT AND IF GAME IS STILL RUNNING
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        #CHECK TO SEE IF MYSTERY SHIP CAN BE SPAWNED AND GAME IS RUNNING
        if event.type == MYSTERY_SHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERY_SHIP,random.randint(4000, 8000))

        #CHECK IF THE BUTTON TO RESET IS PRESSED AFTER GAME OVER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r] and not game.run:
            game.reset()


    #Update player, aliens, lasers, mystery ship while game is not over
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.aliens_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    #CHECK IF LEVEL IS DEFEATED BEFORE RESETTING FOR NEXT LEVEL
    if not game.aliens_group and not game.mystery_ship_group and game.run:
        game.next_level()

    #Drawing
    screen.fill(GREY)

    #UI
    pygame.draw.rect(screen, YELLOW, (10, 10, 780, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, YELLOW, (25, 730), (775, 730), 3)

    if game.run:
        screen.blit(level_surface, (570, 740 , 50, 50))
        formatted_level = str(game.levels).zfill(2)
        format_level_surface = font.render(formatted_level, False, YELLOW)
        screen.blit(format_level_surface, (650, 740, 50, 50))
    else:
        screen.blit(game_over_surface, (570, 740 , 50, 50))
        screen.blit(restart_surface, (OFFSET, 740, 50, 50))

    x = OFFSET
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += OFFSET


    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface= font.render(formatted_score, False, YELLOW)
    screen.blit(score_surface, (50, 40, 50, 50))
    screen.blit(highscore_text_surface, (550, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, YELLOW)
    screen.blit(highscore_surface, (625, 40, 50, 50))

    #SHOW ALL THE SPRITES ONTO THE GAME SCREEN
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.aliens_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    pygame.display.update()
    clock.tick(60) #60 fps

