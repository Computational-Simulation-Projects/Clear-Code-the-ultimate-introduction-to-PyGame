import pygame
from sys import exit

# initialize pygame
pygame.init()

# create a display surface
width = 800  # in pixels
height = 400
screen = pygame.display.set_mode((width, height))

# change the title of the window
pygame.display.set_caption('Runner')

# set the title of the window

# create the game loop
game_running = True
while game_running:
    # event loop for all the player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # the game quits when the user has clicked the close button of the window
            game_running = False

    # draw all the elements
    # update everything
    pygame.display.update()  # updates the display

# quits the initialized pygame
pygame.quit()
exit()  # exits the program
