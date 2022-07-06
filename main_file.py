import pygame
import random

# Importing the other files needed
import shape
import start_pause

# Colours
black = (0, 0, 0)
white = (255, 255, 255)
grey = (100, 100, 100)
dark_grey = (85, 85, 85)
blue = (0, 0, 200)
purple = (200, 0, 200)
orange = (200, 100, 0)
turqoise = (0, 150, 200)
red = (200, 0, 0)
green = (0, 200, 0)
yellow = (200, 200, 50)

# Initializing the window with a smaller size to allow lower resolution screens to see the screen
pygame.init()
pygame.display.set_caption("Tetris")
screen = pygame.display.set_mode((640, 480), 0, 0)

window_width, window_height = screen.get_size()

play_height = window_height
play_width = (window_height / 2)
block_size = play_width / 10

play_offset = (window_width / 2) - (play_width / 2)

# A default font used for score and next shape
side_fonts = pygame.font.Font ("Tetris.ttf", int (window_width // 30))

#Shapes and their rotations
S = [['....',
      '..00',
      '.00.',
      '....'],
     ['....',
      '.0..',
      '.00.',
      '..0.']]

Z = [['....',
      '.00.',
      '..00',
      '....'],
     ['....',
      '..0.',
      '.00.',
      '.0..']]

I = [['....',
      '0000',
      '....',
      '....'],
     ['..0.',
      '..0.',
      '..0.',
      '..0.']]

O = [['....',
      '....',
      '.00.',
      '.00.']]

J = [['....',
      '.0..',
      '.000',
      '....'],
     ['....',
      '..0.',
      '..0.',
      '.00.'],
     ['....',
      '.000',
      '...0',
      '....'],
     ['....',
      '.00.',
      '.0..',
      '.0..']]

L = [['....',
      '...0',
      '.000',
      '....'],
     ['....',
      '.00.',
      '..0.',
      '..0.'],
     ['....',
      '....',
      '.000',
      '.0..'],
     ['....',
      '.0..',
      '.0..',
      '.00.']]

T = [['....',
      '..0.',
      '.000',
      '....'],
     ['....',
      '..0.',
      '.00.',
      '..0.'],
     ['....',
      '....',
      '.000',
      '..0.'],
     ['....',
      '.0..',
      '.00.',
      '.0..']]

shapes = [S, Z, I, O, J, L, T]
colours = [green, red, turqoise, yellow, blue, orange, purple]

# Function that takes the current shape, duplicates it's blocks, and shows where the shape will go if the user hard drops the shape
def show_drop(current_shape, possible_down_collisions, block_edge):
    hit_bottom = False
    number_drop = 0

    ghost_shape = []
    for block in current_shape.shape_blocks:
        ghost_shape.append([block[0], block[1]])

    while not hit_bottom:
        for block in ghost_shape:
            if (block[1] >= ((play_height / block_size) - 1)) \
                    or (block[0], (block[1] + 1)) in possible_down_collisions:
                        hit_bottom = True
        if not hit_bottom:
            for block in ghost_shape:
                block[1] += 1

            number_drop += 1

    for ghost_block in ghost_shape:

        original_colour = current_shape.colour
        ghost_colour = []
        for colour in original_colour:
            ghost_colour.append(colour + 50)

        pygame.draw.rect (screen, ghost_colour,
                          ((ghost_block[0] * block_size) + play_offset, (ghost_block[1] * block_size), block_size, block_size))
        pygame.draw.rect (screen, (grey), (
        (ghost_block[0] * block_size) + play_offset + block_edge / 2, (ghost_block[1] * block_size) + block_edge / 2, block_size - block_edge,
        block_size - block_edge))

    return number_drop

# Function that takes the shape that will appear next (next shape variable) and displays it on the right side
def display_next(next_shape):
    window_width = screen.get_size()[0]

    next_label = side_fonts.render ("Next Shape:", True, white)
    next_label_rect = next_label.get_rect (center=((window_width), play_height / 4))
    screen.blit (next_label, (window_width - (next_label_rect.w * 1.2), next_label_rect[1]))


    for shape_block in next_shape.shape_blocks:
        half_block = block_size / 1.5

        pygame.draw.rect (screen, white,
                          ((shape_block[0] * half_block) + (window_width - (next_label_rect.w * 1)), (shape_block[1] * half_block) + play_height / 3.5, half_block, half_block))

# Function that displays the score and high score on the left side
def display_scores(score, high_score):

    score_label = side_fonts.render ("Score:", True, white)
    score_text = side_fonts.render (str(score), True, white)

    high_label = side_fonts.render ("High Score:", True, white)
    high_text = side_fonts.render (str(high_score), True, white)

    score_text_rect = score_text.get_rect (center=((block_size * 2), (play_height / 4) + (block_size * 3)))
    screen.blit (score_label, score_text_rect)
    text_location = (score_text_rect.x, score_text_rect.y)
    screen.blit (score_text, (text_location[0], text_location[1] + block_size))

    screen.blit(high_label, (text_location[0], text_location[1] - (block_size * 3)))
    screen.blit(high_text, (text_location[0], text_location[1] - (block_size * 2)))

# Function that creates a random shape instance and returns it to prepare for use
def generate_next_shape():
    random_shape_choice = random.choice (shapes)

    next_shape = shape.Shape (random_shape_choice, -1, [0, 0], grey)
    next_shape.generate_shape ()

    return next_shape

# Function that will check any possible collision locations of all the static blocks from previous shapes. Based on the variable 'side', the function
# will check either the top, right or left of blocks depending on the need for collisions. This is used to make the process of checking for
# collisions more efficient by avoiding the need to check every block for collision with any of the blocks in the current shape
def get_possible_collisions(shape_dict, side):
    collision_list = []

    for block in shape_dict:
        if side == "top":
            if shape_dict.get((block[0], block[1] - 1)) == None:
                collision_list.append(block)
        elif side == "right":
            if shape_dict.get((block[0] - 1, block[1])) == None:
                collision_list.append(block)
        elif side == "left":
            if shape_dict.get((block[0] + 1, block[1])) == None:
                collision_list.append(block)

    return collision_list

# Function that will go through each row and check if it is full (10 blocks across) and will delete it and lower any blocks above it by one.
# When rows are deleted, the score increases depending on the amount of rows removed.
def check_full_row(static_blocks, score):
    new_dictionary = {}
    all_possible_rows = []

    delete_rows = 0

    delete_blocks = []

    drop_rows_above = []

    for block in static_blocks:
        if block[1] not in all_possible_rows:
            all_possible_rows.append(block[1])

    for row in all_possible_rows:
        number_blocks = 0
        block_list = []
        for block in static_blocks:
            if block[1] == row:
                number_blocks += 1
                block_list.append(block)
        if number_blocks == 10:
            drop_rows_above.append(row)
            delete_blocks.extend(block_list)
            delete_rows += 1

    for block in static_blocks:
        if block not in delete_blocks:

            drop_times = 0
            for drop_rows in drop_rows_above:
                if block[1] < drop_rows:
                    drop_times += 1

            new_dictionary[(block[0], (block[1] + drop_times))] = static_blocks[block]

    if delete_rows == 1:
        score += 40
    if delete_rows == 2:
        score += 100
    if delete_rows == 3:
        score += 300
    if delete_rows == 4:
        score += 1200

    return new_dictionary, score

# This function gets a random rotation value and gets the corresponding colour of the shape for what is considered the upcoming shape and generates
# it as a new Shape class instance to make it usable within the game. It is then adjusted to spawn before the line and in the middle
def creating_shape(shape_info):
    random_rotate_choice = random.randint (0, len (shape_info.shape) - 1)
    random_colour_choice = colours[shapes.index (shape_info.shape)]

    current_shape = shape.Shape (shape_info.shape, random_rotate_choice, shape_info.current_location, random_colour_choice)

    current_shape.generate_shape ()
    current_shape.move_shape (3, -3)

    return current_shape

# The score file is iterated through and the highest score is saved, so that a high score can be displayed
def get_score(file):
    high_score = 0
    for score in file:
        if score.isdigit():
            if int(score) > high_score:
                high_score = int(score)

    return high_score

# The main function. This function is responsible for variables whenever the game starts, for taking keyboard input, displaying the shapes and
# screen colours, updating the screen, checking and initiating movement and rotations, storing previous shapes, and keeping track of score.

# The main function uses a while loop to continue until the user quits, the game ends or temporarily goes into another loop while the player pauses
def main():

#Starting values ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    make_new_shape = True

# Variables that change when a user inputs a rotation or movement are set to False in the beginning
    rotate_cw = False
    rotate_ccw = False
    check_rows = False

    move_left = False
    move_right = False
    move_down = False

# Variables that check if the user can move the shape for a little after collision with the bottom or if the user requests a hard drop
    next_collision = False
    can_delay = True
    collision_delay = None
    hard_drop = False

# A dictionary that stores the location of previous shape blocks and their colour
    static_blocks = {}

# Tick used to count number of ticks before a shape can drop. Not using this will mean the shape will drop through every iteration of the main loop,
# which would be too fast
    starting_tick = pygame.time.get_ticks()

# User starts with a score of 0
    score = 0

# Two shapes need to be generated at the start, so one shape is made before hand, as within the loop, only one shape is created at a time
    next_shape = generate_next_shape()

# Getting the high score from the scores.txt file
    score_file = open("scores.txt", "r")
    high_score = get_score(score_file)
    score_file.close()

# MAIN LOOP ========================================================================================================

    while True:

    # Creating the screen background (black, with a checkered grey play area in the middle) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        screen.fill(black)
        pygame.draw.rect(screen, (grey), (play_offset, 0, play_width, play_height))

        for x in range(int(play_height / block_size)):
            pygame.draw.line(screen, (dark_grey), (play_offset, x * block_size), (play_offset + play_width, x * block_size), 2)
        for y in range(int(play_width / block_size)):
            pygame.draw.line (screen, (dark_grey), (play_offset + (y * block_size), 0), (play_offset + (y * block_size), play_height), 2)

        display_scores(score, high_score)

# Creation of new shape to generate ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if make_new_shape:
            make_new_shape = False

            current_shape = creating_shape (next_shape)

            next_shape = generate_next_shape()

# Movements and rotations (checks for collisions prior) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Gets the locations of the current shape's blocks and the possible collision locations of previous blocks

# Then, depending on the movement, if any collision occurs with other blocks or any space outside the play area, the movement or rotation is denied.
# Otherwise, the movement occurs

        shape_hitbox = current_shape.shape_blocks

        possible_left_collisions = get_possible_collisions (static_blocks, "left")
        possible_right_collisions = get_possible_collisions (static_blocks, "right")
        possible_down_collisions = get_possible_collisions (static_blocks, "top")


        if rotate_cw or rotate_ccw:
            if rotate_cw:
                rotation = "CW"
            if rotate_ccw:
                rotation = "CCW"
            check_rotate = current_shape.check_rotate(rotation)

            rotate_cw = False
            rotate_ccw = False

            can_rotate = True

            for block in check_rotate:
                block_tuple = (block[0], block[1])

                if block_tuple[1] >= play_height / block_size:
                    can_rotate = False
                if block_tuple in possible_left_collisions:
                    can_rotate = False
                if block_tuple in possible_right_collisions:
                    can_rotate = False
                if block_tuple in possible_down_collisions:
                    can_rotate = False
                if block[0] > ((play_width / block_size) - 1) or block[0] < 0:
                    can_rotate = False

            if can_rotate:
                current_shape.rotate_shape(rotation)


        if move_left:
            move_left = False
            can_left = True

            for block in shape_hitbox:
                if ((block[0] - 1), block[1]) in possible_left_collisions or block[0] < 1:
                    can_left = False

            if can_left:
                current_shape.move_shape (-1, 0)

        if move_right:
            move_right = False
            can_right = True

            for block in shape_hitbox:
                if ((block[0] + 1), block[1]) in possible_right_collisions or block[0] > (play_width / block_size) - 2:
                    can_right = False

            if can_right:
                current_shape.move_shape(1, 0)

# Using ticks to drop the blocks at a reduced rate or a slightly faster rate if the user presses the 'down' button

        gravity_tick = pygame.time.get_ticks()
        down_tick = pygame.time.get_ticks()
        if move_down and not next_collision and (down_tick - starting_tick) > 30:
            starting_tick = pygame.time.get_ticks ()
            current_shape.move_shape(0, 1)
        elif (gravity_tick - starting_tick > 200) and not next_collision:
            starting_tick = pygame.time.get_ticks()
            current_shape.move_shape (0, 1)

# Getting the edge of blocks to have a displayed edge instead of one full colour for each block
        block_edge = block_size / 5

# Checking location of hard drop
        drop_amount = show_drop(current_shape, possible_down_collisions, block_edge)

# If a hard drop occured the 'dropped' variable will be used to get a new shape later in the loop
        dropped = False
        if hard_drop:
            hard_drop = False
            current_shape.move_shape(0, drop_amount)
            dropped = True

# COLLISIONS ========================================================================================================

    # Checking for collision with bottom or shapes from the top ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        next_collision = False

        for block in shape_hitbox:
            if (block[1] >= ((play_height / block_size) - 1)) \
            or (block[0], (block[1] + 1)) in possible_down_collisions:

                if can_delay:
                    collision_delay = pygame.time.get_ticks ()

                next_collision = True
                can_delay = False

                check_rows = True

        if not next_collision:
            can_delay = True

    # Allows a short amount of time to move side to side or rotate after collision

        collision_tick = pygame.time.get_ticks()
        if (next_collision and (collision_tick - collision_delay) > 500) or dropped:

            make_new_shape = True
            can_delay = True

            for each_block in current_shape.shape_blocks:
                tuple_location = tuple (each_block)
                static_blocks[tuple_location] = current_shape.colour

    # Checking for if rows need to be cleared

        if check_rows:
            static_blocks, score = check_full_row (static_blocks, score)

# Drawing current shape ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for block_in_shape in current_shape.shape_blocks:
            current_colour = current_shape.colour
            lighter_colour = []

            for colour in current_colour:
                lighter_colour.append(colour + 50)

            pygame.draw.rect(screen, current_colour, ((block_in_shape[0] * block_size) + play_offset, (block_in_shape[1] * block_size), block_size, block_size))
            pygame.draw.rect(screen, (lighter_colour), ((block_in_shape[0] * block_size) + play_offset + block_edge / 2, (block_in_shape[1] * block_size) + block_edge / 2, block_size - block_edge, block_size - block_edge))

# Drawing static blocks ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for block in static_blocks:
            shape_colour = static_blocks.get(block)
            pygame.draw.rect (screen, (shape_colour), ((block[0] * block_size) + play_offset, (block[1] * block_size), block_size, block_size))
            pygame.draw.rect (screen, (shape_colour[0] + 50, shape_colour[1] + 50, shape_colour[2] + 50), ((block[0] * block_size) + block_edge / 2 + play_offset, (block[1] * block_size) + block_edge / 2, block_size - block_edge, block_size - block_edge))

# Checking if game over. If it is, it goes to the main menu, notifying it that the game ended after the score is saved.
        for block in static_blocks:
            if block[1] < 0:
                score_file = open ("scores.txt", "a")
                score_file.write("\n" + str(score))
                score_file.close ()
                start_pause.menu_screen (False, False, True, score)
                break

# Drawing next shape and updating screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        display_next(next_shape)

        pygame.display.update ()

# Keyboard Inputs ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        for x in pygame.event.get ():
            if x.type == pygame.QUIT:
                pygame.quit()
                exit ()
            if x.type == pygame.KEYDOWN:
                if pygame.K_a == x.key or pygame.K_LEFT == x.key:
                    move_left = True
                if pygame.K_d == x.key or pygame.K_RIGHT == x.key:
                    move_right = True
                if pygame.K_s == x.key or pygame.K_DOWN == x.key:
                    move_down = True
                if pygame.K_w == x.key or pygame.K_UP == x.key or pygame.K_x == x.key:
                    rotate_cw = True
                if pygame.K_z == x.key:
                    rotate_ccw = True
                if pygame.K_SPACE == x.key:
                    hard_drop = True
                if pygame.K_ESCAPE == x.key or pygame.K_p == x.key:
                    start_pause.menu_screen(False, False, False, 0, True)
                if pygame.K_q == x.key:
                    pygame.quit()
                    exit()
            if x.type == pygame.KEYUP:
                if pygame.K_s == x.key or pygame.K_DOWN:
                    move_down = False


if __name__ == "__main__":
    start_pause.menu_screen(True)