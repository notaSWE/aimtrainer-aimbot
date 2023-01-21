from settings import *
import pygame

class Target(pygame.sprite.Sprite):
    def __init__(self, x, y, *groups):
        super().__init__(*groups)
        pygame.mixer.init()
        self.image = pygame.image.load(TARGET_IMAGE)
        self.rect = self.image.get_rect(topleft = (x, y))
        self.hit_sound = pygame.mixer.Sound('audio/hit.mp3')
        self.hit_channel = pygame.mixer.Channel(5)

    def update(self):
        # Get the x and y coordinates of the mouse cursor and check for a collision
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.hit_channel.play(self.hit_sound)
            self.kill()