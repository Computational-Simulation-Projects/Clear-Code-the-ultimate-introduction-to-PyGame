import pygame
from sys import exit

from pygame import mouse

# initialize pygame
pygame.init()

# create a display surface
width = 800  # in pixels
height = 400
screen = pygame.display.set_mode((width, height))

# set the title of the window
pygame.display.set_caption('Runner')

# create a clock
clock = pygame.time.Clock()

# create a font
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)

# create a surface
# .convert() converts the surface to the display format... it's fast
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/Ground.png').convert()

# True = anti-aliased && aniti-aliased is slow but looks better by smoothening the jagged edges by averaging pixels
# here ani-aliasing is turned off since it is a pixel art
score_surf = test_font.render('Runner Game', False, (64, 64, 64))
score_rect = score_surf.get_rect(center=(width // 2, 50))

# here convert() is not needed since the sprite needs transparent background
# convert_alpha() considers th transparency / alpha values too
snail_surf = pygame.image.load(
    './graphics/Snail/snail1.png').convert_alpha()
snail_rect = snail_surf.get_rect(bottomright=(800, 300))

player_surf = pygame.image.load(
    './graphics/Player/player_walk_1.png').convert_alpha()
# takes a surface and returns a rectangle
player_rect = player_surf.get_rect(midbottom=(80, 300))

# create the game loop
game_running = True
while game_running:
    # event loop for all the player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # the game quits when the user has clicked the close button of the window
            game_running = False

        # if event.type == pygame.MOUSEMOTION:
        #     if player_rect.collidepoint(event.pos):
        #         print('Collision!')

    # draw all the elements
    # fill the screen with black to reset the screen every frame
    screen.fill('Black')
    # blit (Block-Image-Transfer) is used to draw the surface on another
    # blit works on the order of the interpreter... top to bottom
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))

    # 2 times drawn to cover the score text since having width argument in pygame.draw.rect() stops coloring the center
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, width=10)

    screen.blit(score_surf, score_rect)
    screen.blit(snail_surf, snail_rect)
    screen.blit(player_surf, player_rect)

    # pygame.draw.line(screen, 'Gold', (0, 0), pygame.mouse.get_pos(), 10) # creates a line from (0, 0) to the mouse position
    # pygame.draw.ellipse(screen, 'Brown', pygame.Rect(50, 200, 100, 100)) # creates an ellipse

    # update everything

    # check the motion of the snail
    if snail_rect.right < 0:
        snail_rect.left = 800
    else:
        snail_rect.x -= 4

    # check if the player has collided with the snail or not
    # if player_rect.colliderect(snail_rect):
    #     print('Collision!')
    #     game_running = False

    # mouse_pos = pygame.mouse.get_pos()
    # if player_rect.collidepoint(mouse_pos):
    #     # returns a tuple of booleans of the mouse buttons left, middle, right
    #     print(pygame.mouse.get_pressed())

    pygame.display.update()  # updates the display
    clock.tick(60)  # 60 frames per second

# quits the initialized pygame
pygame.quit()
exit()  # exits the program
