from countdown import Countdown
from postgame import PostGame
from settings import *
from title import TitleScreen
import ctypes, pygame, sys

# Maintain resolution regardless of Windows scaling settings
ctypes.windll.user32.SetProcessDPIAware()

class Game:
    def __init__(self):

        # General setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE_STRING)
        self.clock = pygame.time.Clock()
        self.game_state = "waiting"

        # Boolean to keep track of whether or not to use aimbot
        self.cheat = False

        # Set self.click_count depending on whether or not aimbot is enabled
        self.click_count = 0

        # Background image and shot sound
        self.bg_image = pygame.image.load(BG_IMAGE_PATH)
        self.shot_sound = pygame.mixer.Sound('audio/shot.mp3')

        # Create objects of relevant classes
        self.title = TitleScreen()

    def run(self):
        while True:
            # Handle quit operation
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and self.game_state == "waiting":
                    if event.key == pygame.K_SPACE:
                        self.countdown = Countdown(self.cheat, 5)
                        self.game_state = "playing"

                elif event.type == pygame.MOUSEBUTTONDOWN and self.game_state == "waiting":
                    # Toggle aimbot
                    if event.button == 1:
                        self.cheat = not self.cheat
                        self.click_count = -2
                        self.title.aimbot_enabled = not self.title.aimbot_enabled

                elif event.type == pygame.KEYDOWN and self.game_state == "gameover":
                    # Reset the game state and clear click/target details
                    if event.key == pygame.K_SPACE:
                        self.cheat, self.title.aimbot_enabled = False, False
                        self.click_count = 0
                        self.countdown.targets_spawned = 0
                        self.game_state = "waiting"
                        del self.countdown

                elif event.type == pygame.MOUSEBUTTONUP and self.game_state == "playing" and not self.cheat:
                    self.click_count += 1
                    self.shot_sound.play()
                    self.countdown.target_group.update()

                elif self.cheat and self.game_state == "playing":
                    # This works well but is "semi-automatic"
                    #if event.type == pygame.MOUSEBUTTONUP:

                    # Currently there is a bug here.  The initial click does not result in a hit, simply the jump to the target.
                    # This impacts the first AND last clicks, and thus an off-by-two error.
                    # Can be corrected by setting self.click_count to -2
                    # Not a great solution because it means the manual version of aimbot above gives inaccurate results
                    # However, a fine solution if you add an aimbot TYPE selector...
                    # Aimbot (Manual) - self.click_count unchanged (0)
                    # Aimbot (Super Turbo) - self.click_count = -2
                    if pygame.mouse.get_pressed()[0]:
                        self.click_count += 1
                        self.shot_sound.play()
                        self.countdown.target_group.update()
                        self.countdown.aimbot.reset_detection()

            pygame.display.update()
            self.screen.blit(self.bg_image, (0, 0))
            self.clock.tick(FPS)

            # Game specific updates
            if self.game_state == "waiting":
                self.title.update()
            elif self.game_state == "playing" and self.countdown.time_left > 0:
                self.countdown.update()
            elif self.game_state == "playing" and self.countdown.time_left == 0:
                self.game_state = "gameover"
                self.postgame = PostGame(self.click_count, self.countdown.targets_spawned - 1) # total_clicks, total_hits
            elif self.game_state == "gameover":
                self.postgame.update()

if __name__ == '__main__':
    game = Game()
    game.run()