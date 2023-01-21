from settings import *
import pygame

class TitleScreen():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(COUNTDOWN_FONT, FONT_SIZE)
        self.space_font = pygame.font.Font(COUNTDOWN_FONT, 60)

    def update(self):
        # Load background image and create text objects
        title_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        aim_trainer_text = self.font.render("AIM TRAINER", True, (255, 255, 255))
        press_space_text = self.space_font.render(f"Press Space to Start", True, (255, 0, 0))

        # Create rectangles from text objects
        aim_trainer_rect = aim_trainer_text.get_rect()
        press_space_rect = press_space_text.get_rect()

        aim_trainer_rect.centerx, aim_trainer_rect.centery = self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery
        press_space_rect.centerx, press_space_rect.centery = self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery + 150

        # Draw
        self.display_surface.blit(title_image, (0, 0))
        self.display_surface.blit(aim_trainer_text, aim_trainer_rect)
        self.display_surface.blit(press_space_text, press_space_rect)