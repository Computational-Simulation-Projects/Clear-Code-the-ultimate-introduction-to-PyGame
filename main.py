import pygame
from sys import exit
from random import randint, choice


def display_score():  # display score
    # gives time in miliseconds since pygame.init() was called
    current_time = (pygame.time.get_ticks() // 1000) - start_time

    # True = anti-aliased && aniti-aliased is slow but looks better by smoothening the jagged edges by averaging pixels
    # here ani-aliasing is turned off since it is a pixel art
    score_surf = test_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(width // 2, 50))

    # 2 times drawn to cover the score text since having width argument in pygame.draw.rect() stops coloring the center
    pygame.draw.rect(screen, '#c0e8ec', score_rect)
    pygame.draw.rect(screen, '#c0e8ec', score_rect, width=10)

    screen.blit(score_surf, score_rect)
    return current_time


# obstacle movement function
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:

            obstacle_rect.x -= 5
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf, obstacle_rect)

        obstacle_list = [
            obstacle_rect for obstacle_rect in obstacle_list if obstacle_rect.x > -50]
        return obstacle_list
    return []

# detect collision between player and obstacles


def collision_detection(player_rect, obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            if player_rect.colliderect(obstacle_rect):
                return False
    return True

# animate the player screen


def player_animation():
    global player_surf, player_walk_index

    if player_rect.bottom < 300:
        # display the jump surface when player is not on floor
        player_surf = player_jump
    else:
        # play walking animation if the player is on the floor
        # since 2 is the length of the list
        player_surf = player_walk[int(player_walk_index) % 2]
        player_walk_index += 0.1


# initialize pygame
pygame.init()

# create a display surface
width = 800  # in pixels
height = 400
screen = pygame.display.set_mode((width, height))

# set the title of the window
pygame.display.set_caption('Pixel Runner')

# create a clock
clock = pygame.time.Clock()

# create a font
test_font = pygame.font.Font('./font/Pixeltype.ttf', 50)

# create a surface
# .convert() converts the surface to the display format... it's fast
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/Ground.png').convert()


# here convert() is not needed since the sprite needs transparent background
# convert_alpha() considers th transparency / alpha values too
player_walk_1 = pygame.image.load(
    './graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load(
    './graphics/Player/player_walk_2.png').convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_walk_index = 0  # index of the player_walk list

player_jump = pygame.image.load(
    './graphics/Player/player_jump.png').convert_alpha()

player_surf = player_walk[player_walk_index]
# .get_rect() takes a surface and returns a rectangle
player_rect = player_surf.get_rect(midbottom=(80, 300))
player_gravity = 0

player_stand_surf = pygame.image.load(
    './graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(
    center=(width // 2, height // 2))


# obstacles
obstacle_rect_list = []

# frames for the snail
# rectangles are not needed as they are added during the event loop
snail_frame_1 = pygame.image.load(
    './graphics/Snail/snail_1.png').convert_alpha()
snail_frame_2 = pygame.image.load(
    './graphics/Snail/snail_2.png').convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surf = snail_frames[snail_frame_index]

# frames for the fly
fly_frame_1 = pygame.image.load('./graphics/Fly/fly_1.png').convert_alpha()
fly_frame_2 = pygame.image.load('./graphics/Fly/fly_2.png').convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surf = fly_frames[fly_frame_index]

# intro screen
game_title_surf = test_font.render('Pixel Runner', False, (111, 196, 169))
game_title_rect = game_title_surf.get_rect(
    center=(width // 2, height // 4 - 50))

game_message_surf = test_font.render(
    'Press SPACE to run...', False, (111, 196, 169))
game_message_rect = game_message_surf.get_rect(
    center=(width // 2, (height * 3) // 4 + 50))


# timers
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 2000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

# create the game loop
game_running = True
game_active = False
start_time = 0
score = 0

while game_running:
    # event loop for all the player inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # the game quits when the user has clicked the close button of the window
            game_running = False

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if player_rect.collidepoint(event.pos) and player_rect.bottom >= 300:
                        player_gravity = -20

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -20

            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(
                        snail_surf.get_rect(bottomright=(randint(900, 1400), 300)))
                else:
                    obstacle_rect_list.append(
                        fly_surf.get_rect(bottomright=(randint(900, 1400), 210)))

            if event.type == snail_animation_timer:
                if snail_frame_index == 0:
                    snail_frame_index = 1
                else:
                    snail_frame_index = 0
                # print(snail_frame_index)
                snail_surf = snail_frames[snail_frame_index]

            if event.type == fly_animation_timer:
                if fly_frame_index == 0:
                    fly_frame_index = 1
                else:
                    fly_frame_index = 0
                fly_surf = fly_frames[fly_frame_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = (pygame.time.get_ticks() // 1000)

    if game_active:
        # draw all the elements
        # fill the screen with black to reset the screen every frame
        screen.fill('Black')

        # blit (Block-Image-Transfer) is used to draw the surface on another
        # blit works on the order of the interpreter... top to bottom
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))

        # display the score
        score = display_score()

        # screen.blit(snail_surf, snail_rect)
        screen.blit(player_surf, player_rect)

        # update everything
        player_animation()  # update player animation frames

        # update the motion of obstacles
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # update the player gravity and position
        player_gravity += 1
        player_rect.y += player_gravity

        # check if the player is on the ground
        if player_rect.bottom >= 300:
            player_gravity = 0
            player_rect.bottom = 300

        # collision detection
        game_active = collision_detection(player_rect, obstacle_rect_list)

    else:
        screen.fill((94, 129, 162))
        screen.blit(game_title_surf, game_title_rect)

        # setting the game environment for the next game
        obstacle_rect_list = []
        player_rect.midbottom = (80, 300)
        player_gravity = 0

        if score == 0:
            screen.blit(player_stand_surf, player_stand_rect)

        else:
            player_stand_rect.y = height // 2 - 110
            screen.blit(player_stand_surf, player_stand_rect)
            score_message = test_font.render(
                f'Your Score: {score}', False, (111, 196, 169))
            score_message_rect = score_message.get_rect(
                center=(width // 2, (height * 3) // 4))
            screen.blit(score_message, score_message_rect)
        screen.blit(game_message_surf, game_message_rect)

    pygame.display.update()  # updates the display
    clock.tick(60)  # 60 frames per second

# quits the initialized pygame
pygame.quit()
exit()  # exits the program
