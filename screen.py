# Importing the main file to access the screen object and to make changes to global variables
import main_file
import start_pause

class Screen:
    def __init__(self, w, h, fullscreen, height_div = 2):
        self.w = w
        self.h = h
        self.fullscreen = fullscreen
        self.height_div = height_div

# Any changes to the screen will create ratio and size changes to the block size, play area, fonts and aspect ratio and will need to be applied
    def apply_changes(self):
        window_width, window_height = main_file.screen.get_size ()

        main_file.play_height = window_height
        main_file.play_width = (window_height / self.height_div)
        main_file.block_size = main_file.play_width / 10

        main_file.play_offset = (window_width / 2) - (main_file.play_width / 2)

        main_file.side_fonts = main_file.pygame.font.Font ("Tetris.ttf", int (window_width // 30))

        start_pause.main_font = main_file.pygame.font.Font ("Tetris.ttf", int (window_width // 15))
        start_pause.settings_font = main_file.pygame.font.Font ("Tetris.ttf", int (window_width // 20))
        start_pause.game_over_font = main_file.pygame.font.Font ("Tetris.ttf", int (window_width // 5))

# Using inbuilt pygame.FULLSCREEN, fullscreen is set for the window
    def set_fullscreen(self):
        main_file.screen = main_file.pygame.display.set_mode ((0, 0), main_file.pygame.FULLSCREEN)
        self.apply_changes()
# Windowed mode is set for the window
    def set_windowed(self):
        main_file.screen = main_file.pygame.display.set_mode ((self.w, self.h))
        self.apply_changes ()
# Resolution is set if changes for the window and the resoltion is saved in the class instance
    def set_res(self, wdth, hght):
        main_file.screen = main_file.pygame.display.set_mode ((wdth, hght))
        self.w = wdth
        self.h = hght
        self.apply_changes ()
# Play height is changed and saved if changed
    def set_height_div(self, new_height_div):
        self.height_div = new_height_div
        self.apply_changes ()
