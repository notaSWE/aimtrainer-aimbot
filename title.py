from settings import *
import pygame

class TitleScreen():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(COUNTDOWN_FONT, FONT_SIZE)
        self.space_font = pygame.font.Font(COUNTDOWN_FONT, 60)
        self.aimbot_enabled = False

    def update(self):
        # Load background image and create text objects
        title_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        aim_trainer_text = self.font.render("AIM TRAINER", True, (255, 255, 255))
        press_space_text = self.space_font.render(f"Press Space to Start", True, (255, 0, 0))
        aimbot_on = pygame.image.load("graphics/aimbot_on.png").convert_alpha()
        aimbot_off = pygame.image.load("graphics/aimbot_off.png").convert_alpha()

        # Create rectangles from text objects
        aim_trainer_rect = aim_trainer_text.get_rect()
        press_space_rect = press_space_text.get_rect()

        aim_trainer_rect.centerx, aim_trainer_rect.centery = self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery
        press_space_rect.centerx, press_space_rect.centery = self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery + 150

        # Draw
        self.display_surface.blit(title_image, (0, 0))
        if self.aimbot_enabled:
            self.display_surface.blit(aimbot_on, (0, 0))
        else:
            self.display_surface.blit(aimbot_off, (0, 0))
        self.display_surface.blit(aim_trainer_text, aim_trainer_rect)
        self.display_surface.blit(press_space_text, press_space_rect)