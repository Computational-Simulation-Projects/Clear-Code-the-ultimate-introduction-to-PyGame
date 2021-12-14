import pygame
from sys import exit
from random import randint, choice

# player class


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # important

        # here convert() is not needed since the sprite needs transparent background
        # convert_alpha() considers th transparency / alpha values too
        player_walk_1 = pygame.image.load(
            './graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load(
            './graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_walk_index = 0  # index of the player_walk list
        self.player_jump = pygame.image.load(
            './graphics/Player/player_jump.png').convert_alpha()

        self.image = self.player_walk[self.player_walk_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20

        if mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos) and self.rect.bottom >= 300:
                self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_walk_index += 0.1
            # 2 is the length of the self.player_walk()
            self.image = self.player_walk[int(self.player_walk_index) % len(
                self.player_walk)]

    def prepare_player(self):
        self.rect.y = 300
        self.gravity = 0

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()


# class for obstacles
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'snail':
            snail_frame_1 = pygame.image.load(
                './graphics/Snail/snail_1.png').convert_alpha()
            snail_frame_2 = pygame.image.load(
                './graphics/Snail/snail_2.png').convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_pos = 300

        else:
            fly_frame_1 = pygame.image.load(
                './graphics/Fly/fly_1.png').convert_alpha()
            fly_frame_2 = pygame.image.load(
                './graphics/Fly/fly_2.png').convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_pos = 210

        self.x_speed = randint(3, 4)
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(
            midbottom=(randint(900, 1400), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        self.image = self.frames[int(self.animation_index) % len(self.frames)]

    def destroy_obstacle(self):
        if self.rect.x <= -100:
            self.kill()  # removes the object from all the groups containing it

    def update(self):
        self.rect.x -= self.x_speed

        self.animation_state()
        self.destroy_obstacle()


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


# collision detection function for sprite groups an groupsingle
def collision_sprite():
    # this false booolean will not kill the obstacle if it collides with player
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    return True


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

# create surfaces

# .convert() converts the surface to the display format... it's fast
sky_surface = pygame.image.load('./graphics/Sky.png').convert()
ground_surface = pygame.image.load('./graphics/Ground.png').convert()

player_stand_surf = pygame.image.load(
    './graphics/Player/player_stand.png').convert_alpha()
player_stand_surf = pygame.transform.rotozoom(player_stand_surf, 0, 2)
player_stand_rect = player_stand_surf.get_rect(
    center=(width // 2, height // 2))

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

# creating a player object
player = pygame.sprite.GroupSingle()
player.add(Player())


# creating a sprite group for the obstacles
obstacle_group = pygame.sprite.Group()

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
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['fly', 'fly', 'snail', 'snail', 'snail'])))

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

        # update everything

        # update the player object
        player.draw(screen)
        player.update()

        # update the obstacle objects
        obstacle_group.draw(screen)
        obstacle_group.update()

        # collision detection
        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(game_title_surf, game_title_rect)

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
