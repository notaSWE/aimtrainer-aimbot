from settings import *
import pygame

class PostGame():
    def __init__(self, total_clicks, total_hits):
        self.display_surface = pygame.display.get_surface()
        self.total_clicks, self.total_hits = total_clicks, total_hits
        self.misses = self.total_clicks - self.total_hits
        self.font = pygame.font.Font(COUNTDOWN_FONT, FONT_SIZE)
        self.base_font_size = 60
        self.multiplier = 1

        # Increase multiplier based on number of total hits; penalty for misses
        if self.total_hits > 1:
            self.multiplier = self.get_new_multiplier(self.total_hits, self.misses)

        self.score_font = pygame.font.Font(COUNTDOWN_FONT, self.base_font_size + (7 * self.total_hits))
        self.stats_font = pygame.font.Font(COUNTDOWN_FONT, self.base_font_size)

        if self.total_clicks > 0:
            self.accuracy = round((self.total_hits / self.total_clicks) * 100, 2)
            self.final_score = "{:,}".format(int(self.accuracy * self.total_hits) * self.multiplier)
        else:
            self.accuracy, self.final_score = 0, 0

    def get_new_multiplier(self, num_hits, num_misses):
        basis = num_hits - num_misses
        if basis > 3 and basis < 6:
            return 2
        elif basis > 5 and basis < 10:
            return 3
        elif basis > 9 and basis < 15:
            return 4
        elif basis > 14:
            return 5
        else:
            return 1

    def update(self):
        # Load background image and create text objects
        postgame_image = pygame.image.load(BG_IMAGE_PATH).convert_alpha()
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        stats_numbers_text = self.score_font.render(f"SCORE: {self.final_score}", True, (255, 255, 255))
        stats_percentage_text = self.stats_font.render(f"Press Space to Try Again", True, (255, 255, 255))
        if stats_numbers_text.get_width() > 1920:
            # Scale the score surface down and maintain aspect ratio
            new_height = int((stats_numbers_text.get_height() / stats_numbers_text.get_width()) * 1920)
            stats_numbers_text = pygame.transform.scale(stats_numbers_text, (1920, new_height))

        # Create rectangles from text objects
        game_over = game_over_text.get_bounding_rect()
        stats_numbers = stats_numbers_text.get_bounding_rect()
        stats_percentage = stats_percentage_text.get_bounding_rect()

        height = game_over_text.get_height() + stats_numbers_text.get_height() + stats_percentage_text.get_height()
        final_surface = pygame.Surface((1920, 1080))
        final_surface_rect = final_surface.get_rect()
        final_surface_rect.centerx, final_surface_rect.centery = self.display_surface.get_rect().centerx, self.display_surface.get_rect().centery

        # Adjusting rectangle locations to match final_surface_rect
        game_over.centerx, game_over.y = 960, (1080 - height) / 2
        stats_numbers.centerx, stats_numbers.y = 960, game_over.bottom + 20
        stats_percentage.centerx, stats_percentage.y = 960, stats_numbers.bottom + 20

        final_surface.blit(game_over_text, game_over)
        final_surface.blit(stats_numbers_text, stats_numbers)
        final_surface.blit(stats_percentage_text, stats_percentage)

        self.display_surface.blit(postgame_image, (0, 0))
        self.display_surface.blit(final_surface, (0, 0))