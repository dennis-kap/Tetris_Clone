# Importing Pygame to use screen and font methods
import pygame

# Importing main_file to modify the screen and return to the game and screen to use screen functions
import main_file
import screen

pygame.init()

# Font sizes based on the width of the window
main_font = pygame.font.Font ("Tetris.ttf", int (main_file.window_width // 15))
settings_font = pygame.font.Font ("Tetris.ttf", int (main_file.window_width // 20))
game_over_font = pygame.font.Font ("Tetris.ttf", int (main_file.window_width // 5))

# Only function in this file. It is a loop that constantly displays selectable text and runs as a start, end, settings or pause screen
def menu_screen(start = False, settings = False, end = False, score = 0, pause = False):

# Selection variables inputted by user set to False
    go_back = False

    selection_right = False
    selection_left = False
    selection_up = False
    selection_down = False
    select = False

# Type of selection within the home menu set to first one
    home_type = 0

# A value for the number of iterations that selected text turns green for
    turns_green = 160

# All of the saved options are set to the first choice
    saved_height = 0
    saved_res = 0
    saved_full = 0
    saved_back = 0
    saved_resume = 0
    saved_quit = 0

    setting_type = 0
    setting_choice = 0

    pause_type = 0
    pause_choice = 0

# The loop continues while it is not required to return to the game screen
    goto_game = False

# Making a variable to access the main file screen easier
    main_screen = main_file.screen

    pygame_Screen = screen.Screen(640, 480, False)

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ FOR SETTINGS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# The options for each menu and their values are put into tuples as they will not be changed
    main_menu = ("Play", "Settings", "Quit")
    end_menu = ("Restart", "Settings", "Quit")

    play_height = ("Normal", "Tall", "Short")
    res_size = ((640, 480), (1280, 720), (1366, 768), (1920, 1080))
    fullscreen_toggle = ("OFF", "ON")

# The values for these are not mandatory, but allow use of universal code that can be used for the other tuples as well
    back = (go_back, "")
    resume = ("Resume", "")
    quit_game = ("Quit", "")

# Settings and pause have slightly difference options and certain values have to be saved, requiring lists for changes
    saved_settings = [saved_height, saved_res, saved_full, saved_back]
    settings_menu = ((play_height, "Height: "), (res_size, "Resolution: "), (fullscreen_toggle, "Fullscreen: "), (back, "Back  "))

    saved_pause = [saved_resume, saved_height, saved_res, saved_full, saved_quit]
    pause_menu = ((resume, "Resume  "), (res_size, "Resolution: "), (fullscreen_toggle, "Fullscreen: "), (quit_game, "Quit  "))

# While the menu screen is active and not the game, there is a loop
    while not goto_game:

    # Black background
        main_screen.fill (main_file.black)

    # As start and end screens are similar, selections are made based on the boolean values of 'end' and 'start'
    # If a selection is made, variables are set, and the displayed action occurs
        if start or end:
            if selection_down:
                selection_down = False
                if home_type < len(main_menu) - 1:
                    home_type += 1
                else:
                    home_type = 0

            if selection_up:
                selection_up = False
                if home_type > 0 :
                    home_type -= 1
                else:
                    home_type = len(main_menu) - 1

            if select:
                select = False

                turns_green = 0

                if main_menu[home_type] == "Play":
                    main_file.main()
                elif main_menu[home_type] == "Settings":
                    settings = True
                    start = False
                    end = False
                elif main_menu[home_type] == "Quit":
                    pygame.quit()
                    exit()

            if turns_green < 160:
                turns_green += 1


    # There are only two differences between the start and end screen. Start screen has "Start" and end screen has "Restart", which are simply changed
    # using different tuples. The other difference, however, is that the end screen displays a score, so that must be added
            if start:
                selection_menu = main_menu
            if end:
                selection_menu = end_menu

                game_over_text = main_font.render ("Game over!", True, main_file.green)
                score_text = main_font.render ("Score: " + str(score), True, main_file.green)

                window_width = main_file.screen.get_size()[0]

                score_text_rect = score_text.get_rect (center=((window_width / 2), main_file.play_height / 5))
                main_file.screen.blit(score_text, score_text_rect)
                over_rect = game_over_text.get_rect (center=((window_width / 2), (main_file.play_height / 5) - score_text_rect.h))
                main_file.screen.blit (game_over_text, over_rect)


    # Text is coloured grey, white or green depending on if it is selected or not and if it has been pressed
            for home_options in range(len(selection_menu)):

                text_colour = main_file.grey
                if home_options == home_type:
                    text_colour = main_file.white

                if turns_green < 150:
                    text_colour = main_file.green

                home_text = main_font.render (selection_menu[home_options], True, text_colour)

                home_text_rect = home_text.get_rect (center=((main_file.play_width / 2) + main_file.play_offset, main_file.play_height / 2))
                home_text_rect.y += (home_options * home_text_rect.h) - home_text_rect.h
                main_screen.blit (home_text, home_text_rect)


    # Settings and pause screens are similar
        if settings or pause:

            change_current_set = False

    # The options differ based on setting or pause
            if settings:
                type = setting_type
                choice = setting_choice

                menu = settings_menu
                saved = saved_settings
            elif pause:
                type = pause_type
                choice = pause_choice

                menu = pause_menu
                saved = saved_pause

    # To save and make selections, tuples and lists are iterated through, and index values are stored so that the selected value can be seen again
    # after another option is used and then the user returns to the previous option
            if selection_down:
                selection_down = False
                change_current_set = True
                if type < len(menu) - 1:
                    type += 1
                else:
                    type = 0

            if selection_up:
                selection_up = False
                change_current_set = True
                if type > 0 :
                    type -= 1
                else:
                    type = len(menu) - 1

            if change_current_set:
                for s in range (len(menu)):
                    if s == type:
                        choice = saved[s]

            if selection_right:
                selection_right = False
                if choice < len(menu[type][0]) - 1:
                    choice += 1
                else:
                    choice = 0

            elif selection_left:
                selection_left = False
                if choice > 0:
                    choice -= 1
                else:
                    choice = len(menu[type][0]) - 1


    # The selected setting is set aside to have it diplayed in white
            selected_setting = menu[type][0][choice]

    # Based on the selection, the option and choice will do something that the user requests and will show as green for a short moment. Variables
    # are reset to avoid issues as the menu loop goes on
            if select:
                select = False

                turns_green = 0

                if menu[type][0] == play_height:
                    if selected_setting == "Normal":
                        pygame_Screen.set_height_div(2)
                    elif selected_setting == "Tall":
                        pygame_Screen.set_height_div(2.5)
                    elif selected_setting == "Short":
                        pygame_Screen.set_height_div (1.5)

                elif menu[type][0] == res_size:
                    pygame_Screen.set_res(selected_setting[0], selected_setting[1])

                elif menu[type][0] == fullscreen_toggle:
                    if selected_setting == "ON":
                        pygame_Screen.set_fullscreen()
                    else:
                        pygame_Screen.set_windowed ()

                elif menu[type][0] == back:
                    go_back = True

                elif menu[type][0] == resume:
                    goto_game = True
                    start = False
                    end = False
                    settings = False
                    resume = False

                elif menu[type][0] == quit_game:
                    pause = False
                    start = True

                for s in range (len(menu)):
                    if s == type:
                        saved[s] = choice

            if go_back:
                go_back = False
                settings = False
                end = False
                start = True

            if turns_green < 160:
                turns_green += 1

    # Text is grey if not selected, white if selected and green is pressed or chosen. Text is also centered
            for set_count, setting in enumerate(menu):
                text_colour = main_file.grey
                if setting[0] == menu[type][0]:
                    text_colour = main_file.white

                    if turns_green < 150:
                        text_colour = main_file.green

                    if menu[type][0] == res_size:
                        text = settings_font.render ((setting[1]) + str (selected_setting[0]) + " x " + str (selected_setting[1]), True, text_colour)
                    elif menu[type][0] == back or menu[type][0] == quit_game or menu[type][0] == resume:
                        text = settings_font.render (setting[1][:-2], True, text_colour)
                    else:
                        text = settings_font.render ((setting[1]) + str (selected_setting), True, text_colour)

                else:
                    text = settings_font.render (setting[1][:-2], True, text_colour)


                settings_text_rect = text.get_rect(center=((main_file.play_width / 2) + main_file.play_offset, main_file.play_height / 2))
                settings_text_rect.y += (set_count * settings_text_rect.h) - settings_text_rect.h
                main_screen.blit(text, settings_text_rect)

    # Since changes to lists are made depending on if it was the setting or pause menu, the settings and pause values are updated
                if settings:
                    setting_type = type
                    setting_choice = choice

                    saved_settings = saved
                elif pause:
                    pause_type = type
                    pause_choice = choice

                    saved_pause = saved

    # User inputs are taken in
        for x in pygame.event.get ():
            if x.type == pygame.QUIT:
                pygame.quit()
                exit ()
            if x.type == pygame.KEYDOWN:
                if pygame.K_q == x.key:
                    pygame.quit()
                    exit()
                if pygame.K_RIGHT == x.key or pygame.K_d == x.key:
                    selection_right = True
                if pygame.K_LEFT == x.key or pygame.K_a == x.key:
                    selection_left = True
                if pygame.K_UP == x.key or pygame.K_w == x.key:
                    selection_up = True
                if pygame.K_DOWN == x.key or pygame.K_s == x.key:
                    selection_down = True
                if pygame.K_SPACE == x.key or pygame.K_RETURN == x.key:
                    select = True
                if pygame.K_ESCAPE == x.key:
                    if settings:
                        go_back = True

    # Display is updated
        main_file.pygame.display.update()
