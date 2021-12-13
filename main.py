import pygame
from sys import exit

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
text_surface = test_font.render('Runner Game', False, 'Black')

# create the game loop
game_running = True
while game_running:
    # event loop for all the player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # the game quits when the user has clicked the close button of the window
            game_running = False

    # draw all the elements
    # blit (Block-Image-Transfer) is used to draw the surface on another
    # blit works on the order of the interpreter... top to bottom
    screen.blit(sky_surface, (0, 0))
    screen.blit(ground_surface, (0, 300))
    screen.blit(text_surface, (width // 2 - text_surface.get_width() // 2, 50))

    # update everything
    pygame.display.update()  # updates the display
    clock.tick(60)  # 60 frames per second

# quits the initialized pygame
pygame.quit()
exit()  # exits the program
